import configparser
from crate import client
import pycurl
from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv
# import json
import os
from dotenv import load_dotenv

import _query
# import _dataTemplate
import _curl_calls

# <-- Docker
Docker = True
# Docker = True
Debug = False
# Docker -->


script_dir = os.path.dirname(__file__)


# <-- nickjj Web server https://github.com/nickjj/webserver


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        updateContexBroker()

        if Debug:
            print("[INFO]" + "[WebServer]" + "Headers:" + "\n")
            print(self.headers)
            print("[INFO]" + "[WebServer]" + "Content:" + "\n")
            print(content.decode("utf-8"))

    def do_GET(self):
        self.write_response(b"")

    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)
        self.write_response(body)


def httpWebServer(_BIND_HOST="0.0.0.0", _PORT=8008):
    try:
        httpd = HTTPServer((_BIND_HOST, _PORT), SimpleHTTPRequestHandler)
        print("[INFO]" + "[WebServer]" + f"Listening on http://{_BIND_HOST}:{_PORT}\n")
        httpd.serve_forever()
    except Exception as e:
        print(
            "[ERROR]"
            + "[WebServer]"
            + f"Fail on http://{_BIND_HOST}:{_PORT}\n"
            + str(e)
            + "\n"
        )


# nickjj Web server > https://github.com/nickjj/webserver -->
# <-- Crate-DB


def query_CrateDB(_sqlCommands):
    try:
        print("[INFO]" + "[CrateDB]" + "Connecting...")
        connection = client.connect(CRATE + ":" + CRATE_PORT_ADMIN, error_trace=True)
        print("[INFO]" + "[CrateDB]" + "Connection Successful.")
        try:
            cursor = connection.cursor()
            print("[INFO]" + "[CrateDB]" + "Cursor created." + "\n")
            # print(_sqlCommands)
            for command in _sqlCommands:
                # print(command)
                try:
                    cursor.execute(command)
                    if command.startswith("SELECT"):
                        records = cursor.fetchall()
                        return records
                    print("[INFO]" + "[CrateDB]" + "Exectuded query -->\n")
                except Exception as e:
                    print(
                        "[ERROR]"
                        + "[CrateDB]"
                        + "Error in query execution:\n"
                        + str(e)
                        + "\n"
                    )
                print(command + "\n")
                print(
                    "#####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  ##### \n"
                )
        except Exception as e:
            print(
                "[ERROR]" + "[CrateDB]" + "Error in cursor creation:\n" + str(e) + "\n"
            )
        finally:
            cursor.close()
            print("[INFO]" + "[CrateDB]" + "Cursor Closed.")
            connection.close()
            print("[INFO]" + "[CrateDB]" + "Connection Closed.")
    except Exception as e:
        print("[ERROR]" + "[CrateDB]" + "Connection fail:\n" + str(e) + "\n")


# Crate-DB -->
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
# <-- Update Orion Contex Broker

def updateContexBroker():
    oeeCallBackQuery = _query.oeeCallBack(CRATE_SCHEMA, CRATE_TABLE_OEE)
    oeeCallBackQueryResults = query_CrateDB([oeeCallBackQuery])
    # oeeCallBackQueryResultsDataTemplate = _dataTemplate.append_ARGS(oeeCallBackQueryResults)
    cUrl_call = _curl_calls.update_ARGS(ORION, ORION_PORT, Service, ServicePath, contentType, DEVICE_ID, DEVICE_TYPE, oeeCallBackQueryResults)
    curl_calls_function(cUrl_call)

# Update Orion Contex Broker -->
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


# cUrl Calls
def curl_call(_cursor, _method, _url, _header=None, _payload=None):
    try:
        _cursor.reset()
        _cursor.setopt(_cursor.URL, _url)
        _cursor.setopt(_cursor.CUSTOMREQUEST, _method)
        if _header:
            _cursor.setopt(_cursor.HTTPHEADER, _header)
        if _payload:
            _cursor.setopt(_cursor.POSTFIELDS, _payload)
        _cursor.perform()
    except Exception as e:
        print("[ERROR]" + "[cUrl]" + "Error in cUrl execution:\n" + str(e) + "\n")


def curl_calls_function(_cUrl_calls, _payload_OverRide=False):
    try:
        cursor = pycurl.Curl()
        print("[INFO]" + "[cUrl]" + "Cursor created:\n")
        for call in _cUrl_calls:
            try:         
                paths = [call['NGSI'], call['endpoint'], call['path']]
                pathFiltered = []
                for path in paths:
                    if path != None:
                        pathFiltered.append(path)
                urlSeparator = "/"
                urlPath = urlSeparator.join(pathFiltered)

                url = f"http://{call['service']}:{call['port']}/{urlPath}"
 
                print(
                    "\n #####   #####   #####   #####   #####   #####   #####   #####   ##### \n"
                )

                # print(url, "\n")
                # print(call, "\n")
                print(f"curl {call['method']} \\")
                print(f"{url} \\")
                for header in call["header"]:
                    print(f"-H {header} \\")

                if _payload_OverRide == False:
                    print(f"-d {call['payload']}", "\n")
                    curl_call(
                        cursor, call["method"], url, call["header"], call["payload"]
                    )
                else:
                    print(f"-d {_payload_OverRide}", "\n")
                    curl_call(
                        cursor, call["method"], url, call["header"], _payload_OverRide
                    )

                print(
                    "\n #####   #####   #####   #####   #####   #####   #####   #####   ##### \n"
                )
            except Exception as e:
                print(
                    "[ERROR]" + "[cUrl]" + "Error in cUrl execution:\n" + str(e) + "\n"
                )
        cursor.close()
    except Exception as e:
        print("[ERROR]" + "[cUrl]" + "Error in cUrl execution:\n" + str(e) + "\n")


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
CONTEXTS_TYPE = os.getenv("CONTEXTS_TYPE")  # PLC

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

# ROSEAP_OEE_CONTAINER = os.getenv('ROSEAP_OEE_CONTAINER')

# .env -->


print(f"[INFO] Timestep is {TIMESTEP}.")

# Configuration -->
# <-- Script
# <-- Docker

if Docker == False:
    ORION = IOTA = CRATE = BIND_HOST = "localhost"
else:
    BIND_HOST = "0.0.0.0"

PORT = 8008

# Docker -->
# <-- Main Variables

if len(argv) > 1:
    arg = argv[1].split(":")
    BIND_HOST = arg[0]
    PORT = int(arg[1])
    
Service = f"fiware-service: {FIWARE_SERVICE}"
ServicePath = f"fiware-servicepath: {FIWARE_SERVICEPATH}"
contentType = {"json": "Content-Type: application/json"}

# Main Variables -->
# <-- External Variables

processDuration = _query.processDuration(
	CRATE_SCHEMA,
	CRATE_TABLE_DURATION,
	OCB_ID,
	DEVICE_ID,
	CRATE_TABLE_DEVICE
)

oee = _query.oee(
    CRATE_SCHEMA,
    CRATE_TABLE_OEE,
    CRATE_TABLE_DURATION,
    OCB_ID,
    ENDSGOOD,
    ENDSBAD,
    TIMESUP,
    TIMESDOWN,
    IDEALTIME,
    TIMESTEP,
    STARTDATETIME,
)

provisioning_ARGS = _curl_calls.provisioning_ARGS(
    IOTA,
    IOTA_NORTH_PORT,
    ORION,
    ORION_PORT,
    DEVICE_BASE_ID,
    DEVICE_ID,
    DEVICE_TYPE,
    OCB_ID,
    ROSEAP_OEE,
    ROSEAP_OEE_PORT,
    QUANTUMLEAP,
    QUANTUMLEAP_PORT,
    Service,
    ServicePath,
    contentType,
)

# def replace_in_string(replaces, dirSurce, dirTarget):
#     with open(f"{script_dir}\{dirSurce}", "r") as inputFile:
#         fileContent = inputFile.read()

#     for key, value in replaces.items():
#         fileContent = fileContent.replace(key, value.lower())

#     with open(f"{script_dir}\{dirTarget}", "w") as outputFile:
#         outputFile.write(fileContent)

# replacesGrafana = {
#     "mtopcua_car": CRATE_SCHEMA,
#     "process_status_oee": CRATE_TABLE_OEE,
#     "etplc": CRATE_TABLE_DEVICE
# }

# replace_in_string(replacesGrafana, "..\\grafana\\dashboards\\dashboard.src", "..\\grafana\\dashboards\\dashboard.json")

## Set CrateDB Views
query_CrateDB([processDuration, oee])

## Provisioning
curl_calls_function(provisioning_ARGS)

# Star webserver, listening for notification
httpWebServer(BIND_HOST, PORT)
