# 03 · Quote Generator (JSON → priced DOCX)

**Context:** after the August 2026 earthquake in Cali, my firm issued many inspection and repair quotes to residential complexes over the following months. Each one had the same structure: scope, line items, payment milestones and schedule. Only the quantities and the client changed.

Instead of editing Word files by hand, every quote was generated from a short job file, so that:

- **the total is computed once.** The quote table and the payment schedule both come from the same numbers.
- **payment milestones always add up to the total.** Rounding goes to the last milestone, and shares that do not add up to 100 % are rejected.
- **the schedule comes from productivity.** Field days are the units divided by the units per day, rounded up, plus the days for the report.
- **a new quote takes minutes.** You copy the last job file, change the quantities and regenerate.

This is a cleaned-up, generic version of that tool. The client, prices and quantities in `example_job.json` are fictional.

## Files

| File | What it does |
|---|---|
| `generate_quote.py` | `compute_quote()` validates and prices the job; `write_docx()` writes the client document |
| `example_job.json` | Sample job: 30 units plus extras, 50/30/20 payments, no VAT |
| `test_generate_quote.py` | Checks the totals, the milestone rounding, VAT, the rejection of bad shares, and that the DOCX carries the same total |

## Run

```bash
pip install python-docx
python test_generate_quote.py      # prints "ok"
python generate_quote.py           # writes INS-02_000-DEMO.docx
```

## How the production version differs

- It writes onto the firm's letterhead template, which already carries the signature and the legal clauses.
- The full scope text is about 15 sections: methodology, deliverables, report card fields, severity criteria, exclusions and acceptance.
- Unit prices come from a pricing model in Excel that works backwards from cost:
  - It adds the subcontracted engineer's fee plus their VAT, own field costs and a target profit.
  - It grosses that up for the withholding tax the client deducts, and divides by the number of units.
  - A verification block checks that the target profit comes back exactly, and a sensitivity table shows the price for different subcontractor fees.
