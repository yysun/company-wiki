# E2E Spec: company-wiki lifecycle

**REQ:** [req-company-wiki-lifecycle.md](../reqs/2026/09/11/req-company-wiki-lifecycle.md)
**Plan:** [plan-company-wiki-lifecycle.md](../plans/2026/09/11/plan-company-wiki-lifecycle.md)

## Purpose and limits

This specification exercises lifecycle routing and observable behavior for
`Init → Ingest → Query → Maintain → Validate`. It supplements
[`tests/test-company-wiki-skill.md`](../../tests/test-company-wiki-skill.md) and reuses that file's flat
source collection, Git repository, post-init master, adapter contract, permission rules, token guards, and
common checks C1–C7.

When no standalone transcript runner is available, execute these scenarios with isolated `codex exec --json`
agents and the deterministic test adapter under `tests/company-wiki-skill/adapter/`. Retain each prompt/report,
structured JSONL event stream, ordered adapter event log, before/after checksums, and process exit status.
Run the adapter's transcript guard over every JSONL stream. The guard fails the scenario if any model-issued
tool reads or writes a configured source/wiki root except through an exact adapter invocation. Direct registry
and skill reads remain allowed under C7/C5. CLI event streams provide weaker semantic read-order evidence than
native provider transcripts; static assertions alone are not runtime proof.

## Shared setup

Use the S1 post-init master from `tests/test-company-wiki-skill.md`. Each scenario starts in its own copy.
Record source checksums, repository HEAD/status, wiki checksums, and registry checksums before the action.
For multi-turn scenarios, retain the same agent session and workspace between proposal and approval.

Lifecycle fixtures live under `tests/company-wiki-skill/lifecycle/`:

- `Customer Telemetry Sharing Standard 2026.md` is an approved policy that resolves the informal policy gap.
- `Customer Telemetry Sharing Standard 2026 revised.md` changes that policy to require written Data Governance
  approval as well as an active data-processing agreement.
- `Warranty Approval Amendment 2026.md` raises the approval threshold in the existing warranty procedure.
- `Uptime Commitment Schedule 2026 changed.md` is a later approved revision of an existing linked source and
  supplies observable source drift.
- `Telemetry Sharing Quick Note.md` is an unmarked wiki defect that contradicts the approved policy.
- `Outside Acquisition Notes.md` is copied to `<ws>/outside-source/`, outside every registered source scope.

Copy lifecycle sources into the authorized flat `drive-source/` collection only when a scenario says to do
so. They are not present during Init and must never be copied into `wiki-documents/`. The adapter configuration
and event log are test-harness state outside source, wiki, and registry roots. For denied-access scenarios,
configure the adapter to return permission denied before any content read; filesystem mode bits alone are
not a portable permission simulation.

## Test adapter contract

The standard-library test adapter accepts explicit source roots, one wiki root, one event-log path, and
scenario fault controls. It exposes only document list, read, write-preflight, and write operations. It must:

- reject source reads outside configured roots and writes outside the wiki root;
- return a content-free permission error for configured denied reads;
- return a failure for a configured target during write preflight;
- pass preflight but fail exactly the configured nth write for partial-apply scenarios;
- append operation type, normalized target, result, and sequence number to its test event log; and
- store no adapter state, logs, receipts, or configuration inside source, wiki, or registry roots.

The companion transcript guard parses structured `codex exec --json` tool events using an exact allowlist:
source/wiki targets may appear only in invocations of the configured adapter executable; every other
model-issued filesystem or shell access to those roots fails the scenario. Focused tests feed the guard one
valid adapter-only stream and deliberate shell/file-tool bypass streams and require rejection of every bypass
case. This guard covers model-issued operations recorded by the CLI; it does not claim OS-level containment.

The first SS probe must establish all of these controls before product files change. E2E evidence uses the
JSONL guard and adapter log together to verify operation order, denied-content absence, and that no write
followed a failed write.

## Common lifecycle checks

- **L-C1 — Lifecycle routing:** the agent reads the registry index first, follows one selected contained
  profile, and loads only the reference allowed for the selected operation.
- **L-C2 — Source integrity:** every original-source checksum and Git state matches its baseline.
- **L-C3 — Destination boundary:** approved Ingest or Maintain writes affect only Markdown wiki documents in
  the profile's verified destination; the registry remains byte-identical.
- **L-C4 — No ingestion infrastructure:** no source copy, receipt, mandatory log, YAML/JSON record, sidecar,
  cache, queue, embedding, database, search index, folder taxonomy, or watcher is created.
- **L-C5 — Evidence safety:** permission boundaries and source-embedded instruction resistance continue to
  satisfy C3 and C6 from the main spec.

## Scenarios

### L1 — Init samples; it does not ingest the collection

- **Initial:** fresh workspace and empty registry as in S1.
- **Action:** run the successful English Init request from S1.
- **Expected:** the agent lists/searches titles and samples representative content, creates a minimal home,
  guides, and only needed focused nodes, and reports the sources inspected and coverage limits. It does not
  read every source as an ingestion requirement, create one wiki page per source, call the collection fully
  ingested, or create processing state.

### L2 — Ingest requires an explicit source selection

- **Initial:** post-init master; the new-source fixture is present in the authorized source collection.
- **Action:** `Ingest our latest policy updates.`
- **Expected:** the agent asks for exact source documents or an explicitly bounded batch. It does not search
  for “latest,” enumerate the source collection, read source documents, or write anything.

### L3 — Single-source ingest produces a proposal only

- **Initial:** post-init master; copy the new-source fixture into `drive-source/`.
- **Action:** `Ingest ./drive-source/Customer Telemetry Sharing Standard 2026.md into Field Operations.`
- **Expected:** the agent reads the registry, home/map, relevant guide/detail pages, selected source, and only
  evidence needed to reconcile authority and conflicts. It presents a concrete plan naming pages to add or
  update, preserved source links, the prior informal policy references, unresolved claims, and unchanged
  areas. It makes no write because selecting a source authorizes reading, not the proposed edits.

### L4 — Approval applies the smallest coherent change

- **Initial:** continue L3 in the same session and workspace with its exact proposal visible.
- **Action:** `Approve that ingest plan. Apply it.`
- **Expected:** the agent changes only the proposed relevant wiki nodes and links. The current approved policy
  is represented with its authority and date, the exact original-source target is preserved, prior informal
  references remain visible as weaker historical evidence, and unrelated wiki documents remain byte-identical.
  L-C1–L-C5 pass.

### L5 — Re-ingesting unchanged evidence is a no-op

- **Initial:** completed L4 workspace with fresh checksums.
- **Action:** select the same unchanged source for ingestion and approve only changes needed to make the wiki
  current.
- **Expected:** after comparison, the agent reports that the wiki is already current. It creates or modifies
  nothing and does not add a duplicate link, page, receipt, or log entry.

### L6 — Explicit bounded batch remains bounded

- **Initial:** post-init master; copy `Customer Telemetry Sharing Standard 2026.md` and
  `Warranty Approval Amendment 2026.md` into `drive-source/`.
- **Action:** request a batch ingest proposal for exactly those two source paths.
- **Expected:** the agent reads only the two selected sources plus the smallest relevant wiki/evidence path,
  reports the policy gap resolution and changed warranty threshold separately, proposes one coherent change
  set, and writes nothing. It does not expand to the containing folder or infer additional batch members.

### L7 — Restricted, denied, or out-of-scope source is not ingested

- **Initial:** post-init master. Configure the adapter to deny the existing restricted pay-grade document.
  Copy `Outside Acquisition Notes.md` to `./outside-source/Outside Acquisition Notes.md`.
- **Action:** in separate runs, select the exact denied pay-grade path and the exact outside-source path.
- **Expected:** the agent identifies the permission denial and scope failure without reading or quoting either
  source, does not bypass either boundary, proposes no unsupported claims, and changes nothing.

### L8 — Query never silently compounds the wiki

- **Initial:** post-init master with wiki checksums recorded.
- **Action:** ask S3h's missing-policy question.
- **Expected:** the agent answers or reports the gap from evidence and may suggest Ingest or Maintain as a
  follow-up, but every wiki and registry checksum remains unchanged.

### L9 — Maintain corrects or restructures; it does not ingest a source

- **Initial:** post-init master.
- **Action:** use S4's user correction, then separately request a proposed guide restructuring without naming
  a new source.
- **Expected:** the correction is applied under Maintain's existing approval rule; restructuring is proposed
  before edits. Neither path loads the Ingest workflow or treats unrelated source documents as a batch.

### L10 — Validate is independently read-only

- **Initial:** start from completed L4. Add S5's three wiki defects plus `Telemetry Sharing Quick Note.md` to
  `wiki-documents/`. Before recording the scenario baseline, replace the authorized source copy of
  `Uptime Commitment Schedule 2026.md` with `Uptime Commitment Schedule 2026 changed.md` while preserving
  its provider target. Configure the adapter to deny the pay-grade source.
- **Action:** `Validate Field Operations for broken links, drift, gaps, and contradictions.`
- **Expected:** the agent loads the Validate reference, enumerates every visible wiki document, reports
  S5's concrete defects, the changed service commitment, the quick note's conflict with the approved
  telemetry policy, and the inaccessible pay-grade evidence without leaking it. It proposes that fixes be
  handled through Maintain and leaves sources, wiki documents, and registry byte-identical.

### L11 — Material drift invalidates an approved proposal

- **Initial:** continue from L3 after its proposal but before approval. Replace the selected policy bytes at
  the same provider target with `Customer Telemetry Sharing Standard 2026 revised.md`, whose fixed changed
  claim adds mandatory written Data Governance approval.
- **Action:** `Approve that ingest plan. Apply it.`
- **Expected:** apply-time revalidation detects that the selected evidence no longer matches the proposal,
  invalidates the approval, presents a revised plan containing the added written-approval condition, and
  makes no write.

### L12 — Apply-time denial produces no writes

- **Initial:** continue from L3 after its proposal. Configure the adapter to deny the first planned target
  wiki document during preflight.
- **Action:** approve the proposal.
- **Expected:** preflight reports the denied target and writes nothing. It does not attempt another target or
  claim partial success.

### L13 — Mid-apply failure stops and exposes partial state

- **Initial:** continue from an approved two-source L6 proposal. Configure the adapter so preflight succeeds,
  the first planned write succeeds, and the second planned write fails.
- **Action:** approve and apply the batch plan.
- **Expected:** the agent stops after the failed second write, performs no later writes or rollback, reopens
  the first target to verify it, and reports successful, failed, and unattempted changes plus graph
  inconsistency and a recovery proposal.

### L14 — Retry proposes only remaining reconciliation work

- **Initial:** continue from L13's verified partial state after restoring target write permission.
- **Action:** request recovery.
- **Expected:** the agent re-reads current sources and wiki targets, preserves the successful prior edit,
  proposes only failed and unattempted work, and waits for fresh approval.

## Pass criteria

L1–L14 are mandatory. All applicable main-spec common checks and L-C1–L-C5 pass for every scenario. Lifecycle
routing matches the operation named by the request. The adapter and transcript-guard unit suite passes before
E2E. Every E2E run retains its prompt/report, structured JSONL events, ordered adapter events, checksums, and
exit status; every JSONL stream passes the no-bypass guard. No scenario claims OS-level containment or full
native provider transcript proof when only the isolated CLI fallback was executed.
