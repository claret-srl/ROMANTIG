-- Crea una View con la durata dei processi.
CREATE VIEW mtopcua_car.process_status_duration AS
SELECT
	processstatus,
	time_index,
	lag(time_index, + 1, time_index) OVER (
		ORDER BY
			time_index DESC
	) - time_index AS duration
FROM
	mtopcua_car.etplc
ORDER BY
	time_index DESC;

-- Creo o Aggiorno una View selezionando la tabella con tutti i dati dell'oee, ragruppati per intervallo di tempo. che punta alla vista precedentemente creata.
CREATE
OR REPLACE VIEW mtopcua_car.process_status_oee AS WITH subquery_01 AS (
	SELECT
		date_bin(
			'5 minute' :: INTERVAL,
			time_index,
			'2023-01-01T08:00:00Z' :: TIMESTAMP
		) + '5 minute' :: INTERVAL AS time_frame,
		SUM(
			CASE
				WHEN processstatus = 'In Placing' THEN 1
				ELSE 0
			END
		) AS parts_good,
		SUM(
			CASE
				WHEN processstatus = 'In Trashing' THEN 1
				ELSE 0
			END
		) AS parts_bad,
		sum(
			CASE
				WHEN processstatus IN (
					'In Picking',
					'In Welding',
					'In QC',
					'In Placing'
				) THEN duration
				ELSE 0
			END
		) AS time_up,
		sum(
			CASE
				WHEN processstatus IN (
					'Idle',
					'In Reworking',
					'In QC from rework',
					'In Trashing'
				) THEN duration
				ELSE 0
			END
		) AS time_down
	FROM
		mtopcua_car.process_status_duration
	GROUP BY
		time_frame
),
subquery_02 AS (
	SELECT
		*,
		parts_good + parts_bad AS parts_total,
		time_up + time_down AS time_total
	FROM
		subquery_01
),
subquery_03 AS (
	SELECT
		*,
		20 * 1000 * parts_total / NULLIF(time_total :: DECIMAL, 0) AS performance,
		parts_good / NULLIF(parts_total :: DECIMAL, 0) AS quality,
		time_up / NULLIF(time_total :: DECIMAL, 0) AS availability
	FROM
		subquery_02
)
SELECT
	*,
	performance * quality * availability AS oee
FROM
	subquery_03;

-- Grafana
SELECT
	time_frame AS "time",
	oee AS "OEE",
	availability AS "Availability",
	performance AS "Performance",
	quality AS "Quality",
	parts_good AS "Parts Good",
	parts_bad AS "Parts Bad",
	parts_total AS "Parts Total",
	time_up AS "Time Up",
	time_down AS "Time Down",
	time_total AS "Time Total"
FROM
	"mtopcua_car"."process_status_oee"
ORDER BY
	1 DESC
LIMIT
	1;