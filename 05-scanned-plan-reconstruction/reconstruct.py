"""Scanned floor plan -> rectified image + DXF with grid axes and wall outlines, in metres.

Generic version of the tool used to rebuild the drawings of a 1977 building that only existed
as paper scans. The scan is not trusted to be at scale: paper shrinks, scanners skew, and the
spacing between grid bubbles drifts. So each bay between two grid bubbles is scaled with its
own written dimension, not with the nominal scale.

    python reconstruct.py config.json          # writes <name>.png and <name>.dxf next to the config
    python test_reconstruct.py                  # synthetic check

Config (all pixel values measured on the native scan):
    image        path to the scan (PNG/JPG)
    axes_x       {"A": 0.0, "B": 7.55, ...}     grid lines in metres, left to right
    axes_y       {"1": 0.0, "3": 8.05, ...}     grid lines in metres, top to bottom
    bubbles_x_top / bubbles_x_bottom            pixel x of each vertical axis at the top/bottom edge
    bubbles_y_left / bubbles_y_right            pixel y of each horizontal axis at the left/right edge
    extent       [x0, x1, y0, y1] in metres     area to rebuild (may extend past the outer axes)
"""
import json
import sys
from pathlib import Path

import cv2
import ezdxf
import numpy as np

PPM = 50  # pixels per metre of the rectified image (2 cm per pixel)


def piecewise(v, metres, pixels):
    """Map metres -> pixels bay by bay; extrapolate past the outer axes with the edge bay."""
    xp, fp = np.asarray(metres, float), np.asarray(pixels, float)
    out = np.interp(v, xp, fp)
    lo, hi = v < xp[0], v > xp[-1]
    out[lo] = fp[0] + (v[lo] - xp[0]) * (fp[1] - fp[0]) / (xp[1] - xp[0])
    out[hi] = fp[-1] + (v[hi] - xp[-1]) * (fp[-1] - fp[-2]) / (xp[-1] - xp[-2])
    return out


def chain(bubbles, axes):
    keys = sorted(bubbles, key=lambda k: axes[k])
    return [axes[k] for k in keys], [bubbles[k] for k in keys]


def rectify(cfg, scan):
    """Resample the scan onto a regular metre grid. Top/bottom (and left/right) bubble rows are
    blended linearly, which also corrects a scan that is slightly rotated or trapezoidal."""
    x0, x1, y0, y1 = cfg["extent"]
    xs, ys = np.arange(x0, x1, 1 / PPM), np.arange(y0, y1, 1 / PPM)
    MX, MY = np.meshgrid(xs, ys)
    ax, ay = cfg["axes_x"], cfg["axes_y"]
    wy = np.clip((MY - min(ay.values())) / (max(ay.values()) - min(ay.values())), 0, 1)
    wx = np.clip((MX - min(ax.values())) / (max(ax.values()) - min(ax.values())), 0, 1)
    f = lambda M, c: piecewise(M.ravel(), *c).reshape(M.shape)
    px = (1 - wy) * f(MX, chain(cfg["bubbles_x_top"], ax)) + wy * f(MX, chain(cfg["bubbles_x_bottom"], ax))
    py = (1 - wx) * f(MY, chain(cfg["bubbles_y_left"], ay)) + wx * f(MY, chain(cfg["bubbles_y_right"], ay))
    return cv2.remap(scan, px.astype(np.float32), py.astype(np.float32), cv2.INTER_AREA, borderValue=255)


def walls(rect, extent, min_len_m=0.55):
    """Thick, straight dark bands -> closed polylines in metres (y up, as in CAD)."""
    x0, _, y0, _ = extent
    bw = (rect < 150).astype(np.uint8) * 255
    k = lambda w, h: cv2.getStructuringElement(cv2.MORPH_RECT, (w, h))
    t = cv2.morphologyEx(cv2.morphologyEx(bw, cv2.MORPH_CLOSE, k(7, 7)), cv2.MORPH_OPEN, k(5, 5))
    m = cv2.bitwise_or(cv2.morphologyEx(t, cv2.MORPH_OPEN, k(25, 1)), cv2.morphologyEx(t, cv2.MORPH_OPEN, k(1, 25)))
    contours, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in contours:
        (_, _), (w, h), _ = cv2.minAreaRect(c)
        if max(w, h) / PPM < min_len_m:  # drops text and loose symbols
            continue
        out.append([(x0 + p[0][0] / PPM, -(y0 + p[0][1] / PPM)) for p in cv2.approxPolyDP(c, 1.5, True)])
    return out


def write_dxf(cfg, rect, polys, png_name, dxf_path):
    x0, x1, y0, y1 = cfg["extent"]
    doc = ezdxf.new("R2018", setup=True)
    doc.units = ezdxf.units.M
    for layer, color in (("SCAN", 8), ("AXES", 1), ("WALLS-SCAN", 7)):
        doc.layers.add(layer, color=color)
    doc.layers.get("AXES").dxf.linetype = "CENTER"
    msp = doc.modelspace()
    h, w = rect.shape
    idef = doc.add_image_def(filename=png_name, size_in_pixel=(w, h))
    msp.add_image(idef, insert=(x0, -(y0 + h / PPM)), size_in_units=(w / PPM, h / PPM), dxfattribs={"layer": "SCAN"})
    doc.layers.get("SCAN").lock()
    for name, x in cfg["axes_x"].items():
        msp.add_line((x, -y0), (x, -y1), dxfattribs={"layer": "AXES"})
        msp.add_text(name, height=0.4, dxfattribs={"layer": "AXES"}).set_placement((x, -y0 + 0.5))
    for name, y in cfg["axes_y"].items():
        msp.add_line((x0, -y), (x1, -y), dxfattribs={"layer": "AXES"})
        msp.add_text(name, height=0.4, dxfattribs={"layer": "AXES"}).set_placement((x0 - 0.8, -y))
    for p in polys:
        msp.add_lwpolyline(p, close=True, dxfattribs={"layer": "WALLS-SCAN"})
    doc.saveas(dxf_path)


def run(config_path):
    config_path = Path(config_path)
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    scan = cv2.imread(str(config_path.parent / cfg["image"]), cv2.IMREAD_GRAYSCALE)
    rect = rectify(cfg, scan)
    polys = walls(rect, cfg["extent"])
    stem = config_path.parent / config_path.stem
    cv2.imwrite(str(stem) + ".png", rect)
    write_dxf(cfg, rect, polys, stem.name + ".png", str(stem) + ".dxf")
    return rect, polys


if __name__ == "__main__":
    _, polys = run(sys.argv[1])
    print(f"{len(polys)} wall outlines written")
