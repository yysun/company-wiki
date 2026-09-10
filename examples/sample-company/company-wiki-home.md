> Illustrative example only; this is not an organization's wiki.

# Sample company — company wiki home

This home document is the Level 0 entry point for a small, flat cloud-drive collection. Start here, then
follow only the guide that matches the question.

## How to use this example

Treat the Markdown files in this directory as one flat document collection. The intended reading path is:

`this home → one guide → one focused detail document → the linked source`

For a local test, open this file first and ask the agent to answer from documents reachable from it. Do not
start with a detail document: the point of the example is to exercise progressive disclosure and ordinary
document links. In a real deployment, the equivalent documents live in the chosen cloud drive and are
opened through the host's existing cloud-drive/document skill, MCP tool, or agent plugin.

## Start here

- [People guide](people-guide.md) — workplace rules and the `vacation-policy` reading path.
- [Customer guide](customer-guide.md) — customer lifecycle and the `customer-churn` metrics path.
- [Authoritative lookup guide](authoritative-lookup-guide.md) — how to decide which source answers a fact.
- [Question guide](question-guide.md) — recurring questions and their shortest reading paths.

## Source boundaries

- **HR collection (`hr-wecom`):** open through the host app's already-available WeCom document skill,
  MCP tool, or agent plugin. It is the source for workplace policy and people definitions.
- **Product collection (`product-drive`):** open through the host app's already-available Google Drive
  document skill, MCP tool, or agent plugin. It is the source for customer and product definitions.

These are illustrative provider capabilities. A real wiki records only what the host exposes and preserves
the native document targets it returns. The wiki links to sources; it does not copy them.

## Reading rules

Read this summary and the guide headings first. A guide points to focused detail; focused detail points to
the source of truth. Treat a proposed relationship as an inference until evidence or a user confirmation
supports it. Surface conflicts instead of hiding them.

## Authority

Current approved or canonical source documents take precedence over drafts, informal notes, and historical
documents when their scope and date support that conclusion. When precedence is not explicit, report the
conflict as unresolved.
