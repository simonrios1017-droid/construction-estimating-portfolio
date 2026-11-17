"""Steel roof replacement, existing two-tower building (client and address not published).

    python build_quantities.py   ->   Steel_Roof_Quantities.xlsx + quantities.csv

pieces.csv is the piece list taken from the roof model: one line per beam,
post, purlin, rod, gutter, downspout and drip. The memo adds them up with
SUMIF/SUMPRODUCT, so every total can be traced back to its pieces.
"""
import csv
import math
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.page import PageMargins

HERE = Path(__file__).resolve().parent
BLUE, SKY, YELLOW, PINK = "1F4E78", "DDEBF7", "FFF2CC", "FCE4D6"
N = 7

pieces = list(csv.DictReader((HERE / "pieces.csv").open(encoding="utf-8")))


def paint(c, color):
    c.fill = PatternFill("solid", fgColor=color)


def new_sheet(wb, name, title, subtitle, widths):
    ws = wb.create_sheet(name)
    ws["A1"], ws["A2"] = title, subtitle
    ws["A1"].font = Font(bold=True, size=14, color=BLUE)
    ws["A2"].font = Font(italic=True, color="595959")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=.25, right=.25, top=.4, bottom=.4)
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = w
    return ws


def band(ws, r, text):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=N)
    c = ws.cell(r, 1, text)
    paint(c, BLUE)
    c.font = Font(bold=True, color="FFFFFF")
    return r + 1


def header(ws, r, names):
    for i, t in enumerate(names, 1):
        c = ws.cell(r, i, t)
        paint(c, SKY)
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    return r + 1


def text_lines(ws, r, texts, color=None):
    for t in texts:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=N)
        c = ws.cell(r, 1, t)
        if color:
            paint(c, color)
        r += 1
    return r


wb = Workbook()
wb.remove(wb.active)

# ---- PIECES ----
pc = new_sheet(wb, "PIECES", "PIECE LIST", "One line per piece. Lengths in m, measured on slope.",
               [8, 14, 26, 28, 11, 9, 1])
header(pc, 3, ["GROUP", "ID", "PROFILE / ITEM", "LOCATION", "LENGTH m", "COUNT"])
for i, p in enumerate(pieces, 4):
    pc.cell(i, 1, p["group"]); pc.cell(i, 2, p["id"]); pc.cell(i, 3, p["profile"])
    pc.cell(i, 4, p["location"]); pc.cell(i, 5, float(p["length_m"])).number_format = "0.000"
    if p["count"]:
        pc.cell(i, 6, int(p["count"]))
last = 3 + len(pieces)
G, L, C = f"PIECES!$A$4:$A${last}", f"PIECES!$E$4:$E${last}", f"PIECES!$F$4:$F${last}"
ID = f"PIECES!$B$4:$B${last}"

# ---- TAKEOFF ----
ws = new_sheet(wb, "TAKEOFF", "STEEL ROOF REPLACEMENT — QUANTITY MEMO",
               "Existing building, two towers. Members in m, parts in ea, panel in m². Net quantities.",
               [11, 52, 12, 7, 34, 11, 1])
summary_top = 4
r = summary_top + 2 + 27 + 1  # room for the summary block

r = band(ws, r, "A. DATA")
r = header(ws, r, ["KEY", "DESCRIPTION", "VALUE", "UNIT", "SOURCE"])
D = {}
for key, desc, val, unit, src in [
    ("DEMO", "Masonry gables to demolish", 437.71, "m²", "gable elevations, closed polylines"),
    ("BOARD_END", "Board on end walls", 66.00, "m²", "end wall elevations"),
    ("BOARD_FAC", "Board on facade closures", 68.97, "m²", "facade elevations"),
    ("PANEL", "Roof panel on slope", 555.76, "m²", "roof plan, closed polyline / cos(slope)"),
    ("RIDGE", "Ridge", 27.86, "m", "roof plan"),
    ("GABLE", "Gable trim", 33.34, "m", "roof plan, both gables"),
    ("WALLF", "Wall flashing, shafts and hatch", 81.75, "m", "roof plan, panel against walls"),
    ("SCREW", "Panel screws per m of purlin", 3, "ea/m", "panel supplier"),
    ("BRK", "Gutter bracket spacing", 0.60, "m", "detail, gutter"),
    ("STRAP", "Downspout strap spacing", 1.50, "m", "detail, downspout"),
]:
    D[key] = f"C{r}"
    ws.cell(r, 1, key); ws.cell(r, 2, desc); ws.cell(r, 3, val); ws.cell(r, 4, unit); ws.cell(r, 5, src)
    paint(ws.cell(r, 3), YELLOW)
    ws.cell(r, 3).number_format = "#,##0.00"
    r += 1

r += 1
r = band(ws, r, "B. MEASUREMENT AND CALCULATION")
r = header(ws, r, ["ITEM", "DESCRIPTION", "NET QTY", "UNIT", "HOW", "PIECES"])
sumif = lambda g: f'=SUMIF({G},"{g}",{L})'
countif = lambda g: f'=COUNTIF({G},"{g}")'
lines = [
    ("A", "DEMOLITION AND CLOSURES"),
    ("A.1", "Demolition of masonry gable walls", f"={D['DEMO']}", "m²", "data", ""),
    ("A.2", "Water-resistant board on exterior gable faces", f"={D['BOARD_END']}+{D['BOARD_FAC']}", "m²", "end walls + facade closures", ""),
    ("B", "STRUCTURAL STEEL"),
    ("B.1", "Main beam VP, HSS 200x100x5.0", sumif("VP"), "m", "sum of VP lengths", countif("VP")),
    ("B.2", "Edge beam VB, HSS 200x100x5.0", sumif("VB"), "m", "sum of VB lengths", countif("VB")),
    ("B.3", "Post CM, HSS 100x100x4.0", sumif("CM"), "m", "sum of post heights", countif("CM")),
    ("B.4", "Purlin C1, C 160x60x2.0 (tower A)", sumif("C1"), "m", "sum of C1 lengths", countif("C1")),
    ("B.5", "Purlin C2, C 203x67x2.0 (tower B)", sumif("C2"), "m", "sum of C2 lengths", countif("C2")),
    ("B.6", "X-bracing, 5/8\" rod with turnbuckle", sumif("XB"), "m", "sum of bracing lengths", countif("XB")),
    ("B.7", "Sag rods at L/2, 3/8\" rod", sumif("SR"), "m", "sum of sag rod lengths", countif("SR")),
    ("B.8", "Base plate 250x250x9.5 + 4 epoxy anchors 1/2\"", countif("CM"), "ea", "1 per post", ""),
    ("B.9", "Edge beam plate 200x150x9.5 + 2 epoxy anchors 1/2\"", f'=2*COUNTIF({G},"VB")', "ea", "2 per VB", ""),
    ("B.10", "Purlin clip, angle 2\"x2\"x3/16\" x 0.15", f'=SUMIF({G},"C*",{C})', "ea", "1 per purlin support", ""),
    ("C", "ROOFING"),
    ("C.1", "Sandwich panel 1 1/2\"", f"={D['PANEL']}", "m²", "data", ""),
    ("C.2", "Self-drilling screw with EPDM washer", f"=ROUNDUP((SUMIF({G},\"C1\",{L})+SUMIF({G},\"C2\",{L}))*{D['SCREW']},0)", "ea", "purlin m x 3", ""),
    ("C.3", "Ridge cap", f"={D['RIDGE']}", "m", "data", ""),
    ("C.4", "Eave drip, both facades", f'=SUMIF({ID},"GU-A",{L})+SUMIF({ID},"GU-B",{L})', "m", "eave gutters GU-A + GU-B", ""),
    ("C.5", "Gable trim", f"={D['GABLE']}", "m", "data", ""),
    ("C.6", "Wall flashing, shafts and hatch", f"={D['WALLF']}", "m", "data", ""),
    ("C.7", "Aluminium drip on shaft parapets", sumif("DR"), "m", "sum of DR pieces", countif("DR")),
    ("D", "RAINWATER"),
    ("D.1", "Gutter ga. 22, 0.15 x 0.15", sumif("GU"), "m", "sum of gutters", countif("GU")),
    ("D.2", "Gutter bracket @ 0.60", f'=SUMPRODUCT(({G}="GU")*ROUNDUP({L}/{D["BRK"]},0))', "ea", "per gutter, L / 0.60 up", ""),
    ("D.3", "Gutter end cap", f'=2*COUNTIF({G},"GU")', "ea", "2 per gutter", ""),
    ("D.4", "PVC downspout 4\"", sumif("DS4"), "m", "sum of 4\" downspouts", countif("DS4")),
    ("D.5", "PVC downspout 3\" (inside shafts)", sumif("DS3"), "m", "sum of 3\" downspouts", countif("DS3")),
    ("D.6", "Gutter outlet with strainer", f'=SUMIF({G},"GU",{C})', "ea", "1 per downspout", ""),
    ("D.7", "45° elbow (gooseneck)", f'=2*SUMIF({G},"GU",{C})', "ea", "2 per downspout", ""),
    ("D.8", "Downspout strap @ 1.50", f'=SUMPRODUCT((LEFT({G},2)="DS")*ROUNDUP({L}/{D["STRAP"]},0))', "ea", "per downspout, L / 1.50 up", ""),
]
B = {}
for ln in lines:
    if len(ln) == 2:
        ws.cell(r, 1, ln[0]).font = Font(bold=True)
        ws.cell(r, 2, ln[1]).font = Font(bold=True)
    else:
        item, desc, f, unit, how, n = ln
        B[item] = r
        for i, v in enumerate([item, desc, f, unit, how, n], 1):
            if v != "":
                ws.cell(r, i, v)
        ws.cell(r, 3).number_format = "#,##0.00" if unit != "ea" else "#,##0"
    r += 1

r += 1
r = band(ws, r, "OPEN ITEMS — NOT ADDED")
r = text_lines(ws, r, [
    "Masonry behind the demolished gables: condition seen only after demolition.",
    "Panel closures and sealant tape: per supplier's accessory list.",
], PINK)
r += 1
r = band(ws, r, "NOTES")
text_lines(ws, r, [
    "Members in m, plates and clips by piece. No kg.",
    "Net quantities. Laps and waste go in the unit-rate sheets.",
    "Tower A / tower B and shaft S1-S4 replace the real names.",
])

# summary on top: one line per item, pulled from section B
r = band(ws, summary_top, "SUMMARY")
r = header(ws, r, ["ITEM", "DESCRIPTION", "NET QTY", "UNIT", "FROM"])
for ln in lines:
    if len(ln) == 2:
        continue
    item, desc, _, unit, _, _ = ln
    ws.cell(r, 1, item); ws.cell(r, 2, desc); ws.cell(r, 3, f"=C{B[item]}"); ws.cell(r, 4, unit)
    ws.cell(r, 5, f"B, row {B[item]}")
    ws.cell(r, 3).number_format = "#,##0.00" if unit != "ea" else "#,##0"
    r += 1

wb.move_sheet("TAKEOFF", offset=-1)
wb.active = 0
wb.save(HERE / "Steel_Roof_Quantities.xlsx")

# quantities.csv for anyone without Excel (same rules in Python)
grp = lambda g: [p for p in pieces if p["group"] == g]
length = lambda g: round(sum(float(p["length_m"]) for p in grp(g)), 2)
gutters = grp("GU")
ds = [p for p in pieces if p["group"].startswith("DS")]
purlin_supports = sum(int(p["count"]) for p in pieces if p["group"] in ("C1", "C2"))
n_ds = sum(int(p["count"]) for p in gutters)
values = {
    "A.1": 437.71, "A.2": 134.97, "B.1": length("VP"), "B.2": length("VB"), "B.3": length("CM"),
    "B.4": length("C1"), "B.5": length("C2"), "B.6": length("XB"), "B.7": length("SR"),
    "B.8": len(grp("CM")), "B.9": 2 * len(grp("VB")), "B.10": purlin_supports,
    "C.1": 555.76, "C.2": math.ceil((length("C1") + length("C2")) * 3), "C.3": 27.86,
    "C.4": round(sum(float(p["length_m"]) for p in gutters if p["id"] in ("GU-A", "GU-B")), 2),
    "C.5": 33.34, "C.6": 81.75, "C.7": length("DR"),
    "D.1": length("GU"), "D.2": sum(math.ceil(round(float(p["length_m"]) / .6, 6)) for p in gutters),
    "D.3": 2 * len(gutters), "D.4": length("DS4"), "D.5": length("DS3"), "D.6": n_ds, "D.7": 2 * n_ds,
    "D.8": sum(math.ceil(round(float(p["length_m"]) / 1.5, 6)) for p in ds),
}
with (HERE / "quantities.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["item", "description", "unit", "net_qty"])
    for ln in lines:
        w.writerow([ln[0], ln[1], "", ""] if len(ln) == 2 else [ln[0], ln[1], ln[3], values[ln[0]]])
print("saved Steel_Roof_Quantities.xlsx and quantities.csv")
