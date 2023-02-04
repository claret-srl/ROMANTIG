processDuration = f'''CREATE OR REPLACE VIEW {CRATE_SCHEMA}.{CRATE_TABLE_DURATION} AS
SELECT
	{OCB_ID},
	time_index,
	lag(time_index, + 1, time_index) OVER (
		ORDER BY
			time_index DESC
	) - time_index AS duration
FROM
	{CRATE_SCHEMA}.{CRATE_TABLE_DEVICE}
ORDER BY
	time_index DESC;'''

oee = f'''CREATE OR REPLACE VIEW {CRATE_SCHEMA}.{CRATE_TABLE_OEE} AS WITH subquery_01 AS (
	SELECT
		date_bin('{timestep}' :: INTERVAL, time_index, '{startDateTime}' :: TIMESTAMP) + '{timestep}' :: INTERVAL AS time_frame,
		sum(CASE WHEN {OCB_ID} IN ('{endsGood}') THEN 1 ELSE 0	END) AS parts_good,
		sum(CASE WHEN {OCB_ID} IN ('{endsBad}') THEN 1 ELSE 0 END) AS parts_bad,
		sum(CASE WHEN {OCB_ID} IN ({timesUp}) duration ELSE 0 END) AS time_up,
		sum(CASE WHEN {OCB_ID} IN ({timesDown}) duration ELSE 0 END) AS time_down
	FROM
		{CRATE_SCHEMA}.{CRATE_TABLE_DURATION}
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
		{idealTime} * 1000 * parts_total / NULLIF(time_total :: DECIMAL, 0) AS performance,
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