# 03 – Quote generator

After the August 2026 earthquake in Cali we sent a lot of inspection quotes to residential complexes. They were all the same document: scope, items, payment schedule and duration. Only the client and the quantities changed, so each quote is generated from a short job file instead of editing Word by hand.

What the script checks:

- The total is calculated once; the price table and the payment schedule use the same figure.
- Payment shares must add up to 100 %. Rounding goes to the last payment.
- Field days = units ÷ units per day, rounded up, plus the days for the report.

Client, prices and quantities in `example_job.json` are made up.

| File | |
|---|---|
| `generate_quote.py` | prices the job and writes the DOCX |
| `example_job.json` | sample job: 30 apartments + extras, payments 50/30/20, no VAT |
| `test_generate_quote.py` | checks totals, rounding of payments, VAT and that the DOCX shows the same total |

```bash
pip install python-docx
python test_generate_quote.py
python generate_quote.py
```

The version we use writes on the company letterhead and has the full scope text (methodology, deliverables, severity criteria, exclusions, acceptance). Unit prices come from an Excel price model that starts from cost: engineer's fee + VAT, field costs and target margin, grossed up for the withholding tax the client deducts. It has a check row so the margin comes back exactly, and a table of prices for different engineer fees.
