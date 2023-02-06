# CRUD Action
## IoT-Agent
### Device

#### Provisioning a Service Group
curl -iX POST \
'http://localhost:4041/iot/services' \
-H 'Content-Type: application/json' \
-H 'fiware-service: opcua_car' \
-H 'fiware-servicepath: /demo' \
-d '{ "services": [{ "apikey": "4jggokgpepnvsb2uv4s40d59ov", "cbroker": "http://orion:1026", "entity_type": "PLC", "resource": "/iot/d" }] }'

#### List Service Groups
curl -X GET \
'http://localhost:4041/iot/services' \
-H 'fiware-service: opcua_car' \
-H 'fiware-servicepath: /demo' | jq

#### Delete service group
curl -iX DELETE \
'http://localhost:4041/iot/services/?resource=/iot/d&apikey=localhost-1026-PLC-/iot/d' \
-H 'fiware-service: opcua_car' \
-H 'fiware-servicepath: /demo'

curl -iX DELETE \
'http://localhost:4041/iot/services/?resource=/iot/d&apikey=orion-1026-PLC-/iot/d' \
-H 'fiware-service: opcua_car' \
-H 'fiware-servicepath: /demo'



    types: {
    PLC: {
      active: [
        {
          name: 'processStatus',
          type: 'Text'
        }
      ],
      lazy: [],
      commands: []
    }
  },
  contexts: [
    {
      id: 'urn:ngsiv2:I40Asset:PLC:001',
      type: 'PLC',
      mappings: [
        {
          ocb_id: 'processStatus',
          opcua_id: 'ns=4;i=198',
          // object_id: 'ns=4;i=198',
          inputArguments: []
        }
      ]
    }
  ],
  contextSubscriptions: [],


#### Provisioning a Device NEW
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
      mappings: [
        {
          ocb_id: 'processStatus',
          opcua_id: 'ns=4;i=198',
          inputArguments: []
        }
      ],
      "attributes": [
        {
          "name": "processStatus",
          "type": "Text"
        }
      ]
    }
  ]
}
'


#### Provisioning a Device OLD
curl -iX POST \
'http://localhost:4041/iot/devices' \
-H 'Content-Type: application/json' \
-H 'fiware-service: opcua_car' \
-H 'fiware-servicepath: /demo' \
-d '{
"devices": [
    {
      "entity_name": "urn:ngsiv2:I40Asset:PLC:001",
      "entity_type": "PLC",
      "device_id": "urn:ngsiv2:I40Asset:PLC:001",
      "apikey": "urn:ngsiv2:I40Asset:PLC:001",
      "endpoint": "opc.tcp://10.0.7.236:4840/",
      "attributes": [
        {
          "object_id": "processStatus",
          "name": "processStatus",
          "type": "Text"
        }
      ],
      "lazy": [],
      "commands": [],
      "static_attributes": [],
      "explicitAttrs": false
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