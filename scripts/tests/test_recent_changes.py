"""Keep the curated README intact when refreshing generated documentation."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "update_recent_changes", ROOT / "scripts/update_recent_changes.py")
recent_changes = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recent_changes)


class RecentChangesTest(unittest.TestCase):
    def refresh_in_workspace(self, readme=None):
        with tempfile.TemporaryDirectory(prefix="til-recent-test-") as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            (docs / "Example.md").write_text("# Example\n", encoding="utf-8")
            readme_path = root / "README.md"
            if readme is not None:
                readme_path.write_bytes(readme)
            log = ["COMMIT_START|2026-09-14 12:00|docs: 예제 추가",
                   "docs/Example.md", "README.md", "docs/Deleted.md"]
            previous_directory = Path.cwd()
            try:
                os.chdir(root)
                with patch.object(recent_changes, "get_git_log", return_value=log):
                    recent_changes.main()
                    first = (docs / "Recent_Changes.md").read_bytes()
                    recent_changes.main()
            finally:
                os.chdir(previous_directory)

            generated = (docs / "Recent_Changes.md").read_bytes()
            self.assertEqual(first, generated)
            self.assertIn("[Example.md](Example.md)", generated.decode("utf-8"))
            self.assertNotIn("Deleted.md", generated.decode("utf-8"))
            if readme is None:
                self.assertFalse(readme_path.exists())
            else:
                self.assertEqual(readme, readme_path.read_bytes())

    def test_refresh_preserves_curated_readme(self):
        self.refresh_in_workspace((ROOT / "README.md").read_bytes())

    def test_refresh_does_not_require_or_create_readme(self):
        self.refresh_in_workspace()


if __name__ == "__main__":
    unittest.main()
