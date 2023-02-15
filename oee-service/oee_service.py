import configparser
import json
import os
import pycurl


from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from sys import argv


# <-- Docker
# Docker = False
Docker = True


script_dir = os.path.dirname(__file__)

# <-- .env

load_dotenv(script_dir + "//" + ".env")

LOG_LEVEL = os.getenv("LOG_LEVEL")  # debug

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

# Docker -->

if Docker == False:
    ORION = IOTA = CRATE = BIND_HOST = "localhost"
else:
    BIND_HOST = "0.0.0.0"

PORT = 8008

if len(argv) > 1:
    arg = argv[1].split(":")
    BIND_HOST = arg[0]
    PORT = int(arg[1])

# Docker -->

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
            output += f"'{element}'{spacing}"

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
# <-- Main Variables
    
Service = f"fiware-service: {FIWARE_SERVICE}"
ServicePath = f"fiware-servicepath: {FIWARE_SERVICEPATH}"
contentType = {"json": "Content-Type: application/json"}

# Main Variables -->
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
# <-- Curl Calls

def curl_calls_function(call, _payload_OverRide=False):

    try:
        cursor = pycurl.Curl()
        print("[INFO] [cUrl] Cursor created.")
        print("[INFO] [cUrl] Exectuded call:")

        try:         
            paths = [call['NGSI'], call['endpoint'], call['path']]
            pathFiltered = [path for path in paths if path is not None]
            urlPath = "/".join(pathFiltered)
            url = f"http://{call['service']}:{call['port']}/{urlPath}"
            
            if _payload_OverRide != False:
                call["payload"] = json.dumps(_payload_OverRide)
                
            # if LOG_LEVEL == "debug":
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
                cursor.close()
                
                data = data.getvalue()

                if len(data):
                    return json.loads(data)

            except Exception as e:
                print(f"[ERROR] [cUrl] Error in cUrl execution: {str(e)}")

        except Exception as e:
            print(f"[ERROR] [cUrl] Error in cUrl defenition:\n{str(e)}")

    except Exception as e:
        print(f"[ERROR] [cUrl] Error in cUrl function:\n{str(e)}")

# Curl Calls -->
# <-- Update Orion Contex Broker

def provisioning_subscription(NOTIFY_DESCRIPTION, NOTIFY_HOST, NOTIFY_PORT):
    return {
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
    }

def updateContexBroker():
    oeeCallBackQueryResults = curl_calls_function(CrateDB, {"stmt": oeeCallBack})
    
    values = {}
    
    for item in oeeCallBackQueryResults["cols"]:
        values[item] = {"type": "Float", "value": oeeCallBackQueryResults["rows"][0][oeeCallBackQueryResults["cols"].index(item)]}
        
    curl_calls_function(updateAttributes, values)

def notifySubscription(NOTIFY_HOST, NOTIFY_PORT): 
    notifyDescription = f"{DEVICE_TYPE}:{DEVICE_ID}:{OCB_ID}:{NOTIFY_HOST}"
    if notifyDescription not in SubscriptionsProvisioned:
        curl_calls_function(provisioning_subscription(notifyDescription, NOTIFY_HOST, NOTIFY_PORT))
        print(f"[INFO] [Orion] Subscription {notifyDescription} provisioned.")
    else:
        print(f"[INFO] [Orion] Subscription {notifyDescription} already provisioned.")

processDuration = f"""CREATE OR REPLACE VIEW {CRATE_SCHEMA.lower()}.{CRATE_TABLE_DURATION.lower()} AS
	SELECT
		{OCB_ID.lower()},
		time_index,
		lag(time_index, + 1, time_index) OVER (
			ORDER BY
				time_index DESC
		) - time_index AS duration
	FROM
		{CRATE_SCHEMA.lower()}.{CRATE_TABLE_DEVICE.lower()}
	WHERE
 		"entity_id"='{DEVICE_ID}' 
	ORDER BY
		time_index DESC;"""

oee = f"""CREATE OR REPLACE VIEW {CRATE_SCHEMA.lower()}.{CRATE_TABLE_OEE.lower()} AS WITH
	subquery_01 AS (
		SELECT
			date_bin('{TIME_STEP}' :: INTERVAL, time_index, '{START_DATE_TIME}' :: TIMESTAMP) + '{TIME_STEP}' :: INTERVAL AS time_frame,
			sum(CASE WHEN {OCB_ID.lower()} IN ({ENDS_GOOD}) THEN 1 ELSE 0 END) AS parts_good,
			sum(CASE WHEN {OCB_ID.lower()} IN ({ENDS_BAD}) THEN 1 ELSE 0 END) AS parts_bad,
			sum(CASE WHEN {OCB_ID.lower()} IN ({TIMES_UP}) THEN duration ELSE 0 END) AS time_up,
			sum(CASE WHEN {OCB_ID.lower()} IN ({TIMES_DOWN}) THEN duration ELSE 0 END) AS time_down
		FROM
			{CRATE_SCHEMA.lower()}.{CRATE_TABLE_DURATION.lower()}
		GROUP BY
			time_frame
	),
	subquery_02 AS (
		SELECT
			*,
			parts_good + parts_bad AS parts_total,
			time_up + time_down AS time_total
		FROM
			subquery_01
	),
	subquery_03 AS (
		SELECT
			*,
			{TIME_IDEAL} * 1000 * parts_total / NULLIF(time_total :: DECIMAL, 0) AS performance,
			parts_good / NULLIF(parts_total :: DECIMAL, 0) AS quality,
			time_up / NULLIF(time_total :: DECIMAL, 0) AS availability
		FROM
			subquery_02
	)
	SELECT
		*,
		performance * quality * availability AS oee
	FROM
		subquery_03;"""

CrateDB = {
    "method": "POST",
    "service": CRATE,
    "port": CRATE_PORT_ADMIN,
    "NGSI": None,
    "endpoint": "_sql" ,
    "path": None,
    "header": [contentType["json"]],
    "payload": None
}

get_subscriptions = {
    "method": "GET",
    "service": ORION,
    "port": ORION_PORT,
    "NGSI": "v2",
    "endpoint": "subscriptions" ,
    "path": None,
    "header": [Service, ServicePath],
    "payload": None
}

updateAttributes = {
    "method": "POST",
    "service": ORION,
    "port": ORION_PORT,
    "NGSI": "v2",
    "endpoint": "entities" ,
    "path": DEVICE_ID + "/attrs",
    "header": [Service, ServicePath, contentType["json"]],
    "payload": None
}

SubscriptionsToBeProvisioned = [
    {"host": QUANTUMLEAP,   "port": QUANTUMLEAP_PORT},
    {"host": ROSEAP_OEE,    "port": ROSEAP_OEE_PORT}
]

oeeCallBack = f'''SELECT oee, availability, performance, quality FROM "{CRATE_SCHEMA.lower()}"."{CRATE_TABLE_OEE.lower()}" ORDER BY time_frame DESC LIMIT 1;'''

# Update Orion Contex Broker -->
# <-- Script
# <-- External Variables

# ## Provisioning Subscriptions

# ### Check Subscriptions  
subscriptions = curl_calls_function(get_subscriptions)
print(f"[INFO] [Orion] Provisioning subscriptions.")

# ### For each subscription in Orion json respond
SubscriptionsProvisioned = []

for subscription in subscriptions:
    SubscriptionsProvisioned.append(subscription["description"])

for SubscriptionToBeProvisioned in SubscriptionsToBeProvisioned:
    notifySubscription(SubscriptionToBeProvisioned["host"], SubscriptionToBeProvisioned["port"])

## Set CrateDB Views
curl_calls_function(CrateDB, {"stmt": processDuration})
curl_calls_function(CrateDB, {"stmt": oee})

# Star webserver, listening for notification
httpWebServer(BIND_HOST, PORT)
