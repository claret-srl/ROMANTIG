# Creating a Service Group
curl -iX POST \
	'http://localhost:4041/iot/services' \
	-H 'Content-Type: application/json' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' \
	-d '{"services": [{"apikey": "4jggokgpepnvsb2uv4s40d59ov","cbroker": "http://orion:1026","entity_type": "Device","resource": "/iot/d"}]}'

# List all Service Groups
curl -X GET \
	'http://localhost:4041/iot/services' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq

# Read Service Group Details
curl -X GET \
	'http://localhost:4041/iot/services?resource=/iot/d' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq

# Delete service group
curl -iX DELETE \
	'http://localhost:4041/iot/services/?resource=/iot/d&apikey=4jggokgpepnvsb2uv4s40d59ov' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'

curl -iX DELETE \
	'http://localhost:4041/iot/services/?resource=/iot/opcua&apikey=iot' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'

# Creating a Provisioned Device
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

# List all Device
curl -X GET \
	'http://localhost:4041/iot/devices' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo' | jq

# Delete a Provisioned Device
curl -iX DELETE \
	'http://localhost:4041/iot/devices/plc001' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'

curl -iX DELETE \
	'http://localhost:4041/iot/devices/age01_Car' \
	-H 'fiware-service: opcua_car' \
	-H 'fiware-servicepath: /demo'