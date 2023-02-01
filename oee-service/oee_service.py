import configparser
from crate import client
import pycurl
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv
# import json
from dotenv import load_dotenv


script_dir = os.path.dirname(__file__)

# <-- .env

load_dotenv(script_dir + "//" + ".env")

LOG_LEVEL = os.getenv('LOG_LEVEL') # debug

COMPOSE_PROJECT_NAME = os.getenv('COMPOSE_PROJECT_NAME') # fiware
ORG_FIWARE = os.getenv('ORG_FIWARE') # claret-romantig

CONTEXTS_ID = os.getenv('CONTEXTS_ID') # age01_Car
CONTEXTS_TYPE = os.getenv('CONTEXTS_TYPE') # PLC

DEVICE_ID = os.getenv('DEVICE_ID') # urn:ngsiv2:I40Asset:PLC:001
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
CRATE_TABLE_DURATION = os.getenv('CRATE_TABLE') # etprocessduration		# I don't think they are used --> Used in pyhon and Query.sql
CRATE_TABLE_OEE = os.getenv('CRATE_TABLE') # etoee	

MONGO = os.getenv('MONGO') # db-mongo
MONGO_PORT = os.getenv('MONGO_PORT') # 27017

REDIS = os.getenv('REDIS') # db-redis
REDIS_PORT = os.getenv('REDIS_PORT') # 6379

GRAFANA = os.getenv('GRAFANA') # grafana
GRAFANA_PORT = os.getenv('GRAFANA_PORT') # 3000


# ROSEAP_OEE_CONTAINER = os.getenv('ROSEAP_OEE_CONTAINER')
# .env -->
# <-- Docker

Docker = True

if Docker == False:
	orionHost = crateHost = BIND_HOST = 'localhost'
else:
	orionHost = ORION
	crateHost = CRATE
	BIND_HOST = '0.0.0.0'

PORT = 8008

# Docker -->
# <-- Main Variables

if len(argv) > 1:
	arg = argv[1].split(':')
	BIND_HOST = arg[0]
	PORT = int(arg[1])

# ##############################################
# 
# Devo capire come settare il nome della tabella
# 
# ##############################################

sql = [f'''SELECT
		oee,
		availability,
		performance,
		quality
	FROM
	"{CRATE_SCHEMA}"."{CRATE_TABLE_OEE}"
	LIMIT 1;''']
 
jsonDataTemplate = '''{
  "actionType": "append",
  "entities": [
	{
	  "id": "urn:ngsiv2:I40Asset:PLC:001",
	  "type": "PLC",
	  "OEE": {
		"type": "Float",
		"value": "%s"
	  },
	  "Availability": {
		"type": "Float",
		"value": "%s"
	  },
	  "Performance": {
		"type": "Float",
		"value": "%s"
	  },
	  "Quality": {
		"type": "Float",
		"value": "%s"
	  }
	}
  ]
}'''

# Main Variables -->
# <-- nickjj Web server https://github.com/nickjj/webserver

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	def write_response(self, content):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(content)
		updateContexBroker(sql, jsonDataTemplate)
		print("[INFO]" + "[WebServer]" + "Headers:" + "\n")
		print(self.headers)
		print("[INFO]" + "[WebServer]" + "Content:" + "\n")
		print(content.decode('utf-8'))

	def do_GET(self):
		self.write_response(b'')

	def do_POST(self):
		content_length = int(self.headers.get('content-length', 0))
		body = self.rfile.read(content_length)
		self.write_response(body)


def httpWebServer (_BIND_HOST = '0.0.0.0', _PORT = 8008):
	try:
		httpd = HTTPServer((_BIND_HOST, _PORT), SimpleHTTPRequestHandler)
		print("[INFO]" + "[WebServer]" + f"Listening on http://{_BIND_HOST}:{_PORT}\n")
		httpd.serve_forever()
	except Exception as e:
		print("[ERROR]" + "[WebServer]" + f"Fail on http://{_BIND_HOST}:{_PORT}\n" + str(e) + "\n")

# nickjj Web server > https://github.com/nickjj/webserver -->
# <-- Crate-DB

def query_CrateDB(_sqlCommands):
	try:
		print("[INFO]" + "[CrateDB]" + "Connecting...")
		connection = client.connect(crateHost + ":" + CRATE_PORT_ADMIN, error_trace=True)
		print("[INFO]" + "[CrateDB]" + "Connection Successful.")
		try:
			cursor = connection.cursor()
			print("[INFO]" + "[CrateDB]" + "Cursor created." + "\n")
			# print(_sqlCommands)
			for command in _sqlCommands:
				# print(command)
				try:
					cursor.execute(command)
					if command.startswith('SELECT'):
						records = cursor.fetchall()
						return records
					print("[INFO]" + "[CrateDB]" + "Exectuded query -->\n")
				except Exception as e:
					print("[ERROR]" + "[CrateDB]" + "Error in query execution:\n" + str(e) + "\n")
				print(command + "\n")
				print("#####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  ##### \n")
		except Exception as e:
			print("[ERROR]" + "[CrateDB]" + "Error in cursor creation:\n" + str(e) + "\n")
		finally:
			cursor.close()
			print("[INFO]" + "[CrateDB]" + "Cursor Closed.")
			connection.close()
			print("[INFO]" + "[CrateDB]" + "Connection Closed.")
	except Exception as e:
		print("[ERROR]" + "[CrateDB]" + "Connection fail:\n" + str(e) + "\n")

# Crate-DB -->
# <-- Units to Seconds

SECONDS_PER_UNIT = {"second":1, "minute":60, "hour":60*60, "day":60*60*24, "week":60*60*24*7, "month":60*60*24*7*30, "year":60*60*24*7*365}

def convert_to_seconds(s):
	s = s.split(" ")
	return int(s[0]) * SECONDS_PER_UNIT[s[1]]

# Units to Seconds -->
# <-- Update Orion Contex Broker

def updateContexBroker(_sql, _jsonObject):
	data = query_CrateDB(_sql)
	jsonObjectData = _jsonObject % tuple(data[0])

	c = pycurl.Curl()

	method = "POST"
	url = f"http://{orionHost}:{ORION_PORT}/v2/op/update"
	header = ["Content-Type: application/json", f"fiware-service: {FIWARE_SERVICE}", f"fiware-servicepath: {FIWARE_SERVICEPATH}"]

	print(url)
	# print("\n ##### A ##### \n")

	c.setopt(c.URL, url)
	c.setopt(c.CUSTOMREQUEST, method)
	c.setopt(c.HTTPHEADER, header)
	c.setopt(c.POSTFIELDS, jsonObjectData)
	c.perform()
	c.reset()


	method = "GET"
	url = f"http://{orionHost}:{ORION_PORT}/v2/entities/{DEVICE_ID}"
	header = [f"fiware-service: {FIWARE_SERVICE}", f"fiware-servicepath: {FIWARE_SERVICEPATH}"]

	print(url)
	# print("\n ##### B ##### \n")
	
	c.setopt(c.URL, url)
	c.setopt(c.CUSTOMREQUEST, method)
	c.setopt(c.HTTPHEADER, header)
	# c.setopt(c.POSTFIELDS, None)
	# c.unsetopt(c.POSTFIELDS)
	c.perform()
	c.reset()	
 
	c.close()


# Update Orion Contex Broker -->
# <-- Configuration

def arrayToString(_Array):
	_Array = _Array.split(",")
	output = str()
	spacing = ", "
	spacingLen = len(spacing)
	for element in _Array:
		# output = element
		output += f"'{element}'" + spacing
	# return (f"({output})")
	if output[-spacingLen:] == spacing:
		return output[:-spacingLen]

	else:
		return output

config = configparser.ConfigParser()
config.read(script_dir + "//" + "oee_conf.config")

timesUp = arrayToString(config["PROCESS"]["timesUp"])
timesDown = arrayToString(config["PROCESS"]["timesDown"])

endsGood = arrayToString(config["PROCESS"]["endsGood"])
endsBad = arrayToString(config["PROCESS"]["endsBad"])

startDateTime = config["START_DATE_TIME"]["date"] + "T" + config["START_DATE_TIME"]["time"] + "Z"

idealTime = str(convert_to_seconds(config["OEE"]["idealTime"]))
timestep = str(config["OEE"]["timestep"])

print(f"[INFO] Timestep is {timestep}.")

# Configuration -->
# <-- Script

sqlFilePath = script_dir + "//" + "Query" + ".sql"

try:
	print("[INFO]" + "[Query file]" + "Opening...")
	sqlFile = open(sqlFilePath, 'r')
	print("[INFO]" + "[Query file]" + "Successful opened.")
except Exception as e:
	print("[ERROR]" + "[Query file]" + "Opening failed:\n" + str(e) + "\n")

sqlFileContent = sqlFile.read()
sqlFile.close()
sqlFile_rows = sqlFileContent.split("\n")

sqlCommands = str()

for row in sqlFile_rows:
	if row.find('-- ') == -1:
	# if not row.startswith('-- '):
	# if not row.startswith('-- ') or not row.find('-- '):

		row = row.replace("\t", "").replace("\n", "")

		if row.find("20 * 1000") != -1 : row = f"{idealTime} * 1000"
		elif row.find("5 minute") != -1 : row = f"'{timestep}'"
		elif row.find("2023-01-01T08:00:00Z") != -1 : row = f"'{startDateTime}'"
		elif row.find("'In Picking','In Welding','In QC','In Placing'") != -1 : row = timesUp
		elif row.find("'Idle','In Reworking','In QC from rework','In Trashing'") != -1 : row = timesDown
		elif row.find("In Placing") != -1 : row = endsGood
		elif row.find("In Trashing") != -1 : row = endsBad

		elif row.find("mtopcua_car") != -1 : row = row.replace("ocua_car", FIWARE_SERVICE.lower())
		elif row.find("etplc") != -1 : row = row.replace("plc", CONTEXTS_TYPE.lower())

		# FIWARE_SERVICE=opcua_car
		# FIWARE_SERVICEPATH=/demo
		# CONTEXTS_ID=age01_Car
		# CONTEXTS_TYPE=PLC
  
		sqlCommands += str(row) + " "

# print(sqlCommands)

sqlCommands = sqlCommands.split(';')
try:
	sqlCommands.remove(' ')
except Exception as e:
	print("[WARNING]" + "[SQL Commands]" + ": " + str(e) + "\n")

# Set CrateDB View
query_CrateDB(sqlCommands)

# Star webserver listening for notification
httpWebServer(BIND_HOST, PORT)