def processDuration(CRATE_SCHEMA, CRATE_TABLE_DURATION, OCB_ID, DEVICE_ID, CRATE_TABLE_DEVICE):
    return f"""CREATE OR REPLACE VIEW {CRATE_SCHEMA.lower()}.{CRATE_TABLE_DURATION.lower()} AS
	SELECT
		{OCB_ID.lower()},
		time_index,
		lag(time_index, + 1, time_index) OVER (
			ORDER BY
				time_index DESC
		) - time_index AS duration
	FROM
		{CRATE_SCHEMA.lower()}.{CRATE_TABLE_DEVICE.lower()}
	WHERE
 		"entity_id"='{DEVICE_ID}' 
	ORDER BY
		time_index DESC;"""


def oee(
    CRATE_SCHEMA,
    CRATE_TABLE_OEE,
    CRATE_TABLE_DURATION,
    OCB_ID,
    endsGood,
    endsBad,
    timesUp,
    timesDown,
    idealTime,
    timestep,
    startDateTime,
):
    return f"""CREATE OR REPLACE VIEW {CRATE_SCHEMA.lower()}.{CRATE_TABLE_OEE.lower()} AS WITH
	subquery_01 AS (
		SELECT
			date_bin('{timestep}' :: INTERVAL, time_index, '{startDateTime}' :: TIMESTAMP) + '{timestep}' :: INTERVAL AS time_frame,
			sum(CASE WHEN {OCB_ID.lower()} IN ({endsGood}) THEN 1 ELSE 0 END) AS parts_good,
			sum(CASE WHEN {OCB_ID.lower()} IN ({endsBad}) THEN 1 ELSE 0 END) AS parts_bad,
			sum(CASE WHEN {OCB_ID.lower()} IN ({timesUp}) THEN duration ELSE 0 END) AS time_up,
			sum(CASE WHEN {OCB_ID.lower()} IN ({timesDown}) THEN duration ELSE 0 END) AS time_down
		FROM
			{CRATE_SCHEMA.lower()}.{CRATE_TABLE_DURATION.lower()}
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
		subquery_03;"""

def oeeCallBack(CRATE_SCHEMA, CRATE_TABLE_OEE):
    return f'''SELECT oee, availability, performance, quality FROM "{CRATE_SCHEMA.lower()}"."{CRATE_TABLE_OEE.lower()}" LIMIT 1;'''
