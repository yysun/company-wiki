"""Protect the evaluation from invented scores, unseen citations, and bypassed retrieval."""

import json
import shlex
import sys
import unittest
from pathlib import Path

import benchmark as bench


class ScoringTest(unittest.TestCase):
    def setUp(self):
        self.docs = [{"id": "E01", "role": "source", "text": "Approved: 18 days."},
                     {"id": "W01", "role": "wiki", "text": "Follow the policy."}]
        self.case = {"required_sources": ["E01"]}
        self.trace = {"source_reads": ["E01"]}

    def test_missing_citations_and_semantic_review_are_not_perfect_scores(self):
        score = bench.objective_scores(self.case, {"answer": "18 days", "citations": []}, self.trace, self.docs)
        self.assertIsNone(score["citation_integrity"])
        self.assertIsNone(score["answer_correctness"])
        self.assertIsNone(score["answer_grounding"])

    def test_citation_must_be_opened_exact_original_and_inline(self):
        response = {"answer": "18 days [E01]", "citations": [{"source_id": "E01", "quote": "18 days"}]}
        self.assertEqual(1, bench.objective_scores(self.case, response, self.trace, self.docs)["valid_citations"])
        self.assertEqual(0, bench.objective_scores(self.case, response, {"source_reads": []}, self.docs)["valid_citations"])
        response["citations"][0]["quote"] = "22 days"
        self.assertEqual(0, bench.objective_scores(self.case, response, self.trace, self.docs)["valid_citations"])

    def test_wiki_cannot_prove_company_fact(self):
        response = {"answer": "Policy [W01]", "citations": [{"source_id": "W01", "quote": "Follow the policy."}]}
        self.assertEqual(0, bench.objective_scores(self.case, response, {"source_reads": ["W01"]}, self.docs)["valid_citations"])

    def test_direct_file_read_is_rejected(self):
        event = {"type": "item.completed", "item": {"type": "command_execution", "command": "cat /tmp/gold.json"}}
        self.assertTrue(bench.inspect_trace(json.dumps(event), Path("/tmp/corpus"), self.docs)["integrity_failures"])

    def test_unrecognized_tool_event_is_rejected(self):
        event = {"type": "item.completed", "item": {"type": "collab_agent_tool_call"}}
        self.assertTrue(bench.inspect_trace(json.dumps(event), Path("/tmp/corpus"), self.docs)["integrity_failures"])

    def test_exact_tool_read_is_counted_and_content_verified(self):
        corpus = Path("/tmp/corpus")
        command = shlex.join([sys.executable, str(Path(bench.__file__).resolve()), "tool", "--corpus", str(corpus), "read", "E01"])
        item = {"type": "command_execution", "command": command, "exit_code": 0,
                "aggregated_output": json.dumps({"operation": "read", "documents": [self.docs[0]]})}
        checks = bench.inspect_trace(json.dumps({"type": "item.completed", "item": item}), corpus, self.docs)
        self.assertEqual(["E01"], checks["source_reads"])
        self.assertFalse(checks["integrity_failures"])
        item["aggregated_output"] = item["aggregated_output"].replace("18 days", "22 days")
        self.assertTrue(bench.inspect_trace(json.dumps({"type": "item.completed", "item": item}), corpus, self.docs)["integrity_failures"])

    def test_command_substitution_is_rejected(self):
        command = shlex.join([sys.executable, str(Path(bench.__file__).resolve()), "tool", "--corpus",
                              "/tmp/corpus", "search", "$(cat /tmp/gold.json)"])
        event = {"type": "item.completed", "item": {"type": "command_execution", "command": command}}
        self.assertTrue(bench.inspect_trace(json.dumps(event), Path("/tmp/corpus"), self.docs)["integrity_failures"])


if __name__ == "__main__":
    unittest.main()
