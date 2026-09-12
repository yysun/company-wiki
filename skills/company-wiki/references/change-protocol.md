# Durable change protocol

Init, Bootstrap, Curate, Add Source, Maintain, and promotion share this protocol. It applies to provider pages
and registration; original sources are never written. Apply the [publication boundary](publication.md) first.

1. Propose exact scope, destination, affected targets, evidence and versions, conflicts, preserved organization,
   ordered writes, audience result, and continuing-protection coverage. Include per-target version conditions,
   create/retry semantics, exact lookup targets, and supported operation keys. Create/verify dependencies before
   exposing links to them; this ordering reduces partial graph inconsistency but does not hide native search results.
   Every intermediate write must satisfy the publication boundary. A source selection or correction request is not
   approval of edits.
2. Bind approval to the authenticated principal, scope, destination, targets, proposal, evidence versions, and
   audience/protection result, target versions, and operation parameters. Reuse an operation key only for the same
   approved intent; changed content is a new operation. Approval in the current session need not be requested again
   when it already covers the concrete unchanged action.
3. Immediately before apply, recheck identity; exact write/govern capability; source/destination audiences;
   continuing protection; source and target versions/content/links; and target preflight. Any material change,
   unavailable result, or failed preflight invalidates approval and writes nothing before apply. If discovered
   between writes, stop further writes and reconcile partial state. A content ETag does not prove unchanged ACLs.
4. Use provider-enforced conditional updates tied to the approved version, or a verified equivalent exclusive-write
   mechanism spanning recheck and write. Rereading alone does not prevent a concurrent overwrite. Creates require
   provider-supported idempotency or conditional create-if-absent at an exact target with reconcilable outcomes.
   Unsupported protection yields a proposal, not a blind overwrite/create. Recheck per-target authorization before
   each write; source/destination continuing protection must be enforced by the provider during the write as well.
5. Write in order, verify each result, and stop at first failure or unknown outcome. Verify identity, exact target,
   resulting version/content, and protection before counting success. Do not roll back or continue after a partial
   write. A timeout or missing response is unknown, not evidence that the provider made no change.

## Reconcile and recover

Report confirmed successful, confirmed failed, unknown, and unattempted work, graph inconsistency, and a
remaining-work-only proposal. Keep diagnostics within the requester's disclosure boundary. Reconcile only exact
approved resources and native operation keys; do not scan another collection or the registry to find missing work.
If an outcome remains unknown or the original operation identity is lost, stop and report that limitation; do not
retry a create, delete a possible result, or invent an idempotency key. A supported original key may be replayed only
after its semantics and unchanged authorization/intent are verified; it must not duplicate the resource.

On recovery, reread current source/target state, preserve successful and concurrent edits, and identify only work
still needed. Drift invalidates old approval; obtain approval for the revised concrete proposal. An unchanged
remaining action already concretely authorized in the session needs no redundant approval. Native idempotency does
not waive authorization checks, and a completed operation must not overwrite a later edit when replayed. Cleanup
is an explicit version-protected Maintain change, never an automatic destructive rollback.

For source-derived shared writes, the destination audience must be a subset of every evidence audience and the
writer must have authenticated governance capability. Apply-time rereads count against bounds. Setup preflights
registry feasibility before creating provider pages, then writes the completed profile before its index link using
the [registration protocol](registry.md). Preserve successful pages and pre-existing registry bytes on failure.
V1 has no recovery ledger; if native exact lookup/session state cannot establish a result after a crash, report
unknown rather than promising automatic recovery.
