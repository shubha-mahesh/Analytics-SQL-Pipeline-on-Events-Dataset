# Analytics SQL Pipeline on Events Dataset

Short: Designed a star schema (fact_event + dims) and analytics queries (DAU, top-N, rolling retention, funnel) for event data. Includes synthetic data generator, Postgres loader, and query benchmarking scripts.

## How to run (local)
1. `docker-compose up -d`  # starts Postgres
2. `psql -h localhost -U demo -d analytics -f schema.sql`
3. `python generate_events.py --rows 100000 --out data/events.csv`
4. `python load_to_postgres.py --csv data/events.csv --pg postgresql://demo:demo@localhost:5432/analytics`
5. `python bench_queries.py --pg postgresql://demo:demo@localhost:5432/analytics --queries queries.sql --explain`

## What to show on resume
- Built analytics pipeline: star schema, DAU/top-N/retention/funnel queries, and query optimizations with indexing and EXPLAIN analysis.
- Example resume line:
  > Designed a star-schema analytics pipeline and authored DAU, top-N, rolling-7d retention and funnel queries; benchmarked queries and tuned indexes to improve query performance. (Demo data: synthetic.)
