# Wiki update authorization

**REQ:** [req-wiki-update-authorization.md](../../../../reqs/2026/09/14/req-wiki-update-authorization.md)
**Story base:** `6682cc6` (clean worktree at entry)

## Contract

For updates to an existing selected wiki, distinguish authorization to complete a bounded task from approval
of an exact reviewed proposal. Both require a concrete plan before protected writes. A task request can cover
routine implementation choices and a fresh reconciliation; exact-proposal approval cannot silently cover a
materially revised proposal. A review-first request restricts authorization even when the verb says update.

Carry update intent through candidate selection without expanding the exact displayed set or resetting bounds.
Read-only requests and source access alone never establish update intent. Ask only for missing decisions or
additional authority after making the proposed action concrete. Setup and registration keep their existing
exact-proposal gates; promotion requires explicit destination authority and its own requested scope.

## Tasks

- [x] Update AGENTS.md, SKILL.md, change-protocol.md, add-source.md, curate.md, maintain.md, and related live
  references for task authorization, review-first behavior, concrete planning, drift, and recovery semantics.
- [x] Reconcile EN/CN/package guides and current product/article descriptions; update affected lifecycle
  scenarios while keeping proposal-approval failure cases explicitly review-first. Remove obsolete static
  wording assertions without adding tests that merely mirror instruction wording.
- [x] Run the adapter/contract suite, relevant package/link validation, and independent synthetic decision
  cases in [the story spec](../../../../tests/test-wiki-update-authorization.md). Record expected/observed
  behavior and limits; fix contradictions revealed by those checks.

## Verification and risk

Non-low risk: changes user-authorization semantics across write workflows. Independent AR/CR/VR review applies.
Read inspection confirms the shipped adapter supports list/read/preflight/write only, so it cannot execute
positive governed-publication cases. Use isolated read-only decision evaluation of the skill for this change;
do not claim that it verifies provider enforcement or actual wiki writes. This is the planned story ET surface.
Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/company-wiki-skill/adapter -p 'test_*.py' -v`,
skill-creator `quick_validate.py`, Markdown link checks for changed files, and `git diff --check`.
The independent evaluator receives scenario inputs and the skill, without expected decisions or author conclusions.

## Review evidence

AR passed: no blocking architecture flaws

AR risk: non-low — user-authorization semantics across durable write workflows.
AR review round: 1; reviewer: new (`authorization_review`)

The independent reviewer identified no blocking flaw. Implementation must distinguish registry/setup version
binding from task-authorized page replanning in registry.md as well as the shared protocol.

Implementation verification: 23 adapter/contract tests passed; skill-creator validation passed; 16 added Markdown
links resolved; diff whitespace check passed. The obsolete assertion that every correction needs a second approval
was removed; independent decision cases cover authorization behavior rather than matching instruction wording.
Independent evaluator `authorization_decisions` completed all 12 raw-input cases and variants with the expected
decisions and no instruction conflict changing those decisions. The execution record is in the story spec.
No provider writes were run.

Implementation milestone: `3e22631` — authorization contract, affected guides and scenarios. Verification at commit:
23 package tests, skill validation, 16 added links and whitespace check passed; decision evaluation subsequently passed.

CR round 1 (`authorization_review`, reused) found one blocking scenario inconsistency: L-C6 still scored bounds
per turn while the contract and L-C6's later rules require an operation-wide budget. Corrected the scorer contract
to aggregate selection, approval, revalidation, replanning, and recovery event logs; expansions preserve consumed
counts. CR round 2 verified that fix and found its dependent positive recovery fixture would exceed the default
five-read allowance. L13 now explicitly authorizes 12 source read calls across its L18/L19 recovery chain while
preserving exact source selection and all other bounds. A low-remaining-budget variant requires expansion or
narrowing instead of a turn-based reset. A supplemental independent budget case confirmed that any smaller
selection must also fit mandatory rereads; one remaining read is insufficient even for one report.

CR passed: no major findings

CR risk: non-low — changes authorization across durable wiki workflows.
CR review round: 3; reviewer: reused (`authorization_review`)

VR passed: all acceptance criteria complete

VR risk: non-low — user-authorization semantics and preserved publication/recovery boundaries.
VR review round: 1; reviewer: reused (`authorization_review`)

All six acceptance criteria and all plan tasks passed independent review. Existing test and skill evidence remains
valid: later edits corrected only the affected scenario budget and recorded review/evaluation results. The full
criterion-level VR result is retained in the completion report. Provider execution remains outside scope.

Correction milestone: `04aabff` — operation-wide scenario budgets, explicit recovery allowance, and completed
independent evaluation/review evidence. No push or final-delivery GC was performed.
