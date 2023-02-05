SELECT "processstatus", count(*) as count
FROM (
SELECT "entity_id", "processstatus", "time_index",
lag("processstatus", -2, NULL)
OVER (ORDER BY "time_index" DESC)
as prev_status
FROM "mtopcua_car"."etplc"
) as subq
WHERE prev_status = 'In Reworking' AND entity_id = 'urn:ngsiv2:I40Asset:PLC:001'
GROUP BY "processstatus";



SELECT COUNT(*) 
FROM "mtopcua_car"."etplc" 
WHERE (processstatus = 'In Placing' OR processstatus = 'In Trashing') 
AND "time_index" > (
  SELECT "time_index" 
  FROM "mtopcua_car"."etplc" 
  WHERE processstatus = 'In Reworking' 
  ORDER BY "time_index" DESC 
  LIMIT 1, 1
);


SELECT COUNT(*) AS qualcosa FROM (
  SELECT 
    "entity_id", "processstatus", "time_index",
    lag("processstatus", -2)
    OVER (ORDER BY "time_index" DESC)
    as prev_status
    FROM "mtopcua_car"."etplc" order by "time_index") AS subquery WHERE (processstatus = 'In Placing' OR processstatus = 'In Trashing')  limit 100;