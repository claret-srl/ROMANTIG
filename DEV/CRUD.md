
# CRUD Action

## IoT-Agent

### Service Group

#### Creating a Service Group
curl -iX POST \
	'http://localhost:4041/iot/services' \
	-H 'Content-Type: application/json' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' \
	-d '{"services": [{"apikey": "4jggokgpepnvsb2uv4s40d59ov","cbroker": "http://orion:1026","entity_type": "PLC","resource": "/iot/d"}]}'


#### List all Service Groups
curl -X GET \
	'http://localhost:4041/iot/services' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq


#### Read Service Group Details
curl -X GET \
	'http://localhost:4041/iot/services?resource=/iot/d' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq


#### Delete service group
curl -iX DELETE \
	'http://localhost:4041/iot/services/?resource=/iot/d&apikey=4jggokgpepnvsb2uv4s40d59ov' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'

curl -iX DELETE \
	'http://localhost:4041/iot/services/?resource=/iot/opcua&apikey=iot' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'

### Device

#### Creating a Provisioned Device
curl -iX POST \
	'http://localhost:4041/iot/devices' \
	-H 'Content-Type: application/json' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' \
	-d '{
    "devices": [
        {
            "device_id": "plc001",
            "entity_name": "urn:ngsi-v2:Plc:001",
            "entity_type": "Plc",
            "timezone": "Europe/Berlin",
            "attributes": [
                {
                    "object_id": "processStatus",
                    "type": "STRING"
                }
            ],
            "lazy": [],
            "commands": [],
            "static_attributes": []
        }
    ]
}'

#### List all Devices
curl -X GET \
	'http://localhost:4041/iot/devices' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq


#### Read Device Details
curl -X GET \
	'http://localhost:4041/iot/devices/urn:ngsiv2:I40Asset:PLC:001' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq


#### Delete a Provisioned Device
curl -iX DELETE \
	'http://localhost:4041/iot/devices/urn:ngsiv2:I40Asset:PLC:001' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'

curl -iX DELETE \
	'http://localhost:4041/iot/devices/age01_Car' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'


## Orion

### Version
curl -X GET \
	'http://localhost:1026/version'

### Get entities
curl -X GET \
	--url 'http://localhost:1026/v2/entities' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq

### Get types
curl -X GET \
	--url 'http://localhost:1026/v2/types' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq

### Get registrations
curl -X GET \
	--url 'http://localhost:1026/v2/registrations' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq


### Find By relation "hasParentI40Asset" vith value "urn:ngsiv2:I40Asset:Workstation:001"
curl -X GET \
  'http://localhost:1026/v2/entities/?q=hasParentI40Asset==urn:ngsiv2:I40Asset:Workstation:001' | jq


### Find By relation "hasParentI40Asset" vith value "urn:ngsiv2:I40Asset:Area:001"
curl -X GET \
  'http://localhost:1026/v2/entities/?q=hasParentI40Asset==urn:ngsiv2:I40Asset:Area:001' | jq


### Provison an entity
curl -iX POST \
	'http://localhost:1026/v2/entities' \
	-H 'Content-Type: application/json' \
	-d '
{
	"type": "PLC",
	"id": "urn:ngsiv2:I40Asset:PLC:001",
	"Availability": {
        "type": "Text",
        "value": null
    },
	"Performance": {
        "type": "Text",
        "value": null
    },
	"Quality": {
        "type": "Text",
        "value": null
    },
	"OEE": {
        "type": "Text",
        "value": null
    }
}'


### Read Entity details
curl -G -X GET \
	'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' \
	-d 'options=keyValues' | jq


### Read Entity details, where attributes type is PLC
curl -G -X GET \
	'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001/attrs?type=PLC' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' \
	-d 'options=keyValues' | jq

### Get all subscriptions (endpoint: /v2/subscriptions/)
curl -X GET \
	--url 'http://localhost:1026/v2/subscriptions' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq

### Read the detail of a Subscription (endpoint: /v2/subscriptions/<subscription-id>)
curl -X GET \
	--url 'http://localhost:1026/v2/subscriptions/63d62efe603056276828003b' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq

### Edit am Orion Subscription to Quantumleap
curl -iX PATCH \
	--url 'http://localhost:1026/v2/subscriptions/63d62efe603056276828003b' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' \
	-H 'content-type: application/json' \
	-d '{"id": "123456789"}'

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
				"idPattern": ".*",
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
		"attrs": ["processStatus"],
		"metadata": ["dateCreated", "dateModified"]
	},
	"throttling": 1
}'


### Provision a subscription notification to http://tutorial:3000/subscription/oee-change
curl -iX POST \
	--url 'http://localhost:1026/v2/subscriptions' \
	--data '{
	"description": "Notify me of all OEE changes",
	-H 'content-type: application/json' \
	"subject": {
		"entities": [{"idPattern": ".*", "type": "Product"}],
		"condition": {
			"attrs": [ "Availability", "Performance", "Quality", "OEE" ]
			]
		}
	},
	"notification": {
		"http": {
			"url": "http://tutorial:3000/subscription/oee-change"
		}
	}
}'


### Provision a subscription notification to python
curl -iX POST \
	--url 'http://localhost:1026/v2/subscriptions' \
	--data '{
	"description": "Notify me of all OEE changes",
	-H 'content-type: application/json' \
	"subject": {
		"entities": [{"idPattern": ".*", "type": "Product"}],
		"condition": {
			"attrs": [ "Availability", "Performance", "Quality", "OEE" ]
			]
		}
	},
	"notification": {
		"http": {
			"url": "http://localhost:3000/python_websocket_test/"
		}
	}
}'



<!-- ### Get quantumleap subscriptions
curl -X GET \
	--url 'http://localhost:8668/v2/subscriptions' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq -->

http://orion:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001/attrs?type=Device

curl -X GET \
  --url 'http://localhost:1026/v2/entities/urn:ngsi-ld:Product:010?type=Product'
curl -X GET \
  --url 'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001?type=Device'

curl -X GET \
  --url 'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001'

curl -X GET \
  --url 'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001/attrs?type=Device'

/v2/entities/urn:ngsiv2:I40Asset:PLC:001/attrs?type=Device


curl -iX PUT \
  --url 'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001/attrs/processStatus/value' \
  --data "Sto Cazzo"

  -H 'Content-Type: text/plain' \
curl -iX PATCH \
  --url 'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001/attrs' \
  --data ' {
      "processStatus": {"type":"Text", "value": "Un Grande Processo"}
  -H 'Content-Type: application/json' \
}'


curl -X GET \
  --url 'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001/attrs?type=Device'