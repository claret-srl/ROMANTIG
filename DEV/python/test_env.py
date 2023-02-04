import os
from dotenv import load_dotenv


script_dir = os.path.dirname(__file__)
load_dotenv(script_dir + "//" + ".env")

" + PLACE_HOLDER + "
ENDSGOOD = os.getenv('ENDSGOOD')
ENDSBAD = os.getenv('ENDSBAD')
TIMESUP = os.getenv('TIMESUP')
TIMESDOWN = os.getenv('TIMESDOWN')
TIMESTEP = os.getenv('TIMESTEP')
IDEALTIME = os.getenv('IDEALTIME')
OEE_START_DATE = os.getenv('OEE_START_DATE')
OEE_START_TIME = os.getenv('OEE_START_TIME')

COMPOSE_PROJECT_NAME = os.getenv('COMPOSE_PROJECT_NAME')
CONTEXTS_ID = os.getenv('CONTEXTS_ID')
CONTEXTS_TYPE = os.getenv('CONTEXTS_TYPE')
CRATE_PORT_ADMIN = os.getenv('CRATE_PORT_ADMIN')
CRATE_PORT_TRANSPORT_PROTOCOL = os.getenv('CRATE_PORT_TRANSPORT_PROTOCOL')
CRATE_PORT_DATA = os.getenv('CRATE_PORT_DATA')
# I don't think they are used
# CRATE_SCHEMA = os.getenv('CRATE_SCHEMA')
# CRATE_TABLE = os.getenv('CRATE_TABLE')
DEVICE_ID = os.getenv('DEVICE_ID')
DEVICE_TYPE = os.getenv('DEVICE_TYPE')
FIWARE_SERVICE = os.getenv('FIWARE_SERVICE')
FIWARE_SERVICEPATH = os.getenv('FIWARE_SERVICEPATH')
GRAFANA_PORT = os.getenv('GRAFANA_PORT')
IOTA_NORTH_PORT = os.getenv('IOTA_NORTH_PORT')
IOTA_SOUTH_PORT = os.getenv('IOTA_SOUTH_PORT')
MONGO_DB_PORT = os.getenv('MONGO_DB_PORT')
ORION_PORT = os.getenv('ORION_PORT')
QUANTUMLEAP_PORT = os.getenv('QUANTUMLEAP_PORT')
REDIS_PORT = os.getenv('REDIS_PORT')
ROSEAP_OEE_PORT = os.getenv('ROSEAP_OEE_PORT')

ROSEAP_OEE = os.getenv('ROSEAP_OEE')
ORION = os.getenv('ORION')
MONGO = os.getenv('MONGO')
QUANTUMLEAP = os.getenv('QUANTUMLEAP')
CRATE = os.getenv('CRATE')
REDIS = os.getenv('REDIS')
GRAFANA = os.getenv('GRAFANA')

print(DEVICE_ID)