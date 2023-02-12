import configparser
from crate import client
import pycurl
from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv
import os
from dotenv import load_dotenv

import function._query as _query
# import function._curl_calls as _curl_calls

from io import BytesIO
import json


# <-- Docker
# Docker = False
Docker = True
# Docker -->


script_dir = os.path.dirname(__file__)

# <-- .env

load_dotenv(script_dir + "//" + ".env")

LOG_LEVEL = os.getenv("LOG_LEVEL")  # debug
if LOG_LEVEL == "debug":
    import pprint

COMPOSE_PROJECT_NAME = os.getenv("COMPOSE_PROJECT_NAME")  # fiware
ORG_FIWARE = os.getenv("ORG_FIWARE")  # claret-romantig

CONTEXTS_ID = os.getenv("CONTEXTS_ID")  # age01_PLC

DEVICE_BASE_ID = os.getenv("DEVICE_BASE_ID")  # urn:ngsiv2:I40Asset
DEVICE_ID = os.getenv("DEVICE_ID")  # urn:ngsiv2:I40Asset:PLC:001
DEVICE_TYPE = os.getenv("DEVICE_TYPE")  # PLC
OCB_ID = os.getenv("OCB_ID")  # processStatus

FIWARE_SERVICE = os.getenv("FIWARE_SERVICE")  # opcua_plc
FIWARE_SERVICEPATH = os.getenv("FIWARE_SERVICEPATH")  # /demo

IOTA = os.getenv("IOTA")  # iot-agent
IOTA_NORTH_PORT = os.getenv("IOTA_NORTH_PORT")  # 4041
IOTA_SOUTH_PORT = os.getenv("IOTA_SOUTH_PORT")  # 9229
IOTA_OPCUA_ID = os.getenv("IOTA_OPCUA_ID")  # "ns=4;i=198"

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
CRATE_SCHEMA = os.getenv("CRATE_SCHEMA")  # mtopcua_plc
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

config = configparser.ConfigParser()
config.read(script_dir + "//" + ".config")

TIMES_UP = envArrayToString(config["MACHINE_STATES"]["TIMES_UP"])
TIMES_DOWN = envArrayToString(config["MACHINE_STATES"]["TIMES_DOWN"])
ENDS_GOOD = envArrayToString(config["MACHINE_STATES"]["ENDS_GOOD"])
ENDS_BAD = envArrayToString(config["MACHINE_STATES"]["ENDS_BAD"])
START_DATE_TIME = (config["TIMING"]["START_DATE"] + "T" + config["TIMING"]["START_TIME"] + "Z")
TIME_IDEAL = str(convert_to_seconds(config["TIMING"]["TIME_IDEAL"]))
TIME_STEP = str(config["TIMING"]["TIME_STEP"])

print(f"[INFO] Timestep is {TIME_STEP}.")

# Configuration -->
# <-- nickjj Web server https://github.com/nickjj/webserver

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_version(self):
        self.wfile.write(b'''{"service" : "ROSE-AP OEE-Service", "version" : 1.0}''')

    def do_notify(self):
        updateContexBroker()
    
    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        if LOG_LEVEL == "debug":
            print("[INFO] [WebServer] Headers:")
            print(self.headers)
            print("[INFO] [WebServer] Content:")
            print(content.decode("utf-8"))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        if self.path == '/version':
            SimpleHTTPRequestHandler.do_version(self)
        if self.path == '/v2/notify':
            SimpleHTTPRequestHandler.do_notify(self)


    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)
        self.write_response(body)
        updateContexBroker()


def httpWebServer(_BIND_HOST="0.0.0.0", _PORT=8008):
    try:
        httpd = HTTPServer((_BIND_HOST, _PORT), SimpleHTTPRequestHandler)
        print(f"[INFO] [WebServer] Listening on http://{_BIND_HOST}:{_PORT}")
        httpd.serve_forever()
    except Exception as e:
        print(f"[ERROR] [WebServer] Fail on http://{_BIND_HOST}:{_PORT} \n {str(e)}")


# nickjj Web server > https://github.com/nickjj/webserver -->
# <-- Crate-DB

def query_CrateDB(_sqlCommands):
    try:
        print("[INFO] [CrateDB] Connecting...")
        connection = client.connect(CRATE + ":" + CRATE_PORT_ADMIN, error_trace=True)
        print("[INFO] [CrateDB] Connection Successful.")
        try:
            cursor = connection.cursor()
            print("[INFO] [CrateDB] Cursor created.")

            if LOG_LEVEL == "debug":
                print(_sqlCommands)

            for command in _sqlCommands:
                try:
                    cursor.execute(command)
                    print("[INFO] [CrateDB] Exectuded query:")
                except Exception as e:
                    print(f"[ERROR] [CrateDB] Error in query execution: {str(e)}")
                    
                print(f"\n  {command}\n")

                if command.startswith("SELECT"):
                    
                    # return cause the hard ends of the loop
                    # so it can cause unintended behavior
                    return cursor.fetchall()

        except Exception as e:
            print(f"[ERROR] [CrateDB] Error in cursor creation: {str(e)}")
        finally:
            cursor.close()
            print("[INFO] [CrateDB] Cursor Closed.")
            connection.close()
            print("[INFO] [CrateDB] Connection Closed.")
    except Exception as e:
        print(f"[ERROR] [CrateDB] Connection fail:{str(e)}")

# Crate-DB -->
# <-- Update Orion Contex Broker

def updateAttributes(_data):
    return [
        # ##### Contex Broker
        # ##### Append or Update attribute
        # ##### OEE, Availability, Performance, Quality
        # ##### of
        # ##### urn:ngsiv2:I40Asset:PLC:001
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "entities" ,
            "path": DEVICE_ID + "/attrs",
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '''{
    "OEE"           :    {"type": "Float", "value": ''' + str(_data[0][0]) + '''},
    "Availability"  :    {"type": "Float", "value": ''' + str(_data[0][1]) + '''},
    "Performance"   :    {"type": "Float", "value": ''' + str(_data[0][2]) + '''},
    "Quality"       :    {"type": "Float", "value": ''' + str(_data[0][3]) + '''}
}'''
        }
    ]

def updateContexBroker():
    oeeCallBackQuery = _query.oeeCallBack(CRATE_SCHEMA, CRATE_TABLE_OEE)
    oeeCallBackQueryResults = query_CrateDB([oeeCallBackQuery])
    if LOG_LEVEL == "debug":
        print("oeeCallBackQueryResults: ", oeeCallBackQueryResults)
    
    for i in range(len(oeeCallBackQueryResults[0])):
        if oeeCallBackQueryResults[0][i] == None:
            oeeCallBackQueryResults[0][i] = "Null"
    
    cUrl_call = updateAttributes(oeeCallBackQueryResults)
    
    curl_calls_function(cUrl_call)

# Update Orion Contex Broker -->
# <-- Curl Calls

def body(buf):
    # Print body data to stdout
    import sys
    sys.stdout.write(buf)
    # Returning None implies that all bytes were written

def curl_calls_function(_cUrl_calls, _payload_OverRide=False):

    try:
        cursor = pycurl.Curl()
        print("[INFO] [cUrl] Cursor created.")
        print("[INFO] [cUrl] Exectuded call:")

        for call in _cUrl_calls:

            try:         
                paths = [call['NGSI'], call['endpoint'], call['path']]
                pathFiltered = [path for path in paths if path is not None]
                urlPath = "/".join(pathFiltered)
                url = f"http://{call['service']}:{call['port']}/{urlPath}"
 
                if _payload_OverRide != False:
                    call["payload"] = _payload_OverRide

                # if LOG_LEVEL == "debug":
                print("\n")
                print(f"  curl -X {call['method']} \\")
                print(f"    {url} \\")

                for header in call["header"]:
                    print(f"    -H '{header}' \\")

                print(f"    -d '{call['payload']}'", "\n")

                try:
                    cursor.reset()
                    cursor.setopt(cursor.URL, url)
                    cursor.setopt(cursor.CUSTOMREQUEST, call["method"])

                    if call["header"]:
                        cursor.setopt(cursor.HTTPHEADER, call["header"])

                    if call["payload"]:
                        cursor.setopt(cursor.POSTFIELDS, call["payload"])
                        
                    data = BytesIO()
                    cursor.setopt(cursor.WRITEFUNCTION, data.write)

                    cursor.perform()

                    if call["method"] == "GET":
                        
                        # return cause the hard ends of the loop
                        # so it can cause unintended behavior
                        return data

                except Exception as e:
                    print(f"[ERROR] [cUrl] Error in cUrl execution: {str(e)}")

            except Exception as e:
                print(f"[ERROR] [cUrl] Error in cUrl defenition:\n{str(e)}")
            
        cursor.close()

    except Exception as e:
        print(f"[ERROR] [cUrl] Error in cUrl function:\n{str(e)}")


# Curl Calls -->
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
    ENDS_GOOD,
    ENDS_BAD,
    TIMES_UP,
    TIMES_DOWN,
    TIME_IDEAL,
    TIME_STEP,
    START_DATE_TIME,
)
# External Variables -->

def provisioning_subscription(NOTIFY_DESCRIPTION, NOTIFY_HOST, NOTIFY_PORT):
    return [{
        "method": "POST",
        "service": ORION,
        "port": ORION_PORT,
        "NGSI": "v2",
        "endpoint": "subscriptions",
        "path": None,
        "header": [Service, ServicePath, contentType["json"]],
        "payload": '''{
            "description": "''' + NOTIFY_DESCRIPTION + '''",
            "subject": {
                "entities": [
                    {
                        "id": "''' + DEVICE_ID + '''",
                        "type": "''' + DEVICE_TYPE + '''"
                    }
                ],
                "condition": {
                    "attrs": ["''' + OCB_ID + '''"]
                }
            },
            "notification": {
                "http": {
                    "url": "http://''' + NOTIFY_HOST + ''':'''+ NOTIFY_PORT + '''/v2/notify"
                },
                "attrs": ["''' + OCB_ID + '''"]
            }
        }'''
    }]

# ## Provisioning Subscriptions
print(print(f"[INFO] [Orion] Provisioning subscriptions."))

# ### Check Subscriptions
def get_subscriptions():
    # ##### Get subscriptions from the Contex Broker
    return [
        {
            "method": "GET",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "subscriptions" ,
            "path": None,
            "header": [Service, ServicePath],
            "payload": None
        }
    ]
    
data = curl_calls_function(get_subscriptions())

# ### Load Orion json respond
subscriptions = json.loads(data.getvalue())

# ### For each subscription in Orion json respond
SubscriptionsProvisioned = []

for subscription in subscriptions:
    SubscriptionsProvisioned.append(subscription["description"])


def notifySubscription(NOTIFY_HOST, NOTIFY_PORT): 
    notifyDescription = f"{DEVICE_TYPE}:{DEVICE_ID}:{OCB_ID}:{NOTIFY_HOST}"
    if notifyDescription not in SubscriptionsProvisioned:
        curl_calls_function(provisioning_subscription(notifyDescription, NOTIFY_HOST, NOTIFY_PORT))
        print(f"[INFO] [Orion] Subscription {notifyDescription} provisioned.")
    else:
        print(f"[INFO] [Orion] Subscription {notifyDescription} already provisioned.")


SubscriptionsToBeProvisioned = [
    {"host": QUANTUMLEAP,   "port": QUANTUMLEAP_PORT},
    {"host": ROSEAP_OEE,    "port": ROSEAP_OEE_PORT}
]

for SubscriptionToBeProvisioned in SubscriptionsToBeProvisioned:
    notifySubscription(SubscriptionToBeProvisioned["host"], SubscriptionToBeProvisioned["port"])

## Set CrateDB Views
query_CrateDB([processDuration, oee])

# Star webserver, listening for notification
httpWebServer(BIND_HOST, PORT)
