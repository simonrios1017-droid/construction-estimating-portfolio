"""Checks for generate_quote.py. Run: python test_generate_quote.py"""
import copy
import json
import tempfile
from pathlib import Path

from docx import Document

from generate_quote import compute_quote, write_docx

job = json.loads(Path(__file__).with_name("example_job.json").read_text(encoding="utf-8"))
q = compute_quote(job)

# totals: 30 x 150.000 + 2 x 450.000 + 550.000 + 2 x 550.000
assert q["total"] == 7_050_000, q["total"]
# milestones add back to the total, even with rounding
assert sum(p["amount"] for p in q["payments"]) == q["total"]
assert [p["amount"] for p in q["payments"]] == [3_525_000, 2_115_000, 1_410_000]
# 30 units at 15 per day -> 2 field days + 3 report days
assert (q["field_days"], q["total_days"]) == (2, 5)

# VAT is applied on the subtotal
j2 = copy.deepcopy(job); j2["vat_rate"] = 0.19
assert compute_quote(j2)["total"] == round(7_050_000 * 1.19)

# milestones that do not add up to 100 % are rejected
j3 = copy.deepcopy(job); j3["payments"][0]["share"] = 0.4
try:
    compute_quote(j3)
    raise AssertionError("expected ValueError")
except ValueError:
    pass

# the document carries the same total
out = Path(tempfile.mkdtemp()) / "q.docx"
write_docx(job, q, out)
text = "\n".join(c.text for t in Document(out).tables for r in t.rows for c in r.cells)
assert "$ 7.050.000" in text

print("ok")
