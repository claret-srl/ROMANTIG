SELECT start_date AS "time",
oee AS "OEE",
availability AS "Availability",
performance AS "Performance",
quality AS "Quality"
FROM oee
ORDER BY 1
LIMIT 100;

SELECT
start_date AS "Time Start",
end_date AS "Time End",
num_prod AS "Parts Produced",
num_good AS "Parts Good",
num_bad AS "Parts Bad",
up_time AS "Time Up",
down_time AS "Time Down",
oee AS "OEE",
availability AS "Availability",
performance AS "Performance",
quality AS "Quality"
FROM "mtopcua_car"."oee"
LIMIT 100;