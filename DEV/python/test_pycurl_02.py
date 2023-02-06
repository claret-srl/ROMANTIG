import pycurl
import os
from dotenv import load_dotenv

orionPort = 1026

script_dir = os.path.dirname(__file__)

# <-- .env

load_dotenv(script_dir + "//" + ".env")

def curl_call(_cursor, _method, _url, _header = None, _payload = None):
	try:
		_cursor.reset()
		_cursor.setopt(_cursor.URL, _url)
		_cursor.setopt(_cursor.CUSTOMREQUEST, _method)
		_cursor.setopt(_cursor.HTTPHEADER, _header)
		_cursor.setopt(_cursor.POSTFIELDS, _payload)
		_cursor.perform()
	except Exception as e:
			print("[ERROR]" + "[cUrl]" + "Error in cUrl execution:\n" + str(e) + "\n")

# method = "POST"
# url = f"http://{orionHost}:{orionPort}/v2/op/update"
# header = ["Content-Type: application/json", f"fiware-service: {FIWARE_SERVICE}", f"fiware-servicepath: {FIWARE_SERVICEPATH}"]

# print(url)
# # print("\n ##### A ##### \n")




# method = "GET"
# url = f"http://{orionHost}:{orionPort}/v2/entities/urn:ngsiv2:I40Asset:PLC:001"
# header = [f"fiware-service: {FIWARE_SERVICE}", f"fiware-servicepath: {FIWARE_SERVICEPATH}"]

# print(url)
# # print("\n ##### B ##### \n")

# c.setopt(c.URL, url)
# c.setopt(c.CUSTOMREQUEST, method)
# c.setopt(c.HTTPHEADER, header)
# # c.setopt(c.POSTFIELDS, None)
# # c.unsetopt(c.POSTFIELDS)
# c.perform()
# c.reset()	

# c.close()

FIWARE_SERVICE = os.getenv('FIWARE_SERVICE')
FIWARE_SERVICEPATH = os.getenv('FIWARE_SERVICEPATH')
CONTEXTS_ID = os.getenv('CONTEXTS_ID')
CONTEXTS_TYPE = os.getenv('CONTEXTS_TYPE')
DEVICE_ID = os.getenv('DEVICE_ID')

Service = f"fiware-service: {FIWARE_SERVICE}"
ServicePath = f"fiware-servicepath: {FIWARE_SERVICEPATH}"
contentType = {"json":"Content-Type: application/json"}

cUrl_calls = [
    {
        "method"	:	"POST",
        "service"	:	"orion",
        "NGSI"		:	"V2",
        "endpoint"	:	"op/update",
        "id"		:	None,
        "header"	:	[Service, ServicePath, contentType["json"]],
		"payload"	:	None
    },
    {
        "method"	:	"GET",
        "service"	:	"orion",
        "NGSI"		:	"V2",
        "endpoint"	:	"entities",
        "id"		:	DEVICE_ID,
        "header"	:	[Service, ServicePath],
		"payload"	:	None
    }
]

try:
	cursor = pycurl.Curl()
	print("[INFO]" + "[cUrl]" + "Cursor created:\n")
	for call in cUrl_calls:
		try:
			url = f"http://{call['service']}:{orionPort}/{call['NGSI']}/{call['endpoint']}"
			curl_call(cursor, call['method'], url, call['header'], call['payload'])
		except Exception as e:
			print("[ERROR]" + "[cUrl]" + "Error in cUrl execution:\n" + str(e) + "\n")
	cursor.close()
except Exception as e:
	print("[ERROR]" + "[cUrl]" + "Error in cUrl execution:\n" + str(e) + "\n")

# for command in thisdict:
# 	print(command)
	# try:
	# 	cursor.execute(command)
	# 	if command.startswith('SELECT'):
	# 		records = cursor.fetchall()
	# 		return records
	# 	print("[INFO]" + "[CrateDB]" + "Exectuded query -->\n")
	# except Exception as e:
	# 	print("[ERROR]" + "[CrateDB]" + "Error in query execution:\n" + str(e) + "\n")
	# print(command + "\n")
	# print("#####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  ##### \n")


# def query_CrateDB(_sqlCommands):
# 	try:
# 		print("[INFO]" + "[CrateDB]" + "Connecting...")
# 		connection = client.connect(crateHost + ":" + CRATE_PORT_ADMIN, error_trace=True)
# 		print("[INFO]" + "[CrateDB]" + "Connection Successful.")
# 		try:
# 			cursor = connection.cursor()
# 			print("[INFO]" + "[CrateDB]" + "Cursor created." + "\n")
# 			# print(_sqlCommands)
# 			for command in _sqlCommands:
# 				# print(command)
# 				try:
# 					cursor.execute(command)
# 					if command.startswith('SELECT'):
# 						records = cursor.fetchall()
# 						return records
# 					print("[INFO]" + "[CrateDB]" + "Exectuded query -->\n")
# 				except Exception as e:
# 					print("[ERROR]" + "[CrateDB]" + "Error in query execution:\n" + str(e) + "\n")
# 				print(command + "\n")
# 				print("#####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  #####  ##### \n")
# 		except Exception as e:
# 			print("[ERROR]" + "[CrateDB]" + "Error in cursor creation:\n" + str(e) + "\n")
# 		finally:
# 			cursor.close()
# 			print("[INFO]" + "[CrateDB]" + "Cursor Closed.")
# 			connection.close()
# 			print("[INFO]" + "[CrateDB]" + "Connection Closed.")
# 	except Exception as e:
# 		print("[ERROR]" + "[CrateDB]" + "Connection fail:\n" + str(e) + "\n")
  

