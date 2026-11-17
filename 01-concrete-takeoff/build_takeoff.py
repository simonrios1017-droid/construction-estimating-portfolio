"""Foundation quantity memo from the public bid set (sheets S1, S2, S3).

    python build_takeoff.py   ->   Takeoff_Concrete_Foundations.xlsx

Every quantity is an Excel formula over the yellow input cells, so the
workbook can be checked or changed without this script.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.page import PageMargins

HERE = Path(__file__).resolve().parent
OUT = HERE / "Takeoff_Concrete_Foundations.xlsx"
BLUE, SKY, YELLOW, PINK = "1F4E78", "DDEBF7", "FFF2CC", "FCE4D6"
N = 8  # columns used on every sheet


def paint(cell, color):
    cell.fill = PatternFill("solid", fgColor=color)


def new_sheet(wb, name, title, subtitle, widths):
    ws = wb.create_sheet(name)
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=14, color=BLUE)
    ws["A2"] = subtitle
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
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    return r + 1


def row(ws, r, values, num_cols=(), fmt="#,##0.00"):
    for i, v in enumerate(values, 1):
        if v not in (None, ""):
            ws.cell(r, i, v)
    for col in num_cols:
        ws.cell(r, col).number_format = fmt
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
ws = new_sheet(wb, "TAKEOFF", "FOUNDATION TAKEOFF — QUANTITY MEMO",
               "Restroom / concession building, public bid set. Sheets S1, S2, S3. Net quantities.",
               [11, 44, 13, 9, 16, 13, 9, 46])

# ---- A. DATA (written first so formulas can point to it; summary goes on top) ----
SUMMARY_ROWS = 7
r = 4 + 2 + SUMMARY_ROWS + 1
r = band(ws, r, "A. DATA — READ FROM DRAWINGS")
r = header(ws, r, ["KEY", "DESCRIPTION", "VALUE", "UNIT", "", "", "", "SOURCE"])
data = [
    ("SLAB_L", "Slab, overall length", 58, "ft", "S2: 58'-0\""),
    ("SLAB_W", "Slab, overall width", "=30+8/12", "ft", "S2: 30'-8\""),
    ("SLAB_T", "Slab thickness", "=5/12", "ft", "S2 note: 5\" slab, #3 @ 18\" EW top"),
    ("GB_B", "Grade beam width", "=14/12", "ft", "S3 F1: 1'-2\""),
    ("GB_D", "Grade beam depth, top of footing to FF", 2, "ft", "S3 F1: 2'-0\""),
    ("FTG_B", "Continuous footing width", 3, "ft", "S3 F1: 3'-0\""),
    ("FTG_D", "Continuous footing depth", 1, "ft", "S3 F1: 1'-0\""),
    ("GB_LF", "Grade beam, centerline length", 215.76, "LF", "S2: perimeter + interior runs, measured"),
    ("FTG_LF", "Footing, centerline length", 200.43, "LF", "S2: beam runs less footing overlap at T's"),
    ("F3_N", "F3 runs (under CMU partitions)", 4, "ea", "S2: F3 marks, toilet partitions"),
    ("F3_RUN", "F3 run length", 9.5, "ft", "S2: 9'-6\" each"),
    ("F3_A", "F3 section below slab", "=(9/12)*(8/12+26/12)/2", "SF", "S3 F3: 9\" deep, 8\" bottom, 26\" top"),
    ("F9_LF", "F9 thickened porch edge", 54.33, "LF", "S2: west + north + south edge"),
    ("F9_A", "F9 section below slab", "=(9/12)*(8/12+17/12)/2", "SF", "S3 F9: 9\" deep, 8\" bottom, 17\" top"),
    ("COV_TOP", "Cover, grade beam top", 1.5, "in", "S1: 1 1/2\" top"),
    ("COV_BOT", "Cover, grade beam bottom", 3, "in", "S1: 3\" bottom"),
    ("COV_SIDE", "Cover, grade beam sides", 2, "in", "S1: 2\" sides (formed)"),
    ("HOOK", "Stirrup hook, each end", 3, "in", "ACI 318: 135° hook, 6 db, 3\" min"),
    ("SP_ST", "Stirrup spacing", 12, "in", "S3 F1: #3 @ 12\" o.c."),
    ("SP_FTG", "Footing bar spacing", 12, "in", "S3 F1: #5 @ 12\" both ways"),
    ("FTG_BAR", "Footing transverse bar", 2.5, "ft", "S3 F1: #5 x 2'-6\""),
    ("SP_SLAB", "Slab bar spacing", 18, "in", "S2 note: #3 @ 18\" EW"),
    ("CORNERS", "Exterior grade beam corners", 4, "ea", "S2: building outline"),
    ("CORNER_L", "Corner bar length", 4, "ft", "S1: 1-#6 x 4'-0\" top and bottom"),
    ("CHAIR_SP", "Slab chairs, max spacing", 4, "ft", "S1: chairs @ 4'-0\" max"),
    ("LAP_DB", "Lap, bar diameters", 40, "db", "S1: lap unscheduled bars 40 db"),
    ("STOCK", "Bar stock length", 20, "ft", "Stock length"),
    ("DB3", "#3 diameter", .375, "in", "ASTM A615"),
    ("DB5", "#5 diameter", .625, "in", "ASTM A615"),
    ("DB6", "#6 diameter", .75, "in", "ASTM A615"),
    ("W3", "#3 weight", .376, "lb/ft", "ASTM A615"),
    ("W5", "#5 weight", 1.043, "lb/ft", "ASTM A615"),
    ("W6", "#6 weight", 1.502, "lb/ft", "ASTM A615"),
]
D = {}
for key, desc, val, unit, src in data:
    D[key] = f"TAKEOFF!$C${r}"
    row(ws, r, [key, desc, val, unit, "", "", "", src], (3,), "#,##0.000")
    paint(ws.cell(r, 3), YELLOW)
    r += 1
d = {k: v.replace("TAKEOFF!", "") for k, v in D.items()}  # same-sheet refs

# ---- B. MEASUREMENT ----
r += 1
r = band(ws, r, "B. MEASUREMENT AND CALCULATION")
r = header(ws, r, ["ITEM", "ELEMENT", "MEASURE", "UNIT", "x FACTOR", "NET QTY", "UNIT", "HOW"])
B = {}
meas = [
    ("B-01", "Slab on grade, 5\"", f"={d['SLAB_L']}*{d['SLAB_W']}", "SF", f"={d['SLAB_T']}", "CF", "S2 overall x 5\""),
    ("B-02", "F3 thickened slab", f"={d['F3_N']}*{d['F3_RUN']}", "LF", f"={d['F3_A']}", "CF", "4 x 9'-6\" x F3 section"),
    ("B-03", "F9 thickened porch edge", f"={d['F9_LF']}", "LF", f"={d['F9_A']}", "CF", "S3 F9 section"),
    ("B-04", "Grade beams, below slab", f"={d['GB_LF']}", "LF", f"={d['GB_B']}*({d['GB_D']}-{d['SLAB_T']})", "CF", "1'-2\" x (2'-0\" - 5\"), slab counted in B-01"),
    ("B-05", "Continuous footing", f"={d['FTG_LF']}", "LF", f"={d['FTG_B']}*{d['FTG_D']}", "CF", "3'-0\" x 1'-0\""),
    ("B-06", "Grade beam forms, both faces", f"={d['GB_LF']}", "LF", f"=2*{d['GB_D']}", "SF", "2 faces x 2'-0\""),
    ("B-07", "Slab bar chairs", f"=ROUNDUP({d['SLAB_L']}/{d['CHAIR_SP']},0)+1", "rows", f"=ROUNDUP({d['SLAB_W']}/{d['CHAIR_SP']},0)+1", "ea", "grid @ 4'-0\" each way"),
]
for item, el, m, u, f, nu, how in meas:
    B[item] = r
    row(ws, r, [item, el, m, u, f, f"=C{r}*E{r}", nu, how], (3, 5, 6))
    r += 1

# ---- open items and notes ----
r += 1
r = band(ws, r, "OPEN ITEMS — NOT ADDED")
r = text_lines(ws, r, [
    "S1: footings 3000 psi, slab 3500 psi. Grade beam strength not listed.",
    "S3 F1: 2-#5 dowels @ 24\" footing to beam, length not shown.",
    "S3 F3: 2-#5 \"into grade beams at ends\", embedment not shown. Bars taken to run length.",
    "S3 F10 (3 columns): \"widen as required at column\", size not defined. Measured as F1.",
    "S2: band at porch joint has no section mark.",
    "S1: slab construction joints #3 x 2'-0\" @ 18\", locations by contractor.",
    "S2 vs A101: porch 12'-6\" vs 9'-6\". S2 used.",
], PINK)
r += 1
r = band(ws, r, "NOTES")
text_lines(ws, r, [
    "Net quantities. Waste goes in PARAMETRIC.",
    "Rebar bar by bar in REBAR SCHEDULE: 40 db laps only where the run passes 20'-0\" stock.",
    "S1: footings poured right after excavation, no footing forms.",
    "S3 F1: CMU vertical #5 @ 16\" goes with masonry.",
])

# ---- REBAR SCHEDULE ----
rb = new_sheet(wb, "REBAR SCHEDULE", "REBAR SCHEDULE — BAR BY BAR",
               "Run + hooks drawn + laps. Lap = 40 db each time the run passes stock length.",
               [7, 34, 7, 8, 10, 9, 7, 9, 10, 11, 8, 11, 34])
rb.column_dimensions["M"].width = 34
heads = ["MARK", "BAR", "SIZE", "PCS", "RUN ft", "HOOKS ft", "LAPS", "LAP ft", "UNIT LEN ft",
         "TOTAL LF", "LB/FT", "WEIGHT lb", "SOURCE"]
for i, t in enumerate(heads, 1):
    c = rb.cell(4, i, t)
    paint(c, SKY)
    c.font = Font(bold=True)
    c.alignment = Alignment(horizontal="center", wrap_text=True)
stirrup = (f"2*(({D['GB_B']}*12-2*{D['COV_SIDE']})+({D['GB_D']}*12-{D['COV_TOP']}-{D['COV_BOT']}))/12")
bars = [
    ("R1", "Grade beam top, 2-#5 cont.", 5, "2", f"={D['GB_LF']}", 0, "S3 F1"),
    ("R2", "Grade beam bottom, 2-#5 cont.", 5, "2", f"={D['GB_LF']}", 0, "S3 F1"),
    ("R3", "Grade beam stirrups #3 @ 12\"", 3, f"=ROUNDUP({D['GB_LF']}*12/{D['SP_ST']},0)", f"={stirrup}",
     f"=2*{D['HOOK']}/12", "S3 F1; covers S1"),
    ("R4", "Corner bars 1-#6 x 4'-0\", top and bottom", 6, f"={D['CORNERS']}*2", f"={D['CORNER_L']}", 0, "S1 reinforcing note"),
    ("R5", "Footing longitudinal #5 @ 12\"", 5, f"=ROUNDUP({D['FTG_B']}*12/{D['SP_FTG']},0)", f"={D['FTG_LF']}", 0, "S3 F1: cont. #5 @ 12\""),
    ("R6", "Footing transverse #5 x 2'-6\" @ 12\"", 5, f"=ROUNDUP({D['FTG_LF']}*12/{D['SP_FTG']},0)", f"={D['FTG_BAR']}", 0, "S3 F1"),
    ("R7", "F3, 2-#5 cont. per run", 5, f"=2*{D['F3_N']}", f"={D['F3_RUN']}", 0, "S3 F3"),
    ("R8", "F9, 2-#5 cont.", 5, "2", f"={D['F9_LF']}", 0, "S3 F9"),
    ("R9", "Slab #3 @ 18\", long direction", 3, f"=ROUNDUP({D['SLAB_W']}*12/{D['SP_SLAB']},0)+1", f"={D['SLAB_L']}", 0, "S2 note"),
    ("R10", "Slab #3 @ 18\", short direction", 3, f"=ROUNDUP({D['SLAB_L']}*12/{D['SP_SLAB']},0)+1", f"={D['SLAB_W']}", 0, "S2 note"),
]
first = 5
for i, (mark, desc, size, pcs, run, hooks, src) in enumerate(bars):
    r = first + i
    pcs = pcs if str(pcs).startswith("=") else int(pcs)
    vals = [mark, desc, f"#{size}", pcs, run, hooks,
            f"=MAX(0,ROUNDUP(E{r}/{D['STOCK']},0)-1)",
            f"=G{r}*{D['LAP_DB']}*{D['DB' + str(size)]}/12",
            f"=E{r}+F{r}+H{r}", f"=D{r}*I{r}", f"={D['W' + str(size)]}", f"=J{r}*K{r}", src]
    row(rb, r, vals, (5, 6, 8, 9, 10, 11, 12))
last = first + len(bars) - 1
REBAR_TOTAL = last + 2
rb.cell(REBAR_TOTAL, 10, "TOTAL").font = Font(bold=True)
rb.cell(REBAR_TOTAL, 12, f"=SUM(L{first}:L{last})").font = Font(bold=True)
rb.cell(REBAR_TOTAL, 12).number_format = "#,##0.0"

# ---- PARAMETRIC (unit rate per LF of typical F1 grade beam + footing) ----
pm = new_sheet(wb, "PARAMETRIC", "PARAMETRIC — GRADE BEAM + FOOTING, PER LF (S3 F1)",
               "What one LF consumes. Waste and reuse go here, not in the memo. No prices.",
               [11, 46, 12, 10, 50, 1, 1, 1])
r = band(pm, 4, "A. DATA")
r = header(pm, r, ["KEY", "DESCRIPTION", "VALUE", "UNIT", "SOURCE"])
P = {}
for key, desc, val, unit, src in [
    ("USES", "Form reuses", 2, "uses", "estimator"),
    ("ORDER", "Cut / handling factor, lumber and plywood", 1.10, "x", "estimator"),
    ("SHEET", "Plywood sheet 4' x 8'", 32, "SF", "stock size"),
    ("BRACE_SP", "Braces (balú) spacing per face", "=20/12", "ft", "1'-8\" (0.50 m)"),
    ("REL", "Release agent coverage", "=20*10.7639", "SF/gal", "20 m²/gal"),
    ("WASTE_C", "Concrete waste", .05, "%", "estimator"),
]:
    P[key] = f"C{r}"
    row(pm, r, [key, desc, val, unit, src], (3,), "#,##0.000")
    paint(pm.cell(r, 3), YELLOW)
    r += 1
r += 1
r = band(pm, r, "B. CONCRETE AND STEEL PER LF")
r = header(pm, r, ["ITEM", "DESCRIPTION", "QTY", "UNIT", "FORMULA"])
conc = r
for vals in [
    ("C-01", "Grade beam below slab", f"={D['GB_B']}*({D['GB_D']}-{D['SLAB_T']})", "CF/LF", "1'-2\" x (2'-0\" - 5\")"),
    ("C-02", "Footing", f"={D['FTG_B']}*{D['FTG_D']}", "CF/LF", "3'-0\" x 1'-0\""),
    ("C-03", "Concrete net", f"=(C{conc}+C{conc + 1})/27", "CY/LF", "(C-01 + C-02) / 27"),
    ("C-04", "Concrete to order", f"=C{conc + 2}*(1+{P['WASTE_C']})", "CY/LF", "C-03 x (1 + waste)"),
    ("C-05", "Rebar, grade beam", f"=SUM('REBAR SCHEDULE'!L5:L7)/{D['GB_LF']}", "lb/LF", "R1 + R2 + R3 / beam LF"),
    ("C-06", "Rebar, footing", f"=SUM('REBAR SCHEDULE'!L9:L10)/{D['FTG_LF']}", "lb/LF", "R5 + R6 / footing LF"),
]:
    r = row(pm, r, vals, (3,), "#,##0.000")
r += 1
r = band(pm, r, "C. FORMWORK AS BUILT, PER LF OF GRADE BEAM")
r = header(pm, r, ["ITEM", "DESCRIPTION", "QTY", "UNIT", "FORMULA"])
f0 = r
for vals in [
    ("F-01", "Contact area, 2 faces x 2'-0\"", f"=2*{D['GB_D']}", "SF/LF", "S3 F1"),
    ("F-02", "Plywood", f"=C{f0}/{P['SHEET']}/{P['USES']}*{P['ORDER']}", "sheets/LF", "F-01 / 32 / uses x 1.10"),
    ("F-03", "Runners (costanera), 2 per face", f"=2*2/{P['USES']}*{P['ORDER']}", "LF/LF", "2 faces x 2 / uses x 1.10"),
    ("F-04", "Braces (balú), length 2'-0\" - 2 x 2\"", f"=2/{P['BRACE_SP']}*({D['GB_D']}-4/12)/{P['USES']}*{P['ORDER']}",
     "LF/LF", "2 faces / 1'-8\" x 1'-8\" / uses x 1.10"),
    ("F-05", "4x4 (cuartón), 1 per face", f"=2/{P['USES']}*{P['ORDER']}", "LF/LF", "2 faces / uses x 1.10"),
    ("F-06", "Release agent", f"=C{f0}/{P['REL']}", "gal/LF", "F-01 / 215.3 SF/gal"),
    ("F-07", "End bulkhead, each pour end", f"={D['GB_B']}*{D['GB_D']}", "SF/end", "1'-2\" x 2'-0\"; 2 per pour"),
]:
    r = row(pm, r, vals, (3,), "#,##0.000")
r += 1
r = band(pm, r, "NOTES")
text_lines(pm, r, [
    "Footing poured against earth (S1), no forms. One mat in footing, no chairs.",
    "Pour lengths set by contractor joints (S1); bulkheads per pour end.",
])

# ---- SUMMARY on top of TAKEOFF ----
r = band(ws, 4, "SUMMARY")
r = header(ws, r, ["ITEM", "DESCRIPTION", "NET QTY", "UNIT", "FROM", "", "", ""])
for vals in [
    ("03 30 00", "Concrete 3500 psi, slab on grade incl. F3 and F9", f"=SUM(F{B['B-01']}:F{B['B-03']})/27", "CY", "B-01 to B-03"),
    ("03 30 00", "Concrete, grade beams (strength open)", f"=F{B['B-04']}/27", "CY", "B-04"),
    ("03 30 00", "Concrete 3000 psi, continuous footing", f"=F{B['B-05']}/27", "CY", "B-05"),
    ("03 20 00", "Reinforcing steel, Gr 60", f"='REBAR SCHEDULE'!L{REBAR_TOTAL}", "lb", "REBAR SCHEDULE"),
    ("03 11 13", "Formwork, grade beams", f"=F{B['B-06']}", "SF", "B-06"),
    ("03 21 00", "Slab bar chairs", f"=F{B['B-07']}", "ea", "B-07"),
]:
    r = row(ws, r, vals, (3,))
ws.cell(r, 2, "Concrete total").font = Font(bold=True)
ws.cell(r, 3, f"=SUM(C6:C8)").number_format = "#,##0.00"
ws.cell(r, 3).font = Font(bold=True)
ws.cell(r, 4, "CY")

# ---- SUPPORT: one clip per page ----
sp = wb.create_sheet("SUPPORT")
sp.sheet_view.showGridLines = False
sp.page_setup.orientation = "landscape"
sp.sheet_properties.pageSetUpPr.fitToPage = True
sp.page_setup.fitToWidth, sp.page_setup.fitToHeight = 1, 0
from openpyxl.worksheet.pagebreak import Break
for i, (caption, name) in enumerate([
    ("S1 — General notes: concrete strength, covers, 40 db lap, corner bars, chairs.", "sup_S1.png"),
    ("S2 — Foundation plan: runs measured for grade beams, footing, F3 and F9.", "sup_S2.png"),
    ("S3 — Sections F1 to F10.", "sup_S3.png"),
]):
    top = 1 + i * 45
    sp.cell(top, 1, caption).font = Font(bold=True, color=BLUE)
    img = Image(str(HERE / "support" / name))
    scale = 1100 / img.width
    img.width, img.height = 1100, int(img.height * scale)
    sp.add_image(img, f"A{top + 1}")
    if i:
        sp.row_breaks.append(Break(id=top - 1))

wb.save(OUT)
print("saved", OUT.name)
