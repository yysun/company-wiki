# Company Wiki — Personal Wiki & Company Library Index Requirements

**Version:** 0.3
**Status:** Draft
**Date:** 2026-09-11
**Related Product:** `company-wiki`
**Related Docs:** Company Wiki PRD v0.3, Schema v0.1, Competency Questions

---

## 1. Purpose

This document defines requirements for extending `company-wiki` from a curated company-document navigation layer into a **personalized, progressively constructed wiki system** over the company's existing cloud document library.

The primary deployment uses native cloud documents and links for the index and wiki. Markdown and YAML examples
describe logical content or optional local representations; they do not require Markdown files, a Git repository,
or commit-driven maintenance. The installed skill's document-format contract governs production representation.

The design is based on three principles:

1. **The company cloud drive remains the source of truth.**
2. **The company provides a shared semantic/navigation skeleton.**
3. **Each user builds and evolves their own wiki over the documents they are allowed to access.**

The goal is to achieve the practical goals of RAG—finding relevant knowledge, reasoning across documents, grounding answers in evidence, and preserving provenance—without requiring a centralized duplicate document store or a mandatory vector database.

---

## 2. Product Model

The system SHALL consist of three logical layers.

```text
┌──────────────────────────────────────────────┐
│          Company Cloud Document Library      │
│                                              │
│  Existing Drive / WeCom / SharePoint / etc. │
│  Native documents, folders, ACLs, versions  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│          Company Library Index               │
│                                              │
│  Shared semantic/navigation skeleton         │
│  Topics, concepts, systems, processes,       │
│  projects, policies, source entry points     │
└──────────────────────┬───────────────────────┘
                       │
             visible through user's ACL
                       │
                       ▼
┌──────────────────────────────────────────────┐
│               User Wiki                      │
│                                              │
│  Personal knowledge structure               │
│  Grows from questions, work, and interests  │
│  Links back to authoritative sources         │
└──────────────────────────────────────────────┘
```

The Company Library Index and User Wiki are **navigation and reasoning structures**, not replacements for source documents.

### 2.1 Product lifecycle

The product lifecycle SHALL follow the same architecture:

```text
Company Cloud Document Library
            │
            ▼
Company Library Index
(shared, curated, permission-aware map)
            │
         BOOTSTRAP
            ▼
       Personal Wiki
(minimal user-specific knowledge map)
            │
     actual questions/work
            ▼
     Progressive Expansion
   ┌────────┼─────────┐
   ▼        ▼         ▼
Explore    Query     Curate
   │        │         │
   └────────┴────┬────┘
                 ▼
             Maintain
                 │
                 ▼
             Validate
                 │
                 └──────► Personal Wiki
```

The intended evolution is therefore:

> **Company Library Index → Personal Wiki → Progressive Expansion**

The Company Library Index gives the user a starting map. The Personal Wiki captures the subset of company knowledge that becomes useful to that user. Progressive Expansion grows that wiki from real questions, investigations, projects, and explicitly selected sources.

The system SHOULD NOT require each user to independently rediscover or re-index the company corpus before their wiki becomes useful.

### 2.2 Knowledge ownership layers

The product SHOULD support three logical ownership scopes:

```text
Company Library Index
        │
        ├───────────────┐
        ▼               ▼
   Team Wiki(s)      Team Wiki(s)
        │
      ┌─┴─┐
      ▼   ▼
 Personal Wikis
```

These layers are overlays over the same source document library, not duplicated document repositories.

#### Company-owned knowledge

Examples:

- canonical terminology;
- company-wide concepts;
- products;
- systems;
- official processes;
- policies;
- metrics;
- authoritative source mappings.

This layer is governed by the **Company Wiki Admin**.

#### Team-owned knowledge

Examples:

- department-specific operating knowledge;
- project knowledge;
- team conventions;
- team-specific source collections;
- shared investigations;
- team decisions.

A Team Wiki is OPTIONAL for V1 but the architecture SHOULD support it.

A Team Wiki MAY be governed by:

- a team lead;
- a designated curator;
- multiple approved maintainers.

#### User-owned knowledge

Examples:

- personal research;
- current investigations;
- frequently used concepts;
- project notes;
- personally useful source mappings;
- temporary working hypotheses.

This layer is controlled by the end user.

---


## 3. Roles and Responsibilities

The product SHALL distinguish between shared knowledge governance and personal knowledge use.

The guiding principle is:

> **Agent does the work. User decides what matters personally. Admin decides what is canonical for the company.**

### 3.1 Company Wiki Admin

The Company Wiki Admin owns the **shared knowledge structure**, not the source document repository.

The admin's responsibilities SHOULD include:

- define and evolve the top-level Company Library Index;
- maintain canonical concepts, terminology, aliases, and relationships;
- identify authoritative source collections;
- connect shared wiki nodes to authoritative documents or folders;
- review proposed additions that affect company-wide knowledge;
- resolve duplicate or conflicting shared concepts;
- identify superseded policies, processes, and source mappings;
- review uncovered company-wide knowledge areas;
- monitor broken links, stale mappings, drift, contradictions, and provenance gaps;
- validate that shared navigation does not leak restricted information;
- restructure the shared map when the company organization or knowledge model changes.

The admin SHOULD NOT normally be required to:

- manually ingest every new document;
- classify every file;
- chunk every source;
- embed every source;
- manually attach every file to the wiki;
- recreate cloud-drive lifecycle or access-control functions.

The admin SHOULD curate **meaning and navigation**, not document infrastructure.

### 3.2 End User

The end user's primary activity is doing work through the wiki rather than administering it.

Typical end-user tasks SHOULD include:

- ask questions;
- explore a topic;
- navigate known concepts;
- expand a personal wiki branch;
- save a useful relationship or source;
- add/reconcile a selected document or folder;
- organize personal project knowledge;
- merge or rename personal nodes;
- remove obsolete personal knowledge;
- review warnings affecting the Personal Wiki.

The end user SHOULD NOT be expected to:

- understand ingestion infrastructure;
- manage embeddings or indexes;
- manually classify the company corpus;
- maintain company-wide taxonomy;
- reconcile company-wide duplicates;
- manually track source versions.

### 3.3 Team Wiki Curator

Where Team Wikis are enabled, a Team Wiki Curator SHOULD govern knowledge whose scope is broader than one user but narrower than the whole company.

Typical responsibilities MAY include:

- maintain team-specific structure;
- approve promotion from Personal Wiki to Team Wiki;
- identify team-standard terminology;
- maintain project or department source mappings;
- resolve duplicate team knowledge;
- archive completed team/project branches;
- propose company-wide promotion when team knowledge becomes broadly relevant.

### 3.4 Agent responsibilities

The agent SHOULD perform most repetitive knowledge-management work.

The agent MAY:

- discover sources;
- follow wiki and source links;
- propose nodes;
- identify aliases;
- detect duplicates;
- detect stale or superseded sources;
- generate concise source-grounded summaries;
- preserve provenance;
- identify contradictions;
- suggest promotion;
- suggest restructuring;
- validate source accessibility;
- identify missing coverage;
- propose cleanup;
- perform safe non-destructive maintenance.

Humans SHOULD primarily provide judgment, approval, and intent.

### 3.5 Responsibility boundary

The system SHALL preserve the following boundary:

```text
Source documents
    → owned by existing cloud-drive/document owners

Company Library Index
    → governed by Company Wiki Admin

Team Wiki
    → governed by Team Wiki Curator(s)

Personal Wiki
    → governed by individual user

Agent
    → performs discovery, reasoning, curation assistance, and validation
```

---

## 4. Core Architectural Invariants

The implementation MUST preserve the following invariants.

### 3.1 Source documents remain authoritative

The system MUST NOT require migration of company documents into a new proprietary repository.

The existing company cloud drive SHALL remain authoritative for:

- document content;
- ownership;
- access control;
- sharing;
- version history;
- deletion and retention;
- editing;
- auditability.

Wiki content SHALL link to or derive from these sources rather than silently replacing them.

### 3.2 Wiki is navigation before storage

The wiki SHOULD primarily contain:

- concepts;
- summaries;
- relationships;
- aliases;
- navigation routes;
- source mappings;
- decisions;
- process knowledge;
- user-curated understanding.

It SHOULD NOT become a second copy of the company document library.

### 3.3 Evidence remains source-grounded

When answering factual questions, the agent SHOULD retrieve and cite underlying source documents whenever practical.

A wiki page MAY help locate evidence, but a generated wiki summary MUST NOT automatically become the authoritative evidence for a factual claim.

### 3.4 Access control is inherited, not reinvented

The product MUST rely on the source system's access control whenever possible.

The system MUST NOT expose document content, wiki summaries, titles, links, metadata, or derived knowledge that reveals information unavailable to the current user.

---

## 5. Company Library Index

### 4.1 Purpose

The Company Library Index SHALL provide a small, shared, curated map of the organization's knowledge.

It SHALL answer:

- What major areas of knowledge exist?
- Where should an agent begin exploring?
- What are the canonical business concepts?
- Which documents or folders are authoritative entry points?
- How are concepts, teams, systems, processes, policies, and projects related?

The index SHALL be a **map**, not a flat catalog of every file.

### 4.2 Recommended top-level structure

A default company index MAY resemble:

```text
Company Library

Company
├── Organization
├── Strategy
├── Policies
└── Terminology

Business
├── Sales
├── Marketing
├── Finance
├── Operations
└── HR

Products
├── Product A
├── Product B
└── Product C

Systems
├── CRM
├── ERP
└── PMS

Processes
├── Customer Onboarding
├── Sales Process
├── Billing
└── Employee Onboarding

Projects
├── Active Projects
└── Historical Projects

Data
├── Metrics
├── Datasets
└── Reports
```

This structure SHALL be configurable per company.

### 4.3 Progressive disclosure

Each index node SHOULD reveal only the next useful level of navigation.

Example:

```text
Sales
├── Overview
├── Concepts
│   ├── Lead
│   ├── Opportunity
│   └── Conversion
├── Processes
│   ├── Lead Qualification
│   └── Contract Approval
├── Systems
│   └── CRM
└── Sources
    ├── Sales Handbook
    ├── Pricing Policy
    └── CRM Documentation
```

The system SHOULD avoid placing thousands of source files directly into a top-level wiki index.

### 4.4 Index node types

The initial implementation SHOULD support at least:

- topic;
- concept;
- entity;
- department/team;
- product;
- system;
- process;
- policy;
- project;
- decision;
- metric;
- dataset;
- source collection.

### 4.5 Index visibility

The Company Library Index MAY be logically shared, but its rendered view MUST be permission-aware.

Example:

```text
Finance
├── Annual Reports
├── Budget Process
└── Expense Policy
```

may be visible to one user, while another authorized user may additionally see:

```text
Finance
├── Acquisition Planning
├── Treasury
└── Board Forecast
```

Restricted nodes MUST NOT leak through:

- page titles;
- autocomplete;
- search results;
- backlinks;
- related-page lists;
- summaries;
- embeddings;
- inferred relations;
- activity logs exposed to users.

---

## 6. User Wiki

### 7.1 Purpose

Each user SHALL be able to maintain a personalized wiki representing the knowledge most useful to their role, work, questions, and interests.

Two users MAY build very different wiki structures over the same company document library.

This is intentional.

### 7.2 Storage

The user's wiki SHOULD be stored in a location controlled by the user or company, preferably within the company's existing cloud drive infrastructure.

The implementation SHOULD support:

- a user-specific cloud-drive folder;
- a team/shared wiki folder;
- a locally synced folder;
- future connector-based wiki storage.

A database MUST NOT be required for V1 unless a specific implementation constraint makes it necessary.

### 7.3 Bootstrap

A new user wiki SHALL start with access to the Company Library Index.

Example:

```text
My Company Wiki

Company Library
├── Company
├── Products
├── Sales
├── Finance
├── Operations
└── ...

My Knowledge
└── empty
```

The Company Library Index MAY be referenced dynamically rather than copied physically into every user's folder.

### 7.4 Personal structure

The user SHOULD be free to create structures such as:

```text
My Knowledge
├── Enterprise Sales
│   ├── Pipeline
│   ├── Conversion
│   ├── Pricing
│   └── Q2 Performance
├── PMS3
├── Competitors
├── Customer Patterns
└── Q3 Planning
```

The personal wiki SHOULD NOT be forced to mirror the company's folder hierarchy.

### 7.5 Shared versus personal knowledge

The system SHOULD distinguish:

#### Shared semantic knowledge

Examples:

- company terminology;
- products;
- systems;
- processes;
- metrics;
- policies;
- departments;
- canonical entities.

#### Personal knowledge

Examples:

- investigations;
- working hypotheses;
- research trails;
- frequently used sources;
- personal project maps;
- user annotations;
- current priorities.

Personal knowledge MAY reference shared knowledge without modifying the shared definition.

### 7.6 Optional Team Wiki

The system SHOULD support a Team Wiki as an intermediate sharing scope between Company Library Index and Personal Wiki.

A Team Wiki SHOULD be useful when knowledge is:

- shared by a department or project team;
- too narrow to be company-wide;
- too important to remain private;
- still evolving and not yet canonical;
- operationally useful to a group of users.

A Team Wiki SHOULD be able to reference both Company Library Index nodes and source documents.

A user MAY reference Team Wiki knowledge from their Personal Wiki without copying the underlying content.

---


## 7. Knowledge Lifecycle and Progressive Expansion

The lifecycle SHALL operationalize the architecture:

```text
Company Library Index
        ↓
     Bootstrap
        ↓
   Personal Wiki
        ↓
 Explore ↔ Query
        ↓
      Curate
        ↓
     Maintain
        ↓
     Validate
        ↺
```

**Progressive Expansion** is not a separate ingestion pipeline. It is the cumulative effect of `Explore`, `Query`, and `Curate` operating over time.

### 7.1 Bootstrap

A new user wiki SHALL bootstrap from the shared Company Library Index.

Bootstrap SHOULD create only a minimal personal structure and references to the company map.

Example:

```text
My Company Wiki

Company Library
└── shared permission-aware index

My Knowledge
└── empty or minimal
```

Personal-wiki bootstrap SHALL NOT require:

- representative sampling of the company corpus;
- chunking the entire document library;
- embedding all documents;
- copying the Company Library Index into the user's folder;
- generating large numbers of wiki pages in advance.

Representative sampling MAY be used separately when initially constructing or improving the **shared Company Library Index**.

The principle is:

> **Bootstrap the user from the company map; do not rediscover the company for every user.**

### 7.2 Explore

`Explore` discovers knowledge that the current wiki does not yet adequately represent.

The agent SHOULD explore in progressively broader scopes:

```text
Personal Wiki
    ↓
related personal/shared wiki nodes
    ↓
Company Library Index
    ↓
likely source areas
    ↓
native source search
    ↓
source documents and sections
```

Explore MAY be initiated by:

- a user question;
- "expand this topic";
- navigation from an existing wiki page;
- a missing concept or relationship;
- an explicitly selected source;
- a project or task that requires unfamiliar knowledge.

Exploration results SHALL remain transient unless they are promoted through `Curate`.

### 7.3 Query

`Query` SHALL be the dominant runtime operation.

A query SHOULD use the current Personal Wiki as a high-value starting context, then use the Company Library Index and original documents when more evidence is needed.

Typical flow:

```text
Question
    ↓
Personal Wiki
    ↓
known route available?
  ┌──────────────┴──────────────┐
  │                             │
 yes                            no
  │                             │
follow wiki route            Explore
  │                             │
  └──────────────┬──────────────┘
                 ↓
          retrieve evidence
                 ↓
              reason
                 ↓
       answer + source citations
                 ↓
       reusable discovery?
          ┌──────┴──────┐
          │             │
         no            yes
          │             │
        stop          Curate
```

A successful query MAY therefore improve the wiki as a side effect of solving a real problem.

Query SHALL NOT require that all relevant documents were previously represented in the wiki.

### 7.4 Curate

`Curate` SHALL convert useful discoveries into durable wiki knowledge.

Curate MAY:

- create a new wiki node;
- add a source mapping;
- add an alias;
- add or type a relationship;
- add a concise source-grounded summary;
- connect a personal topic to a shared company concept;
- promote a repeatedly used source;
- reconcile newly discovered information with an existing node.

The system MUST NOT permanently add every discovered fact.

Candidate knowledge SHOULD be promoted when one or more of the following apply:

- the user explicitly asks to add or remember it;
- it is reused repeatedly;
- it becomes important to an active project;
- it is referenced by multiple wiki pages;
- it represents a durable concept, decision, process, or relationship;
- it materially improves future navigation;
- the agent identifies it as structurally useful and promotion policy allows it.

The system SHOULD prefer **small durable navigation knowledge** over large copied summaries.

### 7.5 Maintain

`Maintain` SHALL correct or restructure existing wiki knowledge.

Maintenance MAY include:

- merging duplicate concepts;
- renaming nodes;
- changing hierarchy;
- reorganizing a branch;
- replacing obsolete source references;
- refreshing summaries;
- moving completed projects to historical areas;
- retiring low-value or obsolete nodes;
- correcting relationships;
- resolving aliases.

Maintenance SHOULD preserve user-authored organization unless the user requests or approves restructuring.

### 7.6 Validate

`Validate` SHALL detect problems in the wiki without requiring a full re-ingestion of the source corpus.

Validation SHOULD detect where practical:

- broken source links;
- inaccessible sources;
- source version drift;
- stale derived summaries;
- missing provenance;
- orphan wiki nodes;
- duplicate concepts;
- contradictory sources;
- superseded knowledge;
- missing or suspicious relationships;
- permission leakage;
- gaps in important areas;
- nodes whose underlying evidence is no longer available to the user.

Validation MAY result in:

- a warning;
- a proposed maintenance action;
- a freshness-state change;
- a request for user review;
- automatic repair when safe and unambiguous.

### 7.7 Optional `Add Source` operation

Explicit source reconciliation remains useful, but it SHALL NOT be the default lifecycle for all company documents.

The system MAY expose an operation conceptually equivalent to:

```text
Add Source <document-or-folder>
```

Its meaning is:

```text
selected source
      ↓
read source
      ↓
compare with Personal Wiki + Company Library Index
      ↓
identify relevant new/changed knowledge
      ↓
propose or perform Curate actions
```

`Add Source` replaces the traditional idea of a mandatory top-level `Ingest` stage.

The product SHOULD avoid the term `Ingest` where it would imply that a document must first be copied, chunked, embedded, or indexed by Company Wiki before it can be queried.

### 7.8 Knowledge promotion across scopes

The product SHOULD support bottom-up promotion of useful knowledge:

```text
Personal discovery
      ↓
Personal Wiki
      ↓
useful to team?
      ↓
Team Wiki proposal
      ↓
useful company-wide?
      ↓
Company Library Index proposal
```

Promotion SHALL NOT mean blindly copying content upward.

Promotion SHOULD reconcile the candidate with existing shared knowledge and retain provenance.

#### Personal → Team

A Personal Wiki node MAY be proposed for Team Wiki when it:

- is repeatedly useful to multiple team members;
- documents a team process, decision, project, or shared investigation;
- resolves a recurring team question;
- provides a useful source map for a team domain.

Approval SHOULD be performed by a Team Wiki Curator where team governance is enabled.

#### Team → Company

A Team Wiki node MAY be proposed for the Company Library Index when it:

- represents company-wide terminology;
- defines a canonical process or metric;
- becomes relevant across multiple teams;
- identifies an authoritative source;
- captures durable organizational knowledge.

Approval SHOULD be performed by the Company Wiki Admin.

#### Direct Personal → Company

Direct promotion MAY be allowed for small organizations or simple deployments, but the Company Wiki Admin SHOULD remain the approval authority for company-wide canonical knowledge.

#### Downward reuse

Shared knowledge SHOULD normally be **referenced**, not copied, into lower scopes.

```text
Company node
    ↓ reference
Team Wiki
    ↓ reference
Personal Wiki
```

This minimizes duplication and drift.

### 7.9 User control

The user SHALL be able to:

- add a node;
- remove a node;
- rename a node;
- merge duplicates;
- pin important nodes;
- mark a node as temporary;
- mark a node as canonical for their wiki;
- ask the agent to reorganize a branch;
- ask the agent to expand a topic;
- explicitly add/reconcile a source;
- ask the agent to stop learning from a topic.

### 7.10 Automatic lifecycle assistance

The agent MAY suggest:

- promotion of repeatedly useful discoveries;
- duplicate-page merges;
- stale-node review;
- missing links;
- orphan nodes;
- obsolete project pages;
- source refresh;
- structural improvements.

Automatic destructive changes SHOULD require strong confidence or user approval.

---


## 8. Wiki Structure and Linking

### 7.1 Wiki as a lightweight graph

Wiki pages SHALL support links to other wiki pages and source documents.

This allows the wiki to behave as a lightweight knowledge graph without requiring a graph database.

### 7.2 Link types

Links SHOULD use the chosen provider's native hyperlinks; local Markdown documents MAY use Markdown links.

Where useful, the system SHOULD support typed relationships such as:

- `broader`;
- `narrower`;
- `related`;
- `depends_on`;
- `owned_by`;
- `governed_by`;
- `applies_to`;
- `derived_from`;
- `supersedes`;
- `uses`;
- `produces`;
- `source`;
- `evidence`.

Typed links SHOULD remain optional in V1.

### 7.3 Backlinks

Backlinks SHOULD be generated or discoverable automatically.

The system SHOULD use backlinks during navigation and reasoning where useful.

### 7.4 Aliases

A canonical wiki node SHOULD support aliases.

Example:

```yaml
name: Net Revenue Retention
aliases:
  - NRR
  - Net Dollar Retention
  - Dollar Retention
```

Aliases SHOULD resolve to the same canonical node rather than creating duplicate pages.

---

## 9. Wiki Page Schema

A lightweight schema SHOULD be used.

Example:

```yaml
---
id: concept:nrr
type: metric
title: Net Revenue Retention

aliases:
  - NRR
  - Net Dollar Retention

scope: company

status: active

owner: Finance Analytics

sources:
  - uri: cloud://finance/metric-standard
    relation: primary-source
    version: v7
    section: "4.2 Net Revenue Retention"

related:
  - concept:customer-churn
  - concept:gross-revenue-retention

freshness:
  checked_at: 2026-09-11

derived_access:
  mode: source-constrained
---
```

The exact serialization MAY evolve.

V1 SHOULD use ordinary native documents with readable sections and links. Local Markdown is supported;
front matter and a database schema are not required.

---

## 10. Provenance

### 9.1 Source mapping

Every substantive generated or curated wiki statement SHOULD be traceable to one or more sources where possible.

The system SHOULD retain:

- source URI or stable ID;
- source version if available;
- relevant section/page/block;
- access/check timestamp;
- relationship to source;
- optional confidence or verification state.

### 9.2 Source-first citations

User-facing answers SHOULD cite authoritative source documents rather than wiki summaries when available.

### 9.3 Generated knowledge

Agent-generated content SHOULD be distinguishable from:

- source text;
- human-authored wiki content;
- verified company definitions.

The system MAY use markers such as:

```yaml
origin: agent-generated
verification: unverified
```

### 9.4 Contradictions

If sources conflict, the wiki SHOULD NOT silently collapse them into one fact.

The system SHOULD preserve:

- both sources;
- their dates;
- authority level where known;
- supersession relationships where known;
- an explicit conflict state if unresolved.

---

## 11. Access Control for Derived Knowledge

### 10.1 Source-constrained derived access

Derived wiki knowledge MUST NOT automatically receive broader access than its underlying sources.

For a generated page based on restricted documents:

```text
Restricted sources
       ↓
Derived wiki node
       ↓
Provider-managed wiki access; source access rechecked for factual reuse
```

### 10.2 Shared wiki content

Before durable publication, the system MUST verify authenticated exact-destination authority and that the
destination audience is contained by every contributing evidence audience. Contributions include titles, aliases,
links, relationships, provenance, and transitive inputs, not merely final citations. Unknown proof MUST block the
affected publication. Personal copies of provider-governed evidence are subject to the same rule.

Shared generation MUST use only destination-authorized evidence. If earlier context contains excluded evidence,
regenerate from independently authorized inputs in a clean supported context; otherwise refuse shared generation.
Removing a citation or codename is not proof of sanitization. Proposals and diagnostics must also remain audience-safe.

### 10.3 Native ACL preference

Provider-derived personal and shared wiki files default to provider-managed destination permissions. The provider
MUST enforce the approved wiki audience from creation, including exposed metadata. Current publication authority
and audience containment remain required; unavailable future source-to-wiki inheritance proof alone MUST NOT block
ordinary publication or require a transient draft.

Continuous source inheritance MUST be verified only when explicitly required by the user or applicable governing
policy. Preserve any existing explicit requirement. For that model, verify protection after source ACL, group,
inheritance, and destination changes across content, title/search previews, history, and exports. Current snapshots
and periodic checks do not prove this guarantee. If required protection is unavailable, retain only an authorized
transient result; do not switch models or use a local export to bypass it. V1 supplies no ACL synchronization or recall.

Ordinary wiki reads use provider-enforced current access; factual reuse requires current source evidence. For known
unsafe legacy content or explicit continuous inheritance, establish required disclosure safety before loading bytes,
or bypass the page for separately registered bounded source search. Lack of automatic inheritance alone does not
establish leakage. Validate is read-only; approved cleanup MUST report unresolved native history/search exposure.

### 10.4 Durable changes and recovery

Use the [shared change protocol](../skills/company-wiki/references/change-protocol.md). Explicit update requests
authorize necessary bounded changes in an existing selected wiki, including after exact source selection. Source
selection alone and read-only work authorize no writes. Honor review-first instructions with exact-proposal
approval; setup and registration retain their existing approval gates. Bind each concrete plan to the user's
task or exact-proposal authorization, identity, evidence/target versions, audiences/protection, scope, and operation
parameters. Use native conditional or
exclusive updates and idempotent/conditional creates; reread-then-write alone does not protect concurrent edits.
Verify dependencies before exposing links. Failed or unknown outcomes stop later writes; a timeout may follow a
committed write. Reconcile exact targets/original operation keys before retry, preserve concurrent edits, and propose
only remaining work. Material drift invalidates the plan; routine task-authorized updates may reconcile and
revalidate within the same scope while preserving concurrent edits. Changed exact proposals need fresh approval;
missing decisions or authority block the affected action. No automatic destructive rollback is allowed.

Setup preflights registration and creates verified provider pages before the completed profile and index link.
Atomic, conflict-protected index replacement preserves unrelated entries. Registration remains non-atomic across
resources: failures may leave successful pages or an unlinked completed profile. Preserve pre-existing registry bytes,
do not recreate successful pages, and keep recovery records out of the locator-only registry. Unresolvable outcomes
remain unknown; V1 promises no automatic crash recovery without native lookup/session state.
Reuse an existing profile only if it already exactly matches; changed registrations create a fresh contained profile
and switch the index link last, leaving the old profile intact. Approval binds the exact selected entry delta;
unrelated index entries may be merged after revalidation with a refreshed version guard. Changes to the selected
registration or authority invalidate approval; this exception never permits rebasing source/page edits.

---

## 12. Retrieval and Reasoning

### 11.1 Wiki-first navigation, source-first evidence

The default reasoning pattern SHOULD be:

```text
Question
    ↓
User Wiki
    ↓
Relevant known topic/concept
    ↓
Company Library Index
    ↓
Relevant document area
    ↓
Native cloud search / CLI / MCP / skill
    ↓
Relevant source documents
    ↓
Relevant sections
    ↓
Answer + citations
```

This SHALL be treated as progressive disclosure.

### 11.2 Direct-source fallback

The agent MUST be able to bypass the wiki when:

- the wiki has no relevant route;
- the question asks for an exact filename/identifier;
- recent documents may not yet be represented;
- direct source search is more efficient;
- the user explicitly requests direct search.

### 11.3 Hybrid navigation

The system SHOULD support both:

- wiki-guided navigation;
- direct cloud-drive search.

They are complementary, not mutually exclusive.

### 11.4 Optional advanced retrieval

The architecture SHOULD permit future addition of:

- lexical search;
- embeddings;
- vector indexes;
- hybrid search;
- reranking;
- hierarchical retrieval;
- graph retrieval;
- RAPTOR-like summaries;
- query routing.

None of these SHALL be mandatory dependencies for V1.

They SHOULD be introduced only when native source search plus wiki navigation is insufficient.

---

## 13. Source Adapters

The system SHALL treat document access as an abstraction.

A source adapter MAY use:

- local synced folders;
- cloud-drive APIs;
- MCP servers;
- CLI tools;
- existing document skills/connectors;
- enterprise search APIs.

Example:

```text
SourceAdapter
├── search(query, scope)
├── list(path)
├── read(uri)
├── metadata(uri)
├── permissions(uri)
└── versions(uri)
```

The wiki logic SHOULD remain independent of the underlying cloud-drive provider.

---

## 14. Local Sync Support

Because many enterprise cloud drives support local synchronization, a locally synced folder MAY be treated as a first-class source adapter.

Example:

```text
Company Drive
     ⇅ sync
Local Folder
     ↓
company-wiki
```

Local operation MAY improve:

- compatibility with coding/agent hosts;
- Markdown manipulation;
- low-latency file access;
- offline experimentation.

However, local indexing MUST NOT be treated as an authorization bypass. Only private user-owned local originals
and synthetic fixtures may rely on effective local identity/access and verified private destination scope. Synced
or exported provider-governed evidence still requires provider proof under §10; role labels and filesystem write
access cannot authorize Team/Company publication. See the [publication contract](../skills/company-wiki/references/publication.md).

---

## 15. Query Runtime

`Query` is the primary execution path and the main driver of Progressive Expansion.

The recommended logical runtime is:

```text
1. Understand the user's question.
2. Inspect the most relevant Personal Wiki nodes.
3. Follow useful wiki links and aliases.
4. Consult the Company Library Index when the personal map is insufficient.
5. Identify likely source locations.
6. Search sources using the current user's identity/access.
7. Read the smallest useful source sections.
8. Expand to related sources only when needed.
9. Reason over retrieved evidence.
10. Answer with original-source citations.
11. Identify reusable discoveries.
12. If warranted, Curate them into the Personal Wiki or propose the change.
13. Mark stale/conflicting knowledge for Maintain or Validate when detected.
```

The runtime therefore combines two loops:

```text
Answer loop:
Query → Navigate → Retrieve → Reason → Answer

Learning loop:
Discover → Reuse/Importance Check → Curate → Maintain/Validate
```

The implementation SHOULD avoid loading the entire Personal Wiki, Company Library Index, or large numbers of source documents into model context.

A query MUST be able to fall back directly to source search when the wiki has no useful route.

---


## 16. Performance and Scalability Requirements

### 15.1 Avoid global upfront processing

V1 SHOULD NOT require:

- chunking the entire enterprise corpus;
- embedding every company document;
- generating wiki pages for every source;
- extracting a complete enterprise knowledge graph.

### 15.2 Progressive cost

Processing cost SHOULD grow with actual use.

The system SHOULD prefer:

```text
small shared index
      +
small personal wiki
      +
on-demand source retrieval
```

over:

```text
process everything first
      +
maintain everything forever
```

### 15.3 Bounded navigation

Agent navigation SHOULD have configurable limits such as:

- maximum wiki traversal depth;
- maximum source search rounds;
- maximum source documents opened;
- maximum context/token budget.

The agent MAY exceed defaults when required by a complex research question.

### 15.4 Caching

The implementation MAY cache:

- source metadata;
- page summaries;
- resolved aliases;
- recently used navigation routes;
- non-sensitive source search results.

Caches MUST preserve permission boundaries and freshness requirements.

---

## 17. Freshness and Update Semantics

### 16.1 Wiki staleness

Wiki nodes SHOULD include enough source provenance to determine whether the underlying source has changed.

### 16.2 Source change

When an underlying source changes, the system SHOULD be able to mark dependent wiki content as:

- current;
- potentially stale;
- superseded;
- needs review.

### 16.3 Lazy refresh

The system SHOULD support lazy refresh:

```text
source changed
    ↓
wiki node marked potentially stale
    ↓
next relevant use
    ↓
agent re-reads source
    ↓
wiki updated if needed
```

This is preferred over eagerly regenerating the entire wiki after every document change.

---

## 18. Company Index Curation

### 17.1 Initial construction

The first **shared Company Library Index** MAY be generated from:

- existing folder structures;
- important document collections;
- representative sampling of documents;
- known departments;
- known systems;
- business processes;
- policies;
- product catalogs;
- existing glossaries;
- user-provided organizational knowledge.

Representative sampling belongs to **company-index bootstrap**, not to every user's Personal Wiki bootstrap.

Once the shared Company Library Index exists, a new Personal Wiki SHOULD inherit/reference that map and progressively expand from actual use.

### 17.2 LLM-assisted curation

The LLM MAY propose:

- index categories;
- canonical concepts;
- aliases;
- related topics;
- source mappings;
- missing areas.

Human review SHOULD focus on high-value company-wide semantics rather than file-by-file classification.

### 17.3 Index size

The initial Company Library Index SHOULD remain intentionally small.

A useful target is tens or hundreds of meaningful navigation nodes, not tens of thousands of documents.

---

## 19. Search and Discovery

The user SHOULD be able to ask:

- "What does the company know about X?"
- "Where would I find information about X?"
- "Expand my wiki around X."
- "Show related concepts."
- "What sources support this?"
- "What changed since I last looked at this?"
- "What important areas am I missing?"
- "Build a wiki branch for this project."
- "Merge these two overlapping topics."

The agent SHOULD combine wiki navigation with source search rather than treating search and wiki browsing as separate products.

---

## 20. Agent Behaviors

The agent SHOULD:

- prefer existing canonical nodes over creating duplicates;
- use aliases for terminology resolution;
- follow relevant links before broad search when this is efficient;
- fall back to source search when wiki navigation is insufficient;
- cite source evidence;
- preserve uncertainty;
- expose source conflicts;
- avoid overgrowing the wiki;
- periodically recommend cleanup;
- preserve user-created organization unless asked to reorganize it.

The agent MUST NOT:

- treat generated wiki summaries as unquestionable truth;
- bypass source access controls;
- invent provenance;
- create permanent nodes for every retrieved fact;
- silently overwrite user-authored knowledge;
- expose restricted page titles or relationships.

---

## 21. Optional Local Representation

For explicitly selected local Markdown storage, a user wiki MAY organize readable pages as follows. This is an
illustrative navigation layout, not a required filesystem structure or a cloud-document naming convention:

```text
company-wiki/
├── index.md
├── company-library.md
├── topics/
├── concepts/
├── projects/
├── processes/
└── decisions/
```

`company-library.md` MAY be a logical/dynamic reference rather than a physically duplicated copy of the shared company index.

Local configuration uses the separate `~/company-wiki/index.md` registry and contained profiles defined by the
installed skill. The wiki does not require a `.wiki/` state directory.

Cloud wiki pages SHALL use ordinary native documents and links; local wiki pages MAY use Markdown.

---

## 22. Functional Requirements

### FR-1 — Role separation

The system SHALL distinguish Company Wiki Admin, End User, Agent, and optional Team Wiki Curator responsibilities.

### FR-2 — Company governance

Company-wide canonical knowledge SHALL be governed by the Company Wiki Admin.

### FR-3 — Personal ownership

Users SHALL control the structure and durable contents of their own Personal Wiki.

### FR-4 — Optional Team Wiki

The architecture SHOULD support Team Wikis as an intermediate shared scope.

### FR-5 — Promotion workflow

The system SHOULD support promotion of knowledge from Personal → Team → Company scopes with appropriate approval.

### FR-6 — Shared knowledge reuse

Lower-scope wikis SHOULD reference shared knowledge rather than copy it wherever practical.

### FR-7 — Cloud-drive-backed sources

The system SHALL access company documents through existing cloud-drive/local-sync/connector interfaces.

### FR-8 — Company Library Index

The system SHALL support a shared company-level navigation index.

### FR-9 — Permission-aware index

The index SHALL hide nodes and metadata the current user is not authorized to discover.

### FR-10 — User wiki

Each user SHALL be able to maintain a personalized wiki.

### FR-11 — Wiki bootstrap

A new Personal Wiki SHALL bootstrap from the shared Company Library Index without requiring corpus-wide sampling or indexing.

### FR-12 — Progressive expansion

The agent SHALL progressively expand the Personal Wiki from real questions, exploration, projects, and explicitly selected sources.

### FR-13 — Lifecycle operations

The system SHALL support the logical lifecycle operations `Bootstrap`, `Explore`, `Query`, `Curate`, `Maintain`, and `Validate`.

### FR-14 — Controlled promotion

The system SHALL distinguish transient discoveries from durable wiki knowledge and promote only knowledge that meets curation policy.

### FR-15 — Optional source reconciliation

The system SHOULD allow a user to explicitly add/reconcile a selected document or folder without making ingestion a prerequisite for querying other sources.

### FR-16 — Source links

Wiki pages SHALL support links to authoritative source documents.

### FR-17 — Provenance

Generated or synthesized wiki content SHOULD retain source provenance.

### FR-18 — Source-grounded answers

The agent SHOULD use source documents as evidence when answering factual questions.

### FR-19 — Native access controls

The implementation SHOULD preserve the source system's ACLs rather than recreate them.

### FR-20 — Derived-content protection

Derived knowledge SHALL NOT expose information beyond underlying source permissions.

### FR-21 — Direct-source fallback

The agent SHALL support direct source search independent of the wiki.

### FR-22 — Provider independence

Wiki logic SHALL not depend on a specific cloud-drive provider.

### FR-23 — Document-native storage

Wiki artifacts SHALL remain human-readable documents with links in the selected destination. Cloud destinations
SHOULD use the provider's native document format; explicitly selected local storage MAY use Markdown.

### FR-24 — No mandatory vector DB

V1 SHALL NOT require a vector database.

### FR-25 — No mandatory graph DB

V1 SHALL NOT require a graph database.

### FR-26 — Future retrieval extensions

The architecture SHALL allow advanced search/indexing components to be added later without changing the user-facing wiki model.

---

## 23. Non-Functional Requirements

### NFR-1 — Security

Unauthorized source content or derived knowledge MUST NOT enter user-visible output.

### NFR-2 — Explainability

The system SHOULD make it clear how a conclusion relates to source evidence.

### NFR-3 — Portability

A wiki SHOULD remain readable and navigable through the chosen provider's ordinary document tools without the
agent skill. Local Markdown pages SHOULD remain usable in ordinary text tools.

### NFR-4 — Low infrastructure

The minimum viable implementation SHOULD require little or no new server infrastructure.

### NFR-5 — Incremental scalability

Cost SHOULD scale primarily with active users, active topics, and actual queries rather than total enterprise corpus size.

### NFR-6 — Graceful degradation

If the wiki is incomplete or unavailable, source search SHOULD continue to work.

### NFR-7 — Human readability

Users SHALL be able to inspect and edit the wiki without specialized tools.

---

## 24. Non-Goals for V1

V1 is NOT intended to:

- create a complete enterprise knowledge graph;
- fully replace enterprise search;
- ingest and duplicate every company document;
- maintain a centralized vector copy of all source documents;
- define a formal enterprise ontology;
- automatically summarize every source file;
- solve every possible cross-document reasoning problem;
- create a new document access-control system;
- require a dedicated wiki web application;
- require admins to manually ingest/classify every document;
- require end users to manually maintain the shared company taxonomy.

---

## 25. MVP

The MVP SHALL demonstrate:

1. one existing company cloud-drive source;
2. one Company Library Index governed by an Admin role;
3. permission-aware source access;
4. one user-specific Personal Wiki stored as native cloud documents with links;
5. Personal Wiki bootstrap from the Company Library Index;
6. `Explore` through wiki-guided and source-backed navigation;
7. `Query` with direct source search fallback;
8. source-grounded answers with citations;
9. `Curate` of selected/reusable discoveries into the Personal Wiki;
10. `Maintain` and `Validate` on at least basic stale/broken/conflicting cases;
11. explicit `Add Source` reconciliation for a selected document or folder;
12. provenance on generated nodes;
13. prevention of obvious derived-access leakage;
14. at least one Personal → Company promotion proposal/review flow;
15. optional Team Wiki support may be deferred, but the data model MUST NOT block it.

A database, vector index, GraphRAG pipeline, and custom frontend are explicitly optional for the MVP.

---

## 26. MVP Evaluation

The pilot SHOULD compare:

```text
A. Native/direct document search
B. Direct LLM + document search
C. Company Library Index + document search
D. Personal Wiki + Company Library Index + document search
```

Evaluate:

- answer correctness;
- source discovery success;
- number of search/read operations;
- token usage;
- latency;
- user navigation success;
- citation quality;
- repeated-question efficiency;
- ACL leakage;
- usefulness of accumulated personal wiki knowledge;
- quality of Curate decisions (useful promotions vs noise);
- maintenance/validation effort over time;
- improvement in repeated-query performance as the Personal Wiki grows.

The key questions are:

> Does progressive wiki navigation materially improve knowledge discovery and reasoning compared with repeatedly searching the raw document library?
>
> Does the lifecycle **Company Library Index → Personal Wiki → Progressive Expansion** improve repeated work without creating excessive curation or maintenance overhead?

---

## 27. Product Principle

The product SHOULD preserve the following mental model:

> **The company provides the map.<br>
> The documents provide the evidence.<br>
> The user's questions grow the wiki.**

The wiki is therefore not another document repository.

Governance follows:

> **Admin curates shared knowledge structure, not documents. End users consume knowledge and curate relevance, not infrastructure.**


Its lifecycle is:

```text
Company Library Index
        ↓
   Personal Wiki
        ↓
Progressive Expansion
(Explore → Query → Curate → Maintain → Validate)
```

It is a **persistent, personalized navigation and reasoning layer over the company's existing knowledge estate**.
