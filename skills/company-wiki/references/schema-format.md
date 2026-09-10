# Schema format

This is the compact format contract for the organization files created beside the skill. Use
Markdown headings followed by YAML-compatible blocks. Keep prose readable, use English snake_case
field names, ASCII kebab-case element ids, and the organization's chosen language for names,
definitions, and descriptions. Aliases remain exactly as sources write them.

## Layout and identity

The organization directory is:

```text
schema/
  index.md
  domains/
  concepts/
  sources/
  metrics/
  problem-patterns/
competency-questions.md
```

`schema/index.md` is Level 0 and should normally be 100 lines or fewer. It contains the schema
identity, domain index, major source index, top-level authority rules, important vocabulary, pattern
index, and links to deeper resources. Domain files are Level 1; detailed concepts, sources, metrics,
and patterns are Level 2; original evidence is Level 3 and is read dynamically. A small organization
may keep most elements in `index.md`. Use relative Markdown links and no absolute paths. Treat schema
documents or focused sections as nodes and meaningful links as labeled edges; link readers must retain
the visible label and actual destination so an agent can traverse the graph with ordinary read tools.

The identity requires:

```yaml
schema:
  id: company
  name: Company Knowledge Schema
  version: 0.1
  description: AI-readable map of company knowledge.
  default_language: en
```

`owner`, `updated`, and `additional_languages` are optional. `default_language` is an ISO 639-1
code such as `en` or `zh`; record other supported codes in `additional_languages`.

## Elements

Every schema element has `review_status: proposed | confirmed | deprecated`. A confirmed element
must have `evidence` or `confirmed_by: user`. Apply that rule field by field: an inferred alias is a
separate vocabulary entry, an inferred relationship is a separate relationship entry, and an
inferred authority ranking is a separate authority-rule entry. Do not attach unsupported fields to
an otherwise confirmed element. Deprecating a confirmed element is proposed until explicitly
confirmed.

### Domains and concepts

```yaml
- id: product
  name: Product
  description: Product strategy, requirements, design, and releases.
  aliases: []
  key_concepts: []
  source_routes: []
  related_domains: []
  review_status: confirmed
  evidence: source-id#section
```

Domains are navigation aids, not rigid ownership boundaries. Concepts represent reusable meaning:

```yaml
- id: customer-churn
  name: Customer Churn
  aliases: []
  legacy_terms: []
  definition: A customer relationship ending during a defined period.
  domains: [customers]
  broader: []
  narrower: []
  related_to: []
  owned_by: []
  part_of: []
  depends_on: []
  produces: []
  consumes: []
  measured_by: []
  governed_by: []
  implemented_by: []
  replaces: []
  supersedes: []
  affected_by: []
  source_of_truth_for: []
  source_routes: []
  notes: []
  review_status: confirmed
  evidence: source-id#section
```

Use only fields that improve a competency question or a demonstrated query. Vocabulary entries may
also stand alone:

```yaml
- preferred: Customer Relationship Management
  aliases: [CRM, customer system]
  acronyms: [CRM]
  legacy_terms: [sales database]
  note: CRM can mean the application or the discipline; use context.
  maps_to: customer-relationship-management
  review_status: proposed
  evidence: source-id#section
```

The 15 core relationships are `broader`, `narrower`, `related_to`, `owned_by`, `part_of`,
`depends_on`, `produces`, `consumes`, `measured_by`, `governed_by`, `implemented_by`, `replaces`,
`supersedes`, `affected_by`, and `source_of_truth_for`. Use a relationship only when its meaning is
needed and supported; preserve conditions and scope in a claim or note rather than flattening them.

### Knowledge types and facets

Knowledge types classify what information does, not its storage format:
`policy`, `procedure`, `decision`, `requirement`, `design`, `project`, `plan`, `meeting`, `report`,
`metric`, `dataset`, `source-code`, `incident`, `issue`, `contract`, `reference`, `FAQ`,
`organization`, `role`, and `system`. A file format is not a knowledge type.

Recommended facets are `organization`, `team`, `owner`, `product`, `geography`, `customer_segment`,
`effective_date`, `status`, `confidentiality`, `audience`, `environment`, and `version`. Add a facet
only when it changes retrieval or interpretation. Status values may include `draft`, `proposed`,
`approved`, `active`, `deprecated`, and `archived`.

### Sources and routes

Each source has an id, name, scope, access method, locator, `locator_note`, useful search capability,
authority, freshness, relevant domains, and routes where applicable. The locator is exactly what the
user supplied. Relative locators resolve from the current working directory and must state that base
in `locator_note`.

Allowed access types are `local_folder`, `synced_folder`, `skill`, `cli`, `mcp`, `api`, `database`,
`search_service`, and `web`. A route gives a label and path, collection, query, or other narrow way
to reach evidence. Never put credentials in a source entry.

```yaml
- id: product-source
  name: Product source
  domains: [product]
  access:
    type: local_folder
    locator: ./Product
  locator_note: Relative to the workspace root where the user works.
  routes:
    - label: decisions
      path: Decisions
  authority:
    default: working
  freshness:
    expectation: current
  review_status: proposed
  evidence: user-supplied source route
```

Authority levels, strongest to weakest, are `system_of_record`, `canonical`, `approved`, `working`,
`reference`, `historical`, `derived`, and `unknown`. Authority is about the source; review status is
about the schema element. Rules name their scope, preferred evidence, exceptions, and behavior when
conflict remains. Prefer current applicable evidence, but surface unresolved conflict.

### Business definitions and metrics

A business definition records an important meaning, owner, scope, and source of truth. A metric also
records its formula, numerator, denominator, dimensions, period, owner, and canonical source when
known. Do not place unreviewed figures or a copied restricted source in the schema.

```yaml
- id: active-customer
  name: Active Customer
  type: business_definition
  definition: A customer with an active paid subscription on the evaluation date.
  owner: Revenue Operations
  source_of_truth: customer-system
  review_status: proposed
  evidence: source-id#definition
```

### Problem patterns

Each pattern requires `id`, `name`, `intent`, `requires`, and `investigation`; it may include
`trigger_examples` and `competency_questions`. Seed ids are:

`authoritative-lookup`, `find-owner`, `compare-versions`, `reconstruct-decision`,
`explain-metric-change`, `trace-dependency`, `investigate-incident`, `find-precedent`,
`evaluate-proposal`, `policy-application`, `summarize-status`, and `identify-risk`.

Only retain patterns represented by real questions. Pattern prose is guidance, not deterministic
automation. A pattern can list the question ids it supports.

## Competency-question catalog

Keep `competency-questions.md` separate. Each record has an id in the form `CQ-<CATEGORY>-NNN`, a
question, intent, one or more domains, an expected problem pattern, required evidence,
authority expectation, and notes. A question must map to an existing domain and pattern. Categories
are:

| Category | Capability |
| --- | --- |
| A | authoritative lookup |
| B | ownership and responsibility |
| C | version and change |
| D | decision discovery and reconstruction |
| E | metric explanation and diagnosis |
| F | dependency and impact analysis |
| G | incident investigation |
| H | policy application |
| I | proposal evaluation |
| J | historical reconstruction |
| K | status and situation understanding |
| L | risk identification |
| M | cross-source reconciliation |
| N | vocabulary and semantic navigation |
| O | unknown and missing knowledge |

Use the catalog to expose missing concepts, routes, authority rules, evidence, and investigation
patterns. Add a schema element only when a real question or demonstrated query need requires it.

## Validation

On request, scan every schema file and the catalog, not only files linked from the index. Report
warnings without editing unless the user asks for fixes. Check:

- required identity fields, language code, unique ids, parseable YAML blocks, and valid relative links;
- every element's review status, and evidence or user confirmation for each confirmed field;
- defined targets for concepts and the 15 relationship fields;
- defined sources for every route, an access method for every canonical source, and valid locators;
- compatible authority rules, no deprecated preferred concept, and no conflicting metric definitions;
- pattern requirements, known evidence routes, and competency-question references;
- every question's id, domain, expected pattern, required evidence, and authority expectation;
- no credentials, restricted or confidential content, embeddings, chunk ids, scores, caches, search
  internals, generated summaries, unreviewed extracted entities, or model-specific prompt internals;
- every pattern is referenced: either a question's `expected_problem_pattern` names it or the
  pattern's `competency_questions` lists an existing question id. A pattern with neither is
  unreferenced and must be reported.
