# Bounded wiki retrieval

Completed 2026-09-14. The first three restriction-review findings are fixed in the live company-wiki skill.

- Routine source reads and required update rechecks now have separate finite allowances. Multiple sections share
  a document slot. Explicit existing limits keep their meaning, including higher aggregate allowances; retries
  and pagination cannot reset counters.
- Unambiguous source descriptions and complete, explicitly requested finite batches resolve directly to reported
  exact targets. Ambiguous or incomplete selections still need clarification; later arrivals do not join a batch.
- Query/Explore can make one targeted wiki follow-up when original evidence reveals a missing authority, alias,
  or exception, within existing profile, traversal, and retrieval bounds.

Setup/registration approval, review-first behavior, publication access and governance, protected writes,
original-source immutability, and read-only workflows remain intact. No live registry or wiki was changed.

## Evidence

- [Requirements](../../../../reqs/2026/09/14/req-bounded-wiki-retrieval.md): six acceptance criteria complete.
- [Plan](../../../../plans/2026/09/14/plan-bounded-wiki-retrieval.md): AR round 2, CR round 3, VR round 1 passed.
- [Decision evaluation](../../../../tests/test-bounded-wiki-retrieval.md): all 18 independent scenarios and variants
  passed, including existing higher/lower limits, frozen batch selection, and pagination.
- All 23 adapter/contract tests and 19 benchmark/report unit tests passed (42 total). Skill validation,
  27 added Markdown links, and whitespace checks passed.
- Local implementation milestones: `64ed423` and `a0554d9`. Stopped before GC; no release or push.

The implementation is a skill instruction contract. Checks establish package validity and interpretation;
live-provider execution/enforcement and retrieval-quality improvements remain untested. Historical benchmark
results and the runner's documented stricter overrides are unchanged. Pre-existing authorization-story artifacts
were preserved and excluded from these commits.

## Final independent VR result (verbatim)

VR acceptance results:

1. **Complete — Separate finite budgets.** The shared retrieval contract defines distinct-source, evidence-read, verification-read, discovery, character, and traversal limits. B1/B2 confirm three short documents can be reconciled and rechecked, and multiple sections occupy one distinct-source slot.
2. **Complete — Existing limits and accounting preserved.** Explicit aggregate allowances replace unspecified component defaults while separately explicit caps remain binding. Verification is reserved; retries, overlap, pagination, and recovery consume existing counters. B3–B5/B16–B18 verify these rules and both lower and higher legacy allowances.
3. **Complete — Source intent resolves without redundant selection.** Exact identity or complete finite membership permits a reported, frozen selection. Ambiguity, truncation, incomplete membership, oversized batches, and generic patterns still require selection, refinement, or expansion. B6–B9/B14/B18 cover these boundaries.
4. **Complete — One bounded routing follow-up.** Query/Explore allow one targeted follow-up for an evidence-established gap, including after a direct-source bypass. Profile edges, access, depth, source budgets, and read-only behavior remain enforced. B10–B13 cover permitted and refused cases.
5. **Complete — Protected boundaries unchanged.** Setup/registration approval, review-first instructions, original-source immutability, publication/governance checks, protected writes, and unknown-outcome stops remain intact. B14/B15 and completed CR support this conclusion.
6. **Complete — Documentation and verification agree.** Live instructions, guides, examples, product descriptions, and affected scenarios are reconciled. All plan tasks are complete. Evidence records 42 passing unit tests, skill/link/whitespace validation, and all 18 independent decision scenarios with variants. Historical results and stricter benchmark overrides remain identifiable and unchanged.

The reviewed scope excludes pre-existing wiki-update-authorization artifacts. Verification establishes package validity and instruction interpretation; live-provider execution, provider enforcement, and retrieval-quality improvements remain untested. No tests were rerun during VR.

VR passed: all acceptance criteria complete

VR risk: non-low — source-selection authority and retrieval-limit compatibility.
VR review round: 1; reviewer: reused.
