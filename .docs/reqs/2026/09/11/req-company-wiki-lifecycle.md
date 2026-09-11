# Requirements: company-wiki lifecycle

## Problem

The skill currently exposes initialization, query, and a combined maintenance/validation workflow. A new
source can be handled as generic maintenance, but the product does not name or define the source-centered
operation that turns newly selected evidence into durable wiki changes. This makes initialization sound
like bulk ingestion and leaves users without a clear, auditable path for adding sources after setup.

## Outcome

Expose one coherent lifecycle:

`Init → Ingest → Query → Maintain → Validate`

Init bootstraps a minimal map from representative sampling. Ingest reconciles explicitly selected new
sources into the existing wiki. Query answers through the wiki and original evidence. Maintain corrects or
restructures wiki knowledge. Validate detects graph defects and source drift without changing the wiki by
default.

## Acceptance criteria

- [ ] The skill and user-facing documentation name and distinguish all five lifecycle operations in the
      required order.
- [ ] Init explicitly performs bounded discovery and representative sampling to create the smallest useful
      map; it does not claim to process every source document or mark a source collection as fully ingested.
- [ ] Ingest accepts only source documents or a bounded batch explicitly selected by the user and keeps all
      discovery and reads inside the registered original-material locations and scopes.
- [ ] Ingest defaults to one source at a time. Batch ingestion requires an explicit, bounded user selection;
      a folder, collection, or topic never silently expands into an all-source operation.
- [ ] Ingest reads each selected source deeply enough to assess its claims, authority, scope, dates, links,
      conflicts, and affected wiki routes, then compares it with the relevant existing wiki and evidence.
- [ ] Before any ingest write, the agent presents a concrete change plan naming affected wiki documents,
      preserved evidence links, conflicts or unresolved claims, and what will remain unchanged. Selecting a
      source authorizes reading it, not applying the proposed wiki edits; application requires explicit user
      approval.
- [ ] Immediately before applying an approved ingest plan, the agent reopens the selected sources and planned
      wiki targets, rechecks their material content, link targets, permissions, and destination boundary, and
      invalidates the approval when a material change would alter the plan. A stale plan is revised and
      presented for fresh approval before any write.
- [ ] If an apply-time preflight fails, Ingest writes nothing. If a provider write fails after earlier planned
      writes succeeded, Ingest stops, verifies what succeeded, does not automatically roll it back or continue,
      and reports successful, failed, and unattempted changes plus a recovery proposal. A retry reconciles
      current state and proposes only the remaining work.
- [ ] Approved ingestion applies the smallest coherent set of wiki-node and link edits, keeps original sources
      unchanged, and links to original evidence rather than copying it wholesale.
- [ ] Re-ingesting an unchanged source against an already-current wiki produces a reported no-op and creates
      no duplicate page, link, receipt, metadata record, or log entry.
- [ ] Ingest reports selected sources, documents created or changed, preserved evidence targets, conflicts,
      unsupported claims, permission failures, and sources that were skipped or unchanged.
- [ ] Ingest does not create embeddings, databases, source copies, provider-side search indexes, YAML/JSON
      records, metadata sidecars, folder taxonomies, mandatory ingest logs, or background synchronization.
- [ ] Query remains read-only and follows the smallest useful wiki-to-evidence path; a useful answer is not
      silently written back into the wiki.
- [ ] Maintain is limited to user corrections and approved wiki repair or restructuring that is not centered
      on processing a newly selected source.
- [ ] Validate has its own workflow route and reference contract, enumerates the visible wiki graph, checks
      broken links, drift, gaps, contradictions, authority, permissions, and orphans, and remains read-only
      unless the user separately requests fixes through Maintain.
- [ ] Registry selection, source/destination boundaries, provider capability limits, restricted-content
      handling, embedded-instruction resistance, and original-source immutability apply consistently to all
      five operations.
- [ ] Behavioral specifications cover lifecycle routing, init sampling, missing ingest selection, single and
      batch ingest proposals, approved application, stale proposals, preflight denial, partial writes and
      recovery, conflicts, permissions, idempotency, query immutability, maintenance scope, and validate
      immutability.
- [ ] English and Chinese user-facing documentation describe the same lifecycle and explain that Ingest is
      reconciliation, not centralized ingestion.

## Constraints

- Preserve the document-native graph: provider-native wiki documents are nodes and ordinary links are edges.
- Preserve the registry as locator/navigation configuration only.
- Reuse only host-exposed provider/document/repository capabilities; do not add a connector or dependency.
- Keep existing registry profiles compatible; adding Ingest must not require a migration.
- Keep source documents read-only and all wiki writes inside the profile's verified destination.
- Keep implementation guidance provider-neutral and usable with flat collections or repositories.

## Non-goals

- Automatic folder watching, scheduled ingestion, or continuous synchronization.
- Exhaustive initial ingestion of every document in a source location.
- A processing-status database, content hash ledger, queue, or mandatory chronological log.
- A vector database, search service, graph database, or generated source mirror.
- Automatic promotion of inferred or conflicting claims to authoritative wiki knowledge.
- Provider-specific implementation code.

## Blocking questions

None. The requested lifecycle and the existing safety contracts determine the required behavior.
