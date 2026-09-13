# Publication and disclosure boundary

Read this after registry selection, before discovery, wiki reads, generation, or durable changes. These are
capability requirements on the host/provider, not permission claims the model can establish from prose.

## Capability levels

Use the host's existing, documented plugin, MCP, CLI, or API operations. Determine support for the requested
operation from the exposed tool contract and current authorization; the integration mechanism alone guarantees
neither access control nor safe writes. Evaluate source and wiki-destination capabilities separately, even when
they use the same provider. Do not add a connector, permission service, version store, or persistent capability cache.

| Level | Required capabilities | Supported result |
|---|---|---|
| Read and answer | Scoped discovery when needed, current requester-authorized reads, and usable source identifiers or links for citations | Query and Explore; the read-only Validate checks the interface can establish |
| Draft changes | Authorized reads of the selected evidence and any wiki content needed for concrete edits; a response audience authorized for that evidence | A transient proposal in the current conversation, with publication blockers stated; no wiki or registry writes |
| Publish changes | Read capabilities plus exact-destination write/govern authority, verified current audience containment, safe permissions from creation, and the protected create/update operations required by the plan | Approved writes through the [change protocol](change-protocol.md), including protected registration when needed |

For ordinary reads, a successful operation authenticated as the requesting user can establish access; separate
ACL enumeration is unnecessary. A broader bot or service account needs a host/provider-enforced requester check
before returning metadata or content to the model. Missing requester authorization blocks that evidence at every
level. Preserve the additional pre-read gates below for known unsafe legacy content and explicit continuous inheritance.

Source revision metadata is optional for Query and Explore: read current evidence in the same operation and report
material comparison limits. Destination write permissions, audience enumeration, and conditional-write support
are not prerequisites for ordinary read-only answers. Validate reports checks it cannot perform as inspection
limits; missing ACL visibility alone does not establish a leak or invalidate otherwise authorized evidence.

If publication requirements are unavailable, continue only the authorized reads and transient drafting useful to
the request. State the specific missing capability and that nothing was saved; do not ask for approval to bypass
it or imply that user confirmation supplies provider enforcement. A draft for the requester is not cleared for
the intended wiki audience. Until destination disclosure is verified, do not generate an artifact for that audience
or instruct the user to copy the draft there. If existing target content cannot safely be read, provide an outline
or limitation instead of inventing an exact replacement. Follow the clean-generation rules below before preparing
shared content.

Capability fallback preserves each lifecycle's registry, source-selection, and read bounds. A draft does not create
a registration or turn Init into a completed wiki. Without a profile, direct-source Query/Explore still needs an
exact user-supplied source locator under [Registry](registry.md). Bootstrap still uses only the selected index
reference; it cannot discover or sample source bodies.

For publication, check the operations actually in the plan: protected creates and protected updates are separate
capabilities. Reading a source revision does not prove that the destination supports conditional writes. Source
timestamps and content hashes cannot replace provider-enforced destination version conditions or an equivalent
exclusive-write mechanism. The skill delegates permission and concurrency enforcement to the host/provider.

## Current authorization and provider-managed access

For publication, default to provider-managed wiki access: the cloud provider enforces the destination's own
permissions. Verify authenticated source access, exact-destination write/govern capability, and current source/destination audiences.
Respect applicable confidentiality and publication restrictions. Each required check returns verified, denied,
or unavailable; denied or unavailable current authorization blocks the affected publication. A scope/owner label,
user assurance, local file access, or successful write probe is not provider proof of disclosure authority.
Broader or unknown Personal audiences follow the shared-write rules.

At publication and apply-time revalidation, require for every source-derived page and exposed field:

`destination audience ⊆ intersection of all contributing evidence audiences`

Contributing evidence includes inputs to titles, aliases, summaries, links, relationships, backlinks, provenance,
and interpretations, including transitive inputs through other wiki pages; it is not just the final citation list.
Resolve evidence only inside registered source bounds. Missing lineage or unavailable audience proof blocks that
material; do not search outside the profile or trust a wiki's claim that it is safe.

The provider must enforce the approved wiki audience from creation, including exposed titles and previews;
do not create broadly visible content and tighten it afterward. Current permission evidence can support ordinary
publication when the other requirements pass. Missing proof of future source-to-wiki permission propagation alone
must not block Init, Bootstrap, Add Source, Curate, or Maintain, or force an otherwise authorized result into a draft.

The wiki's permissions govern the published document. V1 supplies no automatic source-to-wiki ACL synchronization
and cannot recall already disclosed/downloaded bytes. State this limitation when relevant; do not promise that a
source revocation changes existing wiki access. Validate can report later drift and Maintain can propose repairs.
Absence of automatic inheritance alone does not establish unsafe exposure or require a new approval.

## Explicit continuous source inheritance

Require provider-enforced continuing protection only when the user or applicable governing policy explicitly
requires the destination's derived content to remain subject to future source-permission changes. Check the selected
destination's governing-capability route and preserve any existing explicit requirement through proposals, follow-ups,
and retries. A missing profile field never cancels a known requirement; registry prose is not proof of enforcement.

For this access model, source ACL changes, destination widening, group changes, and inheritance overrides must not
expose derived bytes to a broader audience. Verify every native exposure surface the deployment offers, including
content, titles/search previews, history, and export endpoints. A current ACL snapshot, same-folder placement,
content version, or scheduled check does not prove continuing protection. The guarantee must apply from creation
onward, including Personal copies and Bootstrap's index reference when that requirement applies.

If explicitly required protection is denied or unavailable, block the affected publication and offer only currently
authorized source queries or a transient draft visible to an authorized requester. Do not silently switch to the
default model or substitute a private local export. Prompts, approval, and local tests cannot supply provider
enforcement. A future asynchronous sync feature would need its own revocation-delay and failure contract.

Private local originals and synthetic fixtures may use effective local identity/access and a verified private
destination without claiming enterprise governance or cloud revocation. This exception does not cover synced or
exported provider-governed evidence, nor Team/Company writes. Keep the same registry, source bounds, lifecycle
prerequisites, and approved-change protocol. Unknown privacy is not private scope.

## Before generation and reading

Authorize source content and metadata for the requesting principal before they enter the model. For a shared
artifact, select only evidence cleared for the destination before generating it. If prior context contains
excluded evidence, regenerate in a host-supported clean context containing only authorized inputs and the exact
bounded task. If isolation is unavailable, refuse shared generation; removing tokens/citations from a contaminated
draft is not sanitization. Independently supported material may be generated from clean authorized evidence.

For ordinary wiki reads, use the provider's current access controls for the page and its metadata; lack of automatic
source inheritance alone is not a reason to bypass an authorized wiki. Recheck original evidence access before
reusing factual claims; a readable wiki is not a substitute for same-operation source evidence.

For known unsafe legacy content or a destination with explicit continuous source inheritance, establish the required
disclosure safety through protected metadata or a provider-enforced read boundary before titles, routes, or content
enter the model. Do not load unsafe bytes and then ask the model to ignore them. If the boundary cannot be established
without exposing those bytes, skip the page and use bounded direct-source search when separately registered. Do not
invent lineage or infer source scope from an inaccessible page. This pre-read gate is not an extra wiki routing phase.

Split mixed-audience content into separately protected pages when useful. A broader page must not name, link, count,
alias, or infer the existence of a narrower page. Apply the same rule to proposals, error messages, recovery reports,
and visible activity: an authorized operator's diagnostics are not automatically safe for a shared destination.

## Legacy cleanup

Validate is read-only and reports unsafe exposure without repeating restricted metadata. Maintain may propose an
exact disclosure-reducing replacement/removal of exposed fields within the registered wiki destination. Require
authenticated write/govern authority, version protection, and approval; use only destination-safe replacement text.
Do not preserve a restricted title, backlink, or `Merged into`/`Retired` reference. This is cleanup, not authorization
to republish the old evidence; no source write or automatic ACL change is allowed. If native history, search previews,
or exports still expose old bytes, report unresolved provider exposure and the needed provider-admin repair. Never
claim that editing the current page erased its history or recalled copies.
