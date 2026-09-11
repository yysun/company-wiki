# company-wiki — Product Requirements Document

**Version:** 0.5

**Status:** Draft for implementation

**Artifact type:** AI-native knowledge skill / plugin

**Primary interface:** LLM + Markdown knowledge architecture + existing source-access skills/CLI/MCP

**Previous version:** 0.4

**Requirements baseline:** [Personal Wiki & Company Library Index Requirements v0.3](company-wiki-personal-wiki-requirements-v0.3.md)

**Story requirements:** [company-wiki personal knowledge lifecycle](../.docs/reqs/2026/09/11/req-company-wiki-lifecycle.md)

---

## 1. Product Summary

`company-wiki` gives each user a **personalized, progressively constructed knowledge map over the company's
existing document library**, anchored by a small shared Company Library Index.

It does not require the company to move documents into a new knowledge base, annotate every file, or maintain a separate metadata database.

The product has three logical knowledge scopes over the same authoritative sources:

- a Company Library Index governed by a Company Wiki Admin;
- optional Team Wikis governed by designated curators; and
- a Personal Wiki controlled by each user.

These are linked navigation and reasoning overlays, not duplicate repositories. Together they tell the LLM:

- what knowledge domains exist;
- what important business concepts mean;
- which terms, aliases, acronyms, and labels refer to the same concepts;
- how concepts, systems, teams, processes, decisions, metrics, and documents relate;
- where authoritative knowledge lives;
- which source should win when sources conflict;
- what kinds of business questions exist;
- what evidence and reasoning patterns are appropriate for solving those questions.

The LLM uses this schema to plan retrieval and investigation, then accesses original documents through existing tools such as local files, synced folders, CLI tools, MCP servers, document skills, search APIs, or cloud-drive connectors.

> The company provides the map. The documents provide the evidence. The user's questions grow the wiki.

---

## 2. Product Thesis

Traditional RAG starts from documents:

```text
documents
  ↓
chunking
  ↓
embeddings / index
  ↓
retrieve chunks
  ↓
LLM answer
```

`company-wiki` starts from the question and the user's accumulated map:

```text
user question
  ↓
Personal Wiki
  ↓
Company Library Index when the personal route is insufficient
  ↓
understand intent, concepts, authority, and problem type
  ↓
identify concepts, authority, sources, and investigation pattern
  ↓
retrieve evidence from original sources
  ↓
iterate if evidence is incomplete
  ↓
reason
  ↓
answer with evidence and uncertainty
```

The key product abstraction is therefore a **progressively expanded, permission-aware knowledge map**, not a
central ingestion index.

Search indexes, embeddings, GraphRAG structures, summaries, caches, and entity extraction may be added later as performance optimizations. They are derived infrastructure and must not become the source of organizational truth.

---

## 3. Product Goals

### 3.1 Primary goals

`company-wiki` should enable an LLM to:

1. find the right knowledge even when user vocabulary differs from document vocabulary;
2. distinguish authoritative sources from convenient or outdated sources;
3. navigate across multiple repositories without requiring central ingestion;
4. decompose complex questions into useful subqueries;
5. solve business problems rather than merely retrieve documents;
6. identify missing, conflicting, stale, or uncertain evidence;
7. progressively load only the knowledge needed for the current task;
8. let each user build a useful Personal Wiki without reprocessing the company corpus;
9. promote useful knowledge across Personal, Team, and Company scopes under the correct authority; and
10. remain understandable and maintainable as plain text by humans and LLMs.

### 3.2 Secondary goals

- support local-first and cloud-first deployments;
- remain portable across AI hosts;
- reuse existing document/search skills instead of recreating them;
- allow organizations to introduce richer retrieval infrastructure incrementally;
- provide enough structure for future automated schema discovery and maintenance;
- let processing cost scale with active questions and topics rather than total corpus size.

---

## 4. Non-Goals

Version 0.5 does **not** require:

- a vector database;
- a graph database;
- RDF, OWL, SPARQL, or a formal ontology engine;
- metadata sidecars for every document;
- metadata embedded into every source document;
- copying all company documents into a dedicated repository;
- pre-generating summaries for every document;
- building a new cloud-drive connector where a suitable skill, CLI, MCP, or API already exists;
- a workflow engine;
- deterministic business-process automation;
- replacing the company's system of record;
- forcing every user to mirror the company folder hierarchy;
- automatically making every discovery durable;
- granting broader access to derived titles, summaries, links, aliases, or relationships than their evidence;
- requiring users or admins to classify and ingest every company document;
- a parallel ACL database, custom permission system, or custom frontend; or
- queues, mandatory activity logs, watchers, scheduled ingestion, or continuous synchronization.

---

## 5. Core Concept: AI-Facing Information Architecture

The schema extends traditional information architecture for AI use.

Traditional IA usually answers:

- How is information organized?
- What is it called?
- How can users navigate it?
- How can users search it?

`company-wiki` must additionally answer:

- What does this concept mean in this company?
- What terms are equivalent or related?
- Where is authoritative evidence?
- Which source takes precedence?
- What type of problem is the user asking?
- What evidence is required to solve it?
- What reasoning or investigation pattern is appropriate?
- What should the LLM do if evidence conflicts or is incomplete?

Therefore:

```text
LLM Wiki Schema
=
Information Architecture
+ Semantic Model
+ Source Map
+ Authority Model
+ Problem-Solving Model
```

This is intentionally lighter than a formal enterprise ontology but richer than a folder hierarchy or taxonomy.
The Company Library Index carries the shared portion of this model. Personal Wikis add user-specific routes,
projects, investigations, annotations, hypotheses, and priorities without redefining canonical company concepts.

---

## 6. Conceptual Architecture

```text
┌──────────────────────────────────────────────────────────┐
│ Company cloud document library                          │
│ Native content, owners, ACLs, versions, retention       │
└──────────────────────────┬───────────────────────────────┘
                           │ source routes and evidence
                           ▼
┌──────────────────────────────────────────────────────────┐
│ Company Library Index                                   │
│ Small shared semantic/navigation skeleton               │
│ Admin-governed and permission-aware                     │
└──────────────────────────┬───────────────────────────────┘
                           │ reference, not copy
             ┌─────────────┴─────────────┐
             ▼                           ▼
┌─────────────────────────┐  ┌─────────────────────────────┐
│ Optional Team Wiki      │  │ Personal Wiki               │
│ Team-curated overlay    │  │ User-controlled overlay     │
└────────────┬────────────┘  └──────────────┬──────────────┘
             └──────────────┬───────────────┘
                            ▼
               Explore / Query / Curate
                            │
                            ▼
              Original-source evidence and answers
```

All layers use the current provider-authenticated identity. A shared Markdown node may contain derived knowledge
only when its destination audience is provably no broader than the audiences of all underlying sources. If that
cannot be established, the product must keep the knowledge in a narrower scope, sanitize it from independently
public evidence, or refuse the shared write.

---

## 7. Virtual Knowledge Layer

`company-wiki` should behave like an **LLM-native virtual knowledge graph composed of shared and personal
overlays**.

The schema models important concepts and relationships, but the underlying knowledge remains in its original systems.

Example:

```yaml
concept: Vacation Policy
domain: People
source_routes:
  canonical:
    source: WeCom
    path: HR/Policies
  historical:
    source: Google Drive
    path: HR/Archive
authority:
  rule: canonical_over_historical
```

The system does not need to materialize every policy document into a graph.

Instead, the LLM reads the concept definition and source route, then queries the original source.

### 7.1 Operational Lifecycle

Company-level setup and personal use are deliberately separate:

```text
Company sources
      ↓
Company Library Index Init
(bounded representative sampling)
      ↓
Personal Wiki Bootstrap
(reference the visible company map; no corpus sampling)
      ↓
Explore ↔ Query → Curate → Maintain → Validate
```

- **Init** builds or improves the small Company Library Index from explicitly bounded representative sampling.
- **Bootstrap** creates a minimal Personal Wiki and references the visible shared map without copying it.
- **Explore** progressively discovers relevant wiki routes and source evidence; results remain transient.
- **Query** is the primary runtime and answers through Personal Wiki, shared index, and original evidence, with
  direct-source fallback and no silent writeback.
- **Curate** turns selected, reused, or structurally valuable discoveries into durable wiki knowledge.
- **Maintain** corrects, merges, retires, or restructures existing durable knowledge.
- **Validate** detects broken/inaccessible links, drift, missing provenance, duplicates, contradictions,
  supersession, permission leakage, gaps, and orphans without rewriting the corpus.

**Add Source** is an optional bounded path into Explore and Curate for explicitly selected documents or one finite
folder/batch. A folder is enumerated and its visible member bound is confirmed before content reads. It replaces
mandatory top-level Ingest. Existing `Ingest` language may survive only as a compatibility alias for this
reconciliation behavior; documents do not need to be copied, chunked, embedded, or indexed before Query.

Every durable change uses the same change contract: identify ownership scope, exact targets, evidence, conflicts,
and preserved content; verify the authenticated principal's governing capability; present a concrete proposal;
bind approval to the principal, scope, targets, evidence versions, audience result, and proposal; then reread and
preflight immediately before ordered writes. Any changed binding invalidates approval. A preflight failure writes
nothing. A provider failure stops later writes and produces verified successful, failed, and unattempted state plus
a remaining-work-only recovery proposal—never destructive automatic rollback.

Init and Bootstrap also register their completed provider documents. Provider creation and registry registration
are non-atomic: provider pages are created first, then the completed profile and registry link. Registration failure
preserves successful provider pages and prior registry bytes and reports exact recovery work.

### 7.2 Roles and knowledge ownership

- The **Company Wiki Admin** governs canonical shared meaning, terminology, aliases, relationships, and source
  entry points—not the source-document repository.
- A **Team Wiki Curator** may govern department or project knowledge when Team Wikis are enabled.
- The **end user** controls Personal Wiki structure, relevance, annotations, hypotheses, and durable personal
  knowledge.
- The **agent** performs discovery, reconciliation, provenance, duplicate/conflict detection, and safe proposals;
  it does not grant authority or silently promote knowledge.

The end user can add, remove, rename, merge, and pin personal nodes; mark them temporary or personally canonical;
request branch expansion or reorganization; explicitly reconcile a source; and ask the agent to stop learning
from a topic. Destructive or structural changes preserve user-authored organization unless the user approves them.

Promotion follows `Personal → Team → Company` where useful. It reconciles against the destination scope and
requires that scope's provider-verified governing authority; it never blindly copies a page upward. Lower scopes
normally reference shared nodes downward.

### 7.3 Access and disclosure boundary

Source-system ACLs remain authoritative. Registry or wiki prose may describe an owner but cannot grant write or
governance capability. Derived pages, titles, links, aliases, backlinks, summaries, inferred relationships, search
results, and exposed activity must not reveal source information unavailable to the viewer. Native ACLs should be
used where practical; V1 does not introduce a parallel permission database.

For a shared write, source readability is not enough. The provider must verify both the authenticated writer's
governance capability on the exact destination and that the destination audience is a subset of every underlying
evidence audience. If either result is unavailable, the product returns a draft or proposal and refuses the write.
Sanitization is valid only when the remaining material is independently non-sensitive and supported by evidence
visible to the entire destination audience.

### 7.4 Registry and scope selection

The local registry is contained locator and navigation configuration, not evidence or an authorization system. A
workflow starts from one explicitly selected profile. A Personal profile may carry one contained relative edge to
its Company Library Index profile; cross-scope work may follow only that exact edge, and promotion still requires
the user to select the destination profile explicitly. The product never scans or guesses a second profile.

Profiles without scope or a governing-capability locator remain legacy combined wikis. They support Query and
Validate. Same-destination Maintain or Add Source may proceed only with provider-verified current-user write
permission. Legacy profiles cannot authorize Bootstrap, shared canonical writes, Team/Company promotion, or
inferred ownership. Upgrade creates a newly scoped registration from explicit inputs and preserves the legacy
profile until the replacement succeeds.

---

## 8. Source Adapter Model

The schema is independent of access mechanism.

A source may be accessed through:

- local filesystem;
- cloud-synced local folder;
- CLI;
- MCP server;
- existing AI skill;
- cloud document connector;
- search API;
- database query tool;
- enterprise application API.

An adapter should expose the provider capabilities available to the authenticated user, conceptually:

```text
identity()
search(query, scope)
list(location)
read(uri)
metadata(uri)
permissions(uri)
audience(uri)
versions(uri)
capabilities(destination)
preflight_write(destination, target)
write(destination, target)
```

The exact interface is provider-specific, but V1 must fail closed when identity, governance, write permission, or
evidence/destination audience containment cannot be verified. Profile text is never a substitute for these
provider responses.

Local sync is a first-class adapter option, but local availability is never an authorization bypass.

Example:

```yaml
sources:
  - id: product-docs
    type: local_folder
    root: ~/Company/Product

  - id: hr-wecom
    type: skill
    capability: wecom-doc-search

  - id: source-code
    type: cli
    command_family: git

  - id: crm
    type: mcp
    server: company-crm
```

`company-wiki` should not duplicate capabilities already supplied by these adapters.

---

## 9. Schema Layers and Progressive Disclosure

The schema itself should follow progressive disclosure.

### Level 0 — Personal entry

Small enough to load almost every time.

Contains:

- Personal Wiki identity and ownership scope;
- a reference to the visible Company Library Index;
- the user's highest-value topics, projects, or current investigations; and
- pointers to deeper personal or shared sections.

Example:

```text
personal-wiki/
  index.md
```

### Level 1 — Shared Company Library Index

Loaded when the personal map does not contain a sufficient route.

```text
company-library/
  index.md
  domains/
    people.md
    product.md
    finance.md
    sales.md
```

Contains:

- scope;
- key concepts;
- source routes;
- major relationships;
- domain-specific authority rules;
- pointers to problem patterns.

### Level 2 — Focused shared or personal resources

Loaded only when relevant.

```text
wiki/
  concepts/
  sources/
  problem-patterns/
  metrics/
  decisions/
```

### Level 3 — Original evidence

Loaded dynamically from source systems.

This prevents the schema itself from becoming a large context dump.

The Company Library Index should remain intentionally small—typically tens or hundreds of meaningful navigation
nodes, not tens of thousands of documents. Personal structure may diverge from the company folder hierarchy and
should grow only where actual work makes a branch useful.

---

## 10. Schema Components

### 10.1 Domains

High-level knowledge areas.

Examples:

- Company
- People
- Product
- Customers
- Sales
- Finance
- Operations
- Technology
- Legal
- Projects
- Policies

Domains are navigation aids, not rigid silos.

A concept may belong to multiple domains.

---

### 10.2 Concepts

Concepts represent stable business meanings.

Example:

```yaml
id: customer-churn
name: Customer Churn
aliases:
  - churn
  - customer attrition
definition: >
  A customer relationship ending during the defined measurement period.
broader:
  - customer-retention
related:
  - cancellation
  - renewal
  - retention-rate
```

Concepts should be created only when they materially improve understanding, retrieval, or reasoning.

---

### 10.3 Vocabulary

Vocabulary maps company language.

It should support:

- preferred terms;
- aliases;
- acronyms;
- legacy terms;
- product names;
- internal nicknames;
- common user language;
- deprecated terminology.

Example:

```yaml
preferred: Customer Relationship Management
aliases:
  - CRM
  - customer system
legacy:
  - sales database
```

---

### 10.4 Relationships

Relationships help the LLM navigate.

Initial relationship vocabulary should remain small.

Recommended core relationships:

```text
broader
narrower
related_to
owned_by
part_of
depends_on
produces
consumes
measured_by
governed_by
implemented_by
replaces
supersedes
affected_by
source_of_truth_for
```

Do not attempt to model every possible relationship.

---

### 10.5 Knowledge Types

Knowledge types classify evidence by function rather than storage format.

Recommended v0.1 types:

- policy
- procedure
- decision
- requirement
- design
- project
- plan
- meeting
- report
- metric
- dataset
- source-code
- incident
- issue
- contract
- reference
- FAQ
- organization
- role
- system

Example:

A PDF is not a knowledge type. It may contain a `policy`, `contract`, or `report`.

---

### 10.6 Facets

Facets help filter retrieved information.

Recommended initial facets:

- organization / team;
- owner;
- product;
- geography;
- customer segment;
- effective date;
- status;
- confidentiality;
- audience;
- environment;
- version.

Only include facets that improve real queries.

---

### 10.7 Source Map

The source map tells the LLM where knowledge lives and how to retrieve it.

Each source should describe:

- source identity;
- scope;
- access method;
- search capability;
- authority;
- freshness characteristics;
- relevant domains;
- useful paths or collections.

Example:

```yaml
id: product-drive
name: Product Google Drive
domains:
  - product
contains:
  - requirements
  - design
  - decision
access:
  type: skill
  capability: google-drive
authority:
  default: working_source
freshness:
  expected: current
```

---

### 10.8 Authority Model

The schema must explicitly help resolve conflicting evidence.

Possible authority levels:

```text
system_of_record
canonical
approved
working
reference
historical
derived
unknown
```

Example rule:

```yaml
authority_rules:
  - when: policy_conflict
    prefer:
      - approved_current_policy
      - canonical_policy_source
      - working_documents
      - historical_documents
```

The LLM should report conflicts rather than silently choose a weak source.

Authority of evidence is separate from authority to edit a wiki scope. A source can be canonical while the current
user lacks permission to publish its derived meaning into the Company Library Index. Wiki write authority must be
verified from the provider-authenticated identity and destination capability, never inferred from profile prose.

---

### 10.9 Business Definitions and Rules

Some concepts require canonical definitions.

Examples:

- revenue;
- active customer;
- churn;
- utilization;
- eligible employee;
- project complete;
- priority;
- SLA breach.

Example:

```yaml
metric: retention-rate
definition: >
  Customers active at the end of the period divided by customers
  eligible for retention at the beginning of the period.
owner: Customer Analytics
canonical_source: analytics-metric-catalog
```

These definitions prevent inconsistent reasoning across documents.

---

### 10.10 Problem Patterns

Problem patterns describe reusable investigation strategies.

They are not deterministic workflows.

Example:

```yaml
id: explain-metric-change
trigger_examples:
  - Why did revenue decline?
  - What caused churn to increase?
requires:
  - metric_definition
  - comparison_period
  - segment_breakdown
  - relevant_changes
  - alternative_explanations
investigation:
  - confirm metric definition
  - establish size and timing of change
  - identify contributing segments
  - search for relevant business events
  - test plausible explanations against evidence
  - separate supported causes from hypotheses
```

Problem patterns make `company-wiki` useful for problem solving rather than retrieval only.

---

## 11. Competency Questions

The schema must be designed from **questions the organization expects the AI to answer**, not from an attempt to model everything.

A competency question describes a capability such as:

- What is the current travel policy?
- Who owns process X?
- What changed between version A and B?
- Why did metric X decline?
- What decisions have already been made about project Y?
- Which systems depend on service Z?
- Has this issue happened before?
- What are the risks of proposal A?
- What should an employee do when condition X occurs?

Competency questions serve four purposes:

1. define schema scope;
2. expose missing concepts and source mappings;
3. drive evaluation;
4. prevent over-modeling.

A separate competency-question catalog is maintained as a first-class product artifact.

---

## 12. Query and Problem-Solving Runtime

### Step 1 — Understand the request

Classify:

- user intent;
- important concepts;
- relevant domain;
- problem type;
- expected answer form;
- time sensitivity.

### Step 2 — Consult schema

Start with the smallest relevant Personal Wiki route. Follow aliases and links, then consult the Company Library
Index when the personal map is insufficient. Do not load either wiki wholesale.

Resolve:

- terminology;
- concepts;
- relationships;
- possible source routes;
- authority expectations;
- applicable problem pattern.

### Step 3 — Build investigation plan

Examples:

```text
direct lookup
comparison
historical reconstruction
dependency tracing
metric diagnosis
policy interpretation
proposal evaluation
incident investigation
decision discovery
```

### Step 4 — Query sources

Use existing adapters.

Retrieval may include:

- filename/path search;
- keyword search;
- semantic search;
- metadata filtering;
- API query;
- database query;
- graph traversal;
- source-code search.

Query must also support direct-source fallback when the wiki has no useful route, the request names an exact
identifier, recent material may be unrepresented, direct search is more efficient, or the user requests it.

### Step 5 — Evaluate evidence

Check:

- authority;
- freshness;
- completeness;
- contradictions;
- coverage of required evidence.

### Step 6 — Iterate

If evidence is insufficient:

- reformulate query;
- search related concepts;
- inspect another source;
- retrieve additional time periods;
- query dependencies;
- search for contradicting evidence.

### Step 7 — Answer

The final response should distinguish:

- established facts;
- inferred conclusions;
- hypotheses;
- unresolved uncertainty.

Where supported by the host, cite or link original sources.

After answering, identify reusable discoveries. They remain transient unless the user asks to retain them or an
explicit curation policy applies. Any durable change is a separate Curate operation with its own proposal and
approval; Query itself is read-only.

---

## 13. Retrieval Strategy

Retrieval is pluggable.

Preferred order:

1. use the Personal Wiki to reuse a known route;
2. use the Company Library Index to reduce the search space;
3. use native source search directly when the maps are missing or insufficient;
4. use lexical and semantic search together when available;
5. add derived indexes only when they solve demonstrated retrieval failures.

Possible optional retrieval infrastructure:

```text
BM25 / full-text index
embedding index
hybrid retrieval
entity index
GraphRAG
hierarchical summaries
query cache
semantic cache
```

All derived artifacts should be rebuildable from the original sources.

Optional caches must preserve the current principal's permission boundary and carry enough freshness information
to avoid serving stale or newly inaccessible material.

Navigation should be explicitly bounded. A practical default is a maximum wiki traversal depth of 3, two source
search/list rounds, and five opened source documents per operation. A deployment or request may use lower finite
limits. When a limit is exhausted, the agent should report it and request a new finite bound rather than silently
expanding scope.

---

## 14. Document Metadata Strategy

Version 0.5 explicitly avoids requiring:

```text
document.md
document.meta.md
```

for every document.

It also avoids injecting large metadata headers into original documents.

Preferred metadata hierarchy:

1. infer from the source system where reliable;
2. express collection/folder/source-level semantics in the schema;
3. curate concept-level metadata only where valuable;
4. add document-level metadata only for exceptional high-value cases.

This minimizes file proliferation and source noise.

Durable generated or curated claims should nevertheless retain enough provenance to be checked:

- stable source URI or provider ID;
- relevant section, page, or block;
- source version when available;
- access/check timestamp;
- relationship to the source; and
- generated, human-authored, or verified status.

If sources conflict, preserve each accessible source, date, known authority, and supersession relationship plus an
explicit unresolved state. Do not flatten contradictory evidence into one synthetic fact.

---

## 15. Schema Authoring Strategy

Initial **Company Library Index** creation should combine:

### Human input

Humans define:

- key domains;
- authoritative sources;
- terminology that has organizational meaning;
- business rules;
- important competency questions.

### LLM assistance

The LLM may propose:

- concepts;
- aliases;
- relationships;
- missing sources;
- duplicate terminology;
- candidate problem patterns;
- potential competency questions.

Representative source sampling belongs here, at shared-index construction or improvement time. A Personal Wiki
does not repeat it: Personal Bootstrap references the existing visible company map and creates only minimal
personal structure.

### Evidence requirement

The LLM should not promote inferred organizational semantics to canonical status without explicit evidence or human approval.

---

## 16. Knowledge Curation, Maintenance, and Validation

Knowledge growth and repair should be incremental.

Possible triggers:

- a question could not be answered;
- a user corrected terminology;
- sources repeatedly conflict;
- a new repository becomes important;
- the same retrieval path is repeatedly discovered;
- a new recurring problem type appears;
- an old concept or source is deprecated.

Explore results are transient. Curate promotes only explicitly requested, repeatedly useful, project-important,
durable, or structurally valuable discoveries. Maintain handles corrections, merges, renames, hierarchy changes,
obsolete-source replacement, summary refresh, archival, and retirement. Validate independently checks every
visible wiki page for broken/inaccessible links, drift, missing provenance, duplicates, contradictions,
supersession, suspicious relationships, leakage, gaps, and orphans.

The LLM may propose changes but should not silently rewrite personal organization or authoritative semantics.
Validation is read-only by default; fixes route through Curate or Maintain under the destination owner's authority.
Freshness should be lazy: mark a dependent node potentially stale and reread its evidence on the next relevant use
rather than regenerating the whole wiki after every source change. Where supported, freshness states are
`current`, `potentially stale`, `superseded`, and `needs review`.

---

## 17. File Structure

Recommended logical deployment:

```text
Company Library Index/
├── index.md
├── domains/
├── concepts/
├── processes/
├── sources/
└── competency-questions.md

Personal Wiki/
├── index.md
├── topics/
├── projects/
├── concepts/
├── decisions/
└── .wiki/              # optional machine state only when necessary
```

A small organization may keep most shared content in one index document. A Team Wiki may use the same shape as a
Personal Wiki while declaring team ownership and governance.

Splitting files is a scalability mechanism, not a requirement.

---

## 18. Skill Behavior

`SKILL.md` should instruct the agent to:

1. distinguish Company Index Init from Personal Wiki Bootstrap;
2. select the exact ownership scope and verify source and destination boundaries;
3. start Query/Explore from the Personal Wiki, then the shared index, then original sources;
4. use direct-source fallback when the maps are insufficient;
5. identify vocabulary, source routes, authority, provenance, and problem pattern;
6. iterate within explicit traversal, search, document, and context bounds;
7. distinguish facts, generated synthesis, inference, hypotheses, conflicts, and uncertainty;
8. cite authoritative current source evidence rather than treating a wiki summary as proof;
9. keep discovery transient until a separate Curate decision;
10. verify authenticated governance and audience containment before every shared write;
11. propose Maintain/Validate actions for drift, defects, and repeated gaps; and
12. treat Add Source as optional bounded reconciliation, never a Query prerequisite.

---

## 19. Minimal Viable Product

### MVP scope

The MVP should prove that a shared map plus a progressively grown Personal Wiki improves repeated company work
without creating a second document repository.

Required:

- one existing cloud/local-sync source adapter;
- one small admin-governed Company Library Index in Markdown;
- one user-controlled Personal Wiki bootstrapped by reference;
- permission-aware source and destination access;
- Explore and Query with direct-source fallback;
- original-source citations and provenance on durable nodes;
- Curate plus basic Maintain and read-only Validate;
- bounded Add Source for one selected document or folder;
- prevention of obvious derived-access leakage; and
- one Personal → Company promotion proposal/review flow.

Team Wiki execution may be deferred, but the ownership model must not block it.

Not required:

- graph database;
- embeddings;
- automated ingestion;
- visual schema editor;
- automated ontology extraction;
- continuous background synchronization;
- corpus-wide sampling for every Personal Wiki;
- mandatory source reconciliation before Query.

---

## 20. Evaluation

The primary evaluation unit is a competency question, measured both on first use and after the Personal Wiki has
accumulated relevant routes.

For each question evaluate:

### Retrieval quality

- Did the agent find the right source?
- Did vocabulary differences cause misses?
- Did it retrieve enough evidence?

### Authority

- Did it prefer the correct source?
- Did it detect stale or conflicting information?
- Did durable writes require provider-verified authority rather than a role claimed in prose?

### Permission safety

- Did the agent avoid exposing inaccessible content and derived metadata?
- Did each shared write prove that its destination audience was contained by every evidence audience?
- Could a less-privileged user discover any restricted title, link, alias, summary, or relationship?

### Reasoning

- Did it choose an appropriate investigation pattern?
- Did it decompose a complex question?
- Did it test plausible alternatives?

### Answer quality

- Correctness
- completeness
- evidence support
- uncertainty handling
- concision

### Layered-wiki contribution

Compare:

```text
A. native/direct document search
B. direct LLM + document search
C. Company Library Index + document search
D. Personal Wiki + Company Library Index + document search
```

Compare correctness, discovery success, source reads/search rounds, token use, latency, citation quality, repeated
question efficiency, ACL leakage, Curate signal-to-noise, and maintenance/validation cost. This isolates the value
of shared and personal navigation from optional retrieval infrastructure.

---

## 21. Success Criteria

The MVP succeeds if the layered wiki materially improves:

- source-selection accuracy;
- answer accuracy;
- multi-source problem solving;
- authority/conflict handling;
- retrieval efficiency;
- robustness to vocabulary mismatch;
- repeated-question efficiency as the Personal Wiki grows;
- user navigation success and usefulness of accumulated personal knowledge;
- useful durable Curate decisions without excessive wiki growth; and
- permission safety for shared and derived knowledge.

A good result should be achieved **without requiring per-document metadata or centralized ingestion**.

---

## 22. Design Principles

### 22.1 Navigation before ingestion

Build a useful semantic map before adding derived retrieval infrastructure. A document never needs to be ingested
before it can be queried through its native source.

### 22.2 Questions before ontology

Use competency questions to decide what deserves modeling.

### 22.3 Original sources remain authoritative

Source systems own content, ACLs, versions, retention, and auditability. Wiki overlays navigate and synthesize;
they do not silently replace evidence. Generated structures may be rebuilt, but user-authored Personal Wiki
organization is not silently discarded or overwritten.

### 22.4 Progressive disclosure

Do not load the whole knowledge architecture when only one domain is relevant.

### 22.5 Curate meaning, automate mechanics

Admins curate shared meaning, users curate personal relevance, and Team Curators govern optional team scope.

Agents can handle discovery, reconciliation, provenance, duplicate/conflict detection, and safe proposals.

### 22.6 Minimum sufficient semantics

Add only enough structure to materially improve querying or reasoning.

### 22.7 Reuse the ecosystem

Use existing document skills, MCP servers, CLIs, and APIs rather than building redundant connectors.

### 22.8 Retrieval is iterative

Complex questions should be investigated through multiple search/reasoning rounds when necessary.

### 22.9 Problem solving is first-class

The system should know not only where knowledge is but how different classes of questions should be investigated.

### 22.10 Personal use drives growth

The Company Library Index gives users a starting map. Actual questions, investigations, projects, and explicitly
selected sources determine what enters each Personal Wiki.

### 22.11 Shared knowledge requires stronger proof

Personal approval does not authorize Team or Company changes. Shared promotion requires provider-verified
governance, destination-audience containment, provenance, and reconciliation with existing canonical knowledge.

---

## 23. Future Directions

Possible later versions:

### v0.5
- schema-assisted query planner;
- automated source discovery;
- schema linting;
- competency-question test runner;
- optional Team Wiki execution and Personal → Team promotion.

### v0.6
- learned retrieval routing;
- generated concept candidates;
- conflict/staleness detection;
- reusable organization-specific problem patterns;
- permission-preserving caches and richer lazy freshness signals.

### v1.0
- schema evolution with human approval;
- optional virtual knowledge graph;
- GraphRAG / hierarchical retrieval integration;
- organization-wide evaluation suite;
- host-independent skill/plugin packaging.

---

## 24. One-Sentence Definition

> **`company-wiki` is a persistent, personalized navigation and reasoning layer over authoritative company
> documents: the company supplies a shared map, the documents supply evidence, and each user's work progressively
> grows their own wiki.**
