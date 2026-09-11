# company-wiki / 企业文库

`company-wiki` is a portable Agent Skill for building a curated, document-native company wiki over a
cloud-drive collection. Ordinary documents are nodes. Native hyperlinks, bookmarks, and heading links
are edges. The agent reads the graph progressively—from a small home/map to guides, focused detail, and
original evidence—then answers with citations and explicit uncertainty.

The drive is the durable home of the wiki. This package does not impose folders, YAML records, a graph
database, a provider-side search/evidence index, embeddings, source copies, or a connector. The small local
Markdown registry is configuration only. A flat document collection is valid.

## Package layout

- `SKILL.md` — concise routing, graph model, loading order, safety, and answer contract.
- `references/init.md` — initialize a home/map and the first reading paths.
- `references/ingest.md` — reconcile explicitly selected new sources through an approved change plan.
- `references/registry.md` — select and safely persist user-level wiki configuration.
- `references/query.md` — traverse the graph and investigate questions.
- `references/maintain.md` — propose and apply corrections, repairs, and restructuring.
- `references/validate.md` — inspect graph health, source drift, gaps, and contradictions without writing.
- `references/document-format.md` — node, edge, disclosure, question-guide, and validation guidance.
- `../../examples/` — a flat illustrative graph, not organization content.

## Try the example

The entry document is [`company-wiki-home.md`](../../examples/sample-company/company-wiki-home.md).
Open it first, then follow the shortest relevant path:

`home/map → guide → focused detail → linked source`

For example, a workplace-policy question goes from the home to `people-guide.md`, then to
`vacation-policy-detail.md`; a customer-metric question goes through `customer-guide.md` to
`churn-rate-detail.md`. `authoritative-lookup-guide.md` explains which source wins when documents
disagree, and `question-guide.md` collects recurring question paths.

The Markdown files under `examples/sample-company/` are a local, flat-drive adapter for testing the
reading order and link graph. They are not a required filesystem layout and are not uploaded or copied
into a real wiki. In production, put equivalent ordinary documents in the chosen cloud drive and let
the host's existing cloud-drive/document skill, MCP tool, or agent plugin open them. For a local smoke
test, give the agent the whole example directory, tell it to start at `company-wiki-home.md`, and ask it
to answer using only documents reached from that entry point.

The installed skill contains no organization wiki. Init creates ordinary wiki documents in the user's
chosen writable cloud-drive collection: normally one home/map, a few guides, and only the focused detail
nodes needed by real questions. It links to original source documents instead of copying them. If the
host cannot create documents or preserve native link targets, the agent reports that limitation and does
not claim the wiki was saved. Init samples representative sources; it does not ingest every document or
create processed-source state.

## Lifecycle

`Init → Ingest → Query → Maintain → Validate`

Ingest is the explicit bridge between initialization and everyday use. The user selects one new source by
default, or supplies a finite batch. The agent reads it, compares it with relevant wiki nodes and evidence,
and presents the exact proposed edits. Source selection permits reading but not those edits; the agent writes
only after approval and revalidation. An unchanged source produces no edit or receipt. Validate is separately
read-only, while fixes route to Maintain.

This source-to-wiki reconciliation does not introduce centralized ingestion. There is no source copy,
embedding pipeline, provider-side index, processing ledger, mandatory log, watcher, or background sync.

Wiki documents are organization data. Keep them in the drive and preserve them when updating or replacing
this skill. Do not move them into the installed package or treat package updates as a migration of the
organization's knowledge.

## Shared local registry

Mutable configuration lives under `~/company-wiki`, with `index.md` as the single entry and linked profiles
under `wikis/`. The registry stores wiki and source locators, language, optional navigation inputs, and the
native home/map link. It stores no source copies, credentials, or evidence. The skill reads the index first,
follows only the selected contained profile, and never scans the directory.

Keep the versioned skill in this repository. Expose it to other same-user local Codex agents with
`~/.agents/skills/company-wiki` as a symlink to this `skills/company-wiki/` directory. The skill is not stored
under `~/company-wiki`. Local or remote agents that cannot read the user's home directory cannot use this
registry and must report that limitation.

## Use it

1. Install the skill where the host can load it.
2. Ask the agent to set up `company-wiki` with four required inputs: wiki name, original-material location
   and scope, writable wiki destination, and wiki language. It asks once for whichever required inputs are
   missing.
   You may also provide four optional inputs: key domains, owners, core/source-of-truth documents, and an
   initial navigation outline. Optional inputs shape the first reading paths but never block creation.
   The outline is navigation, not a required folder tree.
   The agent extracts values already clear from natural language and asks only about genuine gaps. For
   example, “创建一个财务文库” already supplies the name, finance scope, and Chinese language; the agent can
   ask only for the unknown original-material location and writable destination. A subject never authorizes
   a whole-drive search: source discovery stays inside locations the user explicitly specifies.
3. Ingest a new or changed source by selecting its exact native target. Review the proposed wiki changes,
   then approve them if they correctly preserve authority, conflicts, and evidence links.
4. Ask company questions normally. The agent starts at the home/map, follows labeled links, reads only
   relevant evidence, and cites the documents it actually opened.
5. Ask it to maintain corrections or structure, or to validate links and coverage. User corrections approve
   that specific change; other maintenance edits require approval. Validation is always read-only.

For cloud-drive work, the skill reuses only cloud-drive/document skills, MCP tools, or agent plugins the host
app already provides. For non-drive sources it uses only the host's corresponding exposed repository, CLI,
or API tools. It never invents a connector, calls an undocumented provider API, or assumes a new integration.
It reports unreachable sources, missing link metadata, and permission limits instead of inventing facts or
building retrieval infrastructure.
