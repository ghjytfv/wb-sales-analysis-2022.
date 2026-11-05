# Wildberries Sales & Profitability Analysis (2022)

An analytical case study focused on marketplace sales performance, product-category profitability, monthly trends, data quality, and reconciliation of calculation logic.

> **Data privacy:** The source workbook contains transaction-level and product-level commercial information. It is intentionally excluded from this public portfolio. Charts use anonymized category labels and indexed values rather than exact commercial amounts.

## Project overview

The task was to build a consistent profitability view for calendar year 2022 from sales and product-cost data. The analysis covers **29,561 sales records**, **61 product categories**, and monthly activity from February through December 2022. No January sales were present in the source period.

## Key findings

- 29,561 sales records were included in the 2022 analysis.
- 61 product categories were evaluated.
- 9 categories had negative calculated profit.
- All in-scope sales rows matched a valid cost record using a normalized **SKU + size** key.
- Profitability was calculated as revenue minus logistics and product cost.

Exact monetary values, product names, and transaction-level records are withheld to protect the source business data.

## Tools and skills demonstrated

- **Microsoft Excel:** formula-based reporting and lookup/reconciliation logic.
- **Python:** `openpyxl`, data validation, key normalization, duplicate-key checks, aggregation, and independent recalculation.
- **Analytical methods:** exploratory analysis, profitability analysis, category ranking, monthly trend analysis, and reconciliation.

## Methodology

1. Filter sales by sale date to include calendar year 2022.
2. Normalize SKU and size fields by trimming whitespace and comparing case-insensitively.
3. Match each sale to the cost reference using the composite key **SKU + size**.
4. Calculate row-level profit: `revenue - logistics - product_cost`.
5. Aggregate revenue, logistics, cost, and profit by category and month.
6. Reconcile totals and flag categories with negative profit.

## Data-quality investigation

The source workbook's cached cost calculation results were inconsistent with valid SKU + size matches. Some valid matches returned zero cost in the original calculation sheet, which overstated profit in the original summary.

The portfolio analysis was independently recalculated from the source rows using the normalized composite key. All 29,561 in-scope sales rows matched valid cost records. Forty-two cost-reference rows contained `#DIV/0!` values, but none of those keys was used by the 2022 sales records.

A separate source-data correction documented in the workbook involved trimming trailing whitespace from one SKU. The public project does not include that SKU or its underlying transaction row.

## Visuals

### Category profitability (anonymized)

![Top category profit index](screenshots/category_profit_index.png)

### Monthly performance (indexed)

![Monthly revenue and profit trend](screenshots/monthly_trends_index.png)

The monthly chart is indexed to February = 100. Values show relative change against February, not absolute revenue or profit.

## Reproducibility

The original workbook is not distributed. If you have authorized access to the source file, install the dependency and run the script locally:

```bash
python -m pip install -r requirements.txt
python analysis.py "/path/to/source_workbook.xlsx"
```

The script prints aggregate metrics locally and does not export raw transactions. Its console output may still contain confidential aggregate financial figures; do not publish that output.

## Repository structure

```text
wb-sales-analysis-2022/
├── README.md
├── analysis.py
├── methodology.md
├── requirements.txt
├── data/
│   └── README.md
└── screenshots/
    ├── category_profit_index.png
    └── monthly_trends_index.png
```

## Limitations

- The source transaction-level dataset is not redistributed.
- Exact category names, product identifiers, and absolute monetary values are not published.
- The results describe the supplied 2022 dataset and should not be interpreted as current marketplace performance.

## Author's contribution

Prepared the analytical workbook, defined the profitability calculation, validated SKU + size matching logic, investigated inconsistent formula results, reconciled category and monthly aggregates, independently recalculated the results in Python, and prepared anonymized portfolio visuals.
