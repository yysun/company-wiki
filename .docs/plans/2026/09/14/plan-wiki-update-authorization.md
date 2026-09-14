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
- [ ] Run the adapter/contract suite, relevant package/link validation, and independent synthetic decision
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
The evaluator is running against raw inputs and the skill without expected answers. No provider writes were run.
