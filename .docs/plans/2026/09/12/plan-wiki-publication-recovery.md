# Plan: wiki publication and recovery

**Story:** `wiki-publication-recovery`
**Git base:** `0ad9a9e`
**Risk:** non-low — publication authorization, confidentiality, concurrent writes, and recovery contracts.

## Decisions

- The repository ships skill instructions, not a production connector. Fix executable agent guidance and product
  contracts; do not turn the small local fixture adapter into a simulated enterprise security implementation.
- Require continuing source/destination containment for provider-governed derived bytes, including personal copies.
  A provider that exposes only current ACL snapshots cannot support such durable publication. Keep private local
  originals and test fixtures usable; local availability of governed/synced evidence does not qualify for that path.
- Gate legacy wiki reads before content reaches the model, using protected provider metadata/capabilities. If the
  boundary cannot be established, bypass unsafe routing for bounded authorized source search; do not invent provenance.
- Use native idempotency, conditional creation/update, and safe exact-target reconciliation. Unsupported capabilities
  yield a proposal; preserve ambiguity instead of guessing that a timeout means failure. No destructive auto-rollback.
- Registry registration is not a distributed transaction. Per-file atomic replacement plus conflict protection and
  publishing the index link last prevents a reachable incomplete registration; an unlinked completed profile may remain.
  Existing profiles are reused only on exact match; changed registrations create a fresh profile and switch the index
  link last. Approval binds the exact selected-entry delta, permitting a guarded merge of unrelated index entries only.
- Security removal/retirement must not perpetuate a restricted title, link, or relationship in a broad stub.

## Tasks

- [x] Probe package/adapter capabilities by inspection before changing contracts; document the executable coverage
      boundary. Do not run live provider tests without selected source and destination locations.
- [x] Add one publication reference, route every lifecycle read/write through it, and strengthen change/registration
      protocols for current/continuing protection, isolated generation, conditional writes, and unknown outcomes.
- [x] Reconcile repository AGENTS boundaries, PRD sections 7–8, personal access requirements, current lifecycle acceptance criteria, and English,
      Chinese, and package guides. Preserve source-boundary and taxonomy contracts.
- [x] Add focused executable acceptance scenarios with prerequisites and observable outcomes; update affected legacy
      scenarios to distinguish unsafe historical pages from newly publishable pages and existing fixture capabilities.
- [x] Run independent read-only scenario evaluation against the completed skill and review all changes since base.
- [x] Run Python unit/contract suites, skill validator, and relative-link/diff checks; record limits and final evidence.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/company-wiki-skill/adapter -p 'test_*.py' -v`
- Run the installed skill-creator `scripts/quick_validate.py` against `skills/company-wiki`.
- Execute the isolated decision scenarios in `.docs/tests/test-wiki-publication-recovery.md` with an independent agent;
  use fixture/provider response transcripts only. No connected source reads or provider/registry mutations.
- Provider native-access and concurrency scenarios require a separately selected deployment and capability probe;
  this story specifies them, does not claim to implement or execute a cloud connector.

## Review and evidence

AR round 1, independent reviewer `publication_review`: no blocking design flaw. D2 was narrowed to Curate in an
existing private profile, preserving Bootstrap's selected-index prerequisite.

AR passed: no blocking architecture flaws

AR risk: non-low — confidentiality, publication authorization, concurrent writes, and recovery contracts.
AR review round: 1; reviewer: new

Feasibility inspection: the shipped adapter implements only `list`, `read`, `preflight`, and `write`. Richer
operations in the lifecycle specification are requirements, not implemented provider capabilities. Its tests
cannot establish identity, continuing ACL protection, conditional writes, or crash-safe idempotency.

Milestone verification: the 23 existing Python unit/contract tests pass, skill-creator quick validation passes,
and the initial diff whitespace check passes. These are local package checks; independent decision evaluation
and final review remain in progress. No production provider or user registry has been accessed.

Milestone: `9652f51` — publication/recovery contracts, documentation, and acceptance scenarios.

Independent decision evaluation D1–D10 followed the publication/local/cleanup boundaries and found a D5 ambiguity
between index version drift and unchanged entry approval. Fixed with the exact-entry-delta rule above; D5 reevaluation
and new D11 passed without remaining instruction contradictions. See the test specification's execution record.
CR round 1 found existing-profile overwrite and an unsupported local demo route. Fixed by fresh-profile registration
and explicit synthetic-index Personal Bootstrap examples. CR round 2 passed, and round 3 confirmed the final AGENTS
consistency edit preserves the same scope. All reviews were independent and read-only.

CR passed: no major findings

CR risk: non-low — confidentiality, publication authority, concurrency, and recovery contracts.
CR review round: 3; reviewer: reused

Final local verification, 2026-09-12: all 23 Python tests pass on the corrected tree; skill-creator validation
passed (entrypoint unchanged afterward); all 22 added Markdown links resolve; `git diff 0ad9a9e --check` passes.
Independent interpretation coverage is D1–D11, including the corrected D5 rerun. Deployment acceptance cases 1–6
remain explicitly unexecuted; no live provider or registry was selected or accessed. This story implements the
portable contract and refusal/recovery decisions, not a cloud enforcement service.

Correction milestone: `549c7bc` — profile preservation, precise registration approval, supported local examples,
repository boundaries, and independent evaluation evidence. Final VR, round 1 with the reused independent reviewer:
all seven criteria complete; all plan tasks complete. Full verdict is retained in the completion report.

VR passed: all acceptance criteria complete
