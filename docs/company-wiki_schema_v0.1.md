# company-wiki — Schema Specification

**Version:** 0.1  
**Status:** Draft  
**Format:** Markdown-first, YAML-compatible examples  
**Purpose:** Define the minimal AI-readable information architecture used by `company-wiki`.

---

## 1. Design Objective

The schema is a **small curated semantic overlay** over existing company knowledge.

Its purpose is to help an LLM answer five questions:

1. **What does this mean?**
2. **What is it related to?**
3. **Where should I look?**
4. **Which source should I trust?**
5. **How should I investigate this kind of problem?**

The schema is not intended to represent every document, record, or fact in the organization.

---

## 2. Schema Principles

1. **Markdown first** — readable by humans and LLMs.
2. **Minimal semantics** — model only what improves querying or reasoning.
3. **Progressive disclosure** — split large schemas by domain.
4. **Source-preserving** — original systems remain authoritative.
5. **Portable** — no dependency on a specific vector DB, graph DB, or AI host.
6. **Question-driven** — competency questions determine scope.
7. **Authority-aware** — conflicts must be resolvable or surfaced.
8. **Problem-aware** — recurring investigation patterns are part of the schema.
9. **LLM interpretable** — avoid unnecessary formalism where natural language is sufficient.
10. **Extensible** — implementations may add fields without changing the core model.

---

## 3. Top-Level Model

A schema MAY contain:

```yaml
schema:
  id:
  name:
  version:
  description:

domains: []
concepts: []
knowledge_types: []
facets: []
sources: []
authority_levels: []
authority_rules: []
business_definitions: []
problem_patterns: []
```

A large implementation MAY split these into separate Markdown files.

---

## 4. Schema Identity

Required fields:

```yaml
schema:
  id: company
  name: Company Knowledge Schema
  version: 0.1
  description: >
    AI-readable information architecture for company knowledge.
```

Optional:

```yaml
  owner: Knowledge Team
  updated: 2026-09-10
  default_language: en
  additional_languages:
    - zh
```

---

## 5. Domain

A domain represents a major area of organizational knowledge.

### Minimal form

```yaml
- id: product
  name: Product
  description: Product strategy, requirements, design, releases, and operations.
```

### Extended form

```yaml
- id: product
  name: Product
  aliases:
    - Product Management
  description: >
    Product strategy, requirements, design, roadmap, releases, and product operations.
  key_concepts:
    - product-roadmap
    - requirement
    - release
  source_routes:
    - product-drive
    - source-code
  related_domains:
    - technology
    - customers
```

### Guidance

Use domains for navigation, not strict ownership.

A concept may belong to multiple domains.

---

## 6. Concept

A concept represents stable organizational meaning.

### Minimal form

```yaml
- id: customer-churn
  name: Customer Churn
  definition: >
    A customer relationship ending during the defined measurement period.
```

### Extended form

```yaml
- id: customer-churn
  name: Customer Churn
  aliases:
    - churn
    - customer attrition
  legacy_terms:
    - customer loss
  domains:
    - customers
    - finance
  definition: >
    A customer relationship ending during the defined measurement period.
  broader:
    - customer-retention
  narrower:
    - voluntary-churn
    - involuntary-churn
  related_to:
    - cancellation
    - renewal
  measured_by:
    - churn-rate
  governed_by:
    - customer-status-policy
```

### Recommended concept fields

```text
id
name
aliases
legacy_terms
definition
domains
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
source_routes
notes
```

Not all fields apply to every concept.

---

## 7. Vocabulary

Vocabulary can live inside concepts or as a separate section.

Example:

```yaml
vocabulary:
  - preferred: Customer Relationship Management
    aliases:
      - CRM
      - customer system
    legacy:
      - sales database
    note: >
      "CRM" normally refers to the corporate CRM application unless the
      surrounding context explicitly refers to CRM as a business discipline.
```

Vocabulary is especially useful for:

- acronyms;
- overloaded terms;
- internal nicknames;
- renamed products;
- legacy system names;
- business/user terminology mismatches.

---

## 8. Relationship Vocabulary

Recommended core relationships:

| Relationship | Meaning |
|---|---|
| `broader` | More general concept |
| `narrower` | More specific concept |
| `related_to` | Semantically associated |
| `owned_by` | Organizational ownership |
| `part_of` | Structural containment |
| `depends_on` | Dependency |
| `produces` | Creates an output |
| `consumes` | Uses an input |
| `measured_by` | Metric relationship |
| `governed_by` | Policy/rule relationship |
| `implemented_by` | Implementation relationship |
| `replaces` | Replaces another concept/system |
| `supersedes` | Newer authoritative version |
| `affected_by` | Material influence |
| `source_of_truth_for` | Authoritative source relation |

Implementations MAY define domain-specific relationships.

Avoid large relationship vocabularies until actual questions require them.

---

## 9. Knowledge Type

A knowledge type describes the role information plays.

Recommended v0.1 values:

```yaml
knowledge_types:
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
```

Additional values may be added when needed.

Storage formats such as `PDF`, `DOCX`, or `Markdown` are not knowledge types.

---

## 10. Facet

Facets are dimensions useful for filtering.

Example:

```yaml
facets:
  - id: effective-date
    name: Effective Date
    type: date

  - id: status
    name: Status
    values:
      - draft
      - proposed
      - approved
      - active
      - deprecated
      - archived

  - id: audience
    name: Audience
```

Recommended initial facets:

```text
organization
team
owner
product
geography
customer_segment
effective_date
status
confidentiality
audience
environment
version
```

Do not add a facet unless it changes retrieval or interpretation.

---

## 11. Source

A source describes where evidence lives and how it can be accessed.

### Minimal form

```yaml
- id: product-drive
  name: Product Google Drive
  access:
    type: skill
    capability: google-drive
```

### Extended form

```yaml
- id: product-drive
  name: Product Google Drive
  description: >
    Working and approved product requirements, design documents, and decision records.
  domains:
    - product
  contains:
    - requirement
    - design
    - decision
  access:
    type: skill
    capability: google-drive
  routes:
    - label: requirements
      path: Product/Requirements
    - label: decisions
      path: Product/Decisions
  search:
    supports:
      - filename
      - fulltext
      - metadata
  authority:
    default: working
    exceptions:
      - path: Product/Approved
        level: approved
  freshness:
    expectation: current
```

---

## 12. Source Access Types

Recommended access types:

```text
local_folder
synced_folder
skill
cli
mcp
api
database
search_service
web
```

Examples:

```yaml
access:
  type: local_folder
  root: ~/Company/Product
```

```yaml
access:
  type: mcp
  server: company-crm
```

```yaml
access:
  type: cli
  tool: git
```

The schema describes the capability but should not contain credentials.

---

## 13. Source Route

A source route maps a concept or knowledge type to likely evidence.

Example:

```yaml
source_routes:
  - for: vacation-policy
    routes:
      - source: hr-wecom
        location: HR/Policies
        role: canonical
      - source: hr-drive
        location: Archive/Policies
        role: historical
```

Routes can be:

- exact paths;
- folders;
- collections;
- query hints;
- database tables/views;
- API resource families;
- repo paths;
- search instructions.

---

## 14. Authority Level

Recommended standard authority levels, from strongest to weakest:

```yaml
authority_levels:
  - system_of_record
  - canonical
  - approved
  - working
  - reference
  - historical
  - derived
  - unknown
```

Interpretation:

### `system_of_record`

Operational system whose values define current truth for a specific class of facts.

### `canonical`

Official source designated as authoritative.

### `approved`

Formally approved artifact.

### `working`

Current working material that may still change.

### `reference`

Useful informational source but not authoritative.

### `historical`

Previously valid or archived information.

### `derived`

Generated summaries, indexes, extracts, analytics, or AI-produced structures.

### `unknown`

Authority not established.

---

## 15. Authority Rule

Authority rules tell the LLM how to resolve conflicts.

Example:

```yaml
authority_rules:
  - id: current-policy
    when: >
      Multiple documents provide conflicting versions of a policy.
    prefer:
      - active approved policy from canonical HR source
      - newer approved policy
      - working draft
      - historical policy
    behavior:
      conflict: surface
      unresolved: state_uncertainty
```

Another example:

```yaml
  - id: customer-status
    when: customer account status is requested
    prefer:
      - crm-system-of-record
    ignore_for_current_status:
      - meeting notes
      - sales presentations
```

Authority rules MAY be scoped to a domain or concept.

---

## 16. Business Definition

Business definitions provide canonical meaning for important metrics, statuses, and rules.

Example:

```yaml
- id: active-customer
  name: Active Customer
  type: business_definition
  definition: >
    A customer with at least one active paid subscription and no completed
    cancellation effective before the evaluation date.
  owner: Revenue Operations
  source_of_truth: crm
```

Metric example:

```yaml
- id: churn-rate
  name: Churn Rate
  type: metric
  definition: >
    Customers lost during the period divided by customers eligible to churn
    at the start of the period.
  numerator: customers_lost
  denominator: eligible_customers_start
  owner: Customer Analytics
  canonical_source: analytics-catalog
```

---

## 17. Problem Pattern

A problem pattern describes how an LLM should investigate a recurring class of questions.

### Required fields

```yaml
- id:
  name:
  intent:
  requires:
  investigation:
```

### Example: Direct Lookup

```yaml
- id: authoritative-lookup
  name: Authoritative Lookup
  intent: >
    Find the current authoritative answer to a specific factual,
    policy, ownership, or definition question.
  trigger_examples:
    - What is our travel policy?
    - Who owns payroll?
  requires:
    - target concept
    - authoritative source
  investigation:
    - resolve terminology
    - identify canonical source
    - retrieve current evidence
    - check effective date when relevant
    - answer from authoritative source
```

### Example: Explain Metric Change

```yaml
- id: explain-metric-change
  name: Explain Metric Change
  intent: >
    Explain why a metric changed across time, segment, or condition.
  trigger_examples:
    - Why did churn increase?
    - What caused conversion to decline?
  requires:
    - metric definition
    - comparison period
    - magnitude of change
    - segment breakdown
    - relevant events or changes
    - alternative explanations
  investigation:
    - confirm metric definition
    - establish baseline and observed change
    - decompose by important dimensions
    - identify where the change concentrates
    - search for business or system changes during the period
    - test plausible explanations against evidence
    - distinguish supported causes from hypotheses
```

### Example: Decision Reconstruction

```yaml
- id: reconstruct-decision
  name: Reconstruct Decision
  intent: >
    Determine what was decided, why, by whom, and whether the decision
    is still current.
  requires:
    - decision records
    - related proposals
    - meeting notes
    - later superseding decisions
  investigation:
    - search for explicit decision artifacts
    - collect supporting discussions
    - identify decision owner and date
    - search for later changes or superseding decisions
    - summarize decision, rationale, and current status
```

---

## 18. Recommended v0.1 Problem Patterns

Initial implementations SHOULD consider:

```text
authoritative-lookup
find-owner
compare-versions
reconstruct-decision
explain-metric-change
trace-dependency
investigate-incident
find-precedent
evaluate-proposal
policy-application
summarize-status
identify-risk
```

Only implement patterns represented by real competency questions.

---

## 19. Competency Question Link

Problem patterns may list related competency-question IDs.

Example:

```yaml
competency_questions:
  - CQ-METRIC-001
  - CQ-METRIC-002
```

Concepts and sources MAY do the same.

This allows the schema to be tested against expected questions.

---

## 20. Progressive Disclosure Structure

Recommended:

```text
schema/
├── index.md
├── domains/
│   ├── people.md
│   ├── finance.md
│   ├── product.md
│   └── technology.md
├── concepts/
├── sources/
├── metrics/
└── problem-patterns/
```

### `index.md` SHOULD contain

- schema purpose;
- domain index;
- source index;
- top-level terminology;
- authority rules;
- problem-pattern index;
- links to deeper files.

An LLM should normally read `index.md` before deeper schema resources.

---

## 21. Example `schema/index.md`

```markdown
# Company Knowledge Schema

## Domains

- [People](domains/people.md)
- [Product](domains/product.md)
- [Finance](domains/finance.md)
- [Technology](domains/technology.md)

## Primary Sources

- HR policies → WeCom / HR / Policies
- Product decisions → Google Drive / Product / Decisions
- Current customer state → CRM MCP
- Source code → Git repositories

## Authority

1. Operational system of record for live operational state.
2. Current approved policy for policy questions.
3. Explicit decision record for decisions.
4. Working documents when no approved artifact exists.
5. Historical material only for historical questions.

## Important Vocabulary

- CRM → Customer Relationship Management system
- ARR → Annual Recurring Revenue
- GA → General Availability

## Problem Patterns

- [Authoritative Lookup](problem-patterns/authoritative-lookup.md)
- [Decision Reconstruction](problem-patterns/reconstruct-decision.md)
- [Explain Metric Change](problem-patterns/explain-metric-change.md)
```

---

## 22. Schema Validation Rules

An implementation SHOULD warn when:

- duplicate concept IDs exist;
- a relationship references a missing concept;
- a source route references a missing source;
- a canonical source has no access method;
- two authority rules contradict each other;
- a metric has multiple incompatible definitions;
- a deprecated concept is still preferred;
- a problem pattern requires evidence with no known source;
- a competency question cannot be mapped to a domain or problem pattern.

Formal JSON Schema validation is optional.

Semantic validation by an LLM is acceptable for v0.1.

---

## 23. What Must Not Go in the Core Schema

Avoid putting the following into the curated semantic layer unless they have explicit business meaning:

- embedding vectors;
- chunk IDs;
- generated chunk summaries;
- retrieval scores;
- search-engine internals;
- transient cache keys;
- automatically extracted entities with no review;
- per-document boilerplate metadata;
- model-specific prompt internals.

These belong to derived infrastructure.

---

## 24. Evolution

A schema change should be considered when:

- the same terminology mismatch occurs repeatedly;
- the LLM repeatedly searches the wrong source;
- a source becomes canonical or deprecated;
- a recurring question cannot be answered efficiently;
- a new major business concept appears;
- a metric definition changes;
- a recurring reasoning pattern emerges.

Possible change process:

```text
failure / new need
  ↓
LLM proposes schema change
  ↓
human or authoritative evidence validates
  ↓
schema updated
  ↓
competency tests rerun
```

---

## 25. Minimal v0.1 Implementation

A useful first schema may contain only:

```text
3–5 domains
20–50 concepts
5–10 sources
5–10 authority rules
5–10 business definitions
5–10 problem patterns
25–50 competency questions
```

The goal is not completeness.

The goal is to provide enough structure to measurably improve question answering and problem solving.
