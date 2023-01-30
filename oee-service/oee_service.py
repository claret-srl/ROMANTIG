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

FIWARE_SERVICE = os.getenv('FIWARE_SERVICE')
FIWARE_SERVICEPATH = os.getenv('FIWARE_SERVICEPATH')
CONTEXTS_ID = os.getenv('CONTEXTS_ID')
CONTEXTS_TYPE = os.getenv('CONTEXTS_TYPE')
# ROSEAP_OEE_CONTAINER = os.getenv('ROSEAP_OEE_CONTAINER')
# .env -->
# <-- Docker

Docker = True

if Docker == False:
	orionHost = crateHost = BIND_HOST = 'localhost'
else:
	orionHost = "orion"
	crateHost = "crate-db"
	BIND_HOST = '0.0.0.0'

PORT = 8008

orionPort = str(1026)
cratePort = str(4200)

# Docker -->
# <-- Main Variables

if len(argv) > 1:
	arg = argv[1].split(':')
	BIND_HOST = arg[0]
	PORT = int(arg[1])

sql = ['''SELECT
		oee,
		availability,
		performance,
		quality
	FROM
	"mtopcua_car"."process_status_oee"
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
# print("[INFO]" + "[WebServer]" + self.headers)
# TypeError: can only concatenate str (not "HTTPMessage") to str
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
		# print(json.dumps(content.decode('utf-8'), indent=1))
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
		connection = client.connect(crateHost + ":" + cratePort, error_trace=True)
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
	url = f"http://{orionHost}:{orionPort}/v2/op/update"
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
	url = f"http://{orionHost}:{orionPort}/v2/entities/urn:ngsiv2:I40Asset:PLC:001"
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