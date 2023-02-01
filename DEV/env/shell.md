# Project name
${COMPOSE_PROJECT_NAME}=fiware
${ORG_FIWARE}=claret-romantig
${LOG_LEVEL}=debug

# Rose-AP OEE variables
${ROSEAP_OEE}=oee-service
${ROSEAP_OEE_PORT}=8008
${DEVICE_ID}=urn:ngsiv2:I40Asset:PLC:001
${OCB_ID}=processStatus
${OPCUA_ID}="ns=4;i=198"


# ${ROSEAP_OEE_CONTAINER}=True

# Orion variables
${ORION}=orion
${ORION_PORT}=1026

# MongoDB variables
${MONGO}=db-mongo
${MONGO_PORT}=27017

# IoT Agent OPC-UA Variables
${IOTA}=iot-agent
${IOTA_NORTH_PORT}=4041
${IOTA_SOUTH_PORT}=9229

# QuantumLeap Variables
${QUANTUMLEAP}=quantumleap
${QUANTUMLEAP_PORT}=8668

# CrateDB
${CRATE_SCHEMA}=mtopcua_car					# I don't think they are used --> Used in pyhon and Query.sql
${CRATE_TABLE}=etdevice						# I don't think they are used --> Used in pyhon and Query.sql
${CRATE_TABLE_DURATION}=etprocessduration	# I don't think they are used --> Used in pyhon and Query.sql
${CRATE_TABLE_OEE}=etoee					# I don't think they are used --> Used in pyhon and Query.sql
${CRATE}=db-crate
${CRATE_PORT_ADMIN}=4200
${CRATE_PORT_TRANSPORT_PROTOCOL}=4300
${CRATE_PORT_POSTGRES}=5432


# RedisDB Version
${REDIS}=db-redis
${REDIS_PORT}=6379

# fiware
${FIWARE_SERVICE}=opcua_car
${FIWARE_SERVICEPATH}=/demo

# Contexts
${CONTEXTS_ID}=age01_Car
${CONTEXTS_TYPE}=PLC


# Grafana
${GRAFANA}=grafana
${GRAFANA_PORT}=3000

# Superset
# ${SUPERSET_PORT}=3004
