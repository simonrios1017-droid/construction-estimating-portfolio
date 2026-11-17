# 04 · Post-Earthquake Inspection & Repair-Estimate System (case study)

**Context:** after the August 2026 earthquake in Cali, my firm inspected residential complexes apartment by apartment. Each building produced hundreds of findings (cracks, detachments, deformations, leaks). Each finding had to become:

1. a documented record with a photo and location,
2. a priced repair line,
3. a client report that the insurer could audit.

To handle this with several inspectors working at the same time, I specified a web application and ran it in production. The source code stays private because it is in commercial use. This page describes what it does and how it is built.

## What it does

- **Field capture (phone):** the inspector walks a generated list of locations (tower → floor → unit → room, plus common areas). For each finding the inspector records:
  - the element (column, beam, slab, wall, finish…), from a catalog that only accepts valid element–damage pairs;
  - the damage type and severity;
  - the magnitude in m, m² or units;
  - a photo, compressed on the phone to 800 KB or less.
- **From finding to estimate:** each finding maps to repair activities from a catalog, each with its own unit of measure. Quantities roll up into a preliminary repair budget per unit, per tower and per project. Every budget line keeps the finding and location it came from.
- **Report engine:** client reports on Letter-size pages with a summary by structure, severity and type of reform, finding cards, the budget, and habitability and priority flags. A report is versioned and **frozen** when issued, so later edits do not change what the client received.
- **Administration:** progress per project, inspector accounts, release or skip of locations, and CSV export of the full dataset.

## How it is built

```
Browser (Vite, ES modules)
   │  supabase-js
   ├── Auth ......... email + password
   ├── PostgREST .... reads under Row Level Security
   ├── RPC .......... all capture writes (SECURITY DEFINER functions)
   └── Storage ...... private photo bucket
            │
   PostgreSQL 16 · 80+ tables · 170+ functions · 130+ RLS policies · 111 migrations
```

**Key design rule:** the client cannot write capture data directly to any table. Every write goes through a database function that validates the business rules and writes an audit row. A manipulated browser cannot save an invalid finding, because the database rejects it, not the screen.

## Quality checks

There are more than 60 automated test files. Each suite rebuilds the database from zero before it starts. They cover:

- row-level security;
- an end-to-end inspector walk-through in Chromium;
- 4 inspectors capturing on the same project at the same time;
- the report engine, checked page by page against a Letter-size layout;
- the CSV export, checked for completeness and permissions.

## What this shows for estimating work

- Turning a messy field survey into **traceable quantities**: every budget line points back to a photo and a location.
- Designing **units of measure and repair catalogs** that make findings priceable.
- Separating **earthquake damage from pre-existing deterioration**, which is what insurers ask for.

Built with AI-assisted development (Claude Code). I wrote the specification, the domain rules, the catalogs and the acceptance tests, and I reviewed the results.
