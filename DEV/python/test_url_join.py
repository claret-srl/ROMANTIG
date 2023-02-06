import os
from dotenv import load_dotenv


script_dir = os.path.dirname(__file__)

load_dotenv(script_dir + "//" + ".env")

FIWARE_SERVICE = os.getenv("FIWARE_SERVICE")  # opcua_car
FIWARE_SERVICEPATH = os.getenv("FIWARE_SERVICEPATH")  # /demo
CONTEXTS_ID = os.getenv("CONTEXTS_ID")  # age01_Car
CONTEXTS_TYPE = os.getenv("CONTEXTS_TYPE")  # PLC
DEVICE_BASE_ID = os.getenv("DEVICE_BASE_ID")  # urn:ngsiv2:I40Asset
DEVICE_ID = os.getenv("DEVICE_ID")  # urn:ngsiv2:I40Asset:PLC:001
DEVICE_TYPE = os.getenv("DEVICE_TYPE")  # PLC
OCB_ID = os.getenv("OCB_ID")  # processStatus
ORION = os.getenv("ORION")  # orion
ORION_PORT = os.getenv("ORION_PORT")  # 1026


Service = f"fiware-service: {FIWARE_SERVICE}"
ServicePath = f"fiware-servicepath: {FIWARE_SERVICEPATH}"
contentType = {"json": "Content-Type: application/json"}

calls= [
    {
    "method": "POST",
    "service": ORION,
    "port": ORION_PORT,
    "NGSI": "v2",
    "endpoint": "entities" ,
    "path": OCB_ID + "/attrs",
    "header": [Service, ServicePath, contentType["json"]],
    "payload": '{"type": "Area", "id": "' + DEVICE_BASE_ID + ':Area:001"}',
    },
    {
    "method": "POST",
    "service": ORION,
    "port": ORION_PORT,
    "NGSI": "v2",
    "endpoint": "entities",
    "path": None,
    "header": [Service, ServicePath, contentType["json"]],
    "payload": '{"type": "Area", "id": "' + DEVICE_BASE_ID + ':Area:001"}',
    }
]

for call in calls:
    
	paths = [call['NGSI'], call['endpoint'], call['path']]
	pathFiltered = []
	for path in paths:
		if path != None:
			pathFiltered.append(path)
	urlSeparator = "/"
	urlPath = urlSeparator.join(pathFiltered)

	url = f"http://{call['service']}:{call['port']}/{urlPath}"

	print("\n", url)