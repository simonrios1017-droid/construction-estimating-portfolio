# Builds Takeoff_Concrete_Foundations.xlsx — foundations, slab and foundation rebar.
# All quantities are formulas over the DATA block; dimensions come from S2/S3 (see SUPPORT sheet).
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Takeoff_Concrete_Foundations.xlsx")
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "TAKEOFF"
B = Font(bold=True); H = Font(bold=True, color="FFFFFF"); T = Font(bold=True, size=14)
HF = PatternFill("solid", fgColor="1F3864"); SF = PatternFill("solid", fgColor="D9E1F2")
IN = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="999999"); BOX = Border(top=thin, bottom=thin, left=thin, right=thin)

def hdr(r, vals):
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = H; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="center")

r = 1
ws.cell(r, 1, "QUANTITY TAKE-OFF — Liberty City Park Restroom & Concession Building (base bid)").font = T
ws.cell(2, 1, "Scope: foundations, slab on grade and foundation reinforcing. Source: public bid documents, City of Liberty TX (Bid 2026-01), sheets S2 and S3. Quantities only — no pricing.")
ws.cell(3, 1, "Prepared by: Juan Simon Rios Suarez — Civil Engineer, Cost Estimator")

# ---------------- SUMMARY (top) ----------------
r = 5
ws.cell(r, 1, "1. SUMMARY").font = B
hdr(6, ["Item", "Description", "Net qty", "Unit", "Waste %", "Order qty", "Unit", "Ref."])
summary_rows = 7  # filled after data rows are known

# ---------------- DATA ----------------
D = 20
ws.cell(D, 1, "2. INPUT DATA (yellow = read from drawings)").font = B
hdr(D + 1, ["Key", "Description", "Value", "Unit", "Source / how measured"])
data = [
    ("SLAB_L", "Slab overall length (porch + building)", 58.0, "ft", "S2 overall dim 58'-0\""),
    ("SLAB_W", "Slab overall width", 30.667, "ft", "S2 overall dim 30'-8\""),
    ("SLAB_T", "Slab thickness", 5 / 12, "ft", "S2 note: 5\" slab, #3 @ 18\" EW"),
    ("BLDG_L", "Building length (enclosed)", 45.5, "ft", "S2 dim 45'-6\""),
    ("GB_B", "Grade beam width (F1,F2,F4-F8)", 14 / 12, "ft", "S3: 1'-2\""),
    ("GB_D", "Grade beam depth from finished floor", 2.0, "ft", "S3: 2'-0\""),
    ("FTG_B", "Footing width under grade beam", 3.0, "ft", "S3: 3'-0\" (centered on beam, checked on S2 dashed lines)"),
    ("FTG_D", "Footing depth", 1.0, "ft", "S3: 1'-0\""),
    ("LF_PERIM", "Perimeter grade beam, centerline", "=2*((C25-C26)+(C23-C26))", "LF", "Rectangle 45'-6\" x 30'-8\" less one beam width"),
    ("LF_INT", "Interior grade beams, clear between beam faces", 131.43, "LF", "S2 dashed beam faces: 3 x 28.33 + 2 x 14.02 + 2 x 4.33 + 9.74"),
    ("N_TEES", "Beam ends meeting another beam (T-joints)", 16, "EA", "8 interior beams x 2 ends"),
    ("F3_LF", "F3 thickened slab (under CMU toilet partitions + porch joint band)", 48.17, "LF", "S2: 4 runs x 9.50 (x=42'-4\" and 45'-9\") + porch band 10.17"),
    ("F3_A", "F3 section area below slab", 1.0625, "SF", "S3: 1'-2\" deep from FF, 8\" bottom, 45 deg sides -> 9\" x (8\"+26\")/2"),
    ("F9_LF", "F9 thickened porch edge", 54.33, "LF", "S2: west edge 30.67 + north 11.83 + south 11.83"),
    ("F9_A", "F9 section area below slab", 0.781, "SF", "S3: 9\" x (8\"+17\")/2, one vertical face"),
    ("F10_N", "F10 widened beam at HSS columns", 3, "EA", "S2: 3 columns at porch line"),
    ("F10_L", "F10 widened length each", 1.94, "ft", "S2: column block outline 1.94 ft"),
    ("F10_X", "F10 extra width beyond typical beam", 20 / 12, "ft", "S2/S3: 1'-8\""),
    ("W3", "#3 bar weight", 0.376, "lb/ft", "ASTM A615"),
    ("W5", "#5 bar weight", 1.043, "lb/ft", "ASTM A615"),
    ("STIR", "#3 stirrup developed length", 5.67, "ft", "S3: 10\" x 20\" inside cover + 2 hooks (68\")"),
    ("DWL_FTG", "2-#5 footing-to-beam dowel length", 2.5, "ft", "S3 scaled: 12\" footing + 12\" into beam + 6\" leg"),
    ("LAP5", "Lap allowance #5 continuous", 0.08, "%", "40 db lap every 20 ft approx."),
]
row = {}
for i, (k, desc, v, u, src) in enumerate(data):
    rr = D + 2 + i
    row[k] = rr
    ws.cell(rr, 1, k); ws.cell(rr, 2, desc); c = ws.cell(rr, 3, v); ws.cell(rr, 4, u); ws.cell(rr, 5, src)
    if not (isinstance(v, str) and v.startswith("=")): c.fill = IN
    c.number_format = "0.00"
# fix formula refs by key
ws.cell(row["LF_PERIM"], 3).value = f"=2*((C{row['BLDG_L']}-C{row['GB_B']})+(C{row['SLAB_W']}-C{row['GB_B']}))"
C = lambda k: f"C{row[k]}"

# ---------------- CALCULATION ----------------
K = D + 2 + len(data) + 2
ws.cell(K, 1, "3. CALCULATION").font = B
hdr(K + 1, ["Item", "Element", "Length / area", "Unit", "Section / factor", "Quantity", "Unit", "Formula note"])
calc = [
    ("03-01", "Slab on grade 5\" (area)", f"={C('SLAB_L')}*{C('SLAB_W')}", "SF", 1, "SF", "58'-0\" x 30'-8\""),
    ("03-02", "Slab concrete", f"=C{{r1}}", "SF", f"={C('SLAB_T')}", "CF", "area x 5\""),
    ("03-03", "Grade beams below slab (F1,F2,F4-F8)", f"={C('LF_PERIM')}+{C('LF_INT')}", "LF", f"={C('GB_B')}*({C('GB_D')}-{C('SLAB_T')})", "CF", "beam LF x 1'-2\" x (2'-0\" - 5\")"),
    ("03-04", "Continuous footings 3'-0\" x 1'-0\"", f"={C('LF_PERIM')}+{C('LF_INT')}-{C('N_TEES')}*({C('FTG_B')}-{C('GB_B')})/2", "LF", f"={C('FTG_B')}*{C('FTG_D')}", "CF", "beam LF less footing overlap at T-joints"),
    ("03-05", "F3 thickened slab", f"={C('F3_LF')}", "LF", f"={C('F3_A')}", "CF", ""),
    ("03-06", "F9 thickened porch edge", f"={C('F9_LF')}", "LF", f"={C('F9_A')}", "CF", ""),
    ("03-07", "F10 widened beam at columns", f"={C('F10_N')}*{C('F10_L')}", "LF", f"={C('F10_X')}*({C('GB_D')}-{C('SLAB_T')})", "CF", "extra over typical beam"),
    ("05-01", "#5 grade beam continuous (2 top + 2 bottom)", f"=C{{gb}}", "LF", f"=4*(1+{C('LAP5')})*{C('W5')}", "LB", ""),
    ("05-02", "#3 stirrups @ 12\"", f"=C{{gb}}", "LF", f"={C('STIR')}*{C('W3')}", "LB", "1 stirrup per ft"),
    ("05-03", "#5 footing longitudinal (3 bars)", f"=C{{ftg}}", "LF", f"=3*(1+{C('LAP5')})*{C('W5')}", "LB", ""),
    ("05-04", "#5 x 2'-6\" footing transverse @ 12\"", f"=C{{ftg}}", "LF", f"=2.5*{C('W5')}", "LB", ""),
    ("05-05", "2-#5 dowels footing to beam @ 24\"", f"=C{{gb}}", "LF", f"=2/2*{C('DWL_FTG')}*{C('W5')}", "LB", "2 bars every 2 ft"),
    ("05-06", "F3 + F9: 2-#5 continuous", f"={C('F3_LF')}+{C('F9_LF')}", "LF", f"=2*(1+{C('LAP5')})*{C('W5')}", "LB", ""),
    ("05-07", "Slab #3 @ 18\" each way", f"=C{{r1}}", "SF", f"=2/1.5*1.10*{C('W3')}", "LB", "2 directions / 1.5 ft, +10% laps"),
]
rr0 = K + 2
for i, (it, el, ln, u, sec, uq, note) in enumerate(calc):
    rr = rr0 + i
    gb = rr0 + 2; ftg = rr0 + 3
    ln = ln.replace("{r1}", str(rr0)).replace("{gb}", str(gb)).replace("{ftg}", str(ftg))
    ws.cell(rr, 1, it); ws.cell(rr, 2, el); ws.cell(rr, 3, ln); ws.cell(rr, 4, u)
    ws.cell(rr, 5, sec); ws.cell(rr, 6, f"=C{rr}*E{rr}"); ws.cell(rr, 7, uq); ws.cell(rr, 8, note)
    for col in (3, 5, 6): ws.cell(rr, col).number_format = "#,##0.00"
crow = {c[0]: rr0 + i for i, c in enumerate(calc)}

# ---------------- SUMMARY formulas ----------------
conc = [crow[k] for k in ("03-02", "03-03", "03-04", "03-05", "03-06", "03-07")]
rebar = [crow[c[0]] for c in calc if c[0].startswith('05')]
summ = [
    ("03 30 00", "Cast-in-place concrete — slab, grade beams, footings, thickenings", "=(" + "+".join(f"F{x}" for x in conc) + ")/27", "CY", 0.05, "CY", "S2, S3"),
    ("03 30 00", "  of which slab on grade 5\"", f"=F{crow['03-02']}/27", "CY", 0.05, "CY", "S2"),
    ("03 30 00", "  of which foundations (beams, footings, F3/F9/F10)", "=(" + "+".join(f"F{x}" for x in conc[1:]) + ")/27", "CY", 0.05, "CY", "S3"),
    ("03 20 00", "Reinforcing steel Gr. 60 — foundations and slab", "=(" + "+".join(f"F{x}" for x in rebar) + ")", "LB", 0.05, "LB", "S2, S3"),
    ("03 30 00", "Slab on grade area (vapor barrier 15 mil, finish)", f"=F{crow['03-01']}", "SF", 0.10, "SF", "S2"),
]
for i, (it, d_, q, u, w, u2, ref) in enumerate(summ):
    rr = summary_rows + i
    ws.cell(rr, 1, it); ws.cell(rr, 2, d_); ws.cell(rr, 3, q).number_format = "#,##0.0"
    ws.cell(rr, 4, u); ws.cell(rr, 5, w).number_format = "0%"
    ws.cell(rr, 6, f"=ROUNDUP(C{rr}*(1+E{rr}),0)").number_format = "#,##0"; ws.cell(rr, 7, u2); ws.cell(rr, 8, ref)
    if i == 0 or i == 3: ws.cell(rr, 2).font = B

# ---------------- OPEN ITEMS / NOTES ----------------
N = rr0 + len(calc) + 2
ws.cell(N, 1, "4. OPEN ITEMS (RFI)").font = B
rfi = [
    "RFI-1: S2 (Aug-2024) shows slab 58'-0\" with a 12'-6\" porch; A101 (rev. Dec-2025) dimensions 55'-0\" overall with 9'-6\" at the porch. Taken-off per S2 (structural). Confirm porch slab extent.",
    "RFI-2: F10 says 'widen as required at column' — no footing size given. Extra footing at columns not included.",
    "RFI-3: Porch joint band (double dashed line at mid-porch on S2) has no section mark; taken as F3.",
]
for i, t in enumerate(rfi): ws.cell(N + 1 + i, 1, t)
ws.cell(N + 5, 1, "5. NOTES").font = B
notes = [
    "Beam-to-slab haunches (45 deg transitions shown in S3) not included — under 1% of volume.",
    "Concrete below slab only for beams/thickenings; slab measured once over full plan area (no double count).",
    "Excludes: site work and walk slabs (C sheets), CMU and wall dowels (next package), #3 walk-slab dowels at F6/F7/F9, anchor bolts.",
]
for i, t in enumerate(notes): ws.cell(N + 6 + i, 1, t)

for col, w in zip("ABCDEFGH", (11, 52, 12, 7, 14, 12, 7, 44)):
    ws.column_dimensions[col].width = w
ws.column_dimensions["E"].width = 14

# ---------------- SUPPORT ----------------
s = wb.create_sheet("SUPPORT")
s["A1"] = "S2 — Foundation plan (beam faces dashed; dims 58'-0\", 45'-6\", 30'-8\")"; s["A1"].font = B
s.add_image(Image(os.path.join(HERE, "support", "sup_S2.png")), "A2")
s["A55"] = "S3 — Foundation sections F1-F10"; s["A55"].font = B
s.add_image(Image(os.path.join(HERE, "support", "sup_S3.png")), "A56")
wb.save(OUT)
print("ok", OUT)
