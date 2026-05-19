import os
import sys
import tempfile
import shutil
import unittest
# Make scripts/ available on import path
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
sys.path.insert(0, SCRIPTS_DIR)

import validate_wiki_parity as vwp


class TestValidateWikiParity(unittest.TestCase):
    def setUp(self):
        self.base = os.path.abspath(os.path.dirname(__file__))
        self.canonical = os.path.join(self.base, "fixtures", "canonical")
        self.repo = os.path.join(self.base, "fixtures", "repo")

    def test_normalize_excludes(self):
        t = "title: X\nlast_updated: 2026-05-18\nbody line\n"
        out = vwp.normalize_text(t, ["last_updated"])
        self.assertNotIn("last_updated", out)

    def test_compare_dirs(self):
        results = vwp.compare_dirs(self.canonical, self.repo, exclude_keys=["last_updated"])
        self.assertIn("match.md", results)
        self.assertIn("mismatch.md", results)
        self.assertTrue(results["match.md"][0])
        self.assertFalse(results["mismatch.md"][0])

    def test_run_check_and_apply(self):
        tmp_repo = tempfile.mkdtemp(prefix="wiki-parity-test-")
        try:
            # Copy repo fixtures into temp repo so tests don't mutate source fixtures
            shutil.copytree(self.repo, tmp_repo, dirs_exist_ok=True)

            rc = vwp.run(["--check", "--canonical-dir", self.canonical, "--repo-dir", tmp_repo, "--exclude", "last_updated"])
            self.assertEqual(rc, 2)

            rc2 = vwp.run(["--apply", "--canonical-dir", self.canonical, "--repo-dir", tmp_repo, "--exclude", "last_updated"])
            self.assertEqual(rc2, 0)

            rc3 = vwp.run(["--check", "--canonical-dir", self.canonical, "--repo-dir", tmp_repo, "--exclude", "last_updated"])
            self.assertEqual(rc3, 0)
        finally:
            shutil.rmtree(tmp_repo)


if __name__ == "__main__":
    unittest.main()
