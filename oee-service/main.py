import json, os, configparser, pycurl, time

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

IOTA_OPCUA_MT_ENTITY_ID = os.getenv("IOTA_OPCUA_MT_ENTITY_ID")  # age01_PLC

DEVICE_ID_BASE = os.getenv("DEVICE_ID_BASE")  # urn:ngsiv2:I40Asset:PLC:001
DEVICE_TYPE = os.getenv("DEVICE_TYPE")  # PLC
DEVICE_ID = f"{DEVICE_ID_BASE}:{DEVICE_TYPE}:001"

OCB_ID_PROCESS = os.getenv("OCB_ID_PROCESS")  # processStatus

FIWARE_SERVICE = os.getenv("FIWARE_SERVICE")  # opcua_plc
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


def envArrayToString(array, spacing, backTick=""):
    output = str()
    spacingLen = len(spacing)

    array = array.split(",")

    for element in array:
        element = element.strip()
        if len(element) != 0:
            output += f"{backTick}{element}{backTick}{spacing}"

    if output[-spacingLen:] == spacing:
        output = output[:-spacingLen]

    return output

def sStrip(s):
    if s[-1:] == "s":
        s = s[:-1]
    return s

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

TIMES_UP = envArrayToString(config["MACHINE_STATES"]["TIMES_UP"], ", ", "'")
TIMES_DOWN = envArrayToString(config["MACHINE_STATES"]["TIMES_DOWN"], ", ", "'")

ENDS_GOOD = envArrayToString(config["MACHINE_STATES"]["ENDS_GOOD"], ", ", "'")
ENDS_BAD = envArrayToString(config["MACHINE_STATES"]["ENDS_BAD"], ", ", "'")

TIME_IDEAL = str(convert_to_seconds(sStrip(config["TIMING"]["TIME_IDEAL"])))
TIME_STEP = str(sStrip(config["TIMING"]["TIME_STEP"]))

print(f"[INFO] Timestep is {TIME_STEP}.")

START_DATE_TIME = (config["TIMING"]["START_DATE"] + "T" + config["TIMING"]["START_TIME"] + "Z")

# Configuration -->
# <-- nickjj Web server https://github.com/nickjj/webserver


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        if LOG_LEVEL == "debug":
            print("[INFO][WebServer] Headers:")
            print(self.headers)
            print("[INFO][WebServer] Content:")
            print(content.decode("utf-8"))

    def do_version(self):
        self.wfile.write(b"""{"service" : "ROSE-AP OEE-Service", "version" : 1.0}""")

    def do_notify(self):
        updateCB()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        if self.path == "/version":
            SimpleHTTPRequestHandler.do_version(self)
        if self.path == "/v2/notify":
            SimpleHTTPRequestHandler.do_notify(self)

    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)
        self.write_response(body)
        updateCB()


def httpWebServer(_BIND_HOST="0.0.0.0", _PORT=8008):
    try:
        httpd = HTTPServer((_BIND_HOST, _PORT), SimpleHTTPRequestHandler)
        print(f"[INFO][WebServer] Listening on http://{_BIND_HOST}:{_PORT}")
        httpd.serve_forever()
    except Exception as e:
        print(f"[ERROR][WebServer] Fail on http://{_BIND_HOST}:{_PORT} \n {str(e)}")


# nickjj Web server > https://github.com/nickjj/webserver -->
# <-- Curl Calls


def cUrlCall(method, service, port, NGSI, endpoint, path, headers: list, payload=False):

    try:
        cursor = pycurl.Curl()
        # print("[INFO][cUrl] Cursor created.")
        # print("[INFO][cUrl] Executing call:")

        _paths = [NGSI, endpoint, path]
        pathFiltered = [_path for _path in _paths if _path is not None]
        urlPath = "/".join(pathFiltered)
        url = f"http://{service}:{port}/{urlPath}"
        data = BytesIO()

        cursor.reset()

        print(f"curl -X {method} \\")
        cursor.setopt(cursor.CUSTOMREQUEST, method)

        print(f"'{url}' \\")
        cursor.setopt(cursor.URL, url)

        if headers:
            for header in headers:
                print(f"-H '{header}' \\")
            cursor.setopt(cursor.HTTPHEADER, headers)

        if payload is not False:
            payload = json.dumps(payload)
            print(f"-d '{payload}'", "\n")
            cursor.setopt(cursor.POSTFIELDS, payload)
        
        print()

        cursor.setopt(cursor.WRITEFUNCTION, data.write)

        cursor.perform()
        cursor.close()

        data = data.getvalue()

        if len(data):
            return json.loads(data)

    except Exception as e:
        print(f"[ERROR][cUrl] Error in cUrl function:\n{str(e)}")


# Curl Calls -->
# <-- Update Contex Broker

callBack = f"SELECT oee, availability, performance, quality FROM {CRATE_SCHEMA.lower()}.{CRATE_TABLE_OEE.lower()} ORDER BY time_frame DESC LIMIT 1;"

def updateCB():

    callBackResults = cUrlCall("POST", CRATE, CRATE_PORT_ADMIN, None, "_sql", None, [contentType["json"]], {"stmt": callBack})
    # machineStatus = cUrlCall("GET", ORION, ORION_PORT, "v2", f"entities/{DEVICE_ID}", "attrs/machineStatus/value", [Service, ServicePath])

    values = {}

    for col in callBackResults["cols"]:
        values[col] = {
            "type": "Float",
            "value": callBackResults["rows"][0][callBackResults["cols"].index(col)],
        }

    # if machineStatus is False:
    #     for col in callBackResults["cols"]:
    #         values[col]["value"] = None

    # del values[OCB_ID_MACHINE]

    cUrlCall("POST", ORION, ORION_PORT, "v2", "entities", f"{DEVICE_ID}/attrs", [Service, ServicePath, contentType["json"]], values)


# Update Contex Broker -->
# <-- Main Variables

Service = f"fiware-service: {FIWARE_SERVICE}"
ServicePath = f"fiware-servicepath: {FIWARE_SERVICEPATH}"
contentType = {"json": "Content-Type: application/json"}

# Main Variables -->
# <-- Script
# <-- Provisioning Subscriptions
print(f"[INFO][Orion] Provisioning subscriptions.")

# ### Get Existings Subscriptions
activeSubscriptions = cUrlCall("GET", ORION, ORION_PORT, "v2", "subscriptions", None, [Service, ServicePath])

# ### For each subscription in Orion json respond, grab the description
for subscription in activeSubscriptions:
    cUrlCall("DELETE", ORION, ORION_PORT, "v2", "subscriptions", subscription["id"], [Service, ServicePath]) 


def provisionSubscription(notify_host, notify_port, notify_attrs):

    subscriptionDescription = (
        f"{DEVICE_TYPE}:{DEVICE_ID}:{OCB_ID_PROCESS}:{notify_host}"
    )

    payload = {
        "description": subscriptionDescription,
        "subject": {
            "entities": [{"id": DEVICE_ID, "type": DEVICE_TYPE}],
            "condition": {
                "attrs": [notify_attrs],
                "alterationTypes": ["entityChange"],
            },
        },
        "notification": {
            "attrs": [notify_attrs],
            "http": {"url": f"http://{notify_host}:{notify_port}/v2/notify"},
        },
    }

    print(f"[INFO][Orion] Subscription {subscriptionDescription} will be provisioned")
    cUrlCall("POST", ORION, ORION_PORT, "v2", "subscriptions", None, [Service, ServicePath, contentType["json"]], payload)


subscriptions = [
    {"host": QUANTUMLEAP, "port": QUANTUMLEAP_PORT, "attrs": OCB_ID_PROCESS},
    {"host": ROSEAP_OEE, "port": ROSEAP_OEE_PORT, "attrs": OCB_ID_PROCESS}
]

# ### If the grabbed description match the
for sub in subscriptions:
    provisionSubscription(sub["host"], sub["port"], sub["attrs"])

## Set CrateDB Stmt
varTableDrop = f"DROP TABLE IF EXISTS {CRATE_SCHEMA.lower()}.etvars;"
varTableCreate = f"CREATE TABLE {CRATE_SCHEMA.lower()}.etvars (timeBin text);"
varTableValue = f"INSERT INTO {CRATE_SCHEMA.lower()}.etvars (timeBin) VALUES ('{TIME_STEP}');"

processDuration = f"""CREATE OR REPLACE VIEW {CRATE_SCHEMA.lower()}.{CRATE_TABLE_DURATION.lower()} AS SELECT {OCB_ID_PROCESS.lower()}, time_index, lag(time_index, 1, now()) OVER (ORDER BY time_index DESC) - time_index AS duration FROM {CRATE_SCHEMA.lower()}.{CRATE_TABLE_DEVICE.lower()} WHERE entity_id='{DEVICE_ID}' ORDER BY time_index DESC;"""

oee = f"""CREATE OR REPLACE VIEW {CRATE_SCHEMA.lower()}.{CRATE_TABLE_OEE.lower()} AS WITH
	subquery_01 AS (
		SELECT
			date_bin('{TIME_STEP}' :: INTERVAL, time_index, '{START_DATE_TIME}' :: TIMESTAMP) + '{TIME_STEP}' :: INTERVAL AS time_frame,
			sum(CASE WHEN {OCB_ID_PROCESS.lower()} IN ({ENDS_GOOD}) THEN 1 ELSE 0 END) AS parts_good,
			sum(CASE WHEN {OCB_ID_PROCESS.lower()} IN ({ENDS_BAD}) THEN 1 ELSE 0 END) AS parts_bad,
			sum(CASE WHEN {OCB_ID_PROCESS.lower()} IN ({TIMES_UP}) THEN duration ELSE 0 END) AS time_up,
			sum(CASE WHEN {OCB_ID_PROCESS.lower()} IN ({TIMES_DOWN}) THEN duration ELSE 0 END) AS time_down
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

oee = oee.replace("\t","").replace("\n"," ").replace("( ","(").replace(" )",")").replace(" (","(").replace(") ",")")

Health = f"""SELECT processstatus FROM "{CRATE_SCHEMA.lower()}"."{CRATE_TABLE_DEVICE.lower()}" LIMIT 1;"""

test = True

HealthResults = {}
HealthResults['rowcount'] = 0

while test:
    HealthResults = cUrlCall("POST", CRATE, CRATE_PORT_ADMIN, None, "_sql", None, [contentType["json"]], {"stmt": Health})
    print(HealthResults)
    
    if 'error' in HealthResults:
        print("Waiting for IoT Agent provisioning...")
        time.sleep(1)
    else:   
        print("IoT Agent provisioning completed.")
        test = False
        print(HealthResults['rowcount'])
        cUrlCall("POST", CRATE, CRATE_PORT_ADMIN, None, "_sql", None, [contentType["json"]], {"stmt": varTableDrop})
        cUrlCall("POST", CRATE, CRATE_PORT_ADMIN, None, "_sql", None, [contentType["json"]], {"stmt": varTableCreate})
        cUrlCall("POST", CRATE, CRATE_PORT_ADMIN, None, "_sql", None, [contentType["json"]], {"stmt": varTableValue})
        cUrlCall("POST", CRATE, CRATE_PORT_ADMIN, None, "_sql", None, [contentType["json"]], {"stmt": processDuration})
        cUrlCall("POST", CRATE, CRATE_PORT_ADMIN, None, "_sql", None, [contentType["json"]], {"stmt": oee})
    
httpWebServer(BIND_HOST, PORT)
