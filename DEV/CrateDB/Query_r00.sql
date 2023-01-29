-- SELECT
-- processstatus,
-- time_index,
-- lag(time_index, +1, time_index) OVER (ORDER BY time_index DESC) - time_index AS duration
-- FROM mtopcua_car.etplc
-- ORDER BY time_index DESC;

-- Crea la tabella con la durata dei processi
CREATE TABLE mtopcua_car.process_status AS
SELECT
processstatus,
time_index,
lag(time_index, +1, time_index) OVER (ORDER BY time_index DESC) - time_index AS duration
FROM mtopcua_car.etplc
ORDER BY time_index DESC;

-- SELECT * FROM mtopcua_car.process_status
-- DROP TABLE mtopcua_car.process_status

-- Aggiorna la tabella con la durata dei processi considerando solo i dati non presenti
INSERT INTO mtopcua_car.process_status
SELECT
processstatus,
time_index,
lag(time_index, +1, time_index) OVER (ORDER BY time_index DESC) - time_index AS duration
FROM mtopcua_car.etplc newDataTable
WHERE NOT EXISTS (SELECT time_index FROM mtopcua_car.process_status WHERE time_index = newDataTable.time_index);


-- Crea la vista con la durata dei processi
CREATE VIEW mtopcua_car.process_status_view AS
SELECT
processstatus,
time_index,
lag(time_index, +1, time_index) OVER (ORDER BY time_index DESC) - time_index AS duration
FROM mtopcua_car.etplc
ORDER BY time_index DESC;

-- Seleziona i Process Status, la loro durata, e il loro numero raggruppati per tipo
SELECT
processstatus,
sum(duration) AS total_duration,
count(duration) AS total_count
FROM mtopcua_car.process_status
GROUP BY processstatus;

-- Creo una tabella con  la seleziona dei Process Status, la loro durata, e il loro numero raggruppati per tipo
CREATE TABLE mtopcua_car.process_status_duration AS
SELECT
processstatus,
sum(duration) AS total_duration,
count(duration) AS total_count
FROM mtopcua_car.process_status
GROUP BY processstatus;

-- Creo una tabella con  la seleziona dei Process Status, la loro durata, e il loro numero raggruppati per tipo
CREATE VIEW mtopcua_car.process_status_duration_view AS
SELECT
processstatus,
sum(duration) AS total_duration,
count(duration) AS total_count
FROM mtopcua_car.process_status
GROUP BY processstatus;

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
processstatus,
sum(duration) AS total_duration,
count(duration) AS total_count,
date_trunc('day', time_index) AS time_frame
FROM mtopcua_car.process_status
GROUP BY processstatus, time_frame
ORDER BY time_frame DESC;

SELECT
processstatus,
sum(duration) AS total_duration,
count(duration) AS total_count,
date_format('%e/%c/%Y %H:%i', date_trunc('hour', time_index)) AS time_frame
FROM mtopcua_car.process_status
GROUP BY processstatus, time_frame
ORDER BY time_frame DESC;

SELECT
processstatus,
count(duration),
date_bin('1 day'::INTERVAL, time_index, 0) AS time_frame
FROM mtopcua_car.process_status
GROUP BY processstatus, time_frame
ORDER BY time_frame DESC;

SELECT
processstatus,
count(duration),
date_format('%e/%c/%Y %H:%i', date_bin('1 day'::INTERVAL, time_index, 0)) AS time_frame
FROM mtopcua_car.process_status
GROUP BY processstatus, time_frame
ORDER BY time_frame DESC;

SELECT
processstatus,
count(duration) AS count,
date_format('%e/%c/%Y %H:%i:%S', date_bin('1 hour'::INTERVAL, time_index, '2000-01-01T00:00:00Z'::TIMESTAMP)) AS time_frame
FROM mtopcua_car.process_status
GROUP BY processstatus, time_frame
ORDER BY time_frame DESC;

-- Machine States
-- 'In QC',
-- 'In Trashing',
-- 'In Reworking',
-- 'In Picking',
-- 'In Welding',
-- 'In Placing',
-- 'In QC from rework'

-- SELECT
-- processstatus,
-- total_duration
-- FROM "mtopcua_car"."process_status_duration"
-- WHERE processstatus IN ('Idle', 'In QC', 'In Trashing', 'In Reworking', 'In Picking', 'In Welding', 'In Placing', 'In QC from rework');

-- SELECT
-- sum(total_duration) AS time_down
-- FROM "mtopcua_car"."process_status_duration" 
-- WHERE processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing')

SELECT
sum(total_duration) AS time_up
FROM "mtopcua_car"."process_status_duration" 
WHERE processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing')

SELECT
sum(total_duration) AS time_down
FROM "mtopcua_car"."process_status_duration" 
WHERE processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing')

SELECT
processstatus,
count(*) AS parts_good
FROM mtopcua_car.process_status
WHERE processstatus IN ('In Placing')
GROUP BY processstatus;

-- SELECT
-- count(*) AS parts_good
-- FROM mtopcua_car.process_status
-- WHERE processstatus IN ('In Placing');

SELECT
processstatus,
count(*) AS parts_bad
FROM mtopcua_car.process_status
WHERE processstatus IN ('In Trashing')
GROUP BY processstatus;

-- SELECT
-- count(*) AS parts_bad
-- FROM mtopcua_car.process_status
-- WHERE processstatus IN ('In Trashing');

-- SELECT
-- 	(
-- 		SELECT
-- 			count(*)
-- 		FROM
-- 			mtopcua_car.process_status
-- 		WHERE
-- 			processstatus IN ('In Placing')
-- 	) + (
-- 		SELECT
-- 			count(*)
-- 		FROM
-- 			mtopcua_car.process_status
-- 		WHERE
-- 			processstatus IN ('In Trashing')
-- 	) AS parts_total;

-- time_up		time_down	time_total	parts_good	parts_bad	parts_total
-- 57107812		225098419	282206231	1371		438			1809
SELECT
	(
		SELECT
			sum(total_duration)
		FROM
			"mtopcua_car"."process_status_duration"
		WHERE
			processstatus IN (
				'In Picking',
				'In Welding',
				'In QC',
				'In Placing'
			)
	) AS time_up,
	(
		SELECT
			sum(total_duration)
		FROM
			"mtopcua_car"."process_status_duration"
		WHERE
			processstatus IN (
				'Idle',
				'In Reworking',
				'In QC from rework',
				'In Trashing'
			)
	) AS time_down,
	(
		SELECT
			sum(total_duration)
		FROM
			"mtopcua_car"."process_status_duration"
		WHERE
			processstatus IN (
				'In Picking',
				'In Welding',
				'In QC',
				'In Placing',
				'Idle',
				'In Reworking',
				'In QC from rework',
				'In Trashing'
			)
	) AS time_total,
	(
		SELECT
			count(*)
		FROM
			mtopcua_car.process_status
		WHERE
			processstatus IN ('In Placing')
	) AS parts_good,
	(
		SELECT
			count(*)
		FROM
			mtopcua_car.process_status
		WHERE
			processstatus IN ('In Trashing')
	) AS parts_bad,
	(
		SELECT
			count(*)
		FROM
			mtopcua_car.process_status
		WHERE
			processstatus IN ('In Placing', 'In Trashing')
	) AS parts_total;

-- parts_good	parts_bad	parts_total
-- 1371		438			180
SELECT
	parts_good,
	parts_bad,
	(parts_good + parts_bad) AS parts_total
FROM (
SELECT 
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Placing')) AS parts_good,
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Trashing')) AS parts_bad
) alias_for_subquery;

-- time_up		time_down	time_toal
-- 57107812		225098419	282206231
SELECT
	time_up,
	time_down,
	(time_up + time_down) AS time_toal
FROM (
	SELECT
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing')) AS time_up,
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing')) AS time_down
) alias_for_subquery;

-- parts_good	parts_bad	parts_total	quality		time_up		time_down	time_toal	aviability
-- 1371			438			1809		0.7578773	57107812	225098419	282206231	0.20236197
SELECT
	parts_good,
	parts_bad,
	(parts_good + parts_bad) AS parts_total,
	parts_good / (parts_good + parts_bad)::DECIMAL AS quality,
	time_up::TIMESTAMP AS time_up,
	time_down::TIMESTAMP AS time_down,
	(time_up + time_down)::TIMESTAMP AS time_toal,
	time_up / (time_up + time_down)::DECIMAL AS aviability,
	60 * 1000 * (parts_good + parts_bad) / (time_up + time_down)::DECIMAL AS performance
FROM (
SELECT 
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Placing')) AS parts_good,
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Trashing')) AS parts_bad,
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing')) AS time_up,
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing')) AS time_down
) alias_for_subquery;


-- parts_good	parts_bad	parts_total	time_up		time_down	time_total	performance			quality				aviability				oee
-- 1371		438			1809		57107812	225098419	282206231	0.3846123440130562	0.75787728026534	0.2023619811569646		0.058986282871875746

SELECT
parts_good,
parts_bad,
parts_total,
time_up,
time_down,
time_total,
performance,
quality,
aviability,
performance * quality * aviability AS oee
FROM (
SELECT
parts_good,
parts_bad,
parts_total,
time_up,
time_down,
time_total,
60 * 1000 * parts_total / time_total::DECIMAL AS performance,
parts_good / parts_total::DECIMAL AS quality,
time_up / time_total::DECIMAL AS aviability
FROM (
SELECT
	parts_good,
	parts_bad,
	(parts_good + parts_bad) AS parts_total,
	time_up AS time_up,
	time_down AS time_down,
	time_up + time_down AS time_total
FROM (
SELECT 
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Placing')) AS parts_good,
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Trashing')) AS parts_bad,
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing')) AS time_up,
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing')) AS time_down
) alias_for_subquery_01
) alias_for_subquery_02
) alias_for_subquery_03;

-- Contracted form of the precedent query

SELECT
*,
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
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Placing')) AS parts_good,
	(SELECT count(*) FROM mtopcua_car.process_status WHERE processstatus IN ('In Trashing')) AS parts_bad,
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('In Picking', 'In Welding', 'In QC', 'In Placing')) AS time_up,
	(SELECT sum(duration) FROM mtopcua_car.process_status_duration WHERE processstatus IN ('Idle', 'In Reworking', 'In QC from rework', 'In Trashing')) AS time_down
) alias_for_subquery_01
) alias_for_subquery_02
) alias_for_subquery_03;


SELECT FROM ()

SELECT date_bin('1 day'::INTERVAL, time_index, 0) AS time_frame, 
 GROUP BY time_frame ORDER BY time_frame DESC