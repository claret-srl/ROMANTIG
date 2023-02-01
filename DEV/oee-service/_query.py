processDuration = '''CREATE 
OR REPLACE VIEW mtopcua_car.process_status_duration AS
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
	time_index DESC;'''

oee = f'''CREATE
OR REPLACE VIEW mtopcua_car.process_status_oee AS WITH subquery_01 AS (
	SELECT
		date_bin(
			'{timestep}'
			:: INTERVAL,
			time_index,
			'{startDateTime}'
			 :: TIMESTAMP
		) +
		'{timestep}'
		:: INTERVAL AS time_frame,
		SUM(
			CASE
				WHEN processstatus IN (
					'{endsGood}'
				) THEN 1
				ELSE 0
			END
		) AS parts_good,
		SUM(
			CASE
				WHEN processstatus IN (
					'{endsBad}'
				) THEN 1
				ELSE 0
			END
		) AS parts_bad,
		sum(
			CASE
				WHEN processstatus IN (
					{timesUp}
				) THEN duration
				ELSE 0
			END
		) AS time_up,
		sum(
			CASE
				WHEN processstatus IN (
					{timesDown}
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
		{idealTime} * 1000
		 * parts_total / NULLIF(time_total :: DECIMAL, 0) AS performance,
		parts_good / NULLIF(parts_total :: DECIMAL, 0) AS quality,
		time_up / NULLIF(time_total :: DECIMAL, 0) AS availability
	FROM
		subquery_02
)
SELECT
	*,
	performance * quality * availability AS oee
FROM
	subquery_03;'''