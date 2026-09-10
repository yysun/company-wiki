# company-wiki / 企业文库

`company-wiki` is a portable Agent Skill for building a curated, document-native company wiki over a
cloud-drive collection. Ordinary documents are nodes. Native hyperlinks, bookmarks, and heading links
are edges. The agent reads the graph progressively—from a small home/map to guides, focused detail, and
original evidence—then answers with citations and explicit uncertainty.

The drive is the durable home of the wiki. This package does not impose folders, YAML records, a graph
database, an index, embeddings, source copies, or a connector. A flat document collection is valid.

## Package layout

- `SKILL.md` — concise routing, graph model, loading order, safety, and answer contract.
- `references/init.md` — initialize a home/map and the first reading paths.
- `references/query.md` — traverse the graph and investigate questions.
- `references/maintain.md` — propose, apply, and validate document/link changes.
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
not claim the wiki was saved.

Wiki documents are organization data. Keep them in the drive and preserve them when updating or replacing
this skill. Do not move them into the installed package or treat package updates as a migration of the
organization's knowledge.

## Use it

1. Install the skill where the host can load it.
2. Ask the agent to set up `company-wiki`, naming the source collections and wiki language. It asks only
   for whichever required answer is missing, checks drive capabilities, and creates a minimal linked graph.
3. Ask company questions normally. The agent starts at the home/map, follows labeled links, reads only
   relevant evidence, and cites the documents it actually opened.
4. Ask it to suggest or apply a wiki change, or to validate links and coverage. User corrections approve
   that specific change; other edits require approval. Validation is read-only by default.

For cloud-drive work, the skill reuses only cloud-drive/document skills, MCP tools, or agent plugins the host
app already provides. For non-drive sources it uses only the host's corresponding exposed repository, CLI,
or API tools. It never invents a connector, calls an undocumented provider API, or assumes a new integration.
It reports unreachable sources, missing link metadata, and permission limits instead of inventing facts or
building retrieval infrastructure.
