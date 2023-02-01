#!/bin/bash
set -e
# Set enviroment from .env file
setEnviroment () {
	export $(cat .env | grep "#" -v)
}

setEnviroment

docker run --rm -v $(pwd)/provision-devices:/provision-devices \
	--network fiware_default \
	-e ORION="${ORION}" \
	-e ORION_PORT="${ORION_PORT}" \
	-e IOTA_NORTH_PORT="${IOTA_NORTH_PORT}" \
	-e FIWARE_SERVICE="${FIWARE_SERVICE}" \
	-e FIWARE_SERVICEPATH="${FIWARE_SERVICEPATH}" \
	-e DEVICE_ID="${DEVICE_ID}" \
	-e FIWARE_SERVICE="${FIWARE_SERVICE}" \
	-e FIWARE_SERVICEPATH="${FIWARE_SERVICEPATH}" \
	-e OCB_ID="${OCB_ID}" \
	-e OPCUA_ID="${OPCUA_ID}" \
	--entrypoint /bin/ash curlimages/curl provision-devices