# Methodology and validation notes

## Scope

- Reporting period: 1 January–31 December 2022, based on sale date.
- Included sales records: 29,561.
- Product categories: 61.
- Monthly activity: February–December 2022; no January sales were present.

## Source fields and calculations

| Concept | Source field | Treatment |
|---|---|---|
| Sale date | Sale date | Used to filter the reporting period and derive month |
| Revenue | Sale price | Summed at transaction level |
| Logistics | Average logistics cost in month of sale | Summed at transaction level |
| Product cost | Average unit cost | Matched by SKU + size |
| Profit | Derived | Revenue - logistics - product cost |

## Matching and cleaning

- SKU and size form a composite lookup key.
- Leading and trailing whitespace is removed.
- Matching is case-insensitive.
- Blank sizes are treated as blank values.
- All 29,561 in-scope sales records matched valid cost-reference records.
- 42 cost-reference records had calculation errors; none of those keys occurred in the in-scope sales records.
- The Python script checks for duplicate valid SKU + size keys and stops if any are found.

## Reconciliation

The source workbook's stored cost-formula results did not consistently reflect valid SKU + size matches. The analysis was independently recomputed from the source records before preparing the portfolio summary. Category and monthly totals were reconciled using the same row-level calculation.

## Confidentiality

Raw sales rows, exact product names, SKUs, and absolute financial values are not included in this repository. Public charts use anonymized category labels and indexed values. The local analysis script reads the original workbook but does not export transaction-level data.
