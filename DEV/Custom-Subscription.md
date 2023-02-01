## CrateDB

curl -iX POST \
 'http://localhost:4200/\_sql' \
 -H 'Content-Type: application/json' \
 -d '{"stmt":"SELECT oee, availability, performance, quality FROM mtopcua_car.process_status_oee LIMIT 1;"}'

{
	"cols":[
		"oee",
		vailability",
		"performance",
		"quality"
		],
	"rows":[
		[
			0.337986164407029805451858502940435594146027098682,
			0.7256200821785637,
			0.5988721241661537,
			0.7777777777777778
		]
	],
	"rowcount":1,
	"duration":5.9293
}

### Provision a subscription notification to Quantumleap

curl -s -o /dev/null -X POST \
 'http://orion:1026/v2/subscriptions/' \
 -H 'fiware-service: opcua_car' \
 -H 'fiware-servicepath: /demo' \
 -H 'Content-Type: application/json' \
 -d '{
"description": "Provision subscriptions for QuantumLeap",
"subject": {
"entities": [
	{
	"id": "urn:ngsiv2:I40Asset:PLC:001",
	"type": "PLC"
	}
],
"condition": {
"attrs": ["processStatus"]
}
},
"notification": {
"http": {
"url": "http://quantumleap:8668/v2/notify"
},
"attrs": [
		"oee": ${oee},
		"availability": ${availability},
		"performance": ${performance},
		"quality": ${quality}
		],
"metadata": ["dateCreated", "dateModified"]
},
"throttling": 1
}'



curl -iX POST \
 'http://localhost:4200/\_sql' \
 -H 'Content-Type: application/json' \
 -d '{"stmt":"SELECT oee, availability, performance, quality FROM mtopcua_car.process_status_oee LIMIT 1;"}'
 

curl -s -o /dev/null -X POST \
 'http://orion:1026/v2/subscriptions/' \
 -H 'fiware-service: opcua_car' \
 -H 'fiware-servicepath: /demo' \
 -H 'Content-Type: application/json' \
 -d '{
"description": "Provision subscriptions for QuantumLeap",
"subject": {
"entities": [
	{
	"id": "urn:ngsiv2:I40Asset:PLC:001",
	"type": "PLC"
	}
],
"condition": {
"attrs": ["processStatus"]
}
},
"notification": {
"httpCustom": {
  curl -iX POST \
 'http://localhost:4200/\_sql' \
 -H 'Content-Type: application/json' \
 -d '{"stmt":"SELECT oee, availability, performance, quality FROM mtopcua_car.process_status_oee LIMIT 1;"}'
}
"http": {
"url": "http://quantumleap:8668/v2/notify"
},
"attrs": [
		"oee": ${oee},
		"availability": ${availability},
		"performance": ${performance},
		"quality": ${quality}
		],
"metadata": ["dateCreated", "dateModified"]
},
"throttling": 1
}'