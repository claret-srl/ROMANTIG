#!/bin/bash
#
#  curl commands to reload the data
#
#

set -e

# # Set enviroment from .env file
# setEnviroment () {
# 	export $(cat .env | grep "#" -v)
# }

# setEnviroment

# printf "⏳ Deleting the slef provisioned service-gropu and device from OPC-UA IoT-Agent"

# curl -iX DELETE \
#   "http://localhost:4041/iot/services/?resource=/iot/opcua&apikey=iot" \
#   -H "fiware-service: ${FIWARE_SERVICE}" \
#   -H "fiware-servicepath: ${FIWARE_SERVICEPATH}"

printf "⏳ Provisioning IoT devices "

# ####################################################
# #
# # Create a Service Groups for all OPC-UA IoT devices
##

# curl -s -o /dev/null -X POST \
#   "http://iot-agent:4041/iot/services" \
#   -H "Content-Type: application/json" \
#   -H "fiware-service: ${FIWARE_SERVICE}" \
#   -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
#   -d "{
#  'services': [
#    {
#      'apikey':      '1068318794',
#      'cbroker':     'http://${ORION}:${ORION_PORT}',
#      'entity_type': 'Device',
#      'resource':    '/iot/d'    
#    }
#  ]
# }"

# "entity_type": "PLC",

# ####################################################
# #
# # Provision devices for Orion
# #

## Area
printf "\nProvisioning IoT devices [1]"

curl -iX POST \
  "http://${ORION}:${ORION_PORT}/v2/entities" \
  -H "Content-Type: application/json" \
  -H "fiware-service: ${FIWARE_SERVICE}" \
  -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
  -d "{
	'type': 'Area',
	'id': 'urn:ngsiv2:I40Asset:Area:001'
}"

## Workstation
printf "\nProvisioning IoT devices [2]"

curl -iX POST \
  "http://${ORION}:${ORION_PORT}/v2/entities" \
  -H "Content-Type: application/json" \
  -H "fiware-service: ${FIWARE_SERVICE}" \
  -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
  -d "{
	'type': 'Workstation',
	'id': 'urn:ngsiv2:I40Asset:Workstation:001'
}"
# ## PLC - Should be already provisioned by the IoT Agent

# curl -iX POST \
#   "http://${ORION}:${ORION_PORT}/v2/entities" \
#   -H "fiware-service: ${FIWARE_SERVICE}" \
#   -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
#   -H "Content-Type: application/json" \
#   -d "
# {
# 	'type': 'PLC',
# 	'id': '${DEVICE_ID}'
# }"

## PLC - Add OEE attributes
printf "\nProvisioning IoT devices [3]"

curl -iX POST \
  "http://${ORION}:${ORION_PORT}/v2/entities/${DEVICE_ID}/attrs" \
  -H "Content-Type: application/json" \
  -H "fiware-service: ${FIWARE_SERVICE}" \
  -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
  -d "{
	'Availability': {
		'type': 'Float',
		'value': null
	},
	'Performance': {
		'type': 'Float',
		'value': null
	},
	'Quality': {
		'type': 'Float',
		'value': null
	},
	'OEE': {
		'type': 'Float',
		'value': null
	}
}"


# ####################################################
# #
# # Provision Relationship
# #

## Workstation hasParent Area
printf "\nProvisioning IoT devices [4]"

curl -iX POST \
  "http://${ORION}:${ORION_PORT}/v2/op/update" \
  -H "Content-Type: application/json" \
  -H "fiware-service: ${FIWARE_SERVICE}" \
  -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
  -d "{
  'actionType': 'APPEND',
  'entities': [
    {
      'id': 'urn:ngsiv2:I40Asset:Workstation:001',
      'type': 'PLC',
      'hasParentI40Asset': {
        'type': 'Relationship',
        'value': 'urn:ngsiv2:I40Asset:Area:001'
      }
    }
  ]
}"

## PLC hasParent Workstation
printf "\nProvisioning IoT devices [5]"

curl -iX POST \
  "http://${ORION}:${ORION_PORT}/v2/op/update" \
  -H "Content-Type: application/json" \
  -H "fiware-service: ${FIWARE_SERVICE}" \
  -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
  -d "{
  'actionType': 'APPEND',
  'entities': [
    {
      'id': ${DEVICE_ID},
      'type': 'PLC',
      'hasParentI40Asset': {
        'type': 'Relationship',
        'value': 'urn:ngsiv2:I40Asset:Workstation:001'
      }
    }
  ]
}"


# ####################################################
# #
# # Provision subscriptions for QuantumLeap
# #
printf "\nProvisioning IoT devices [6]"


curl -s -o /dev/null -X POST \
	"http://${ORION}:${ORION_PORT}/v2/subscriptions" \
	-H "Content-Type: application/json" \
	-H "fiware-service: ${FIWARE_SERVICE}" \
	-H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
	-d "{
  'description': 'Orion notify Quantumleap',
  'subject': {
    'entities': [
      {
        'idPattern': '.*',
        'type': 'PLC'
      }
    ],
    'condition': {
      'attrs': [
        ${OCB_ID}
      ]
    }
  },
  'notification': {
    'http': {
      'url': 'http://quantumleap:8668/v2/notify'
    },
    'attrs': [
      ${OCB_ID}
    ],
    'metadata': [
      'dateCreated',
      'dateModified'
    ]
  },
  'throttling': 1
}"

printf "\nProvisioning IoT devices [7]"

curl -s -o /dev/null -X POST \
	"http://${ORION}:${ORION_PORT}/v2/subscriptions" \
	-H "Content-Type: application/json" \
	-H "fiware-service: ${FIWARE_SERVICE}" \
	-H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
	-d "{
  'description': 'Orion notify the oee-service',
  'subject': {
    'entities': [
      {
        'idPattern': '.*',
        'type': 'PLC'
      }
    ],
    'condition': {
      'attrs': [
        ${OCB_ID}
      ]
    }
  },
  'notification': {
    'http': {
      'url': 'http://oee-service:8008/'
    },
    'attrs': [
      ${OCB_ID}
    ],
    'metadata': [
      'dateCreated',
      'dateModified'
    ]
  },
  'throttling': 1
}"


# ####################################################
# #
# # Provision Sensors
# #


echo -e " \033[1;32mdone\033[0m"