# generate_events.py
"""
Generates synthetic event data CSV for analytics pipeline.
Usage:
  python generate_events.py --rows 500000 --out data/events.csv
"""
import argparse
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def make_events(n_rows=100000, start_ts=None, out_path="data/events.csv"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    np.random.seed(42)
    if start_ts is None:
        start_ts = datetime.utcnow() - timedelta(days=30)
    user_ids = np.random.randint(1, 200000, size=n_rows)
    event_types = np.random.choice(['view','click','add_to_cart','purchase','signup'], size=n_rows, p=[0.6,0.25,0.07,0.05,0.03])
    # timestamps spread across 30 days
    offsets = np.random.randint(0, 60*60*24*30, size=n_rows)
    timestamps = [ (start_ts + timedelta(seconds=int(o))).isoformat() + "Z" for o in offsets ]
    session_id = np.random.randint(1, 300000, size=n_rows).astype(str)
    country = np.random.choice(['IN','US','GB','CA','AU'], size=n_rows, p=[0.5,0.2,0.15,0.1,0.05])
    value = np.where(event_types=='purchase', np.round(np.random.exponential(scale=80, size=n_rows),2), 0.0)
    df = pd.DataFrame({
        "event_id": np.arange(1, n_rows+1),
        "user_id": user_ids,
        "session_id": session_id,
        "event_type": event_types,
        "timestamp": timestamps,
        "country": country,
        "value": value
    })
    # inject some nulls and noise
    mask = np.random.rand(n_rows) < 0.001
    df.loc[mask, "event_type"] = None
    df.to_csv(out_path, index=False)
    print(f"Wrote {n_rows} rows to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=100000)
    parser.add_argument("--out", type=str, default="data/events.csv")
    args = parser.parse_args()
    make_events(args.rows, out_path=args.out)
