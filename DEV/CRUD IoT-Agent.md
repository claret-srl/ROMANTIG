# CRUD Action
## IoT-Agent
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
      "device_id": "urn:ngsiv2:I40Asset:PLC:001",
      "type": "PLC",
      "attributes": [
        {
          "name": "processStatus",
          "type": "Text"
        }
      ]
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