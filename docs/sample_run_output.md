# Sample run output (EXAMPLE — synthetic demo)

Commands run:
- python generate_events.py --rows 100000 --out data/events.csv
- python load_to_postgres.py --csv data/events.csv --pg postgresql://demo:demo@localhost:5432/analytics
- python bench_queries.py --pg postgresql://demo:demo@localhost:5432/analytics --queries queries.sql --explain

Example results (synthetic; run locally to produce real numbers):
- Rows generated: 100000
- Rows loaded into fact_event: 99,850
- DAU (range): 1,200 — 4,500 per day (example)
- Query timings (EXPLAIN ANALYZE):
  - DAU query: 0.15 s
  - Top-3 per day: 0.34 s
  - Rolling retention (7d): 0.55 s
  - Funnel summary: 0.12 s
- Storage: Postgres DB size (approx): 12 MB

Notes:
- Replace above numbers with the outputs you measure locally and publish those honest numbers in README or project page.
