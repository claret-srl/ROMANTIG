#!/bin/bash
#

set -e

echo -e "\n⏳ Provisioning IoT devices\n"

# ####################################################
# #
# # Provision devices for Orion
# #

curl \
-iX POST 'http://'${ORION}':'${ORION_PORT}'/v2/entities' \
-H 'Content-Type: application/json' \
-H 'fiware-service:'${FIWARE_SERVICE} \
-H 'fiware-servicepath:'${FIWARE_SERVICEPATH} \
-d '{
	"type": "Area",
	"id": "'${DEVICE_BASE_ID}':Area:001"
}'

curl \
-iX POST 'http://'${ORION}':'${ORION_PORT}'/v2/entities' \
-H 'Content-Type: application/json' \
-H 'fiware-service:'${FIWARE_SERVICE} \
-H 'fiware-servicepath:'${FIWARE_SERVICEPATH} \
-d '{
	"type": "Workstation",
	"id": "'${DEVICE_BASE_ID}':Workstation:001"
}'

# ####################################################
# #
# # Provision Relationship
# #

## Workstation hasParent Area
curl \
-iX POST 'http://'${ORION}':'${ORION_PORT}'/v2/op/update' \
-H 'Content-Type: application/json' \
-H 'fiware-service:'${FIWARE_SERVICE} \
-H 'fiware-servicepath:'${FIWARE_SERVICEPATH} \
-d '{
  "actionType": "APPEND",
  "entities": [
    {
      "id": "'${DEVICE_BASE_ID}':Workstation:001",
      "type": "Workstation",
      "hasParentI40Asset": {
        "type": "Relationship",
        "value": "'${DEVICE_BASE_ID}':Area:001"
      }
    }
  ]
}'

## <DEVICE> hasParent Workstation
curl \
-iX POST 'http://'${ORION}':'${ORION_PORT}'/v2/op/update' \
-H 'Content-Type: application/json' \
-H 'fiware-service:'${FIWARE_SERVICE} \
-H 'fiware-servicepath:'${FIWARE_SERVICEPATH} \
-d '{
  "actionType": "APPEND",
  "entities": [
    {
      "id": "'${DEVICE_ID}'",
      "type": "'${DEVICE_TYPE}'",
      "hasParentI40Asset": {
        "type": "Relationship",
        "value": "'${DEVICE_BASE_ID}':Workstation:001"
      }
    }
  ]
}'

# ####################################################
# #
# # Provision subscriptions for QuantumLeap
# #

curl \
-X POST 'http://'${ORION}':'${ORION_PORT}'/v2/subscriptions/' \
-H 'Content-Type: application/json' \
-H 'fiware-service:'${FIWARE_SERVICE} \
-H 'fiware-servicepath:'${FIWARE_SERVICEPATH} \
-d '{
  "description": "'${ORION}' notify '${QUANTUMLEAP}'",
  "subject": {
    "entities": [
      {
		"id": "'${DEVICE_ID}'",
		"type": "'${DEVICE_TYPE}'"
      }
    ],
    "condition": {
      "attrs": [
        "'${OCB_ID}'"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://'${QUANTUMLEAP}':'${QUANTUMLEAP_PORT}'/v2/notify"
    },
    "attrs": [
      "'${OCB_ID}'"
    ]
  }
}'

curl \
-X POST 'http://'${ORION}':'${ORION_PORT}'/v2/subscriptions/' \
-H 'Content-Type: application/json' \
-H 'fiware-service:'${FIWARE_SERVICE} \
-H 'fiware-servicepath:'${FIWARE_SERVICEPATH} \
-d '{
  "description": "'${ORION}' notify '${ROSEAP_OEE}'",
  "subject": {
    "entities": [
      {
		"id": "'${DEVICE_ID}'",
		"type": "'${DEVICE_TYPE}'"
      }
    ],
    "condition": {
      "attrs": [
        "'${OCB_ID}'"
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://'${ROSEAP_OEE}':'${ROSEAP_OEE_PORT}'/v2/notify"
    },
    "attrs": [
      "'${OCB_ID}'"
    ]
  }
}'

echo -e "\n\033[1;32mdone\033[0m\n"
