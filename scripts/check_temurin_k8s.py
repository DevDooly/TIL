"""Read Kubernetes settings and optionally render per-node Temurin smoke-test Jobs.

Python 3.10+, standard library only. Never creates/changes cluster resources.
Exit 0 means the report was produced, not that application compatibility passed.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid


PROBE = """set -eu
echo '=== OS / architecture / identity ==='
cat /etc/os-release
uname -m
id
echo '=== Writable temporary directory ==='
check_file=$(mktemp /tmp/temurin-check.XXXXXX)
printf 'ok\n' > "$check_file"
rm "$check_file"
echo '=== JVM / cgroup CPU and memory ==='
java -XshowSettings:system -version
java -XshowSettings:vm -version
echo '=== Diagnostic tools (absence is allowed for JRE) ==='
for tool in javac jcmd jfr; do
    if command -v "$tool" >/dev/null 2>&1; then
        command -v "$tool"
    else
        echo "$tool: not installed"
    fi
done
echo TIL_TEMURIN_PROBE_OK
"""


def kubectl_json(context, namespace, resource, selector=None):
    command = ["kubectl", "--context", context, "--request-timeout=30s"]
    if namespace:
        command += ["--namespace", namespace]
    command += ["get", resource, "-o", "json"]
    if selector:
        command += ["-l", selector]
    result = subprocess.run(command, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=40)
    if result.returncode:
        raise ValueError(f"kubectl get {resource} 실패: {result.stderr.strip()}")
    return json.loads(result.stdout)


def pod_spec(workload):
    kind = workload.get("kind")
    if kind == "Pod":
        return workload["spec"]
    if kind == "CronJob":
        return workload["spec"]["jobTemplate"]["spec"]["template"]["spec"]
    if kind in {"Deployment", "StatefulSet", "DaemonSet", "ReplicaSet", "Job"}:
        return workload["spec"]["template"]["spec"]
    raise ValueError(f"지원하지 않는 workload kind: {kind}")


def select_container(spec, name):
    containers = spec.get("containers", [])
    if name:
        for container in containers:
            if container.get("name") == name:
                return container
        raise ValueError(f"컨테이너를 찾을 수 없음: {name}")
    if len(containers) != 1:
        raise ValueError("컨테이너가 여러 개이면 --container로 Java 컨테이너를 지정하세요.")
    return containers[0]


def selectors(text, spec):
    selected = dict(spec.get("nodeSelector", {}))
    for pair in filter(None, text.split(",")):
        if pair.count("=") != 1 or any(c in pair for c in "!()"):
            raise ValueError("--node-selector는 key=value[,key=value] 형식만 지원합니다.")
        key, value = (part.strip() for part in pair.split("=", 1))
        if not key:
            raise ValueError("node selector key가 비어 있습니다.")
        if key in selected and selected[key] != value:
            raise ValueError(f"workload nodeSelector와 충돌: {key}")
        selected[key] = value
    return selected


def select_nodes(data, selected):
    if data.get("kind") not in {"NodeList", "List"} or not isinstance(data.get("items"), list):
        raise ValueError("nodes JSON에는 kubectl get nodes -o json 결과가 필요합니다.")
    return [node for node in data["items"]
            if all(node.get("metadata", {}).get("labels", {}).get(k) == v
                   for k, v in selected.items())]


def ready(node):
    return any(c.get("type") == "Ready" and c.get("status") == "True"
               for c in node.get("status", {}).get("conditions", []))


def node_os(node):
    return node.get("status", {}).get("nodeInfo", {}).get("operatingSystem", "unknown")


def audit(nodes, spec, container):
    lines = ["Temurin Kubernetes 사전 점검 (설정 조회; 호환성 합격 판정 아님)"]
    for node in nodes:
        info = node.get("status", {}).get("nodeInfo", {})
        lines.append(
            f"NODE {node['metadata']['name']}: {node_os(node)}/{info.get('architecture', '?')} "
            f"Ready={ready(node)} cordoned={bool(node.get('spec', {}).get('unschedulable'))} "
            f"kernel={info.get('kernelVersion', '?')} runtime={info.get('containerRuntimeVersion', '?')}")
        if node_os(node) != "linux":
            lines.append("  WARN Linux 후보 이미지 대상이 아닙니다.")
        if node.get("spec", {}).get("taints"):
            lines.append("  CHECK taint가 있습니다. 실제 workload toleration과 스케줄링 결과를 확인하세요.")
    lines.append("CHECK Node API의 amd64 정보만으로 x86-64-v3를 알 수 없습니다. UBI 10은 대상 노드에서 기동 시험이 필요합니다.")
    lines.append("CHECK 노드 선택에는 nodeSelector만 반영합니다. affinity, taint, topology, RuntimeClass와 신규 노드 풀도 확인하세요.")
    if not container:
        lines.append("CHECK --workload 또는 --workload-json을 주면 Java 컨테이너 설정도 점검합니다.")
        return lines

    lines.append(f"CONTAINER {container['name']}: image={container.get('image', '?')}")
    security = dict(spec.get("securityContext", {}))
    security.update(container.get("securityContext", {}))
    for key in ("runAsUser", "runAsGroup", "runAsNonRoot", "readOnlyRootFilesystem"):
        lines.append(f"  {key}={security.get(key, '미지정')}")
    if security.get("runAsUser") == 0:
        lines.append("WARN 현재 UID가 root입니다. 비루트 전환 시 파일·볼륨 권한을 확인하세요.")
    if not security.get("runAsNonRoot"):
        lines.append("CHECK runAsNonRoot 정책과 이미지 USER 또는 Pod의 숫자 UID를 확인하세요.")
    if security.get("readOnlyRootFilesystem"):
        writable_tmp = any(m.get("mountPath") == "/tmp" and not m.get("readOnly", False)
                           for m in container.get("volumeMounts", []))
        if not writable_tmp:
            lines.append("WARN 읽기 전용 rootfs에 쓰기 가능한 /tmp 마운트가 없습니다. JVM 임시 파일·CA 처리를 확인하세요.")
    if container.get("command"):
        lines.append("WARN command가 이미지 ENTRYPOINT를 덮어씁니다. Temurin CA 처리가 필요하면 기본 entrypoint를 보존하세요.")
    env_names = {item.get("name") for item in container.get("env", [])}
    if "JAVA_HOME" in env_names:
        lines.append("CHECK JAVA_HOME을 직접 지정했습니다. Temurin 경로 /opt/java/openjdk와 대조하세요.")
    if env_names & {"JAVA_TOOL_OPTIONS", "JDK_JAVA_OPTIONS", "_JAVA_OPTIONS"}:
        lines.append("CHECK 사용자 JVM 옵션이 있습니다. 기존 -Xmx, 컨테이너 인식 및 제거된 옵션을 확인하세요. 값은 출력하지 않습니다.")
    if "USE_SYSTEM_CA_CERTS" in env_names or container.get("envFrom"):
        lines.append("CHECK CA 설정 또는 envFrom이 있습니다. Secret 내용은 조회하지 않으므로 실제 truststore·환경변수는 별도 확인하세요.")
    resources = container.get("resources", {})
    lines.append("  resources=" + json.dumps(resources, ensure_ascii=False))
    if not resources.get("limits", {}).get("memory"):
        lines.append("WARN 컨테이너 memory limit가 없습니다. Pod 수준 제한·LimitRange와 실제 적용값을 확인하세요.")
    if not resources.get("requests", {}).get("cpu"):
        lines.append("CHECK CPU request가 없습니다. 스케줄링 자원과 JVM processor 인식값을 확인하세요.")
    if spec.get("resources"):
        lines.append("CHECK Pod 수준 resources가 있습니다. 컨테이너 설정과 함께 실제 cgroup 제한을 확인하세요.")
    for key in ("startupProbe", "readinessProbe"):
        if not container.get(key):
            lines.append(f"CHECK {key}가 없습니다. JDK 변경 후 기동·준비 시간에 맞춰 설정하세요.")
    lines.append("CHECK JNI/APM, 사내 CA, DNS/TLS, 저장소 권한, heap 여유, 종료·부하 테스트는 애플리케이션 이미지로 검증해야 합니다.")
    return lines


def probe_jobs(nodes, spec, image, namespace, uid, gid, pull_secrets, run_id):
    """Keep node affinity/tolerations, but never copy application credentials/code."""
    jobs = []
    for node in nodes:
        if node_os(node) != "linux" or not ready(node) or node.get("spec", {}).get("unschedulable"):
            continue
        name = f"temurin-check-{run_id}-{len(jobs)}"
        labels = {"app.kubernetes.io/name": "temurin-check", "til.dev/check-id": run_id}
        node_affinity = copy.deepcopy(spec.get("affinity", {}).get("nodeAffinity", {}))
        target = {"key": "metadata.name", "operator": "In", "values": [node["metadata"]["name"]]}
        if "requiredDuringSchedulingIgnoredDuringExecution" not in node_affinity:
            node_affinity["requiredDuringSchedulingIgnoredDuringExecution"] = {
                "nodeSelectorTerms": [{"matchFields": [target]}]}
        else:
            required = node_affinity["requiredDuringSchedulingIgnoredDuringExecution"]
            for term in required.get("nodeSelectorTerms", []):
                # An empty existing term matches no nodes; do not broaden it.
                if term.get("matchExpressions") or term.get("matchFields"):
                    term.setdefault("matchFields", []).append(copy.deepcopy(target))
        pod = {
            "restartPolicy": "Never", "automountServiceAccountToken": False,
            "terminationGracePeriodSeconds": 10,
            "affinity": {"nodeAffinity": node_affinity},
            "tolerations": copy.deepcopy(spec.get("tolerations", [])),
            "securityContext": {"runAsNonRoot": True, "runAsUser": uid, "runAsGroup": gid,
                                "fsGroup": gid, "seccompProfile": {"type": "RuntimeDefault"}},
            "containers": [{
                "name": "check", "image": image, "imagePullPolicy": "Always",
                # args preserves Temurin's /__cacert_entrypoint.sh.
                "args": ["sh", "-ec", PROBE],
                "securityContext": {"allowPrivilegeEscalation": False,
                                    "readOnlyRootFilesystem": True,
                                    "capabilities": {"drop": ["ALL"]}},
                "resources": {"requests": {"cpu": "100m", "memory": "128Mi"},
                              "limits": {"cpu": "500m", "memory": "512Mi"}},
                "volumeMounts": [{"name": "tmp", "mountPath": "/tmp"}],
            }],
            "volumes": [{"name": "tmp", "emptyDir": {"sizeLimit": "128Mi"}}],
        }
        if spec.get("nodeSelector"):
            pod["nodeSelector"] = copy.deepcopy(spec["nodeSelector"])
        if spec.get("runtimeClassName"):
            pod["runtimeClassName"] = spec["runtimeClassName"]
        if pull_secrets:
            pod["imagePullSecrets"] = [{"name": value} for value in pull_secrets]
        jobs.append({
            "apiVersion": "batch/v1", "kind": "Job",
            "metadata": {"name": name, "namespace": namespace, "labels": labels,
                         "annotations": {"til.dev/target-node": node["metadata"]["name"]}},
            "spec": {"backoffLimit": 0, "activeDeadlineSeconds": 180,
                     "ttlSecondsAfterFinished": 3600,
                     "template": {"metadata": {"labels": labels}, "spec": pod}},
        })
    if not jobs:
        raise ValueError("Job을 생성할 Ready·uncordoned Linux 노드가 없습니다.")
    return {"apiVersion": "v1", "kind": "List", "items": jobs}


def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("0보다 큰 숫자 UID/GID를 지정하세요.")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", help="명시적으로 선택할 kubectl context")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--workload", help="deployment/api, statefulset/api 또는 pod/api-xxx")
    parser.add_argument("--container", help="Java 컨테이너 이름 (sidecar가 있으면 필수)")
    parser.add_argument("--node-selector", default="", help="key=value[,key=value]")
    parser.add_argument("--nodes-json", type=Path, help="오프라인 nodes JSON")
    parser.add_argument("--workload-json", type=Path, help="오프라인 workload JSON")
    parser.add_argument("--emit-probes", type=Path, help="실행하지 않고 Job List JSON을 새 파일로 저장")
    parser.add_argument("--image", default="eclipse-temurin:25-jdk-noble", help="시험할 Temurin 베이스 이미지")
    parser.add_argument("--uid", type=positive, default=10001)
    parser.add_argument("--gid", type=positive, default=10001)
    parser.add_argument("--pull-secret", action="append", default=[], help="진단 namespace의 imagePullSecret 이름 (반복 가능)")
    args = parser.parse_args(argv)
    if args.nodes_json:
        if args.context or args.workload:
            parser.error("오프라인 모드에서는 --context/--workload 대신 --workload-json을 사용하세요.")
    elif not args.context or args.workload_json:
        parser.error("온라인 모드에는 --context가 필요합니다. --workload-json은 --nodes-json과 함께 사용하세요.")
    if args.container and not (args.workload or args.workload_json):
        parser.error("--container에는 workload가 필요합니다.")
    if args.workload and not re.fullmatch(r"[A-Za-z][A-Za-z0-9.]*/[a-z0-9][a-z0-9.-]*", args.workload):
        parser.error("--workload는 resource/name 형식으로 지정하세요.")
    try:
        workload = None
        if args.workload_json:
            workload = json.loads(args.workload_json.read_text(encoding="utf-8-sig"))
        elif args.workload:
            workload = kubectl_json(args.context, args.namespace, args.workload)
        spec = pod_spec(workload) if workload else {}
        container = select_container(spec, args.container) if workload else None
        selected = selectors(args.node_selector, spec)
        if args.nodes_json:
            data = json.loads(args.nodes_json.read_text(encoding="utf-8-sig"))
        else:
            selector = ",".join(f"{k}={v}" for k, v in selected.items())
            data = kubectl_json(args.context, None, "nodes", selector)
        nodes = select_nodes(data, selected)
        if not nodes:
            raise ValueError("선택한 nodeSelector에 해당하는 노드가 없습니다.")
        print("\n".join(audit(nodes, spec, container)))
        if args.emit_probes:
            run_id = uuid.uuid4().hex[:10]
            manifest = probe_jobs(nodes, spec, args.image, args.namespace,
                                  args.uid, args.gid, args.pull_secret, run_id)
            with args.emit_probes.open("x", encoding="utf-8", newline="\n") as output:
                json.dump(manifest, output, ensure_ascii=False, indent=2)
                output.write("\n")
            print(f"GENERATED {args.emit_probes}: {len(manifest['items'])} Jobs; check-id={run_id}")
            print("클러스터에는 적용하지 않았습니다. 명세를 확인한 뒤 kubectl create -f로 실행하세요.")
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
