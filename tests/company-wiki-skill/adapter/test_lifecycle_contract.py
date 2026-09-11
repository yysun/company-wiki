"""Static lifecycle contract checks for the scoped company-wiki package."""

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[3]


def text(relative: str) -> str:
    return (REPOSITORY / relative).read_text(encoding="utf-8")


class LifecycleContractTest(unittest.TestCase):
    def test_skill_routes_scoped_lifecycle(self) -> None:
        skill = text("skills/company-wiki/SKILL.md")
        self.assertIn("Init → Bootstrap → Explore ↔ Query → Curate → Add Source → Maintain → Validate", skill)
        for name in ("registry", "init", "bootstrap", "query", "curate", "add-source", "maintain", "validate", "change-protocol"):
            self.assertIn(f"references/{name}.md", skill)
        self.assertIn("compatibility alias", skill)

    def test_retrieval_principles_and_bounds(self) -> None:
        skill = text("skills/company-wiki/SKILL.md")
        query = text("skills/company-wiki/references/query.md")
        for phrase in ("router, not a gate", "retrieval prior, not a boundary", "one routing phase", "40,000"):
            self.assertIn(phrase, skill)
        self.assertIn("same operation", query)
        self.assertIn("return to routing", query)
        self.assertIn("Bypass both wikis", query)

    def test_scopes_legacy_and_authority(self) -> None:
        registry = text("skills/company-wiki/references/registry.md")
        protocol = text("skills/company-wiki/references/change-protocol.md")
        for phrase in ("company-index", "team", "personal", "legacy combined wikis", "never grant capability"):
            self.assertIn(phrase, registry)
        for phrase in ("authenticated principal", "destination audience", "invalidates approval", "stop at first failure"):
            self.assertIn(phrase, protocol)

    def test_bootstrap_is_reference_only(self) -> None:
        bootstrap = text("skills/company-wiki/references/bootstrap.md")
        for phrase in ("Do not sample", "opaque", "no child title", "broad direct-source search unavailable"):
            self.assertIn(phrase, bootstrap)

    def test_add_source_and_maintenance_are_bounded(self) -> None:
        add_source = text("skills/company-wiki/references/add-source.md")
        maintain = text("skills/company-wiki/references/maintain.md")
        self.assertIn("compatibility alias", add_source)
        self.assertIn("finite batch", add_source)
        self.assertIn("source/destination audience", add_source)
        self.assertIn("Retired", maintain)
        self.assertIn("Merged into", maintain)

    def test_readmes_and_example_have_current_model(self) -> None:
        for relative in ("README.md", "README.zh-CN.md", "skills/company-wiki/README.md"):
            document = text(relative)
            self.assertIn("Bootstrap", document)
            self.assertIn("Add Source", document)
            self.assertNotIn("home/map → guide → focused detail", document)
        self.assertIn("one routing phase", text("examples/sample-company/company-wiki-home.md"))

    def test_main_contract_requires_proposal_and_one_phase_routing(self) -> None:
        specification = text("tests/test-company-wiki-skill.md")
        self.assertIn("approved proposal", specification)
        self.assertIn("change-protocol.md", specification)
        self.assertIn("one routing phase", specification)
        self.assertIn("correction is not approval", specification)
        self.assertNotIn("references/ingest.md", specification)

    def test_scoped_lifecycle_fixtures_exist(self) -> None:
        root = REPOSITORY / "tests/company-wiki-skill"
        expected = (
            "lifecycle/Acquisition Planning 2026.md",
            "lifecycle/personal/Q3 Field Priorities.md",
            "lifecycle/personal/controls/pinned.md",
            "lifecycle/personal/controls/temporary.md",
            "lifecycle/personal/controls/personal-canonical.md",
            "lifecycle/personal/controls/do-not-curate.md",
            "registry/legacy-profile.md",
            "registry/role-claim-profile.md",
        )
        self.assertTrue(all((root / relative).is_file() for relative in expected))


if __name__ == "__main__":
    unittest.main()
