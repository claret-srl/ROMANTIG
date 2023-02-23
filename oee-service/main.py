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

    for element in _Array:
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
START_DATE_TIME = (
    config["TIMING"]["START_DATE"] + "T" + config["TIMING"]["START_TIME"] + "Z"
)
TIME_IDEAL = str(convert_to_seconds(config["TIMING"]["TIME_IDEAL"]))
TIME_STEP = str(config["TIMING"]["TIME_STEP"])

print(f"[INFO] Timestep is {TIME_STEP}.")

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


def cUrlCall(template, payload=False):

    try:
        cursor = pycurl.Curl()
        print("[INFO][cUrl] Cursor created.")
        print("[INFO][cUrl] Execting call:")

        paths = [template["NGSI"], template["endpoint"], template["path"]]
        pathFiltered = [path for path in paths if path is not None]
        urlPath = "/".join(pathFiltered)
        url = f"http://{template['service']}:{template['port']}/{urlPath}"
        data = BytesIO()

        cursor.reset()

        print(f"curl -X {template['method']} \\")
        cursor.setopt(cursor.CUSTOMREQUEST, template["method"])

        print(f"{url} \\")
        cursor.setopt(cursor.URL, url)

        if template["header"]:
            for header in template["header"]:
                print(f"-H '{header}' \\")
            cursor.setopt(cursor.HTTPHEADER, template["header"])

        if payload is not False:
            template["payload"] = json.dumps(payload)
            print(f"-d '{template['payload']}'", "\n")
            cursor.setopt(cursor.POSTFIELDS, template["payload"])

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


def updateCB():
    callBackResults = cUrlCall(CrateDB, {"stmt": callBack})

    values = {}

    for result in callBackResults["cols"]:
        values[result] = {
            "type": "Float",
            "value": callBackResults["rows"][0][callBackResults["cols"].index(result)],
        }

    cUrlCall(updateAttributes, values)


# Update Contex Broker -->

# <-- Main Variables

Service = f"fiware-service: {FIWARE_SERVICE}"
ServicePath = f"fiware-servicepath: {FIWARE_SERVICEPATH}"
contentType = {"json": "Content-Type: application/json"}

# Main Variables -->


CrateDB = {
    "method": "POST",
    "service": CRATE,
    "port": CRATE_PORT_ADMIN,
    "NGSI": None,
    "endpoint": "_sql",
    "path": None,
    "header": [contentType["json"]],
}

getSubscriptions = {
    "method": "GET",
    "service": ORION,
    "port": ORION_PORT,
    "NGSI": "v2",
    "endpoint": "subscriptions",
    "path": None,
    "header": [Service, ServicePath],
}

templateSubscription = {
    "method": "POST",
    "service": ORION,
    "port": ORION_PORT,
    "NGSI": "v2",
    "endpoint": "subscriptions",
    "path": None,
    "header": [Service, ServicePath, contentType["json"]]
}

updateAttributes = {
    "method": "POST",
    "service": ORION,
    "port": ORION_PORT,
    "NGSI": "v2",
    "endpoint": "entities",
    "path": DEVICE_ID + "/attrs",
    "header": [Service, ServicePath, contentType["json"]],
}

processDuration = f"""CREATE OR REPLACE VIEW {CRATE_SCHEMA.lower()}.{CRATE_TABLE_DURATION.lower()} AS
	SELECT
		{OCB_ID.lower()},
		time_index,
		lag(time_index, + 1, time_index) OVER (ORDER BY time_index DESC) - time_index AS duration
	FROM
		{CRATE_SCHEMA.lower()}.{CRATE_TABLE_DEVICE.lower()}
	WHERE
 		entity_id='{DEVICE_ID}'
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

callBack = f"SELECT oee, availability, performance, quality FROM {CRATE_SCHEMA.lower()}.{CRATE_TABLE_OEE.lower()} ORDER BY time_frame DESC LIMIT 1;"

# <-- Script


# <-- Provisioning Subscriptions
print(f"[INFO][Orion] Provisioning subscriptions.")

# ### Get Existings Subscriptions
activeSubscriptions = cUrlCall(getSubscriptions)

activeSubscriptionsDescription = []

# ### For each subscription in Orion json respond, grab the description
for subscription in activeSubscriptions:
    activeSubscriptionsDescription.append(subscription["description"])


def provisionSubscription(NOTIFY_HOST, NOTIFY_PORT):

    subscriptionDescription = f"{DEVICE_TYPE}:{DEVICE_ID}:{OCB_ID}:{NOTIFY_HOST}"

    print(f"[INFO][Orion] Subscription {subscriptionDescription}", end=" ")

    payload = {
        "description": subscriptionDescription,
        "subject": {
            "entities": [{"id": DEVICE_ID, "type": DEVICE_TYPE}],
            "condition": {
                "attrs": [ "processStatus" ],
                "alterationTypes": [ "entityChange" ]
            }
        },
        "notification": {
            "attrs": [OCB_ID],
            "http": {"url": f"http://{NOTIFY_HOST}:{NOTIFY_PORT}/v2/notify"},
        }
    }

    if subscriptionDescription not in activeSubscriptionsDescription:
        print("will be provisioned:")
        cUrlCall(templateSubscription, payload)

    else:
        print("was already provisioned.")


Subscriptions = [
    {"host": QUANTUMLEAP, "port": QUANTUMLEAP_PORT},
    {"host": ROSEAP_OEE, "port": ROSEAP_OEE_PORT},
]

# ### If the grabbed description match the
for Subscription in Subscriptions:
    provisionSubscription(Subscription["host"], Subscription["port"])

## Set CrateDB Views
cUrlCall(CrateDB, {"stmt": processDuration})
cUrlCall(CrateDB, {"stmt": oee})

httpWebServer(BIND_HOST, PORT)
