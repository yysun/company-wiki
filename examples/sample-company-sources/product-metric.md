# Monthly customer churn measurement

Synthetic original source for the sample company.

Status: Canonical
Effective: 2026-06-01
Owner: Revenue Analytics
Definitions: [Customer lifecycle definitions](customer-definitions.md)

## Formula and population

Monthly customer churn rate equals eligible customers lost during the calendar month divided by
eligible customers at the start of that month, multiplied by 100 percent.

The starting population includes customers with a paid subscription at the start of the month.
Exclude trial-only accounts, internal test accounts, and customers first acquired during the month.
The numerator counts members of this starting population whose last paid subscription ends during
the month. Customers acquired during the month do not enter either the numerator or denominator.

## Comparison

Use the same calendar period definition and exclusions when comparing rates. A higher rate alone
does not establish a cause or show that the number of customers lost increased.
