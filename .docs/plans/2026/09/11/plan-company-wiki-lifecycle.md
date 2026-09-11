# Plan: company-wiki lifecycle

**REQ:** [req-company-wiki-lifecycle.md](../../../../reqs/2026/09/11/req-company-wiki-lifecycle.md)
**E2E:** [test-company-wiki-lifecycle.md](../../../../tests/test-company-wiki-lifecycle.md)

## Outcome and boundaries

Add Ingest and Validate as first-class company-wiki operations while sharpening the boundaries of Init,
Query, and Maintain. This is a provider-neutral skill and documentation change; it introduces no runtime,
connector, index, persistence format, registry migration, or background process.

The story starts at Git base `00e3cac`. Three pre-existing modified closure artifacts for
`confirm-wiki-initialization-inputs` are unrelated and must remain unstaged and uncommitted.

## Consequential decisions

- “Ingest” means reconciling explicitly selected original evidence into an existing wiki. It does not mean
  copying, indexing, embedding, watching, or exhaustively processing a source location.
- Init samples representative sources only to bootstrap a minimal map. It cannot claim collection coverage.
- Ingest defaults to one source. Batches must be explicitly bounded by exact locators or an equally explicit
  finite selection supplied by the user.
- Source selection authorizes reads only. Ingest proposes a concrete change set and waits for explicit
  approval before writing wiki documents.
- Approved plans are revalidated against selected sources, target wiki nodes, exact links, permissions, and
  destination immediately before writing. Material drift invalidates the plan and its approval.
- Provider writes are not assumed atomic. A failed preflight produces no writes. A mid-apply failure stops
  further writes, preserves successful writes, verifies current state, reports successful/failed/unattempted
  changes, and proposes only the remaining reconciliation work; automatic rollback is forbidden because it
  could overwrite concurrent provider edits.
- Idempotency is outcome-based: compare selected evidence with the current wiki and make no edit when there
  is no material delta. No hash ledger, receipt, or sidecar is introduced.
- Validate becomes a separate read-only workflow. Fixes route to Maintain so validation cannot silently
  mutate the graph.

## Tasks

- [x] Update `skills/company-wiki/SKILL.md` to state the five-operation lifecycle, route Ingest and Validate
      independently, and load only each operation's required references.
- [x] Add `skills/company-wiki/references/ingest.md` with explicit selection, bounded reading, reconciliation,
      proposal/approval, application, idempotency, reporting, and failure behavior.
- [x] Add `skills/company-wiki/references/validate.md`; remove validation ownership from
      `skills/company-wiki/references/maintain.md` while preserving repair and restructuring behavior.
- [x] Extend `skills/company-wiki/references/registry.md` and root `AGENTS.md` so Ingest and the split Validate
      workflow inherit registry selection, missing/unsafe-profile behavior, source scope, destination,
      permission, and source-immutability boundaries without weakening Init's four-input gate.
- [x] Tighten `skills/company-wiki/references/init.md`, `query.md`, and `document-format.md` where needed so
      sampling, write boundaries, query immutability, and validation handoff are explicit.
- [x] Update root/package English documentation and `README.zh-CN.md` with the same lifecycle and the narrow
      meaning of Ingest.
- [x] Update the PRD lifecycle language without turning automated ingestion or centralized indexing into an
      MVP requirement.
- [x] Add the minimal standard-library-only test adapter and unit guard under
      `tests/company-wiki-skill/adapter/` as the first SS implementation task. It confines reads
      to configured source/wiki roots, confines writes to the wiki root, exposes list/read/preflight/write
      commands, records ordered test events outside the wiki, and supports deterministic read denial,
      preflight denial, and nth-write failure. Its transcript guard parses `codex exec --json` output and
      fails a run containing any model-issued source/wiki access outside an exact adapter invocation.
- [x] Immediately probe the minimal adapter before broader implementation: run its focused unit guard and one
      isolated read-only `codex exec --json` agent in a neutral temporary workspace. Pass only if the CLI emits
      retained structured command evidence, the guard accepts adapter-only access, a deliberately injected
      direct-access probe is detected as a failing bypass, permission denial and configured write failure are
      observable in adapter events, and source/user state remains unchanged. If any condition fails, stop and
      return to AR; do not continue product implementation or replace runtime evidence with prompting.
- [x] Reconcile `tests/test-company-wiki-skill.md` scenario summary, C2 write permissions, C5 routing table,
      validation wording, and pass criteria with the five workflows. Complete
      `.docs/tests/test-company-wiki-lifecycle.md` and exact fixtures for deterministic single/batch ingest,
      outside-scope and denied access, source drift, contradiction, stale-plan, preflight-denial, partial-write,
      and retry behavior.
- [ ] Run focused package/link/contract checks and commit the implementation milestone without staging the
      unrelated prior-story files.
- [ ] Run CR over the complete story diff and fix every major finding.
- [ ] Run all applicable TT checks. For ET, execute L1–L14. If no standalone transcript runner exists, use
      isolated `codex exec` agents in neutral temporary workspaces with the deterministic test adapter. Retain
      each prompt/report, ordered adapter event log, before/after source/wiki/registry checksums, and exit
      status. Disclose that CLI reports provide weaker proof than native tool-call transcripts and do not call
      the fallback full transcript proof. Stop if the agent fallback or deterministic adapter cannot be
      isolated safely.
- [ ] Run VR against every requirement, write DD with the complete VR result, and complete GC with only this
      story's files.

## Validation

- Verify all Markdown links in changed package, root documentation, and story artifacts resolve.
- Assert that `SKILL.md` routes exactly five lifecycle operations and that each new reference is reachable.
- Assert the Ingest contract contains explicit selection, single-source default, bounded batch behavior,
  proposal-before-write, approval, apply-time revalidation, stale-plan invalidation, partial-write recovery,
  idempotent no-op, original-source immutability, and forbidden infrastructure/state.
- Assert Init rejects exhaustive-ingestion semantics, Query writes nothing, Maintain excludes source-centered
  ingestion, and Validate is read-only and routes fixes to Maintain.
- Assert English and Chinese documentation contain the same lifecycle order and product distinction.
- Run `git diff --check` and inspect the complete diff from `00e3cac`, excluding unrelated pre-existing files.

## Risks

- The word “ingest” commonly implies bulk ETL or indexing. The contract must repeatedly constrain the term at
  user-facing and workflow levels.
- Splitting Validate from Maintain can leave stale links or duplicated instructions. Link and routing checks
  must cover every skill reference.
- Proposal-before-write could be weakened by treating “ingest this” as write approval. Tests must preserve
  the read-selection/write-approval distinction.
- Provider APIs may lack transactions. The workflow must stop at the first failed write and expose partial
  state rather than pretending atomicity or risking destructive rollback.
- A prose-only local adapter cannot prove permission or partial-write handling. Deterministic fault injection
  is test-only and must not leak state files or provider assumptions into the product contract.
- Adapter controls are meaningless if the isolated agent bypasses them with direct filesystem commands. Every
  CLI run must retain structured tool events and pass an allowlist guard that rejects non-adapter source/wiki
  access; the probe must prove the guard rejects a deliberate bypass trace before broader implementation.
- Without persistent hashes, idempotency cannot prove byte identity cheaply. The promised behavior is a
  semantic no-op after comparison, not a high-performance change detector.

## Review record

- AR round 1 blocked on missing partial-write/stale-plan semantics, incomplete lifecycle-wide boundary
  integration, contradictions with the inherited E2E contract, non-deterministic fixtures, an undefined ET
  fallback, and broken artifact links. The requirements, plan, and E2E specification were corrected before
  implementation.
- AR round 2 blocked because protected failure paths still lacked deterministic fault injection, fallback ET
  did not name mandatory scenarios/evidence, and stale-plan drift lacked a fixed fixture. The plan now starts
  SS with an isolation/fault-control probe, adds a test-only adapter and unit coverage, mandates L1–L14 in ET,
  and defines retained evidence.
- AR round 3 blocked because the probe preceded the adapter it needed and did not prevent or detect direct
  filesystem bypass. The minimal adapter and structured-event allowlist guard now precede the probe; broader
  implementation is gated on proving adapter-only evidence and deliberate-bypass rejection.
- `AR passed: no blocking architecture flaws`
- `AR risk: non-low — approval-gated multi-document provider writes cross permission, concurrency, and
  partial-failure boundaries despite the now-sufficient implementation and verification plan`
- `AR review round: 4; reviewer: reused`

## SS evidence

- Milestone `0c9791b` committed the requirements, approved plan, lifecycle E2E specification, deterministic
  adapter/guard, probe runner, unit coverage, and initial source fixture.
- The first adapter/guard unit run passed 6 tests.
- The unprivileged CLI probe could not initialize Codex account state because the repository sandbox exposes
  that state read-only. The required rerun used the approved isolated probe command and passed.
- Retained evidence under `/private/tmp/company-wiki-lifecycle-probe.cgnYgI/evidence-escalated/` includes the
  final report, structured JSONL, ordered adapter events, source checksums, exit status, valid-trace guard, and
  deliberate-bypass rejection. The source checksums were identical before and after.
- The implementation added dedicated Ingest and Validate references, split Maintain, tightened Init and
  Query, extended lifecycle-wide registry/data boundaries, synchronized English/Chinese documentation and the
  PRD, reconciled the main E2E contract, and added deterministic lifecycle fixtures. The focused suite now
  passes 16 adapter, guard, and static lifecycle-contract tests; 43 scoped local Markdown links and
  `git diff --check` pass.
