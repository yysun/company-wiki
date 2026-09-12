# Plan: taxonomy wiki + scoped cloud-drive search

**Story:** `taxonomy-wiki-scoped-cloud-drive-search`
**Git base:** `c2d5afb`

## Outcome

Make the product contract unambiguous: taxonomy is the governed backbone, typed links are the small
useful discovery graph on top, and scoped cloud-drive search retrieves original evidence. Keep the
existing permission, registry, source-immutability, and bounded-routing contracts intact.

## Consequential decisions

- The Company Library Index owns canonical terminology, aliases, source routes, and a limited set of
  reviewable typed relationships; it is not a generic graph or source-document mirror.
- Taxonomy and typed-link signals guide query expansion, source-scope selection, and ranking. They are
  never evidence, access authority, or a hard exclusion when they are incomplete or low-confidence.
- Search uses only the selected profile's registered source boundary and the host's existing cloud-drive
  capabilities. No custom connector, index, or provider-side infrastructure is introduced.
- Documentation and test specifications describe behavior. Provider-specific scoped-search, ACL, and
  native-link capabilities remain deployment feasibility checks rather than claims made by the package.

## Tasks

- [x] Update the requirement and PRD conceptual architecture/retrieval strategy to establish the
      taxonomy → typed links → scoped source-search model and its explicit non-goals.
- [x] Update the skill's product model, document format, and query contract so agents route through
      taxonomy and limited typed links before native source search, preserve a direct-search fallback,
      and do not perform graph-first traversal.
- [x] Synchronize English and Chinese public/package documentation with the same layer responsibilities
      and remove wording that frames the wiki as an undifferentiated knowledge graph.
- [x] Add a focused behavioral specification for taxonomy resolution, bounded direct fallback,
      multi-source evidence, and metadata-safe permission handling.
- [x] Extend the deterministic lifecycle contract checks to prevent the skill and public documentation
      from drifting away from the three-layer model.
- [x] Run the relevant Python contract/adapter suite and documentation consistency checks.

## Validation

- `python3 -m unittest discover -s tests/company-wiki-skill/adapter -p 'test_*.py' -v`
- inspect the story diff for the three-layer model, source-boundary preservation, and no unauthorized
  change to the user's untracked research report;
- execute the focused behavioral specification only when a provider capability probe and authorized
  cloud-drive locations are available. Until then, report it as specified but provider-unverified.

**Verification recorded:** 2026-09-12 — the deterministic adapter/lifecycle suite passed 23 tests with
`PYTHONDONTWRITEBYTECODE=1`. The focused cloud-drive behavioral specification is documentation-level
coverage; no provider, source collection, or writable taxonomy destination was supplied for a live run.

**Milestone:** `57834f5` — taxonomy-led source-retrieval contract, behavioral specification, and static
contract coverage.

**Verification-status record:** `1836f2c` — completed contract criteria and remaining provider/evaluation
evidence are recorded in the REQ.

## Risks

- Calling all ordinary links “graph” obscures the controlled taxonomy-first design and may invite
  unconstrained graph traversal. The updated contract must separate tree placement, typed links, and
  source retrieval.
- A taxonomy can become an accidental ACL side channel. The existing audience-containment and current-
  access reread rules apply equally to aliases, relationship labels, and source routes.
- Native cloud-drive search behavior differs by provider. The package must state unsupported scoped
  search or metadata behavior rather than simulate it.
