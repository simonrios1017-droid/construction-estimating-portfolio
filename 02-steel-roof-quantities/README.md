# 02 – Steel roof replacement, existing building

Two-tower residential building from 1977. The masonry gables come down and a light steel roof goes on top. The only drawings were scans, so the geometry comes from the rebuilt plans in [05](../05-scanned-plan-reconstruction). Client and address are not published.

Members in m, plates and clips by piece, panel in m². No kg, no prices.

| Group | Main quantities |
|---|---|
| A Demolition and closures | 437.71 m² masonry gables · 134.97 m² board |
| B Structural steel | 157.40 m HSS 200x100 beams · 45.36 m HSS 100x100 posts · 472.97 m C purlins · 89.69 m bracing · 118.50 m sag rods · 186 plates and clips |
| C Roofing | 555.76 m² sandwich panel · 1,419 screws · 273.68 m flashings and drips |
| D Rainwater | 84.75 m gutter · 193.43 m PVC downspouts · 145 brackets · 135 straps |

## Workbook

`Steel_Roof_Quantities.xlsx`

- **TAKEOFF**: summary with the row each quantity comes from, data in yellow, measurement and calculation, open items not added, notes.
- **PIECES**: 147 pieces, one per line: each beam, post, purlin, rod, gutter, downspout and drip, with its length on slope. The memo adds them with SUMIF, so any total can be traced to its pieces.

Counted items come from the pieces too:

- base plates: 1 per post;
- edge beam plates: 2 per beam;
- purlin clips: 1 per support;
- gutter brackets: L / 0.60 per gutter, rounded up;
- straps: L / 1.50 per downspout, rounded up;
- outlets and elbows: from the downspouts per gutter.

`pieces.csv` is the input; `quantities.csv` is the same schedule for anyone without Excel.

```bash
pip install openpyxl
python build_quantities.py
```
