# 01 – Foundation take-off, public bid set

Restroom and concession building for a city park in Texas. Structural sheets S1 (general notes), S2 (foundation plan) and S3 (sections F1–F10). Quantities only, no prices.

| Item | Net qty | From |
|---|---:|---|
| Concrete 3500 psi, slab on grade incl. F3 and F9 | 30.52 CY | B-01 to B-03 |
| Concrete, grade beams | 14.76 CY | B-04 |
| Concrete 3000 psi, continuous footing | 22.27 CY | B-05 |
| Reinforcing steel Gr 60 | 3,873 lb | rebar schedule |
| Formwork, grade beams | 863 SF | B-06 |
| Slab bar chairs | 144 ea | B-07 |

Concrete is split by strength because S1 gives 3000 psi for footings and 3500 psi for the slab. S1 doesn't list a strength for the grade beams, so that line stays open.

## Workbook

`Takeoff_Concrete_Foundations.xlsx`

- **TAKEOFF**: summary, data read from the drawings (yellow, with sheet and dimension), measurement with formulas, open items not added, notes.
- **REBAR SCHEDULE**: bar by bar. Run + hooks drawn + laps. A 40 db lap (S1) only where the run passes the 20 ft stock length. Stirrups developed from the S1 covers. It includes the 1-#6 × 4'-0" corner bars from the S1 notes.
- **PARAMETRIC**: what one LF of F1 grade beam + footing uses. It covers concrete, steel by bar and formwork the way it is built: 2 runners per face, braces every 1'-8", one 4x4 per face, ÷ 2 uses × 1.10, release agent at 20 m²/gal. Waste goes here, not in the memo.
- **SUPPORT**: the S1, S2 and S3 clips used.

## Open items (not added)

- Grade beam concrete strength not listed in S1.
- Footing-to-beam dowels 2-#5 @ 24": no length shown.
- F3 bars "into grade beams at ends": no embedment shown.
- F10 "widen as required at column": footing size not defined.
- Porch joint band on S2 has no section mark.
- Slab construction joints: locations are left to the contractor.
- Porch length 12'-6" on S2 vs 9'-6" on A101. S2 used.

```bash
pip install openpyxl
python build_takeoff.py
```
