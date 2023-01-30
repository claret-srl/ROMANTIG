sqlFile = '''
CREATE
OR REPLACE VIEW mtopcua_car.process_status_oee AS WITH subquery_01 AS (
	SELECT
		date_bin(
			'5 minute'
			:: INTERVAL,
			time_index,
			'2023-01-01T08:00:00Z' :: TIMESTAMP
		) +
		'5 minute'
		:: INTERVAL AS time_frame,
		SUM(
			CASE
				WHEN processstatus IN (
					'In Placing'
				) THEN 1
				ELSE 0
			END
		) AS parts_good,
		SUM(
			CASE
				WHEN processstatus IN (
					'In Trashing'
				) THEN 1
				ELSE 0
			END
		) AS parts_bad,
		sum(
			CASE
				WHEN processstatus IN (
					'In Picking','In Welding','In QC','In Placing'
				) THEN duration
				ELSE 0
			END
		) AS time_up,
		sum(
			CASE
				WHEN processstatus IN (
					'Idle','In Reworking','In QC from rework','In Trashing'
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
		20 * 1000
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
 
sqlFile_rows = sqlFile.split("\n")

idealTime = timestep = startDateTime = endsGood = endsBad = timesUp = timesDown = "QUALCOSA"

for row in sqlFile_rows:
	# if not row.find('-- '):
	if not row.startswith('-- '):
	# if not row.startswith('-- ') or not row.find('-- '):

		row = row.replace("\t", "").replace("\n", "")
  
		print(row)
  
		if row.find("20 * 1000"): row = idealTime + "* 1000"
		elif row.find("5 minute"): row = timestep
		elif row.find("2023-01-01T08:00:00Z"): row = startDateTime
		elif row.find("In Placing"): row = endsGood
		elif row.find("In Trashing"): row = endsBad
		elif row.find("'In Picking','In Welding','In QC','In Placing'"): row = timesUp
		elif row.find("'Idle','In Reworking','In QC from rework','In Trashing'"): row = timesDown

		print(row)