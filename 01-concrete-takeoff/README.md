# 01 · Concrete & Foundation Rebar Take-off (public bid documents)

**Project:** Liberty City Park Restroom & Concession Building — City of Liberty, TX (public bid 2026-01).
**Scope:** slab on grade, grade beams, continuous footings, thickened slabs (F3, F9, F10) and foundation reinforcing.
**Sheets used:** S2 (foundation plan) and S3 (foundation sections). Quantities only, no pricing.

## 1. Summary

| CSI | Item | Net qty | Waste | Order qty |
|---|---|---:|---:|---:|
| 03 30 00 | Cast-in-place concrete, total | 80.0 CY | 5 % | 84 CY |
| | of which slab on grade 5" | 27.4 CY | 5 % | 29 CY |
| | of which foundations (beams, footings, F3/F9/F10) | 52.5 CY | 5 % | 56 CY |
| 03 20 00 | Reinforcing steel Gr. 60, foundations and slab | 5,375 LB | 5 % | 5,644 LB |
| 03 30 00 | Slab on grade area (vapor barrier, finish) | 1,779 SF | 10 % | 1,957 SF |

## 2. How the workbook is built

`Takeoff_Concrete_Foundations.xlsx` follows the same order on every memo I prepare:

1. **Summary on top**: what the reader needs first, with net and order quantities.
2. **Input data (yellow cells)**: every dimension read from the drawings, with the sheet and how it was measured.
3. **Calculation**: every quantity is an Excel formula over the input block, so changing one dimension updates the whole estimate.
4. **Open items (RFIs)**: conflicts between sheets, written as the question I would send to the architect or engineer.
5. **Notes / exclusions**: what is deliberately left out, to avoid double counting with other packages.

The `SUPPORT` sheet keeps the drawing clips used for each measurement, so a reviewer can trace any number back to the plan.

## 3. Open items found

- **RFI-1:** S2 (Aug 2024) shows a 58'-0" slab with a 12'-6" porch; A101 (rev. Dec 2025) shows 55'-0" overall. Taken off per S2 (structural governs); porch extent to be confirmed.
- **RFI-2:** F10 says "widen as required at column" with no footing size; extra footing at columns not included.
- **RFI-3:** the porch joint band has no section mark; taken as F3.

## 4. Reproduce

```bash
pip install openpyxl
python build_takeoff.py
```

The script regenerates the workbook from scratch. Open it in Excel and the formulas compute the totals above.
