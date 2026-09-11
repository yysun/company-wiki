# company-wiki — Product Requirements Document

**Version:** 0.4  
**Status:** Draft for implementation  
**Artifact type:** AI-native knowledge skill / plugin  
**Primary interface:** LLM + Markdown knowledge architecture + existing source-access skills/CLI/MCP  
**Previous version:** 0.3

---

## 1. Product Summary

`company-wiki` gives an AI agent an **AI-readable information architecture over existing company knowledge**.

It does not require the company to move documents into a new knowledge base, annotate every file, or maintain a separate metadata database.

Instead, `company-wiki` maintains a small curated **knowledge schema** that tells the LLM:

- what knowledge domains exist;
- what important business concepts mean;
- which terms, aliases, acronyms, and labels refer to the same concepts;
- how concepts, systems, teams, processes, decisions, metrics, and documents relate;
- where authoritative knowledge lives;
- which source should win when sources conflict;
- what kinds of business questions exist;
- what evidence and reasoning patterns are appropriate for solving those questions.

The LLM uses this schema to plan retrieval and investigation, then accesses original documents through existing tools such as local files, synced folders, CLI tools, MCP servers, document skills, search APIs, or cloud-drive connectors.

> `company-wiki` is an AI-facing information architecture and problem-solving map, not a replacement document repository.

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

`company-wiki` starts from the question:

```text
user question
  ↓
understand intent and problem type
  ↓
consult company knowledge schema
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

The key product abstraction is therefore the **schema**, not the index.

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
8. remain understandable and maintainable as plain text by humans and LLMs.

### 3.2 Secondary goals

- support local-first and cloud-first deployments;
- remain portable across AI hosts;
- reuse existing document/search skills instead of recreating them;
- allow organizations to introduce richer retrieval infrastructure incrementally;
- provide enough structure for future automated schema discovery and maintenance.

---

## 4. Non-Goals

Version 0.4 does **not** require:

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
- replacing the company's system of record.

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

---

## 6. Conceptual Architecture

```text
                        ┌──────────────────────────┐
                        │        User / Agent      │
                        └─────────────┬────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │       company-wiki       │
                        │     skill / capability   │
                        └─────────────┬────────────┘
                                      │
                                      ▼
                    ┌──────────────────────────────────┐
                    │       AI-Readable Schema         │
                    │                                  │
                    │ domains                          │
                    │ concepts + vocabulary            │
                    │ relationships                    │
                    │ knowledge types                  │
                    │ facets                           │
                    │ source map                       │
                    │ authority rules                  │
                    │ business definitions             │
                    │ problem patterns                 │
                    └──────────────┬───────────────────┘
                                   │ guides
                                   ▼
                    ┌──────────────────────────────────┐
                    │     Retrieval / Investigation    │
                    │                                  │
                    │ query expansion                  │
                    │ source selection                 │
                    │ decomposition                    │
                    │ iterative search                 │
                    │ evidence comparison              │
                    └──────────────┬───────────────────┘
                                   │
          ┌────────────────────────┼─────────────────────────┐
          │                        │                         │
          ▼                        ▼                         ▼
 ┌─────────────────┐     ┌──────────────────┐      ┌─────────────────┐
 │ Local / Synced  │     │ Cloud Docs /    │      │ Systems / APIs  │
 │ folders / Git   │     │ Wiki / Drive    │      │ DB / MCP / CLI  │
 └─────────────────┘     └──────────────────┘      └─────────────────┘
```

---

## 7. Virtual Knowledge Layer

`company-wiki` should behave like an **LLM-native virtual knowledge graph**.

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

The document-native implementation uses five distinct operations:

```text
Init → Ingest → Query → Maintain → Validate
```

- **Init** creates a minimal map from bounded discovery and representative sampling; it is not a full import.
- **Ingest** reconciles explicitly selected new evidence into the existing wiki through a reviewed and
  approved change plan. One source is the default; batches are finite and user-selected.
- **Query** answers through the wiki and original evidence without writing.
- **Maintain** corrects or restructures wiki knowledge under explicit change control.
- **Validate** detects link failures, source drift, gaps, contradictions, and graph defects without writing.

Ingest is an editorial operation, not centralized ingestion infrastructure. It creates no source mirror,
embedding index, processing ledger, mandatory log, watcher, or background synchronization. Approved writes
are revalidated before application; stale plans require fresh approval, and partial provider failure is
reported without destructive rollback.

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

### Level 0 — Entry

Small enough to load almost every time.

Contains:

- schema identity;
- domains;
- major sources;
- top-level authority rules;
- pointers to deeper schema sections.

Example:

```text
company-wiki/
  SKILL.md
  schema/
    index.md
```

### Level 1 — Domain

Loaded when a question touches a domain.

```text
schema/
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

### Level 2 — Detailed semantic resources

Loaded only when relevant.

```text
schema/
  concepts/
  sources/
  problem-patterns/
  metrics/
  decisions/
```

### Level 3 — Original evidence

Loaded dynamically from source systems.

This prevents the schema itself from becoming a large context dump.

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

Load only relevant schema sections.

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

---

## 13. Retrieval Strategy

Retrieval is pluggable.

Preferred order:

1. use the schema to reduce the search space;
2. use native source search when good enough;
3. use lexical and semantic search together when available;
4. add derived indexes only when they solve demonstrated retrieval failures.

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

---

## 14. Document Metadata Strategy

Version 0.4 explicitly avoids requiring:

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

---

## 15. Schema Authoring Strategy

Initial schema creation should combine:

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

### Evidence requirement

The LLM should not promote inferred organizational semantics to canonical status without explicit evidence or human approval.

---

## 16. Schema Maintenance

Schema maintenance should be incremental.

Possible triggers:

- a question could not be answered;
- a user corrected terminology;
- sources repeatedly conflict;
- a new repository becomes important;
- the same retrieval path is repeatedly discovered;
- a new recurring problem type appears;
- an old concept or source is deprecated.

The LLM may propose schema changes but should not silently rewrite authoritative semantics.

---

## 17. File Structure

Recommended initial implementation:

```text
company-wiki/
├── SKILL.md
├── README.md
├── schema/
│   ├── index.md
│   ├── domains/
│   │   ├── company.md
│   │   ├── people.md
│   │   ├── product.md
│   │   └── technology.md
│   ├── concepts/
│   ├── sources/
│   ├── metrics/
│   └── problem-patterns/
├── competency-questions.md
└── examples/
```

A small organization may keep most schema content in `schema/index.md`.

Splitting files is a scalability mechanism, not a requirement.

---

## 18. Skill Behavior

`SKILL.md` should instruct the agent to:

1. determine whether company knowledge is needed;
2. inspect `schema/index.md`;
3. progressively load the relevant domain/schema section;
4. identify vocabulary, source routes, authority, and problem pattern;
5. query original sources using available skills, CLI, MCP, APIs, or files;
6. iterate until evidence is sufficient or further search is unlikely to help;
7. distinguish facts from inference;
8. prefer authoritative and current evidence;
9. expose unresolved contradictions;
10. suggest schema updates when repeated gaps are discovered.

---

## 19. Minimal Viable Product

### MVP scope

The MVP should prove that a small schema improves the LLM's ability to answer real company questions.

Required:

- Markdown schema;
- 3–5 domains;
- 20–50 key concepts;
- source map;
- authority rules;
- 5–10 problem patterns;
- 25–50 competency questions;
- at least two heterogeneous source adapters;
- progressive schema loading;
- evidence-aware answers.

Not required:

- graph database;
- embeddings;
- automated ingestion;
- visual schema editor;
- automated ontology extraction;
- continuous background synchronization.

---

## 20. Evaluation

The primary evaluation unit is a competency question.

For each question evaluate:

### Retrieval quality

- Did the agent find the right source?
- Did vocabulary differences cause misses?
- Did it retrieve enough evidence?

### Authority

- Did it prefer the correct source?
- Did it detect stale or conflicting information?

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

### Schema contribution

Compare:

```text
agent + raw source search
vs.
agent + company-wiki schema + same source search
```

This isolates the value of the schema from retrieval infrastructure.

---

## 21. Success Criteria

The MVP succeeds if the schema materially improves:

- source-selection accuracy;
- answer accuracy;
- multi-source problem solving;
- authority/conflict handling;
- retrieval efficiency;
- robustness to vocabulary mismatch.

A good result should be achieved **without requiring per-document metadata or centralized ingestion**.

---

## 22. Design Principles

### 22.1 Schema before index

Model how the company understands knowledge before optimizing retrieval.

### 22.2 Questions before ontology

Use competency questions to decide what deserves modeling.

### 22.3 Original sources remain authoritative

Derived AI structures are disposable.

### 22.4 Progressive disclosure

Do not load the whole knowledge architecture when only one domain is relevant.

### 22.5 Curate meaning, automate mechanics

Humans should focus on meaning, authority, and business definitions.

Machines can handle indexing, search, extraction, and caching.

### 22.6 Minimum sufficient semantics

Add only enough structure to materially improve querying or reasoning.

### 22.7 Reuse the ecosystem

Use existing document skills, MCP servers, CLIs, and APIs rather than building redundant connectors.

### 22.8 Retrieval is iterative

Complex questions should be investigated through multiple search/reasoning rounds when necessary.

### 22.9 Problem solving is first-class

The system should know not only where knowledge is but how different classes of questions should be investigated.

---

## 23. Future Directions

Possible later versions:

### v0.5
- schema-assisted query planner;
- automated source discovery;
- schema linting;
- competency-question test runner.

### v0.6
- learned retrieval routing;
- generated concept candidates;
- conflict/staleness detection;
- reusable organization-specific problem patterns.

### v1.0
- schema evolution with human approval;
- optional virtual knowledge graph;
- GraphRAG / hierarchical retrieval integration;
- organization-wide evaluation suite;
- host-independent skill/plugin packaging.

---

## 24. One-Sentence Definition

> **`company-wiki` provides an AI-readable information architecture over existing enterprise knowledge so an LLM can understand what knowledge exists, what it means, where authoritative evidence lives, how concepts relate, and how to investigate common classes of business problems.**
