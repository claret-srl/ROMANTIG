import os
from sys import argv
import configparser
from dotenv import load_dotenv


if len(argv) >= 1:
    DEVICE_TYPE_NEW = argv[1] # bisogna rinominare il vecchio DEVICE_TYPE altrimenti non lo sostituisce
else:
    print("Please provide a new Context Type Name as argument.")

script_dir = os.path.dirname(__file__)


# <-- Units to Seconds

SECONDS_PER_UNIT = {
    "second": 1,
    "minute": 60,
    "hour": 60 * 60,
    "day": 60 * 60 * 24,
    "week": 60 * 60 * 24 * 7,
    "month": 60 * 60 * 24 * 7 * 30,
    "year": 60 * 60 * 24 * 7 * 365,
}


def convert_to_seconds(s):
    s = s.split(" ")
    return int(s[0]) * SECONDS_PER_UNIT[s[1]]


# Units to Seconds -->
# <-- Configuration

def envArrayToString(_Array):
    output = str()
    spacing = ", "
    spacingLen = len(spacing)

    _Array = _Array.split(",")

    for element in _Array :
        element = element.strip()
        if len(element) != 0:
            output += f"'{element}'" + spacing

    if output[-spacingLen:] == spacing:
        output = output[:-spacingLen]

    return output


config = configparser.ConfigParser()
config.read(script_dir + "//" + ".config")

TIMESUP = envArrayToString(config["MACHINE_STATES"]["TIMESUP"])
TIMESDOWN = envArrayToString(config["MACHINE_STATES"]["TIMESDOWN"])
ENDSGOOD = envArrayToString(config["MACHINE_STATES"]["ENDSGOOD"])
ENDSBAD = envArrayToString(config["MACHINE_STATES"]["ENDSBAD"])
STARTDATETIME = (config["TIMING"]["START_DATE"] + "T" + config["TIMING"]["START_TIME"] + "Z")
IDEALTIME = str(convert_to_seconds(config["TIMING"]["IDEALTIME"]))
TIMESTEP = str(config["TIMING"]["TIMESTEP"])

# <-- .env

load_dotenv(script_dir + "//" + ".env")

LOG_LEVEL = os.getenv("LOG_LEVEL")  # debug

COMPOSE_PROJECT_NAME = os.getenv("COMPOSE_PROJECT_NAME")  # fiware
ORG_FIWARE = os.getenv("ORG_FIWARE")  # claret-romantig

CONTEXTS_ID = os.getenv("CONTEXTS_ID")  # age01_Car

DEVICE_BASE_ID = os.getenv("DEVICE_BASE_ID")  # urn:ngsiv2:I40Asset
DEVICE_ID = os.getenv("DEVICE_ID")  # urn:ngsiv2:I40Asset:PLC:001
DEVICE_TYPE = os.getenv("DEVICE_TYPE")  # PLC
OCB_ID = os.getenv("OCB_ID")  # processStatus

FIWARE_SERVICE = os.getenv("FIWARE_SERVICE")  # opcua_car
FIWARE_SERVICEPATH = os.getenv("FIWARE_SERVICEPATH")  # /demo

IOTA = os.getenv("IOTA")  # iot-agent
IOTA_NORTH_PORT = os.getenv("IOTA_NORTH_PORT")  # 4041
IOTA_SOUTH_PORT = os.getenv("IOTA_SOUTH_PORT")  # 9229
OPCUA_ID = os.getenv("OPCUA_ID")  # "ns=4;i=198"

ORION = os.getenv("ORION")  # orion
ORION_PORT = os.getenv("ORION_PORT")  # 1026

QUANTUMLEAP = os.getenv("QUANTUMLEAP")  # quantumleap
QUANTUMLEAP_PORT = os.getenv("QUANTUMLEAP_PORT")  # 8668

ROSEAP_OEE = os.getenv("ROSEAP_OEE")  # oee-service
ROSEAP_OEE_PORT = os.getenv("ROSEAP_OEE_PORT")  # 8008

CRATE = os.getenv("CRATE")  # db-crate
CRATE_PORT_ADMIN = os.getenv("CRATE_PORT_ADMIN")  # 4200
CRATE_PORT_POSTGRES = os.getenv("CRATE_PORT_POSTGRES")  # 5432
CRATE_PORT_TRANSPORT_PROTOCOL = os.getenv("CRATE_PORT_TRANSPORT_PROTOCOL")  # 4300
CRATE_SCHEMA = os.getenv("CRATE_SCHEMA")  # mtopcua_car
CRATE_TABLE = os.getenv("CRATE_TABLE")  # etdevice
CRATE_TABLE_DEVICE = os.getenv("CRATE_TABLE_DEVICE")  # etdevice
CRATE_TABLE_DURATION = os.getenv("CRATE_TABLE_DURATION")  # etprocessduration
CRATE_TABLE_OEE = os.getenv("CRATE_TABLE_OEE")  # etoee

MONGO = os.getenv("MONGO")  # db-mongo
MONGO_PORT = os.getenv("MONGO_PORT")  # 27017

REDIS = os.getenv("REDIS")  # db-redis
REDIS_PORT = os.getenv("REDIS_PORT")  # 6379

GRAFANA = os.getenv("GRAFANA")  # grafana
GRAFANA_PORT = os.getenv("GRAFANA_PORT")  # 3000

def replace_in_string(replaces, dirSurce, dirTarget):
    with open(f"{script_dir}\{dirSurce}", "r") as inputFile:
        fileContent = inputFile.read()

    for key, value in replaces.items():
        fileContent = fileContent.replace(key, value.lower())

    with open(f"{script_dir}\{dirTarget}", "w") as outputFile:
        outputFile.write(fileContent)

replacesGrafana = {
    "mtopcua_car": CRATE_SCHEMA,
    "process_status_oee": CRATE_TABLE_OEE,
    "etplc": CRATE_TABLE_DEVICE
}

replace_in_string(replacesGrafana, "..\\grafana\\dashboards\\dashboard.src", "..\\grafana\\dashboards\\dashboard.json")

