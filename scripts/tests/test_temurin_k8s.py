"""Offline regressions for Kubernetes inspection and generated diagnostic Jobs."""
from contextlib import redirect_stdout, redirect_stderr
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / "check_temurin_k8s.py"
SPEC = importlib.util.spec_from_file_location("temurin_check", SOURCE)
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)


def node(name="worker-1", os="linux", arch="amd64", is_ready=True, cordoned=False):
    return {"kind": "Node", "metadata": {"name": name, "labels": {"pool": "java"}},
            "spec": {"unschedulable": cordoned},
            "status": {"conditions": [{"type": "Ready", "status": "True" if is_ready else "False"}],
                       "nodeInfo": {"operatingSystem": os, "architecture": arch}}}


class TemurinCheckTest(unittest.TestCase):
    def jobs(self, nodes=None, spec=None):
        return check.probe_jobs(nodes or [node()], spec or {},
                                "eclipse-temurin:25-jdk-noble", "diagnostics",
                                10001, 10001, [], "abc123")["items"]

    def test_node_selector_intersection_and_conflict(self):
        selected = check.selectors("kubernetes.io/arch=arm64", {"nodeSelector": {"pool": "java"}})
        arm = node("arm", arch="arm64")
        arm["metadata"]["labels"]["kubernetes.io/arch"] = "arm64"
        data = {"kind": "NodeList", "items": [node(), arm]}
        self.assertEqual(check.select_nodes(data, selected), [arm])
        with self.assertRaises(ValueError):
            check.selectors("pool=batch", {"nodeSelector": {"pool": "java"}})

    def test_multiple_containers_require_explicit_selection(self):
        spec = {"containers": [{"name": "proxy"}, {"name": "java"}]}
        with self.assertRaises(ValueError):
            check.select_container(spec, None)
        self.assertEqual(check.select_container(spec, "java")["name"], "java")

    def test_cronjob_template_is_supported(self):
        pod = {"containers": [{"name": "java"}]}
        obj = {"kind": "CronJob", "spec": {"jobTemplate": {"spec": {"template": {"spec": pod}}}}}
        self.assertEqual(check.pod_spec(obj), pod)

    def test_readonly_tmp_and_entrypoint_are_flagged_without_secrets(self):
        spec = {"securityContext": {"runAsUser": 10001, "runAsNonRoot": True}}
        container = {"name": "app", "securityContext": {"readOnlyRootFilesystem": True},
                     "command": ["java", "-Dpassword=do-not-print"],
                     "env": [{"name": "JAVA_TOOL_OPTIONS", "value": "-Dtoken=do-not-print"}],
                     "envFrom": [{"secretRef": {"name": "credentials"}}]}
        report = "\n".join(check.audit([node()], spec, container))
        self.assertIn("/tmp", report)
        self.assertIn("ENTRYPOINT", report)
        self.assertIn("x86-64-v3", report)
        self.assertNotIn("do-not-print", report)
        self.assertNotIn("credentials", report)
        container["volumeMounts"] = [{"name": "tmp", "mountPath": "/tmp"}]
        self.assertNotIn("/tmp 마운트가 없습니다", "\n".join(check.audit([node()], spec, container)))

    def test_container_uid_takes_precedence(self):
        report = "\n".join(check.audit([node()], {"securityContext": {"runAsUser": 10001}},
                                       {"name": "app", "securityContext": {"runAsUser": 0}}))
        self.assertIn("현재 UID가 root", report)

    def test_probe_excludes_unavailable_and_windows_nodes(self):
        jobs = self.jobs([node(), node("arm", arch="arm64"), node("win", os="windows"),
                          node("down", is_ready=False), node("cordon", cordoned=True)])
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[1]["metadata"]["annotations"]["til.dev/target-node"], "arm")
        with self.assertRaises(ValueError):
            self.jobs([node(is_ready=False)])

    def test_probe_keeps_entrypoint_and_does_not_copy_application_secrets(self):
        spec = {"serviceAccountName": "privileged-app", "imagePullSecrets": [{"name": "app-secret"}],
                "volumes": [{"name": "credentials", "secret": {"secretName": "secret"}}],
                "containers": [{"name": "app", "env": [{"name": "TOKEN", "value": "secret"}]}]}
        job = self.jobs(spec=spec)[0]
        pod = job["spec"]["template"]["spec"]
        container = pod["containers"][0]
        self.assertNotIn("command", container)
        self.assertEqual(container["args"][:2], ["sh", "-ec"])
        self.assertTrue(container["securityContext"]["readOnlyRootFilesystem"])
        self.assertFalse(container["securityContext"]["allowPrivilegeEscalation"])
        self.assertFalse(pod["automountServiceAccountToken"])
        self.assertNotIn("serviceAccountName", pod)
        self.assertNotIn("imagePullSecrets", pod)
        self.assertNotIn("env", container)
        self.assertNotIn("secret", json.dumps(pod))
        self.assertNotIn("nodeName", pod)
        self.assertEqual(job["spec"]["backoffLimit"], 0)
        self.assertEqual(job["spec"]["activeDeadlineSeconds"], 180)

    def test_affinity_or_terms_each_restrict_to_target_node(self):
        affinity = {"requiredDuringSchedulingIgnoredDuringExecution": {"nodeSelectorTerms": [
            {"matchExpressions": [{"key": "zone", "operator": "In", "values": ["a"]}]},
            {"matchExpressions": [{"key": "zone", "operator": "In", "values": ["b"]}]}]}}
        spec = {"affinity": {"nodeAffinity": affinity}, "runtimeClassName": "sandbox",
                "tolerations": [{"key": "dedicated", "operator": "Equal", "value": "java", "effect": "NoSchedule"}]}
        original = copy.deepcopy(spec)
        pod = self.jobs(spec=spec)[0]["spec"]["template"]["spec"]
        for term in pod["affinity"]["nodeAffinity"]["requiredDuringSchedulingIgnoredDuringExecution"]["nodeSelectorTerms"]:
            self.assertEqual(term["matchFields"][0]["values"], ["worker-1"])
        self.assertEqual(spec, original)
        self.assertEqual(pod["tolerations"], spec["tolerations"])
        self.assertEqual(pod["runtimeClassName"], "sandbox")

    def test_empty_affinity_is_not_broadened(self):
        for terms in ([], [{}], [{"matchExpressions": []}]):
            affinity = {"requiredDuringSchedulingIgnoredDuringExecution": {"nodeSelectorTerms": terms}}
            pod = self.jobs(spec={"affinity": {"nodeAffinity": affinity}})[0]["spec"]["template"]["spec"]
            self.assertEqual(pod["affinity"]["nodeAffinity"], affinity)

    def test_online_mode_only_uses_get_and_explicit_context(self):
        completed = type("Result", (), {"returncode": 0, "stdout": json.dumps({"kind": "NodeList", "items": [node()]}), "stderr": ""})()
        with patch.object(check.subprocess, "run", return_value=completed) as run, redirect_stdout(io.StringIO()):
            self.assertEqual(check.main(["--context", "test"]), 0)
        args = run.call_args.args[0]
        self.assertEqual(args, ["kubectl", "--context", "test", "--request-timeout=30s", "get", "nodes", "-o", "json"])
        self.assertNotIn("shell", run.call_args.kwargs)

    def test_offline_cli_emits_jobs_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            source = Path(tmp) / "nodes.json"
            source.write_text(json.dumps({"kind": "NodeList", "items": [node()]}), encoding="utf-8")
            output = Path(tmp) / "jobs.json"
            args = ["--nodes-json", str(source), "--emit-probes", str(output)]
            with patch.object(check.subprocess, "run", side_effect=AssertionError("network not allowed")):
                self.assertEqual(check.main(args), 0)
                contents = output.read_bytes()
                self.assertEqual(json.loads(contents)["items"][0]["kind"], "Job")
                self.assertEqual(check.main(args), 2)
                self.assertEqual(output.read_bytes(), contents)


if __name__ == "__main__":
    unittest.main()
