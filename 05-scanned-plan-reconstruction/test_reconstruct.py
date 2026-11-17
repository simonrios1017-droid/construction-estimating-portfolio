"""Synthetic check for reconstruct.py. Run: python test_reconstruct.py

Draws a fake 'scan' with uneven bay scales (like shrunk paper), three axes per direction and one
wall 0.20 m thick along axis B. After rectification the wall must land on axis B in metres."""
import json
import tempfile
from pathlib import Path

import cv2
import numpy as np

from reconstruct import PPM, run

axes_x = {"A": 0.0, "B": 5.0, "C": 12.0}
axes_y = {"1": 0.0, "2": 6.0, "3": 10.0}
# pixel position of each axis on the fake scan: bays deliberately scaled differently
px_x = {"A": 100, "B": 330, "C": 680}     # 46 px/m, then 50 px/m
px_y = {"1": 100, "2": 400, "3": 590}     # 50 px/m, then 47.5 px/m

scan = np.full((700, 800), 255, np.uint8)
# wall centred on axis B, 0.20 m thick (about 10 px at 46-50 px/m), running from axis 1 to axis 3
cv2.rectangle(scan, (px_x["B"] - 5, px_y["1"]), (px_x["B"] + 5, px_y["3"]), 0, -1)

d = Path(tempfile.mkdtemp())
cv2.imwrite(str(d / "scan.png"), scan)
cfg = dict(image="scan.png", axes_x=axes_x, axes_y=axes_y,
           bubbles_x_top=px_x, bubbles_x_bottom=px_x, bubbles_y_left=px_y, bubbles_y_right=px_y,
           extent=[-1.0, 13.0, -1.0, 11.0])
(d / "plan.json").write_text(json.dumps(cfg), encoding="utf-8")

rect, polys = run(d / "plan.json")

assert len(polys) == 1, f"expected one wall, got {len(polys)}"
xs = [p[0] for p in polys[0]]
ys = [-p[1] for p in polys[0]]  # back to 'down is positive' to compare with axes_y
centre_x = (min(xs) + max(xs)) / 2
assert abs(centre_x - 5.0) < 0.05, centre_x              # on axis B within 5 cm
assert abs((max(xs) - min(xs)) - 0.20) < 0.06, max(xs) - min(xs)   # about 0.20 m thick
assert abs(min(ys) - 0.0) < 0.05 and abs(max(ys) - 10.0) < 0.05, (min(ys), max(ys))  # axis 1 to axis 3
assert (d / "plan.dxf").exists() and (d / "plan.png").exists()
assert rect.shape == (int(round(12 * PPM)), int(round(14 * PPM)))
print("ok")
