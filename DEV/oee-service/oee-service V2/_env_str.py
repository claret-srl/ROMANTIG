LOG_LEVEL = os.getenv('LOG_LEVEL') # debug

COMPOSE_PROJECT_NAME = os.getenv('COMPOSE_PROJECT_NAME') # fiware
ORG_FIWARE = os.getenv('ORG_FIWARE') # claret-romantig

CONTEXTS_ID = os.getenv('CONTEXTS_ID') # age01_Car
CONTEXTS_TYPE = os.getenv('CONTEXTS_TYPE') # PLC

DEVICE_BASE_ID = os.getenv('DEVICE_BASE_ID') # urn:ngsiv2:I40Asset
DEVICE_ID = os.getenv('DEVICE_ID') # urn:ngsiv2:I40Asset:PLC:001
DEVICE_TYPE = os.getenv('DEVICE_TYPE') # PLC
OCB_ID = os.getenv('OCB_ID') # processStatus

FIWARE_SERVICE = os.getenv('FIWARE_SERVICE') # opcua_car
FIWARE_SERVICEPATH = os.getenv('FIWARE_SERVICEPATH') # /demo

IOTA = os.getenv('IOTA') # iot-agent
IOTA_NORTH_PORT = os.getenv('IOTA_NORTH_PORT') # 4041
IOTA_SOUTH_PORT = os.getenv('IOTA_SOUTH_PORT') # 9229
OPCUA_ID = os.getenv('OPCUA_ID') # "ns=4;i=198"

ORION = os.getenv('ORION') # orion
ORION_PORT = os.getenv('ORION_PORT') # 1026

QUANTUMLEAP = os.getenv('QUANTUMLEAP') # quantumleap
QUANTUMLEAP_PORT = os.getenv('QUANTUMLEAP_PORT') # 8668

ROSEAP_OEE = os.getenv('ROSEAP_OEE') # oee-service
ROSEAP_OEE_PORT = os.getenv('ROSEAP_OEE_PORT') # 8008

CRATE = os.getenv('CRATE') # db-crate
CRATE_PORT_ADMIN = os.getenv('CRATE_PORT_ADMIN') # 4200
CRATE_PORT_POSTGRES = os.getenv('CRATE_PORT_POSTGRES') # 5432
CRATE_PORT_TRANSPORT_PROTOCOL = os.getenv('CRATE_PORT_TRANSPORT_PROTOCOL') # 4300

CRATE_SCHEMA = os.getenv('CRATE_SCHEMA') # mtopcua_car # I don't think they are used
CRATE_TABLE = os.getenv('CRATE_TABLE') # etdevice # I don't think they are used
CRATE_TABLE_DURATION = os.getenv('CRATE_TABLE_DURATION') # etprocessduration		# I don't think they are used --> Used in pyhon and Query.sql
CRATE_TABLE_OEE = os.getenv('CRATE_TABLE_OEE') # etoee	

MONGO = os.getenv('MONGO') # db-mongo
MONGO_PORT = os.getenv('MONGO_PORT') # 27017

REDIS = os.getenv('REDIS') # db-redis
REDIS_PORT = os.getenv('REDIS_PORT') # 6379

GRAFANA = os.getenv('GRAFANA') # grafana
GRAFANA_PORT = os.getenv('GRAFANA_PORT') # 3000