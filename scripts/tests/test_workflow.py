"""Regression tests for failed validation never reaching a remote push."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def bash_executable():
    if os.name == "nt":
        candidates = [os.environ.get("TIL_BASH"),
                      r"C:\Program Files\Git\bin\bash.exe"]
        for candidate in candidates:
            if candidate and Path(candidate).is_file():
                return candidate
        raise RuntimeError("Set TIL_BASH to Git Bash (not the WSL launcher)")
    found = shutil.which("bash")
    if not found:
        raise RuntimeError("bash is required")
    return found


class PagesValidationTest(unittest.TestCase):
    def validate(self, contents, create_target=False):
        with tempfile.TemporaryDirectory(prefix="til-pages-test-") as directory:
            docs = Path(directory) / "docs"
            docs.mkdir()
            (docs / ".pages").write_text(contents, encoding="utf-8")
            if create_target:
                (docs / "index.md").write_text("# Example\n", encoding="utf-8")
            env = dict(os.environ, PYTHONUTF8="1")
            return subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_pages.py")],
                cwd=directory, env=env, capture_output=True, text=True,
                encoding="utf-8", timeout=10)

    def test_valid_navigation(self):
        self.assertEqual(self.validate("nav:\n  - index.md\n", True).returncode, 0)

    def test_missing_page_fails(self):
        self.assertNotEqual(self.validate("nav:\n  - missing.md\n").returncode, 0)

    def test_invalid_yaml_fails(self):
        self.assertNotEqual(self.validate("nav: [\n").returncode, 0)

    def test_invalid_navigation_type_fails(self):
        self.assertNotEqual(self.validate("nav: index.md\n").returncode, 0)


class PublishTest(unittest.TestCase):
    def run_publish(self, *, failed_stage="", failed_commit=False, no_changes=False):
        with tempfile.TemporaryDirectory(prefix="til-publish-test-") as directory:
            root = Path(directory)
            scripts = root / "scripts"
            scripts.mkdir()
            shutil.copyfile(ROOT / "scripts/publish.sh", scripts / "publish.sh")
            fake_bin = root / "fake-bin"
            fake_bin.mkdir()
            # No real git, Python validation, or network command can run here.
            fake_git = """#!/usr/bin/env bash
printf 'git %s\\n' "$*" >> calls.log
if [[ "$1" == diff ]]; then
  [[ "$NO_CHANGES" == 1 ]] && exit 0
  exit 1
fi
if [[ "$1" == commit && "$FAIL_COMMIT" == 1 ]]; then exit 7; fi
exit 0
"""
            fake_python = """#!/usr/bin/env bash
printf 'python %s\\n' "$*" >> calls.log
if [[ -n "$FAIL_STAGE" && "$*" == *"$FAIL_STAGE"* ]]; then exit 9; fi
exit 0
"""
            for name, content in (("git", fake_git), ("fake-python", fake_python)):
                path = fake_bin / name
                path.write_text(content, encoding="utf-8", newline="\n")
                path.chmod(0o755)
            env = dict(os.environ, FAIL_STAGE=failed_stage,
                       FAIL_COMMIT="1" if failed_commit else "0",
                       NO_CHANGES="1" if no_changes else "0")
            result = subprocess.run(
                [bash_executable(), "-c",
                 'export PATH="$PWD/fake-bin:$PATH"; '
                 'export PYTHON="$PWD/fake-bin/fake-python"; '
                 'bash scripts/publish.sh "docs: regression"'],
                cwd=root, env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=30)
            calls = (root / "calls.log").read_text(encoding="utf-8")
            return result, calls

    def test_failed_validation_never_amends_or_pushes(self):
        for stage in ("validate_markdown_lists.py", "validate_pages.py",
                      "update_recent_changes.py", "unittest", "mkdocs"):
            with self.subTest(stage=stage):
                result, calls = self.run_publish(failed_stage=stage)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("git commit --amend", calls)
                self.assertNotIn("git push", calls)

    def test_failed_commit_stops_before_generators(self):
        result, calls = self.run_publish(failed_commit=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("python ", calls)
        self.assertNotIn("git push", calls)

    def test_no_changes_never_amends_or_pushes(self):
        result, calls = self.run_publish(no_changes=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("git commit", calls)
        self.assertNotIn("git push", calls)

    def test_success_pushes_only_after_build_and_amend(self):
        result, calls = self.run_publish()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(calls.index("mkdocs build --strict"),
                        calls.index("git commit --amend"))
        self.assertLess(calls.index("git commit --amend"), calls.index("git push"))


if __name__ == "__main__":
    unittest.main()
