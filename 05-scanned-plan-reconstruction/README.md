# 05 – Drawings rebuilt from 1977 scans

Residential building, two towers, 1977. For the roof replacement (piece 02) and the apartment areas the only drawings were scans of the original paper sheets, with handwritten notes on top. Client and address are not published.

Result: 5 floor plans in DWG (garages, intermediate, typical, full typical, penthouse), a Revit model and the internal area of each apartment.

## How

1. Each scan is scaled bay by bay between grid lines, using the dimension written on the drawing for that bay, not the nominal scale. The paper had shrunk differently on each sheet.
2. A first trace of the walls is taken from the scan automatically; then each floor is traced by hand on top of it, with the scan locked on its own layer.
3. Each DWG keeps the trace over the scan and a clean copy to the right, so anyone can compare.
4. Every floor was checked wall by wall against the scan a second time (missing facade pieces, wall thickness, column positions) and corrected until it matched.
5. Where the drawings disagree, the dimensioned one governs. Only the questions that changed quantities went to the client: 4 in total.
6. The Revit model was built from the checked DWGs; the areas come from the model.

`reconstruct.py` is a cleaned-up version of the script for step 1 (scale by bays, first wall trace, DXF with scan, axes and walls on separate layers). `test_reconstruct.py` builds a fake scan with uneven bays and checks that a 0.20 m wall falls on its axis within 5 cm.

```bash
pip install opencv-python numpy ezdxf
python test_reconstruct.py
```
