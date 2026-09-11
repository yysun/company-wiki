# Durable change protocol

Init, Bootstrap, Curate, Add Source, Maintain, and promotion share this protocol. It applies to provider pages
and registration; original sources are never written.

1. Propose exact scope, destination, affected targets, evidence and versions, conflicts, preserved organization,
   ordered writes, and audience result. A source selection or correction request is not approval of edits.
2. Bind approval to the authenticated principal, scope, destination, targets, proposal, evidence versions, and
   audience result.
3. Immediately before apply, recheck identity; exact write/govern capability; source/destination audiences;
   source and target versions/content/links; and target preflight. Any material change, unavailable result, or
   failed preflight invalidates approval and writes nothing.
4. Write in order, verify each result, and stop at first failure. Do not roll back or continue after a partial
   write. Report successful, failed, unattempted work and a remaining-work-only proposal.

For source-derived shared writes, the destination audience must be a subset of every evidence audience and the
writer must have authenticated governance capability. Apply-time rereads count against bounds. Setup creates
provider pages first, then profile and index link; preserve pages and prior registry bytes if registration fails.
