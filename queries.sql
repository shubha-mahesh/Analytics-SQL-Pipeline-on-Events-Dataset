-- ===============================
-- 1) Daily Active Users (DAU)
-- ===============================
SELECT
  date,
  COUNT(DISTINCT user_id) AS dau
FROM fact_event
GROUP BY date
ORDER BY date;



-- ===============================
-- 2) Top 3 Event Types per Day
-- ===============================
SELECT date, event_type, cnt
FROM (
  SELECT 
    date, 
    event_type, 
    COUNT(*) AS cnt,
    ROW_NUMBER() OVER (
      PARTITION BY date 
      ORDER BY COUNT(*) DESC
    ) AS rn
  FROM fact_event
  GROUP BY date, event_type
) t
WHERE rn <= 3
ORDER BY date, cnt DESC;



-- ===============================
-- 3) 7-Day Retention (Cohort)
-- ===============================
WITH cohorts AS (
  SELECT DISTINCT 
    user_id, 
    date AS day0
  FROM fact_event
),

day7 AS (
  SELECT DISTINCT 
    user_id,
    DATE_SUB(date, INTERVAL 7 DAY) AS day0_from7,
    date AS day7_date
  FROM fact_event
)

SELECT 
  c.day0,
  COUNT(DISTINCT CASE 
    WHEN d.user_id IS NOT NULL THEN c.user_id 
  END) AS retained_after_7d,

  COUNT(DISTINCT c.user_id) AS cohort_size,

  ROUND(
    100.0 * COUNT(DISTINCT CASE 
      WHEN d.user_id IS NOT NULL THEN c.user_id 
    END) / NULLIF(COUNT(DISTINCT c.user_id), 0),
  2) AS retention_pct

FROM cohorts c

LEFT JOIN day7 d
  ON c.user_id = d.user_id
  AND c.day0 = d.day0_from7

GROUP BY c.day0
ORDER BY c.day0;



-- ===============================
-- 4) Funnel Analysis
-- (view → add_to_cart → purchase)
-- ===============================
WITH steps AS (
  SELECT 
    session_id,

    MAX(CASE 
      WHEN event_type = 'view' THEN 1 
      ELSE 0 
    END) AS step_view,

    MAX(CASE 
      WHEN event_type = 'add_to_cart' THEN 1 
      ELSE 0 
    END) AS step_cart,

    MAX(CASE 
      WHEN event_type = 'purchase' THEN 1 
      ELSE 0 
    END) AS step_purchase

  FROM fact_event
  GROUP BY session_id
)

SELECT
  SUM(step_view) AS n_view_sessions,

  SUM(CASE 
    WHEN step_cart = 1 THEN 1 
    ELSE 0 
  END) AS n_cart_sessions,

  SUM(CASE 
    WHEN step_purchase = 1 THEN 1 
    ELSE 0 
  END) AS n_purchase_sessions,

  ROUND(
    100.0 * SUM(CASE 
      WHEN step_cart = 1 THEN 1 
      ELSE 0 
    END) / NULLIF(SUM(step_view), 0),
  2) AS view_to_cart_pct,

  ROUND(
    100.0 * SUM(CASE 
      WHEN step_purchase = 1 THEN 1 
      ELSE 0 
    END) / NULLIF(SUM(step_cart), 0),
  2) AS cart_to_purchase_pct

FROM steps;



-- ===============================
-- 5) Query Performance (EXPLAIN)
-- ===============================
EXPLAIN
SELECT 
  date, 
  COUNT(DISTINCT user_id) AS dau 
FROM fact_event 
GROUP BY date;
