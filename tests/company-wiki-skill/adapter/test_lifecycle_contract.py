"""Static contract checks for the five-operation company-wiki lifecycle."""

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[3]


def text(relative: str) -> str:
    return (REPOSITORY / relative).read_text(encoding="utf-8")


class LifecycleContractTest(unittest.TestCase):
    def test_skill_routes_five_operations(self) -> None:
        skill = text("skills/company-wiki/SKILL.md")
        self.assertIn("Init → Ingest → Query → Maintain → Validate", skill)
        for name in ("init", "ingest", "query", "maintain", "validate"):
            self.assertIn(f"references/{name}.md", skill)

    def test_init_is_sampling_not_ingestion(self) -> None:
        init = text("skills/company-wiki/references/init.md")
        self.assertIn("representative sampling, not Ingest", init)
        self.assertIn("do not require reading every source", init)
        self.assertIn("Do not create ingest receipts", init)

    def test_ingest_has_selection_approval_and_failure_contracts(self) -> None:
        ingest = text("skills/company-wiki/references/ingest.md")
        normalized = " ".join(ingest.split())
        required = (
            "Default to one source at a time",
            "Never enumerate a location to manufacture a batch",
            "Source selection authorizes reading, not wiki edits",
            "wait for explicit approval",
            "Immediately before applying an approved plan",
            "invalidate the plan and its approval",
            "If preflight fails for any planned target, make no write",
            "If a write fails after an earlier write succeeded, stop immediately",
            "Do not continue, delete successful work, or attempt automatic rollback",
            "propose only the remaining work for fresh approval",
            "If the comparison finds no material delta",
            "Do not modify or copy original sources",
        )
        for phrase in required:
            self.assertIn(phrase, normalized)

    def test_query_maintain_and_validate_are_separate(self) -> None:
        query = text("skills/company-wiki/references/query.md")
        maintain = text("skills/company-wiki/references/maintain.md")
        validate = text("skills/company-wiki/references/validate.md")
        self.assertIn("Do not write the answer", query)
        self.assertIn("use [Ingest](ingest.md)", maintain)
        self.assertIn("use\n[Validate](validate.md)", maintain)
        self.assertNotIn("## Validation mode", maintain)
        self.assertIn("Validate never edits the wiki, registry, or original sources", validate)
        self.assertIn("Route proposed repairs to Maintain", validate)

    def test_registry_and_repository_boundaries_cover_lifecycle(self) -> None:
        registry = text("skills/company-wiki/references/registry.md")
        agents = text("AGENTS.md")
        for operation in ("Ingest", "Query", "Maintenance", "Validate"):
            self.assertIn(f"**{operation}:**", registry)
        self.assertIn("Init → Ingest → Query → Maintain → Validate", agents)
        self.assertIn("Query and Validate are read-only", agents)

    def test_user_documentation_matches_lifecycle(self) -> None:
        for relative in ("README.md", "README.zh-CN.md", "skills/company-wiki/README.md"):
            document = text(relative)
            self.assertIn("Init → Ingest → Query → Maintain → Validate", document)
        self.assertIn("source-to-wiki reconciliation", text("README.md"))
        self.assertIn("来源到 Wiki 对账", text("README.zh-CN.md"))

    def test_main_e2e_contract_routes_ingest_and_validate(self) -> None:
        specification = text("tests/test-company-wiki-skill.md")
        self.assertIn("| Ingest | `references/registry.md`, `references/ingest.md`", specification)
        self.assertIn("| Validate | `references/registry.md`, `references/validate.md`", specification)
        self.assertIn("Approved Ingest and Maintain may", specification)
        self.assertIn("Query and Validate write nothing", specification)

    def test_lifecycle_fixtures_are_complete(self) -> None:
        fixture_root = REPOSITORY / "tests/company-wiki-skill/lifecycle"
        names = {
            "Customer Telemetry Sharing Standard 2026.md",
            "Customer Telemetry Sharing Standard 2026 revised.md",
            "Warranty Approval Amendment 2026.md",
            "Uptime Commitment Schedule 2026 changed.md",
            "Telemetry Sharing Quick Note.md",
            "Outside Acquisition Notes.md",
        }
        self.assertEqual(names, {path.name for path in fixture_root.glob("*.md")})


if __name__ == "__main__":
    unittest.main()
