# Construction Estimating Portfolio · Juan Simón Ríos Suárez

Civil engineer and construction cost estimator based in Cali, Colombia, with 6+ years in quantity take-off, budgets and bid packages for residential and commercial work. I work in Excel, AutoCAD, Revit and Bluebeam, and I write Python when a repetitive task is worth automating.

This repository shows how I work: how I measure, how I document a quantity so someone else can check it, and the tools I build around estimating. Client names, addresses, drawings and real prices are withheld; sample data is fictional unless the source is public.

| # | Piece | What it shows |
|---|---|---|
| [01](01-concrete-takeoff) | **Concrete & foundation rebar take-off** from public US bid documents | A formula-driven Excel take-off, traceable to the sheet, with RFIs: 80 CY of concrete and 5,375 LB of rebar |
| [02](02-steel-roof-quantities) | **Steel roof replacement quantity memo** for a 1970s building | Steel members in m, plates and clips by piece, sandwich panel, flashings and stormwater; a preliminary sizing check before quantities were frozen |
| [03](03-quote-generator) | **Quote generator**, from a JSON job file to a priced DOCX | Totals, payment milestones and schedule computed once and validated, with tests |
| [04](04-inspection-reporting-app) | **Post-earthquake inspection & repair-estimate system** (case study) | Field findings turned into priced, traceable repair budgets and frozen client reports |
| [05](05-scanned-plan-reconstruction) | **Rebuilding a 1977 building from paper scans** | Bay-by-bay rectification to DWG, audit loop, Revit model and areas, with a tested tool |

## How I write a quantity memo

Every memo here follows the same order, so a reviewer always knows where to look:

1. **Summary** first: the quantities that go into the estimate.
2. **Input data**: each dimension with the sheet it came from.
3. **Calculation**: formulas over the input data, never typed results.
4. **Open items**: conflicts between drawings, written as RFIs.
5. **Notes**: exclusions and what belongs to another package, to avoid double counting.

## Contact

- LinkedIn: <https://www.linkedin.com/in/simon-rios-su%C3%A1rez-a739a0ba>

---

*The software pieces were built with AI-assisted development (Claude Code). I wrote the specifications and domain rules, and I reviewed and tested the results.*
