# 05 · Rebuilding a 1977 Building from Paper Scans

**Problem:** a client needed a roof replacement and floor areas for a 1977 residential building with two towers. The only drawings were scans of the original paper sheets: no CAD, no dimensions you could trust at scale, and handwritten notes on top.

**Result:**
- 5 floor plans rebuilt as DWG: garages, intermediate, typical, full typical and penthouse.
- A Revit model of the building.
- Internal floor areas per apartment.
- The geometry for the steel-roof quantities in [02](../02-steel-roof-quantities).

Client and address are withheld.

## Process

1. **Rectify each scan by bays, not by scale.** Paper shrinks and scanners skew, so the nominal scale did not hold, and it drifted differently on each sheet. The tool reads the pixel position of each grid bubble and maps each bay between two axes with its own written dimension. It also blends the top and bottom rows of bubbles, which corrects slight rotation.
2. **Detect walls automatically as a starting trace.** Thick, straight dark bands become closed outlines in metres on their own layer. Text and symbols shorter than 0.55 m are dropped.
3. **Trace by hand over the rectified scan**, with the scan locked underneath on its own layer. Each DWG keeps the trace on top of the scan plus a clean copy to the right, so anyone can check the trace against the original.
4. **Independent audit of every floor.** A second pass compares the trace with the scan, wall by wall, and lists the differences: missing facade segments, wrong wall thickness, columns out of place. Corrections are applied and audited again until the floor is approved.
5. **Questions only when the drawing cannot answer them.** More than a hundred drawing doubts were settled with documented criteria, for example "where two sheets disagree, the one with dimensions governs". Only 4 questions went to the client, the ones that changed quantities.
6. **Revit model and areas.** The model was built from the approved DWGs, reviewed version by version, and gave the internal areas per apartment.

## Files

| File | What it does |
|---|---|
| `reconstruct.py` | Bay-by-bay rectification, wall detection and DXF output, with the scan on a locked layer, grid axes and wall outlines |
| `test_reconstruct.py` | Builds a fake scan with uneven bay scales and checks that a 0.20 m wall lands on its axis within 5 cm |

```bash
pip install opencv-python numpy ezdxf
python test_reconstruct.py    # prints "ok"
```

The production version also converts the DXF to DWG with AutoCAD's console and stores the bubble positions of every floor. The scans themselves are not published.

## Why it matters for estimating

Old buildings rarely have usable drawings. Being able to produce reliable geometry from whatever exists (scans, photos, partial sheets), and to say how reliable it is, is what makes quantities for renovation and repair work defensible.
