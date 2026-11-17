# 04 – Post-earthquake inspections and repair budgets

After the August 2026 earthquake in Cali we inspected residential complexes apartment by apartment. One building can give several hundred findings (cracks, spalling, detached finishes, leaks), and each one had to end up as:

1. a record with photo and location,
2. a priced repair line,
3. part of a report the insurer can check.

For that we use a small web application with several inspectors capturing at the same time. I defined what it captures and the rules; the code is private because we use it with clients.

## From the field to the budget

- The inspector follows a list of locations: tower → floor → apartment → room, plus common areas.
- Each finding records element (column, beam, slab, wall, finish…), damage type, severity, size in m, m² or units, and a photo.
- Only element–damage combinations that make sense are accepted (a catalog defines them).
- Each finding is linked to repair activities, each with its own unit. Quantities add up per apartment, per tower and per project.
- Every budget line keeps the finding and location it came from, so the client or the insurer can go from the price back to the photo.
- Earthquake damage is kept apart from older deterioration.
- A report is frozen when it is issued; later corrections go into a new version.

## Technical summary

Web app (Vite) on PostgreSQL / Supabase. Field data can only be written through database functions that check the rules and keep an audit trail; the browser cannot write directly to the tables. Automated tests rebuild the database from scratch and cover permissions, several inspectors working at once, the printed report and the data export.
