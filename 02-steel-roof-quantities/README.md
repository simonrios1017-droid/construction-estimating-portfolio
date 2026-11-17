# 02 · Steel Roof Replacement: Quantity Memo

**Project:** replacement of a masonry-gable roof with a light steel roof on an existing 1970s residential building (two towers), Cali, Colombia.
**Client and address withheld.** The original drawings were 1977 scans, so the geometry comes from the plan reconstruction in [05](../05-scanned-plan-reconstruction).
**Deliverable:** quantity schedule for bidding, in metric units: members in linear metres, plates and connections by piece, roofing in m². No pricing.

## 1. Summary

| Group | Main quantities |
|---|---|
| A · Demolition and closures | 437.71 m² of masonry gables removed · 134.97 m² of board |
| B · Structural steel | 157.40 m of HSS 200x100 beams · 45.36 m of HSS 100x100 posts · 472.97 m of C purlins · 186 plates and clips |
| C · Roofing | 555.76 m² of 1 1/2" sandwich panel · 273.68 m of flashings and trims |
| D · Stormwater | 84.75 m of gutter · 193.43 m of PVC downspouts |

The full schedule (27 items) is in [`quantities.csv`](quantities.csv).

## 2. Input data

- **Geometry:** the reconstructed DWG and Revit model of the roof level (axes, shafts, parapets, eaves).
- **Purlin spacing:** 1.61 m maximum, measured along the slope.
- **Member layout:**
  - Main beams sit on the axes of the old masonry gables.
  - Posts sit on the existing columns.
  - Edge beams are anchored to the existing bond beam.
- **Stormwater:** design intensity 150 mm/h. Downspouts sized at 1 cm² per m² of projected roof.

## 3. Calculation approach

- **Linear members:** each member is measured on the model with its real length: sloped, with overhangs, piece by piece. Pieces are then grouped by section.
- **Connections:** counted from the layout. Each post gets one base plate, each edge-beam support one plate, and each purlin-beam crossing one clip.
- **Roofing area:** sloped area per roof plane. Screws are taken at 3 per metre of purlin.
- **Flashings:** measured by type (ridge, eave, gable, wall flashing), because each one is a different piece and price.

Before quantities were frozen, a preliminary sizing check (NSR-10 load combinations) confirmed the sections used for take-off:

| Member | Span (m) | Mu / φMn (kN·m) | Deflection / limit (mm) |
|---|---:|---:|---:|
| Purlin C1 | 4.27 | 5.29 / 7.73 | 18.1 / 23.7 |
| Purlin C2 | 5.76 | 9.67 / 11.55 | 31.8 / 32.0 |
| Main beam VP | 5.31 | 28.72 / 47.26 | 20.0 / 29.5 |
| Edge beam VB | 5.85 | 14.99 / 47.26 | 12.7 / 32.5 |

The final structural design is signed by the structural engineer of record. This memo covers quantities only.

## 4. Notes

- Net quantities with no waste. Waste is applied per material when priced.
- Facade downspouts run to the storm sewer of each street. Interior downspouts end at the trap at the bottom of each shaft.
