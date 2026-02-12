# bench_queries.py
"""
Connect to Postgres, run queries from queries.sql, print timing and optionally save EXPLAIN output.
Usage:
  python bench_queries.py --pg postgresql://demo:demo@localhost:5432/analytics --queries queries.sql
"""
import argparse
import time
from sqlalchemy import create_engine, text

def read_queries(path):
    with open(path, 'r') as f:
        content = f.read()
    # simple split on \n\n for top-level queries (works for our file)
    parts = [p.strip() for p in content.split('\n\n') if p.strip()]
    return parts

def run_query(engine, q, save_explain=False):
    with engine.connect() as conn:
        # EXPLAIN ANALYZE if requested
        if save_explain:
            res = conn.execute(text("EXPLAIN ANALYZE " + q))
            explain = "\n".join([r[0] for r in res])
            return {"explain": explain}
        start = time.time()
        res = conn.execute(text(q))
        # fetch some rows (up to 10) to ensure execution
        rows = res.fetchmany(10)
        elapsed = time.time() - start
        return {"elapsed_seconds": elapsed, "sample_rows": rows}

def main(args):
    engine = create_engine(args.pg)
    queries = read_queries(args.queries)
    for i,q in enumerate(queries):
        print(f"\n--- Query {i+1} ---")
        print(q[:200].replace('\n',' ') + '...')  # preview
        out = run_query(engine, q, save_explain=args.explain)
        if args.explain:
            print("EXPLAIN ANALYZE:")
            print(out['explain'])
        else:
            print("Elapsed:", out['elapsed_seconds'], "s")
            print("Sample rows:", out['sample_rows'][:3])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pg", required=True)
    parser.add_argument("--queries", required=True)
    parser.add_argument("--explain", action="store_true")
    args = parser.parse_args()
    main(args)
