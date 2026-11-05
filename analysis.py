"""Recalculate the 2022 sales profitability metrics from the source workbook.

The source workbook is intentionally not distributed. Run this script locally:
    python analysis.py "/path/to/source_workbook.xlsx"

The script prints aggregate metrics only. It does not export transaction rows,
SKUs, product names, or category-level financial values.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl


def normalize(value: object) -> str:
    """Normalize lookup fields without changing their semantic content."""
    return "" if value is None else str(value).strip().casefold()


def load_cost_lookup(workbook):
    costs: dict[tuple[str, str], float] = {}
    error_keys: set[tuple[str, str]] = set()
    duplicate_keys: set[tuple[str, str]] = set()

    for row in workbook["Себестоимость"].iter_rows(min_row=3, values_only=True):
        sku = row[0]
        if sku is None:
            continue
        key = (normalize(sku), normalize(row[1]))
        raw_cost = row[3]
        if isinstance(raw_cost, str) and raw_cost.startswith("#"):
            error_keys.add(key)
            continue
        if key in costs:
            duplicate_keys.add(key)
        else:
            costs[key] = float(raw_cost or 0)

    if duplicate_keys:
        raise ValueError(
            f"Duplicate valid SKU + size keys in cost reference: {len(duplicate_keys)}"
        )
    return costs, error_keys


def analyze(path: Path) -> dict[str, object]:
    workbook = openpyxl.load_workbook(path, data_only=True, read_only=True)
    required_sheets = {"Продажи", "Себестоимость"}
    if not required_sheets.issubset(workbook.sheetnames):
        raise ValueError(f"Workbook must contain sheets: {sorted(required_sheets)}")

    costs, error_keys = load_cost_lookup(workbook)
    sales_by_year = Counter()
    category_profit = defaultdict(float)
    monthly = defaultdict(lambda: {"revenue": 0.0, "logistics": 0.0, "cost": 0.0})
    totals = {"revenue": 0.0, "logistics": 0.0, "cost": 0.0}
    included_rows = 0
    unmatched = 0
    error_matches = 0

    for row in workbook["Продажи"].iter_rows(min_row=3, values_only=True):
        sale_date = row[4]
        if sale_date is None:
            continue
        sales_by_year[sale_date.year] += 1
        if sale_date.year != 2022:
            continue

        included_rows += 1
        key = (normalize(row[5]), normalize(row[6]))
        if key not in costs:
            unmatched += 1
            if key in error_keys:
                error_matches += 1
            continue

        revenue = float(row[2] or 0)
        logistics = float(row[7] or 0)
        product_cost = costs[key]
        profit = revenue - logistics - product_cost
        category_profit[str(row[1] or "Unknown")] += profit

        month = sale_date.month
        monthly[month]["revenue"] += revenue
        monthly[month]["logistics"] += logistics
        monthly[month]["cost"] += product_cost
        totals["revenue"] += revenue
        totals["logistics"] += logistics
        totals["cost"] += product_cost

    if unmatched:
        raise ValueError(
            f"{unmatched} sales rows could not be matched; "
            f"{error_matches} matched keys have cost formula errors."
        )

    profit = totals["revenue"] - totals["logistics"] - totals["cost"]
    return {
        "sales_by_year": dict(sales_by_year),
        "sales_rows_2022": included_rows,
        "cost_lookup_keys": len(costs),
        "cost_error_keys": len(error_keys),
        "categories": len(category_profit),
        "loss_making_categories": sum(value < 0 for value in category_profit.values()),
        "months_with_sales": len(monthly),
        "revenue": totals["revenue"],
        "logistics": totals["logistics"],
        "product_cost": totals["cost"],
        "profit": profit,
        "margin_pct": profit / totals["revenue"] * 100 if totals["revenue"] else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path, help="Path to the original Excel workbook")
    args = parser.parse_args()
    if not args.workbook.is_file():
        parser.error(f"File not found: {args.workbook}")

    result = analyze(args.workbook)
    print("Validation completed. The following figures are local/private outputs:")
    for key, value in result.items():
        if isinstance(value, float):
            print(f"{key}: {value:,.2f}")
        else:
            print(f"{key}: {value}")
    print("\nDo not publish this console output if the source data is confidential.")


if __name__ == "__main__":
    main()
