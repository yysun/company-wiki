# Validate

Apply the read-only capability level and pre-read rules in [Publication](publication.md) before exposing metadata
or reading wiki bytes. Missing write tools do not block inspection. Missing revision or audience metadata limits
the checks that can be completed; report those limits without treating them as evidence of drift or leakage.
Validate independently enumerates the safely visible selected-scope taxonomy and its bounded typed-link overlay. It is
read-only: never edit the wiki, registry, or original sources. Report broken/inaccessible evidence, taxonomy aliases
without usable source routes, version drift, stale summaries, missing provenance, orphans, duplicates/aliases,
contradictions, superseded knowledge, suspicious relationships, permission leakage, important gaps, missing primary
parents, typed-link-only nodes, and routing-outline/tree drift.

Check the [page timestamps](document-format.md#page-timestamps): report missing fields, malformed or timezone-less
timestamps, and full-page evidence-check claims unsupported by the available provenance. A recent `Updated` value
does not establish fresh evidence. Report `Unknown` or `Not fully checked` as provenance limits, not malformed dates;
do not change either field during validation.

Recheck current requester access before using original evidence. For audience-containment inspection, use available
provider authorization metadata and report unavailable audience proof as an inspection limit; ordinary authorized
reads do not require a separate ACL inventory. Check continuing protection only for explicit continuous-inheritance
requirements. Report current mismatches, unknown lineage or required
protection, and unsafe legacy exposure without quoting restricted titles, routes, or content. Distinguish these
findings from the default model's lack of automatic ACL synchronization, which alone is not evidence of leakage
or grounds to invalidate an otherwise authorized wiki.
Use protected metadata and bounded authorized reads; if these are unavailable, report the inspection limit instead
of reading unsafe pages. Offer repairs through Maintain or Curate, never silently repair them. A current-page edit
does not establish that native history/previews are safe or that previously downloaded bytes were recalled.
