# load_to_postgres.py
"""
Loads CSV into Postgres staging, then upserts dims and inserts into fact table.
Usage:
  python load_to_postgres.py --csv data/events.csv --pg "postgresql://demo:demo@localhost:5432/analytics"
"""
import argparse
import os
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm

def load_csv_to_staging(csv_path, engine, chunksize=50000):
    for chunk in tqdm(pd.read_csv(csv_path, parse_dates=['timestamp'], chunksize=chunksize), desc="loading csv"):
        # basic cleaning
        chunk = chunk.rename(columns={'timestamp':'timestamp'})
        chunk['timestamp'] = pd.to_datetime(chunk['timestamp'], errors='coerce')
        chunk = chunk.dropna(subset=['timestamp','user_id'])
        chunk.to_sql('staging_events', engine, if_exists='append', index=False)

def transform_staging_to_star(engine):
    with engine.begin() as conn:
        # upsert dim_user
        conn.execute(text("""
          INSERT INTO dim_user (user_id, country)
          SELECT DISTINCT user_id, country FROM staging_events
          ON CONFLICT (user_id) DO UPDATE SET country = EXCLUDED.country;
        """))
        # upsert dim_event_type
        conn.execute(text("""
          INSERT INTO dim_event_type (event_type)
          SELECT DISTINCT event_type FROM staging_events
          WHERE event_type IS NOT NULL
          ON CONFLICT (event_type) DO NOTHING;
        """))
        # insert into fact_table (simple insert; dedup/merge logic can be more elaborate)
        conn.execute(text("""
          INSERT INTO fact_event (event_id, user_id, event_type, session_id, event_ts, date, country, value, event_type_id)
          SELECT se.event_id, se.user_id, se.event_type, se.session_id, se.timestamp, se.timestamp::date, se.country, se.value,
                 det.event_type_id
          FROM staging_events se
          LEFT JOIN dim_event_type det ON det.event_type = se.event_type;
        """))
        # cleanup staging for idempotent runs (optionally track watermark)
        conn.execute(text("TRUNCATE TABLE staging_events;"))

def main(args):
    engine = create_engine(args.pg)
    # ensure tables exist (run schema.sql ahead)
    load_csv_to_staging(args.csv, engine, chunksize=args.chunk_size)
    transform_staging_to_star(engine)
    print("Load complete")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--pg", required=True)
    parser.add_argument("--chunk-size", type=int, default=50000)
    args = parser.parse_args()
    main(args)
