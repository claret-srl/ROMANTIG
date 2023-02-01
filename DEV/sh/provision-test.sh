#!/bin/bash
curl -iX POST \
  --url "http://${ORION}:${ORION_PORT}/v2/entities" \
  -H "Content-Type: application/json" \
  -H "fiware-service: ${FIWARE_SERVICE}" \
  -H "fiware-servicepath: ${FIWARE_SERVICEPATH}" \
  -d "{
	'type': 'Area',
	'id': 'urn:ngsiv2:I40Asset:Area:001'
}"