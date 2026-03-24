-- Drop tables (order matters because of foreign keys)
DROP TABLE IF EXISTS fact_event;
DROP TABLE IF EXISTS dim_event_type;
DROP TABLE IF EXISTS dim_user;
DROP TABLE IF EXISTS staging_events;

-- staging table for raw events
CREATE TABLE staging_events (
  event_id BIGINT,
  user_id BIGINT,
  session_id VARCHAR(255),
  event_type VARCHAR(100),
  event_timestamp DATETIME,
  country VARCHAR(100),
  value DECIMAL(10,2)
);

-- dimension: dim_user
CREATE TABLE dim_user (
  user_id BIGINT PRIMARY KEY,
  country VARCHAR(100)
);

-- dimension: dim_event_type
CREATE TABLE dim_event_type (
  event_type_id INT AUTO_INCREMENT PRIMARY KEY,
  event_type VARCHAR(100) UNIQUE
);

-- fact table: fact_event
CREATE TABLE fact_event (
  event_key BIGINT AUTO_INCREMENT PRIMARY KEY,
  event_id BIGINT,
  user_id BIGINT,
  event_type VARCHAR(100),
  event_type_id INT,
  session_id VARCHAR(255),
  event_ts DATETIME,
  date DATE,
  country VARCHAR(100),
  value DECIMAL(10,2),

  -- Foreign Keys
  FOREIGN KEY (user_id) REFERENCES dim_user(user_id),
  FOREIGN KEY (event_type_id) REFERENCES dim_event_type(event_type_id)
);

-- indexes for performance
CREATE INDEX idx_fact_event_date ON fact_event(date);
CREATE INDEX idx_fact_event_user_date ON fact_event(user_id, date);
CREATE INDEX idx_fact_event_type_date ON fact_event(event_type, date);
