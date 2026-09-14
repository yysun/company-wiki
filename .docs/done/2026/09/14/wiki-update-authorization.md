# Wiki update authorization

Explicit Add Source/Ingest, Curate, and Maintain requests now authorize necessary bounded edits to an existing
selected wiki, carrying that intent through later candidate selection. The agent presents concrete changes,
revalidates, and applies without an extra approval turn. Read-only requests and source selection alone authorize
no writes; review-first requests keep exact-proposal approval.

Task-authorized updates may reconcile a changed target while preserving concurrent edits and repeating protection
checks. Material changes to an explicitly approved proposal require fresh approval. Setup/registration approval,
source/destination boundaries, provider authority, audience containment, protected writes, and unknown-outcome stops
remain intact. Current guides, repository rules, and affected scenarios follow the same contract.

## Verification

- 23 adapter/contract tests passed; skill-creator validation passed; 16 added Markdown links resolved; whitespace checks passed.
- All 12 independent decision cases and variants matched expectations. A supplemental budget case correctly required
  explicit expansion when mandatory rereads could not fit. These are instruction interpretation checks.
- AR passed; CR passed in round 3 after fixing operation-wide scenario scoring and its dependent recovery allowance.
- Implementation commits: `3e22631`, `04aabff`; story base: `6682cc6`. No push was performed.

Live provider execution was not tested. This changes the portable skill contract; it neither implements provider
enforcement nor updates a live wiki or registry.

## Final VR result

VR acceptance results:

1. **Complete:** Explicit Add Source, Curate, and Maintain requests authorize bounded edits; subsequent source selection retains intent. Shared protocol and A1/A2/A5/A6 evidence agree.
2. **Complete:** Read-only requests, factual corrections, and suggestions authorize no writes; review-first requests require exact approval. Covered by A3/A4/A5 variants.
3. **Complete:** Concrete plans, provider authority, audience checks, rereads, protected writes, verification, and source immutability remain required. A7 confirms capability failures cannot be bypassed.
4. **Complete:** Task-authorized replanning preserves concurrent edits; materially changed exact proposals require fresh approval. A8/A9 cover drift and recovery.
5. **Complete:** Source/destination boundaries, promotion restrictions, setup/registration approval, unknown-outcome stops, and operation-wide read budgets remain intact. Covered by A2/A6/A9/A11/A12 and corrected lifecycle scenarios.
6. **Complete:** Live instructions, repository rules, guides, and affected scenarios agree. All plan tasks are complete. Recorded evidence comprises 23 passing tests, skill validation, 16 resolved Markdown links, whitespace validation, and 12 independent decision cases with variants.

VR passed: all acceptance criteria complete

VR risk: non-low — user-authorization semantics and preserved publication/recovery boundaries.
VR review round: 1; reviewer: reused.

Verification establishes package validity and instruction interpretation. Live provider execution remains untested and outside scope. No tests were rerun during review.
