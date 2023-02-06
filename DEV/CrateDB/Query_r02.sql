-- Crea la vista con la durata dei processi
CREATE VIEW mtopcua_car.process_status_duration AS
SELECT
processstatus,
time_index,
lag(time_index, +1, time_index) OVER (ORDER BY time_index DESC) - time_index AS duration
FROM mtopcua_car.etplc
ORDER BY time_index DESC;

-- Seleziono o calcolo parts_good	parts_bad	time_up	time_down	parts_total	time_total	performance	quality	aviability	oee
-- Sub-query

WITH subquery_01 AS (
  SELECT 
    date_bin('1 hour'::INTERVAL, time_index, '2023-01-01T08:00:00Z'::TIMESTAMP) AS time_frame,
    SUM(CASE WHEN processstatus = 'In Placing' THEN 1 ELSE 0 END) AS parts_good,
    SUM(CASE WHEN processstatus = 'In Trashing' THEN 1 ELSE 0 END) AS parts_bad,
    sum(CASE WHEN processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing') THEN duration ELSE 0 END) AS time_up,
    sum(CASE WHEN processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing') THEN duration ELSE 0 END) AS time_down
  FROM mtopcua_car.process_status_duration
  GROUP BY time_frame
), subquery_02 AS (
  SELECT
    *,
    (parts_good + parts_bad) AS parts_total,
    time_up + time_down AS time_total
  FROM subquery_01
), subquery_03 AS (
  SELECT
    *,
    60 * 1000 * parts_total / time_total ::DECIMAL AS performance,
    parts_good / parts_total ::DECIMAL AS quality,
    time_up / time_total ::DECIMAL AS availability
  FROM subquery_02
)
SELECT
  *,
  performance * quality * availability AS oee
FROM subquery_03;

-- Seleziono o calcolo parts_good	parts_bad	time_up	time_down	parts_total	time_total	performance	quality	aviability	oee
-- Nested SLEECT
SELECT
*,
date_bin('1 day'::INTERVAL, time_index, 0) AS time_frame
performance * quality * aviability AS oee
FROM (
SELECT
*,
60 * 1000 * parts_total / time_total::DECIMAL AS performance,
parts_good / parts_total::DECIMAL AS quality,
time_up / time_total::DECIMAL AS aviability
FROM (
	
SELECT
	*,
	(parts_good + parts_bad) AS parts_total,
	time_up + time_down AS time_total
FROM (
SELECT 
  date_bin('1 day'::INTERVAL, time_index, 0) AS time_frame,
  SUM(CASE WHEN processstatus = 'In Placing' THEN 1 ELSE 0 END) AS parts_good,
  SUM(CASE WHEN processstatus = 'In Trashing' THEN 1 ELSE 0 END) AS parts_bad,
  sum(CASE WHEN processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing') THEN duration ELSE 0 END) AS time_up,
  sum(CASE WHEN processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing') THEN duration ELSE 0 END) AS time_down
FROM mtopcua_car.process_status_duration
GROUP BY time_frame
ORDER BY time_frame DESC
) alias_for_subquery_01

) alias_for_subquery_02
) alias_for_subquery_03 
GROUP BY time_frame;

SELECT
processstatus,
count(duration),
date_bin('1 day'::INTERVAL, time_index, 0) AS time_frame
FROM mtopcua_car.process_status
GROUP BY processstatus, time_frame
ORDER BY time_frame DESC;

-- ARGUMENTS date_trunc(), date_bin()
-- second
-- minute
-- hour
-- day
-- week
-- month
-- quarter
-- year


SELECT 
  date_bin('1 day'::INTERVAL, time_index, 0) AS time_frame,
  SUM(CASE WHEN processstatus = 'In Placing' THEN 1 ELSE 0 END) AS parts_good,
  SUM(CASE WHEN processstatus = 'In Trashing' THEN 1 ELSE 0 END) AS parts_bad,
  sum(CASE WHEN processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing') THEN duration ELSE 0 END) AS time_up,
  sum(CASE WHEN processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing') THEN duration ELSE 0 END) AS time_down
FROM mtopcua_car.process_status_duration
GROUP BY time_frame
ORDER BY time_frame DESC;