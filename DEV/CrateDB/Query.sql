SELECT
processstatus,
time_index,
time_index - LAG(time_index, -1, time_index) OVER (ORDER BY time_index DESC) AS duration
FROM "mtopcua_car"."etplc"
ORDER BY time_index DESC;

-- Crea la tabella con la durata dei processi
CREATE TABLE "mtopcua_car"."any_table_ident" AS
SELECT
processstatus,
time_index,
time_index - LAG(time_index, -1, time_index) OVER (ORDER BY time_index DESC) AS duration
FROM "mtopcua_car"."etplc"
ORDER BY time_index DESC;

SELECT * FROM "mtopcua_car"."any_table_ident"

DROP TABLE "mtopcua_car"."any_table_ident"

-- Aggiorna la tabella con la durata dei processi considerando solo i dati non presenti
INSERT INTO "mtopcua_car"."any_table_ident"
SELECT
processstatus,
time_index,
time_index - LAG(time_index, -1, time_index) OVER (ORDER BY time_index DESC) AS duration FROM "mtopcua_car"."etplc" newDataTable
WHERE NOT EXISTS (SELECT time_index FROM "mtopcua_car"."any_table_ident" WHERE time_index = newDataTable.time_index) limit 10000;

SELECT
processstatus,
SUM(duration), count(duration) AS total_duration
FROM "mtopcua_car"."any_table_ident"
GROUP BY processstatus limit 100;

SELECT count(*), date_trunc('day', time_index) as "day" FROM "mtopcua_car"."etplc" group by "day" limit 100;
SELECT count(*), date_bin('day', time_index, [[[[ORIGIN]]]] ) as "day" FROM "mtopcua_car"."etplc" group by "day" limit 100;

https://crate.io/docs/crate/reference/en/5.1/general/builtins/scalar-functions.html#date-trunc-interval-timezone-timestamp

timeindex raggruppato per giorno