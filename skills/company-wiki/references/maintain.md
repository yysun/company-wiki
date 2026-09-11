# Maintain the document wiki

Use this workflow when a user asks to correct, repair, refresh, or restructure the company wiki. Select a
profile through [Registry](registry.md), follow its exact home/map link, and open relevant linked documents.
Load [Document graph format](document-format.md) for the node and link contract. When the request centers on
processing explicitly selected new evidence, use [Ingest](ingest.md). For a read-only graph-health check, use
[Validate](validate.md).

If the registry or selected profile is missing or unsafe, follow [Registry](registry.md)'s Maintenance
fallback and do not scan the registry directory. Maintenance of wiki documents does not authorize registry
changes; update a profile only when the user explicitly changes its configuration.

## Propose before changing

Maintenance triggers include a user correction, repeated terminology miss, missing question route, stale
wiki document, broken link, ambiguous title, orphan node, or requested graph restructuring. A new source,
changed source authority, or source conflict discovered while processing selected evidence is an Ingest
trigger, though an approved Ingest recovery proposal may hand a later structural repair to Maintain.

Before editing, state a small proposal containing:

- the document or link to add, repair, or change;
- the trigger and the evidence or user correction;
- the guide, detail node, or question categories affected;
- the exact readable change and any source link that will be preserved; and
- what will remain unchanged.

A user correction is approval for that correction. Other changes require explicit approval. A request to
“suggest improvements” is not approval to apply them.

## Apply the smallest edit

After approval:

1. Edit only the relevant wiki document or create the one missing node needed by the question.
2. Keep the opening summary, headings, and next-reading path accurate.
3. Preserve native link labels and exact targets. Repair a target only when the source or user supplies
   the correct destination; do not guess from a filename or folder.
4. Mark unsupported inferences as proposed and user-confirmed corrections as confirmed by the user.
5. Update a human-readable review date only when the change warrants it and report the date.
6. Do not modify or copy original sources, create sidecars, add credentials, or create a local search/evidence
   index, YAML record, database, embedding, or folder taxonomy. The user registry is configuration, not such
   an index.

Report changed documents, preserved documents, source evidence, link targets, unresolved questions, and
any provider capability limitation. Never silently rewrite confirmed meaning or source authority.
