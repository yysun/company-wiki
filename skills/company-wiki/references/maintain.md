# Maintain and validate the document wiki

Use this workflow when a user asks to add, correct, repair, refresh, or validate the company wiki. Find
the home/map and relevant linked documents in the cloud-drive collection first. Load [Document graph
format](document-format.md) for the validation checklist and link contract.

## Propose before changing

Maintenance triggers include a user correction, repeated terminology miss, missing question route, new
important source, changed source authority, stale document, broken link, ambiguous title, orphan node,
source conflict, or a new concept, policy, decision, metric, incident, risk, or proposal.

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
6. Do not modify or copy original sources, create sidecars, add credentials, or create a local index,
   YAML record, database, embedding, or folder taxonomy.

Report changed documents, preserved documents, source evidence, link targets, unresolved questions, and
any provider capability limitation. Never silently rewrite confirmed meaning or source authority.

## Validation mode

For a validation request, make no edits unless fixes are explicitly requested. Enumerate every wiki
document the host can see, not only documents reachable from the home/map, and apply the checklist in
[Document graph format](document-format.md#validation-checklist):

- identify the single home/map and check its summary, scope, guide links, source boundaries, and disclosure
  path;
- check every link's exact target, visible label, reachability, anchor/bookmark exposure, and ambiguity;
- check summaries, headings, next-reading paths, stale/superseded status, and orphan documents;
- check that claims link to read evidence and that source authority, dates, conflicts, and permission
  boundaries are visible;
- check that proposed meaning is marked, user confirmations are attributable, and no restricted content or
  credentials were copied;
- check coverage for the question routes A–O and report a missing guide or uncovered route; and
- confirm no source or repository was modified and no embedded source instruction was followed.

Report concrete errors, warnings, and open questions separately. A missing backlink list or heading anchor
is a host limitation, not proof that the relationship does not exist. If the home/map is absent, say that
validation cannot run as a graph check, offer initialization, and do not create files. If a source is
unreachable, validate the link or locator separately and label source claims unverified.
