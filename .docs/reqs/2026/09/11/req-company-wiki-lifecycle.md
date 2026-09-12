# Requirements: company-wiki personal knowledge lifecycle

## Requirements source

This story implements the product model and V1 requirements in
[`docs/company-wiki-personal-wiki-requirements-v0.3.md`](../../../../../docs/company-wiki-personal-wiki-requirements-v0.3.md),
plus the five retrieval principles the user added on 2026-09-11, and synchronizes the product contract in
[`docs/company-wiki_PRD_v0.5.md`](../../../../../docs/company-wiki_PRD_v0.5.md).
Where the earlier lifecycle used `Init` and `Ingest`, this requirement separates company-index initialization
from personal-wiki bootstrap and gives bounded source reconciliation the user-facing name `Add Source`.

## Problem

The skill currently treats a wiki as one curated map over one source collection. That collapses three distinct
things: the company's shared navigation skeleton, a user's personal map, and the original documents that remain
authoritative. It also makes representative sampling sound like work every new user must repeat and makes
`Ingest` sound like a prerequisite pipeline that copies or indexes documents before they can be queried.

The product needs a permission-aware shared Company Library Index, a user-controlled Personal Wiki, and a
progressive lifecycle that grows only from useful work. Explicitly selected documents and bounded folders still
need a safe reconciliation path, but that path must not become corpus-wide ingestion infrastructure.

## Outcome

Expose this product architecture:

`Company source library → Company Library Index → Personal Wiki → Progressive Expansion`

The Company Wiki Admin initializes and governs a small shared Company Library Index. A Personal Wiki bootstraps
from references to the visible portion of that index, without resampling the company corpus. The user's actual
work then expands the Personal Wiki through:

`Explore ↔ Query → Curate → Maintain → Validate`

Retrieval follows five principles:

- The wiki is a router, not a gate.
- The Personal Wiki is a retrieval prior, not a retrieval boundary.
- The tree is for navigation; the graph is for discovery.
- The wiki guides; original documents prove.
- Routing is one phase, not many sequential LLM hops.

`Add Source` is an optional, bounded route into Explore and Curate for explicitly selected source documents or
folders. Existing `Ingest` wording may remain only as a compatibility alias for `Add Source`; user-facing guidance
must explain reconciliation and must not imply copying, chunking, embedding, or pre-indexing.

## Acceptance criteria

### Product layers and ownership

- [ ] The skill distinguishes the authoritative company source library, the shared Company Library Index, an
      optional Team Wiki layer, and a user-controlled Personal Wiki as linked overlays rather than duplicate
      document repositories.
- [ ] Company-wide canonical concepts, terminology, aliases, relationships, and authoritative source mappings
      are governed by a Company Wiki Admin. Personal structure and durable personal content are controlled by
      the end user. The data model does not block a future Team Wiki curator or Personal → Team → Company
      promotion path.
- [ ] Lower-scope wikis reference shared knowledge wherever practical instead of copying it. Promotion reconciles
      a candidate with existing shared knowledge, preserves provenance, and requires the destination scope's
      approval authority.
- [ ] At creation/update time and in every agent-mediated read or answer, shared index pages, personal pages,
      titles, links, summaries, backlinks, aliases, inferred relationships, search results, and activity do not
      reveal knowledge outside the current user's source access. Derived knowledge is written only when its
      destination audience is no broader than its evidence audiences.
- [ ] New durable provider-derived content requires provider-enforced continuing audience containment across
      native content, metadata/previews, history, and export surfaces, including Personal copies and index references.
      ACL snapshots alone block publication. Unsafe legacy wiki bytes are gated before model ingestion; bounded
      separately registered source search remains available. V1 supplies no sync service and cannot recall disclosed
      copies; Validate/Maintain report and explicitly repair legacy exposure without claiming history erasure.
- [ ] V1 writes source-derived knowledge to a shared destination only when the provider can verify both the
      authenticated writer's governance capability and that the destination audience is a subset of every
      contributing source audience, including transitive inputs. If authority, current containment, or continuing
      protection is unavailable, refuse publication. Generate only from destination-authorized evidence; excluded
      prior context requires clean-context regeneration or refusal. Removing tokens or citations is not sanitization.
- [ ] Registry text may name an expected owner or role but never grants authority. Personal, Team, and Company
      writes require provider-authenticated identity plus verified write/governance capability on that exact
      destination; unavailable or unverifiable identity, capability, or audience results yield a draft/proposal
      only and no durable write. Private user-owned local originals and synthetic fixtures may use effective local
      identity/access and verified private destination scope; this exception never authorizes export of governed
      evidence or Team/Company writes. Check outcomes distinguish verified, denied, and unavailable.

### Company Library Index initialization

- [ ] Company-index `Init` requires an explicitly named original-material location and a separate writable index
      destination. It performs bounded discovery and representative sampling to create the smallest useful
      permission-aware map; it does not process every document or mark a collection fully ingested.
- [ ] The shared index is a configurable progressive-disclosure map of meaningful topics, concepts, entities,
      teams, products, systems, processes, policies, projects, decisions, metrics, datasets, and source entry
      points—not a flat catalog of files.
- [ ] Representative sampling may construct or improve the shared Company Library Index, but it is never required
      when bootstrapping an individual Personal Wiki.

### Personal Wiki bootstrap

- [ ] `Bootstrap` requires an explicitly selected Company Library Index and a separate writable Personal Wiki
      destination. It creates only a minimal personal structure and references to the visible shared map.
- [ ] Bootstrap does not sample the company corpus, copy the shared index, generate pages in bulk, chunk or embed
      documents, or require a database. If a shared index is unavailable, the skill reports that clearly and may
      still support direct-source Query when the user explicitly provides an accessible source location.
- [ ] Bootstrap never adopts a source boundary declared by wiki content. It may record an exact source location
      only when the user supplies that location as a separate explicit input; otherwise the Personal profile says
      broad direct-source search is unavailable until such a location is supplied.
- [ ] A Personal Wiki may organize topics, projects, investigations, working hypotheses, annotations, frequently
      used sources, and priorities independently of the company folder hierarchy while retaining links to shared
      concepts and original evidence.
- [ ] A scoped Personal profile may contain one explicit contained relative link to its Company Library Index
      profile. Cross-scope work starts from one selected profile and may follow only that named profile edge. A
      promotion additionally requires the user to select the exact destination profile; the agent never scans or
      guesses a second profile.
- [ ] Profiles without a scope or governing-capability locator remain legacy combined wikis. They support Query
      and Validate, plus same-destination Maintain/Add Source only when the provider verifies current-user write
      permission. They cannot authorize Bootstrap, shared canonical writes, Team/Company promotion, or inferred
      ownership. Upgrade requires explicit scope, governing destination, and authority inputs and preserves the
      old profile until the replacement registration succeeds.

### Retrieval principles

- [ ] **Router, not gate.** Wiki content only routes.
      - Missing, incomplete, stale, or unrelated wiki coverage never blocks or narrows retrieval from
        registered, accessible sources.
      - No source must be mapped, curated, or added before it can be searched, read, or cited.
- [ ] **Prior, not boundary.** The Personal Wiki weights where retrieval starts and which routes rank first. It
      never limits the search space to personally curated nodes; the Company Library Index and the registered
      source scope remain searchable within the same bounds.
- [ ] **Tree for navigation; graph for discovery.** Each wiki scope exposes a navigation tree for progressive
      disclosure: every node has one primary parent route from its home/map.
      - Cross-links, backlinks, aliases, and optional typed relationships form a discovery graph. Explore
        follows it across branches and scopes.
      - A graph edge never replaces a node's place in the tree, and a node's position in the tree never implies
        a relationship.
- [ ] **Wiki guides; original documents prove.** Wiki pages select, frame, and connect evidence.
      - Every factual claim in an answer is supported by an original document read in the same operation.
      - A wiki statement that has not been verified that way is presented as unverified navigation, not as fact.
- [ ] **One routing phase.** Query and Explore first read the selected scope's compact routing context
      together: the Personal Wiki home and, through its named edge, the Company Library Index home, with their
      outlines, aliases, and source entry points.
      - From that context they choose candidate wiki nodes, source routes, and direct searches in one decision,
        before retrieving evidence.
      - They do not walk home → guide → detail one LLM hop at a time to locate evidence.
      - Evidence retrieval may iterate inside the selected source routes and registered scope, but the operation
        does not return to wiki routing or run another route-selection LLM phase. An unusable route is reported;
        a materially new route requires a new Query or Explore operation.
      - A direct-source bypass is itself a routing decision and may read no wiki page. Whenever a Query or
        Explore operation reads any wiki page, it reads the routing context first.

### Explore, Query, and Curate

- [ ] `Explore` starts from the single routing phase, whose decision may use discovery-graph edges exposed in the
      routing context. Retrieval then broadens in bounded rounds, not per-hop model calls, through likely source
      areas, native source search, and finally source documents and sections. Exploration remains transient until
      a separate Curate decision makes it durable.
- [ ] `Query` is the dominant runtime path. Its routing phase uses the Personal Wiki as a prior and the shared index
      as a router. It then retrieves the smallest useful original-source evidence and answers with direct source
      citations and explicit uncertainty or conflicts.
- [ ] Query can bypass both wikis for exact identifiers, recent or unrepresented documents, a more efficient direct
      search, an unavailable wiki, or an explicit user request. Query never requires prior Add Source processing.
- [ ] The answer path remains read-only. Reusable discoveries may trigger a separate Curate proposal, but no query
      silently writes back to a Personal, Team, or Company wiki.
- [ ] `Curate` promotes only durable, reused, explicitly requested, project-important, structurally useful, or
      policy-approved discoveries. It prefers small navigation knowledge and may create nodes, links, aliases,
      typed relationships, concise source-grounded summaries, or source mappings without preserving every fact.
- [ ] Before Curate changes durable knowledge, the agent names the destination scope, affected pages, evidence,
      conflicts, proposed edits, and preserved user-authored organization. Application requires the owner or
      governing authority's approval unless an already-defined policy explicitly permits the exact safe action.
- [ ] Personal Wiki controls are durable, human-readable sections in the personal home/map: pinned nodes,
      temporary nodes, personally canonical nodes, and topics the agent must not automatically Curate ("stop
      learning"). The user can add, remove, rename, merge, pin, mark/unmark, and reorganize personal nodes through
      Curate or Maintain; no hidden database or sidecar is required.

### Add Source reconciliation

- [ ] `Add Source` accepts only documents or a finite folder/batch explicitly selected by the user and keeps all
      discovery and reads inside registered source locations. A topic or broad location never silently expands
      into corpus-wide processing; a folder selection is enumerated and bounded before reading its contents.
- [ ] Add Source reads selected evidence deeply enough to assess claims, authority, scope, dates, conflicts, and
      affected routes, then compares it with relevant Personal Wiki and visible shared-index knowledge before
      proposing Curate actions.
- [ ] Selecting a source authorizes reading, not durable edits. Immediately before an approved apply, the agent
      reopens selected sources and targets, rechecks material content, links, permissions, ownership, governing
      authority, and destination boundaries, and invalidates stale approval when the plan would materially change.
- [ ] A preflight failure before apply writes nothing. A failed/unknown outcome during apply stops later writes.
      Add Source reconciles current state without automatic rollback and reports confirmed successful, confirmed
      failed, unknown, and unattempted changes with a recovery proposal. A retry proposes only remaining work and
      follows the shared contract for revised versus unchanged already-authorized actions.
- [ ] Re-adding unchanged evidence to a current wiki is a reported no-op and creates no duplicate pages, links,
      records, receipts, or mandatory logs. Add Source reports selected, changed, unchanged, skipped, unsupported,
      conflicting, and inaccessible material.
- [ ] Add Source never changes original sources and does not require source copies, embeddings, vector or graph
      databases, provider-side indexes, queues, sidecars, processing ledgers, background watchers, or sync jobs.

### Durable change protocol

- [ ] Company-index Init, Personal Bootstrap, Curate, Add Source, Maintain, and promotion all invoke one shared
      durable-change contract. It requires a concrete scope/target/evidence plan, authenticated governing
      authority, explicit approval, immediate source-and-target reread, link/ACL/audience/destination preflight,
      stale-plan invalidation, native conditional/exclusive updates, idempotent/conditional creates, dependencies
      before links, stop on first failed/unknown outcome, current-state verification, and a remaining-work-only
      recovery proposal. Timeouts do not prove failure; reconcile exact approved targets/original operation keys
      before retry. Preserve concurrent edits; unsupported protection yields no write. Unknown outcomes stay unknown.
- [ ] Setup treats provider documents and registry registration as non-atomic. Provider pages are created before
      the completed profile and index link, after registry feasibility preflight. Atomic conflict-protected index
      replacement preserves unrelated entries. A failure may leave an unlinked completed profile, preserves successful
      pages and pre-existing registry bytes, reports exact recovery work, and never deletes/recreates successful pages
      automatically. Recovery uses exact targets only and creates no registry ledger or sidecar.
      Existing profiles are reusable only on exact match; changed registrations create a fresh profile and switch
      the index link last. Approval binds the selected entry delta; unrelated index changes may be preserved via a
      fresh guarded merge, but selected-registration changes require revised approval.
- [ ] Approval is bound to the authenticated principal, destination scope, exact targets, evidence versions,
      audience/continuing-protection result, target versions, operation parameters, and proposal. A principal,
      capability, target, source, audience, or material-content change invalidates approval before any further write.
      An unchanged concrete remaining action already authorized in the session does not require redundant approval.

### Maintain and Validate

- [ ] `Maintain` corrects or restructures durable wiki knowledge: merge or rename nodes, change hierarchy, repair
      links and relationships, refresh summaries, replace obsolete sources, archive completed branches, or retire
      low-value nodes. It preserves user-authored organization unless the governing user approves restructuring.
- [ ] `Validate` independently enumerates the visible wiki graph and detects broken or inaccessible sources,
      source/version drift, stale summaries, missing provenance, orphans, duplicates, contradictions, superseded
      knowledge, suspicious relationships, permission leakage, important gaps, and missing evidence.
- [ ] Validate is read-only by default. It reports warnings, freshness states, and proposed maintenance actions;
      repairs are routed through Maintain or Curate and require the applicable authority or explicit safe-action
      policy. Validation does not require full source-corpus reprocessing.

### Structure, provenance, retrieval, and scale

- [ ] Wiki artifacts remain human-readable Markdown. Ordinary wiki and source links are the graph; aliases resolve
      to canonical nodes; typed relationships and machine-oriented state are optional and used only when useful.
- [ ] Substantive generated or curated claims retain, where available, stable source URI or ID, relevant
      section/page/block, source version, access/check time, source relationship, and verification state. Generated
      content is distinguishable from source text, human-authored notes, and verified company definitions.
- [ ] Conflicting sources remain separately cited with dates, known authority, supersession, and an explicit
      unresolved state; the agent never silently collapses them or invents provenance.
- [ ] Source access is provider-independent and may use local sync, native APIs, MCP, CLI, skills/connectors, or
      enterprise search. Local sync is not an authorization bypass, and native source ACLs remain authoritative.
- [ ] Navigation and retrieval use configurable bounds for traversal depth, search rounds, opened documents, and
      retrieved-evidence context. Cost scales with active questions and topics, not total corpus size; caches are
      optional and must preserve permissions and freshness.
- [ ] Bounds live as human-readable profile/request configuration, not hidden state. Defaults are traversal depth
      3, source search/list rounds 2, source documents opened 5, and 40,000 retrieved UTF-8 characters per
      operation. When the host exposes a reliable token count, a profile/request may set a token limit instead.
      A profile or request may set lower finite values. The agent checks exposed source size before a read where
      possible, stops and reports an exhausted bound before asking to expand it, and never silently raises a bound.
- [ ] Source changes can mark dependent knowledge current, potentially stale, superseded, or needing review.
      Refresh is lazy at the next relevant use rather than an eager full-wiki regeneration.
- [ ] Registry selection, explicit source and destination locations, provider capability limits,
      restricted-content handling, embedded-instruction resistance, and source immutability apply consistently to
      Init, Bootstrap, Explore, Query, Curate, Add Source, Maintain, Validate, and promotion.

### V1 behavior and documentation

- [ ] Behavioral specifications cover layer/role routing, one-phase routing, prior-not-boundary retrieval,
      graph-based discovery, company-index sampling, Personal Wiki bootstrap without
      sampling, bounded Explore, wiki-guided Query and direct-source fallback, Curate approval, Add Source single
      and folder selection, stale plans, permission denial, partial writes and retry, promotion authority,
      provenance/conflicts, query immutability, maintenance scope, validation immutability, and ACL non-disclosure.
- [ ] Tests use at least two authenticated principals with different source and destination capabilities. They
      prove that an admin's access cannot leak restricted derived metadata to a less-privileged reader, registry
      role text cannot self-authorize a write, unavailable identity/capability/audience fails closed, current
      source access is rechecked before agent-mediated use, and principal, target, authority, or audience drift
      invalidates an approved change.
- [ ] English and Chinese user-facing documentation describe the same layered architecture, progressive lifecycle,
      and Add Source semantics. Any retained `Ingest` term is clearly labeled as a compatibility alias for bounded
      reconciliation, not a centralized ingestion stage.
- [ ] The PRD describes the same Company Library Index, optional Team Wiki, Personal Wiki, role/permission model,
      lifecycle operations, source-authority boundary, and V1 scope as this requirement; it does not present the
      earlier single-wiki five-operation lifecycle as the current product.
- [ ] The MVP can demonstrate one source provider, one admin-governed Company Library Index, one Markdown Personal
      Wiki, permission-aware access, bootstrap by reference, Explore, Query with fallback and citations, Curate,
      basic Maintain/Validate, Add Source, provenance, obvious leakage prevention, and a Personal → Company
      promotion proposal/review. Team Wiki execution may be deferred, but its scope is representable.

## Constraints

- Preserve provider-native source documents as the authority for content, ownership, ACLs, sharing, versions,
  deletion, retention, editing, and auditability.
- Preserve the document-native graph: Markdown/provider wiki documents are nodes and ordinary links are edges.
- Preserve the registry as contained locator and navigation configuration only; do not store credentials, source
  copies, evidence caches, records, sidecars, or processing history in it.
- Reuse only host-exposed provider, document, repository, search, and permission capabilities. Keep wiki logic
  provider-neutral and compatible with flat collections, local sync, and repository sources.
- Keep all wiki writes inside the separately verified destination for the selected ownership scope.
- Preserve compatibility with existing registry profiles; adoption must not require a database migration.

## Non-goals

- Exhaustive ingestion, chunking, embedding, summarization, or graph extraction across the company corpus.
- A centralized source mirror, vector database, graph database, search service, parallel ACL system, processing
  ledger, queue, mandatory activity log, watcher, scheduled ingestion, or continuous synchronization.
- Replacing source-system search, storage, permissions, versioning, retention, or audit functions.
- Automatically making every discovery durable or promoting personal knowledge to a shared canonical scope.
- Forcing a Personal Wiki to mirror the company folder structure or requiring every user to curate shared taxonomy.
- Requiring Team Wiki execution, a custom frontend, formal enterprise ontology, or advanced retrieval for V1.

## Blocking questions

None. Version 0.3 resolves the architecture by separating company-index initialization from Personal Wiki
bootstrap and by defining explicit source reconciliation as optional `Add Source`, not mandatory ingestion.
