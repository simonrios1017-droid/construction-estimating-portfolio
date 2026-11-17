"""Commercial quote generator: one JSON job file -> one priced, client-ready DOCX.

Generic version of the tool I use to issue inspection and repair quotes. All sample data is fictional.

    python generate_quote.py example_job.json            # writes <code>.docx next to the JSON
    python test_generate_quote.py                        # runs the checks

The quote is computed once (compute_quote) and then written (write_docx), so the numbers in
the document always come from the same validated source.
"""
import json
import math
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


def cop(n):
    """Colombian peso format: $ 1.234.567"""
    return "$ " + f"{n:,.0f}".replace(",", ".")


def compute_quote(job):
    """Line items, subtotal, VAT, payment milestones and schedule. Raises on inconsistent input."""
    lines = [dict(desc=i["description"], unit=i["unit"], qty=i["qty"], price=i["unit_price"],
                  total=i["qty"] * i["unit_price"]) for i in job["items"]]
    subtotal = sum(l["total"] for l in lines)
    vat = round(subtotal * job.get("vat_rate", 0))
    total = subtotal + vat

    shares = [m["share"] for m in job["payments"]]
    if not math.isclose(sum(shares), 1.0):
        raise ValueError(f"payment milestones add up to {sum(shares):.0%}, not 100 %")
    payments = [dict(desc=m["description"], share=m["share"], amount=round(total * m["share"])) for m in job["payments"]]
    payments[-1]["amount"] = total - sum(p["amount"] for p in payments[:-1])  # rounding goes to the last milestone

    sched = job["schedule"]
    field_days = math.ceil(sched["units"] / sched["units_per_day"])
    return dict(lines=lines, subtotal=subtotal, vat=vat, total=total, payments=payments,
                field_days=field_days, report_days=sched["report_days"],
                total_days=field_days + sched["report_days"])


def write_docx(job, q, out):
    doc = Document()
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(10)

    def heading(text):
        p = doc.add_paragraph()
        p.add_run(text).bold = True

    def table(head, rows, right=()):
        t = doc.add_table(rows=1, cols=len(head))
        t.style = "Table Grid"
        for c, h in zip(t.rows[0].cells, head):
            c.text = h
            c.paragraphs[0].runs[0].bold = True
        for r in rows:
            cells = t.add_row().cells
            for i, v in enumerate(r):
                cells[i].text = str(v)
                if i in right:
                    cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    title = doc.add_paragraph()
    title.add_run(f"OFERTA COMERCIAL {job['code']}").bold = True
    doc.add_paragraph(job["service"])
    table(["", ""], [["Cliente", job["client"]], ["Fecha", job["date"]], ["Ubicación", job["location"]]])

    heading("1. OBJETO")
    doc.add_paragraph(job["scope"])

    heading("2. VALOR DE LA OFERTA")
    rows = [[l["desc"], l["unit"], l["qty"], cop(l["price"]), cop(l["total"])] for l in q["lines"]]
    rows.append(["Subtotal", "", "", "", cop(q["subtotal"])])
    if q["vat"]:
        rows.append([f"IVA {job['vat_rate']:.0%}", "", "", "", cop(q["vat"])])
    rows.append(["TOTAL", "", "", "", cop(q["total"])])
    table(["Descripción", "Und", "Cant.", "Valor unitario", "Subtotal"], rows, right=(2, 3, 4))

    heading("3. FORMA DE PAGO")
    table(["Hito", "%", "Valor"], [[p["desc"], f"{p['share']:.0%}", cop(p["amount"])] for p in q["payments"]], right=(1, 2))

    heading("4. PLAZO")
    s = job["schedule"]
    doc.add_paragraph(
        f"{q['field_days']} días de campo ({s['units']} {s['unit_name']} a {s['units_per_day']} por día) "
        f"y {q['report_days']} días para el informe: {q['total_days']} días hábiles en total.")

    heading("5. EXCLUSIONES")
    for e in job["exclusions"]:
        doc.add_paragraph(e, style="List Bullet")

    doc.save(out)


def main(path):
    job = json.loads(Path(path).read_text(encoding="utf-8"))
    q = compute_quote(job)
    out = Path(path).with_name(f"{job['code']}.docx")
    write_docx(job, q, out)
    print(f"{out.name}: total {cop(q['total'])}, {q['total_days']} business days")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("example_job.json"))
