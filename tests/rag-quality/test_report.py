"""Verify archived results remain tied to the original dataset and reviewed answer bytes."""

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import report as score_report


class ArchivedReportTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        baseline = Path(__file__).parent / "baselines/2026-09-12"
        for name in ("manifest.json", "dataset-at-execution.json", "reviews.json"):
            shutil.copyfile(baseline / name, self.root / name)
        shutil.copytree(baseline / "FQ01", self.root / "FQ01")
        manifest = json.loads((self.root / "manifest.json").read_text())
        manifest["case_ids"] = ["FQ01"]
        (self.root / "manifest.json").write_text(json.dumps(manifest))

    def render(self):
        with contextlib.redirect_stdout(io.StringIO()):
            score_report.report(self.root)

    def test_archived_dataset_works_without_current_dataset(self):
        with patch.object(score_report, "dataset", side_effect=AssertionError("current dataset unavailable")):
            self.render()
        scores = json.loads((self.root / "scores.json").read_text())
        self.assertEqual(1, scores["summary"]["reviewed_cases"])
        self.assertEqual(3, scores["cases"][0]["rubric_passed"])

    def test_result_cannot_substitute_a_different_reviewed_answer(self):
        path = self.root / "FQ01/result.json"
        result = json.loads(path.read_text())
        result["response"]["answer"] = "A substituted answer not covered by the original review."
        path.write_text(json.dumps(result))
        with self.assertRaisesRegex(ValueError, "scored response differs"):
            self.render()

    def test_changed_archive_dataset_is_rejected(self):
        path = self.root / "dataset-at-execution.json"
        gold = json.loads(path.read_text())
        gold["cases"][0]["criteria"] = ["A new criterion cannot replace the historical one."]
        path.write_text(json.dumps(gold))
        with self.assertRaisesRegex(ValueError, "dataset changed"):
            self.render()


if __name__ == "__main__":
    unittest.main()
