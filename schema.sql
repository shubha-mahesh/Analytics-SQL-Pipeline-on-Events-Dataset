-- schema.sql
-- Run this in Postgres (psql -d analytics -U demo -f schema.sql)

-- staging table for raw events
DROP TABLE IF EXISTS staging_events;
CREATE TABLE staging_events (
  event_id BIGINT,
  user_id BIGINT,
  session_id TEXT,
  event_type TEXT,
  timestamp TIMESTAMP,
  country TEXT,
  value NUMERIC
);

-- dimension: dim_user (light)
DROP TABLE IF EXISTS dim_user;
CREATE TABLE dim_user (
  user_id BIGINT PRIMARY KEY,
  country TEXT
);

-- dimension: dim_event_type
DROP TABLE IF EXISTS dim_event_type;
CREATE TABLE dim_event_type (
  event_type_id SERIAL PRIMARY KEY,
  event_type TEXT UNIQUE
);

-- fact table: fact_event
DROP TABLE IF EXISTS fact_event;
CREATE TABLE fact_event (
  event_key BIGSERIAL PRIMARY KEY,
  event_id BIGINT,
  user_id BIGINT REFERENCES dim_user(user_id),
  event_type TEXT,
  event_type_id INT,
  session_id TEXT,
  event_ts TIMESTAMP,
  date DATE,
  country TEXT,
  value NUMERIC
);

-- indexes for performance
CREATE INDEX IF NOT EXISTS idx_fact_event_date ON fact_event(date);
CREATE INDEX IF NOT EXISTS idx_fact_event_user_date ON fact_event(user_id, date);
CREATE INDEX IF NOT EXISTS idx_fact_event_type_date ON fact_event(event_type, date);
