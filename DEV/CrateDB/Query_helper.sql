-- second
-- minute
-- hour
-- day
-- week
-- month
-- quarter
-- year



-- declare function to use as variable
CREATE OR REPLACE FUNCTION time_ideal_cycle()
RETURNS INTEGER
LANGUAGE JAVASCRIPT
AS 'function time_ideal_cycle() { return 120; }';

CREATE OR REPLACE FUNCTION time_grouping_interval()
RETURNS INTERVAL
LANGUAGE JAVASCRIPT
AS 'function time_grouping_interval() { return 1 hour; }';



CREATE TABLE IF NOT EXISTS mtopcua_car.variables (time_ideal_cycle INTEGER, time_grouping_interval TEXT);
INSERT INTO mtopcua_car.variables (time_ideal_cycle, time_grouping_interval) VALUES (20, '60 minute')
UPDATE mtopcua_car.variables SET time_ideal_cycle = 20, time_grouping_interval = '5 minute';
SELECT time_ideal_cycle FROM mtopcua_car.variables;
SELECT time_grouping_interval FROM mtopcua_car.variables;
SELECT * FROM mtopcua_car.variables;
DROP TABLE mtopcua_car.variables;

CREATE OR REPLACE VIEW mtopcua_car.process_status_oee AS
WITH subquery_00 AS (
  SELECT time_ideal_cycle, time_grouping_interval FROM mtopcua_car.variables
  ), subquery_01 AS (
  SELECT 
    date_bin(time_grouping_interval::INTERVAL, time_index, '2023-01-01T08:00:00Z'::TIMESTAMP) AS time_frame,
    SUM(CASE WHEN processstatus = 'In Placing' THEN 1 ELSE 0 END) AS parts_good,
    SUM(CASE WHEN processstatus = 'In Trashing' THEN 1 ELSE 0 END) AS parts_bad,
    sum(CASE WHEN processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing') THEN duration ELSE 0 END) AS time_up,
    sum(CASE WHEN processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing') THEN duration ELSE 0 END) AS time_down
  FROM mtopcua_car.process_status_duration
  GROUP BY time_frame
), subquery_02 AS (
  SELECT
    *,
    parts_good + parts_bad AS parts_total,
    time_up + time_down AS time_total
  FROM subquery_01
), subquery_03 AS (
  SELECT
    *,
    time_ideal_cycle * 1000 * parts_total / NULLIF(time_total::DECIMAL, 0) AS performance,
	parts_good / NULLIF(parts_total::DECIMAL, 0) AS quality,
	time_up / NULLIF(time_total::DECIMAL, 0) AS availability
  FROM subquery_02
)
SELECT
  *,
  performance * quality * availability AS oee
FROM subquery_03;



-- Nested SELECT

-- SELECT
-- *,
-- performance * quality * availability AS oee
-- FROM (
-- SELECT
-- *,
-- time_ideal_cycle() * 1000 * parts_total / NULLIF(time_total::DECIMAL, 0) AS performance,
-- parts_good / NULLIF(parts_total::DECIMAL, 0) AS quality,
-- time_up / NULLIF(time_total::DECIMAL, 0) AS availability
-- FROM (
-- SELECT
-- 	*,
-- 	parts_good + parts_bad AS parts_total,
-- 	time_up + time_down AS time_total
-- FROM (
-- SELECT 
--   date_bin(time_grouping_interval()::INTERVAL, time_index, '2023-01-01T08:00:00Z'::TIMESTAMP) AS time_frame,
--   SUM(CASE WHEN processstatus = 'In Placing' THEN 1 ELSE 0 END) AS parts_good,
--   SUM(CASE WHEN processstatus = 'In Trashing' THEN 1 ELSE 0 END) AS parts_bad,
--   sum(CASE WHEN processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing') THEN duration ELSE 0 END) AS time_up,
--   sum(CASE WHEN processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing') THEN duration ELSE 0 END) AS time_down
-- FROM mtopcua_car.process_status_duration
-- GROUP BY time_frame
-- ORDER BY time_frame DESC
-- ) alias_for_subquery_01
-- ) alias_for_subquery_02
-- ) alias_for_subquery_03