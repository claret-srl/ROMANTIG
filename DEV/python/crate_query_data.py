from crate import client


connection = client.connect("localhost:4200/", error_trace=True) # crate:4200/
cursor = connection.cursor()

query = """SELECT entity_id, entity_type, time_index, fiware_servicepath, __original_ngsi_entity__, instanceid, processstatus FROM "mtopcua_car"."etdevice" LIMIT 100;"""
# query = """SELECT entity_id, entity_type, time_index, fiware_servicepath, __original_ngsi_entity__, instanceid, processstatus FROM "mtopcua_car"."etdevice";"""

cursor.execute(query)

records = cursor.fetchall()

print(records, len(records))