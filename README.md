# Analytics SQL Pipeline on Events Dataset

Designed a star schema (fact_event + dimension tables) and built analytical queries including DAU, top-N event types, rolling 7-day retention, and funnel analysis on event data. Implemented an end-to-end pipeline with synthetic data generation, MySQL-based ETL, and query benchmarking.

docker-compose up -d   # starts MySQL

# create schema
mysql -h 127.0.0.1 -u demo -p analytics < schema.sql

# generate synthetic data
python generate_events.py --rows 100000 --out data/events.csv

# load into MySQL
python load_to_mysql.py \
  --csv data/events.csv \
  --mysql mysql+pymysql://demo:demo@localhost:3306/analytics

# run and benchmark queries
python bench_queries_mysql.py \
  --mysql mysql+pymysql://demo:demo@localhost:3306/analytics \
  --queries queries.sql \
  --explain
