> Illustrative example only; this is not an organization's wiki.

# Sample company — company wiki home

This home document is the Level 0 entry point for a small, flat cloud-drive collection. Its compact outline is
routing context: choose a guide and original evidence route together before reading more.

## How to use this example

Treat the Markdown files in this directory as one flat document collection. The intended reading path is:

`this routing context → one route decision → linked source`

For a local test, open this file first and ask the agent to answer from documents reachable from it.
The synthetic originals are in the separate `../sample-company-sources/` collection. Read original
evidence before stating a company fact. These example files and sources are read-only during a query.
In a real deployment, the equivalent documents live in the chosen provider and are opened through the
host's existing document/search tools.

## Start here

- [People guide](people-guide.md) — workplace rules and the `vacation-policy` reading path.
- [Customer guide](customer-guide.md) — customer lifecycle and the `customer-churn` metrics path.
- [Authoritative lookup guide](authoritative-lookup-guide.md) — how to decide which source answers a fact.
- [Question guide](question-guide.md) — recurring questions and their shortest reading paths.

## Source boundaries

- **HR collection (`hr-wecom`):** [approved annual leave policy](../sample-company-sources/hr-policy-current.md),
  [previous policy](../sample-company-sources/hr-policy-previous.md), and
  [unapproved proposal](../sample-company-sources/hr-policy-draft.md).
- **Product collection (`product-drive`):** [customer definitions](../sample-company-sources/customer-definitions.md),
  [metric rules](../sample-company-sources/product-metric.md),
  [retention review](../sample-company-sources/customer-quarterly-review.md), and
  [outreach discussion](../sample-company-sources/customer-outreach-notes.md).

The collection labels illustrate provider routes; this local demo needs no provider connection.
The exact local source boundary is `examples/sample-company-sources/` only. A real wiki records only
what the host exposes and preserves the native document targets it returns. The wiki links to sources;
it does not copy them.

## Reading rules

Read this summary and guide headings as one compact initial routing phase, then retrieve original evidence.
If originals reveal a concrete authority, alias, or exception gap, one targeted wiki follow-up may resolve it
within the existing profile, traversal, and retrieval bounds. Tree placement is
navigation; cross-links are discovery and do not prove a relationship. Treat a proposed relationship as an
inference until evidence or user confirmation supports it. Surface conflicts instead of hiding them.

## Authority

Current approved or canonical source documents take precedence over drafts, informal notes, and historical
documents when their scope and date support that conclusion. When precedence is not explicit, report the
conflict as unresolved.
