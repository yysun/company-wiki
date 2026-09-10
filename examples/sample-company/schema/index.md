> Illustrative example only; this is not an organization's schema.

---
schema:
  id: sample-company
  name: Sample Company Knowledge Schema
  version: 0.1
  description: Small example of an evidence-backed company knowledge map.
  default_language: en
  updated: 2026-09-10
  review_status: confirmed
  confirmed_by: user
---

# Sample company knowledge schema

## Domains

- [People](domains/people.md)
- [Customers](domains/customers.md)

## Primary sources

```yaml
- id: hr-wecom
  name: HR WeCom
  access:
    type: skill
    capability: wecom-doc
  routes: [{label: policies, path: People/Policies}]
  authority: {default: canonical}
  review_status: confirmed
  evidence: user-supplied source map
- id: product-drive
  name: Product Google Drive
  access:
    type: skill
    capability: google-drive
  routes: [{label: decisions, path: Product/Decisions}]
  authority: {default: approved}
  review_status: confirmed
  evidence: user-supplied source map
```

## Vocabulary and definitions

```yaml
- preferred: GA
  aliases: [General Availability]
  review_status: confirmed
  evidence: product-drive#glossary
- id: active-customer
  name: Active Customer
  definition: A customer with an active paid subscription on the evaluation date.
  review_status: confirmed
  evidence: product-drive#definitions
```

## Authority

```yaml
- id: current-policy
  when: A current policy question has competing sources.
  prefer: [system_of_record, canonical, approved, working, historical]
  behavior: Surface unresolved conflict.
  review_status: confirmed
  confirmed_by: user
```

## Problem patterns

- [Authoritative lookup](problem-patterns/authoritative-lookup.md)

## Deeper resources

See the domain files and the [competency-question catalog](../competency-questions.md).
