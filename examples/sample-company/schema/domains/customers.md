> Illustrative example only; this is not an organization's schema.

# Customers

```yaml
id: customers
name: Customers
description: Customer lifecycle, retention, and commercial definitions.
key_concepts: [active-customer, customer-churn, churn-rate]
source_routes: [product-drive]
review_status: confirmed
evidence: product-drive#customer-domain
```

## Customer concepts

```yaml
- id: customer-churn
  name: Customer Churn
  aliases: [churn, customer attrition]
  definition: A customer relationship ending during the measurement period.
  measured_by: [churn-rate]
  review_status: confirmed
  evidence: product-drive#customer-definitions
- id: churn-rate
  name: Churn Rate
  type: metric
  definition: Customers lost during the period divided by eligible customers at its start.
  numerator: customers_lost
  denominator: eligible_customers_start
  review_status: confirmed
  evidence: product-drive#metric-catalog
```

## Vocabulary

```yaml
- preferred: active-customer
  aliases: [active account]
  maps_to: active-customer
  review_status: confirmed
  evidence: product-drive#customer-definitions
```
