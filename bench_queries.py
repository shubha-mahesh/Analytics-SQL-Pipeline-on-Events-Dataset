# bench_queries_mysql.py
"""
Connect to MySQL, run queries from queries.sql, print timing and optionally save EXPLAIN output.

Usage:
  python bench_queries_mysql.py --mysql mysql+pymysql://demo:demo@localhost:3306/analytics --queries queries.sql
"""

import argparse
import time
from sqlalchemy import create_engine, text


def read_queries(path):
    with open(path, 'r') as f:
        content = f.read()
    # split queries (same logic)
    parts = [p.strip() for p in content.split('\n\n') if p.strip()]
    return parts


def run_query(engine, q, save_explain=False):
    with engine.connect() as conn:

        # =========================
        # EXPLAIN (MySQL version)
        # =========================
        if save_explain:
            res = conn.execute(text("EXPLAIN " + q))
            explain = "\n".join([str(r) for r in res])
            return {"explain": explain}

        # =========================
        # Normal execution
        # =========================
        start = time.time()

        res = conn.execute(text(q))
        rows = res.fetchmany(10)

        elapsed = time.time() - start

        return {
            "elapsed_seconds": elapsed,
            "sample_rows": rows
        }


def main(args):
    engine = create_engine(args.mysql)

    queries = read_queries(args.queries)

    for i, q in enumerate(queries):
        print(f"\n--- Query {i+1} ---")
        print(q[:200].replace('\n', ' ') + '...')

        out = run_query(engine, q, save_explain=args.explain)

        if args.explain:
            print("EXPLAIN:")
            print(out['explain'])
        else:
            print("Elapsed:", round(out['elapsed_seconds'], 4), "s")
            print("Sample rows:", out['sample_rows'][:3])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--mysql", required=True)
    parser.add_argument("--queries", required=True)
    parser.add_argument("--explain", action="store_true")

    args = parser.parse_args()
    main(args)
