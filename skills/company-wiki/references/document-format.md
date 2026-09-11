# Document graph format

This is the document contract for 企业文库. It is guidance for people and agents, not a machine schema.
Use ordinary document prose, headings, lists, tables, and native links. Organization documents do not
need YAML, frontmatter, folders, generated ids, or sidecars.

## Nodes and disclosure levels

Each wiki document is a node in the cloud-drive graph. A useful node normally contains:

- a clear title;
- a one- or two-sentence summary of what the reader will learn;
- headings that expose the document's questions or claims;
- a short “read next” or “related documents” section; and
- links with a human-readable relationship label and a usable native target.

Use four reading levels:

0. **Home/map:** scope, how to start, major guides, source boundaries, and links to Level 1.
1. **Guide:** a domain or competency-question route with key terms, a short answer shape, and links to
   Level 2 detail and Level 3 evidence.
2. **Detail:** one focused concept, policy, decision, definition, metric, dependency, incident, risk, or
   proposal, with claims and their evidence links.
3. **Evidence:** the original cloud-drive document, repository view, or provider-native source record.

The home/map is small enough to read first. A guide should be useful without loading every detail node.
Detail is opened only when the question needs it. Evidence is read from the source system and is never
copied into the wiki.

## Edges and link labels

An edge is a native hyperlink, bookmark, or heading link. Preserve the target exactly as the host exposes
it: provider URL, document id, anchor, or repository locator. Preserve the visible label as well. If a
host cannot expose the target or anchor, say so rather than replacing it with a guessed path.

Prefer labels that tell the reader why to follow the link:

- `defined by` — meaning or terminology comes from the destination;
- `governed by` — a policy or rule controls the destination topic;
- `owned by` — responsibility is described at the destination;
- `depends on` / `affects` — an operational dependency or impact;
- `supersedes` / `superseded by` — a version or decision relationship;
- `evidence` / `source of truth` — the destination supports or authoritatively defines a claim;
- `see also` — useful related reading without a stronger claim;
- `open question` — unresolved evidence or a missing decision.

This vocabulary improves navigation but does not create required fields. A link with no meaningful label
is a weak edge. A label whose target cannot be opened is a broken edge. A relationship is not confirmed
merely because a document links to it; check the destination's wording and authority.

## Human-readable signals

When useful, put these signals near the opening summary as prose or a small table:

| Signal | Meaning |
|---|---|
| Type | guide, concept, policy, decision, metric, incident, risk, proposal, or source note |
| Status | proposed, current, superseded, draft, unresolved, or stale |
| Owner | named responsibility when a source supports it |
| Effective/review date | dates stated by the source or confirmed by the user |
| Language | the language used for this wiki node |
| Authority | approved, canonical, official, informal, historical, derived, or unknown |
| Source route | native link, document id, repository ref, or user-provided locator |

These are readable cues, not mandatory metadata. If a value is inferred, write `Proposed:` or explain the
inference in prose. A user correction may be recorded as `Confirmed by user:`. Do not silently promote a
proposal to official meaning.

## Sources and evidence

For each source family, the home or a guide may state its name, access type, exact user-provided locator,
what the locator is relative to, search/read capabilities, permission boundary, and authority rule. Keep
credentials and copied restricted content out of wiki documents.

Useful access descriptions include cloud-drive document search, native document open, provider bookmark,
repository read-only commands, a host skill, CLI, MCP, or API. Do not imply that a provider supports a
folder, backlink, heading-anchor, or write operation until the host demonstrates it.

Each important claim should link to the evidence actually read. For conflicts, link both documents and
state which one is current, why, or that the precedence remains unresolved. “Not found in the sources
searched” is a coverage statement, not proof that a thing does not exist.

## Question guides

Competency questions are maintained as a readable catalog or as sections in guides. A question entry may
use this shape:

```text
## Q-<CATEGORY>-<NUMBER> — <question>

Question: <the wording a person may ask>
Why it matters: <decision or user need>
Start at: <home or guide link>
Likely path: <labeled links to follow>
Expected evidence: <source types or documents to verify>
Answer shape: <fact, comparison, timeline, diagnosis, proposal, or gap report>
```

The labels above are plain text, not fields an agent must parse. Add a question or a new guide only when
a real question, repeated miss, or demonstrated retrieval failure justifies it. Keep the first reading
path short and link to deeper material instead of expanding the home document.

Use these category routes:

| Category | Route |
|---|---|
| A authoritative lookup | Find the current source-of-truth document and answer the requested fact. |
| B ownership | Follow `owned by` or responsibility links and verify the named owner in evidence. |
| C version/change | Follow dates and `supersedes` links; compare current and historical evidence. |
| D decision | Follow decision or rationale links and reconstruct the chosen option and its date. |
| E metric | Find the definition, formula, period, owner, and source before interpreting movement. |
| F dependency | Traverse `depends on` and `affects` links; separate direct from indirect impact. |
| G incident | Start at the incident guide, then follow timeline, symptoms, evidence, and unresolved causes. |
| H policy application | Read the current policy and apply only the conditions supported by its text. |
| I proposal | Separate an idea from an approved decision and identify evidence still needed. |
| J history | Reconstruct a dated sequence from current and historical documents. |
| K status | Report current state, owner, date, blockers, and missing confirmation. |
| L risk | Follow risk, control, dependency, and open-question links; distinguish known from suspected risk. |
| M reconciliation | Compare conflicting terms or claims, authority, scope, dates, and remaining uncertainty. |
| N vocabulary | Check guide definitions, aliases, and context; do not merge terms with different meanings. |
| O unknown/gap | Search the expected guides and source routes, report coverage, and state what is missing. |

## Validation checklist

Use this checklist through [Validate](validate.md). Scan every wiki document the host can enumerate, not only
documents linked from the home:

1. There is one identifiable home/map with a summary, scope, and links to guides.
2. The home → guide → detail → evidence path is present where the subject needs multiple levels.
3. Every important link has a preserved, reachable target and a useful label; report broken, weak, and
   ambiguous edges separately.
4. Every node has a summary, headings, and a next-reading path; stale or superseded material is labeled.
5. Claims have evidence links, source authority is explicit where known, and conflicts are visible.
6. Every restricted route respects current permissions; no credentials or copied restricted content exist.
7. Orphan nodes, duplicate titles, missing guides, and question categories without a route are reported.
8. Proposals and inferred meanings are visibly marked; user-confirmed corrections identify the confirmation.
9. No source document, repository, or embedded source instruction was modified or followed as an action.

Validation is always read-only. If the user asks for fixes too, finish and report validation first, then use
[Maintain](maintain.md) for proposals and approved edits. Use [Ingest](ingest.md) when a repair depends on
reconciling explicitly selected new evidence.
