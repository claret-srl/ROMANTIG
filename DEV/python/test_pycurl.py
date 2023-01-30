# import configparser
# from crate import client
import pycurl
# import os
# from http.server import HTTPServer, BaseHTTPRequestHandler
# from sys import argv
# import json

print("\n")


Docker = False

if Docker == False:
	orionHost = crateHost = BIND_HOST = 'localhost'
else:
	orionHost = "orion"
	crateHost = "crate-db"
	BIND_HOST = '0.0.0.0'

PORT = 8008

orionPort = str(1026)
cratePort = str(4200)

jsonDataTemplate = '''{"actionType": "append","entities": [{"id": "urn:ngsiv2:I40Asset:PLC:001","type": "PLC","OEE": {"type": "Float","value": "%s"},"Availability": {"type": "Float","value": "%s"},"Performance": {"type": "Float","value": "%s"},"Quality": {"type": "Float","value": "%s"}}]}'''

# data = [[None, None, None, None]]
data = [[1, 2, 3, 4]]

jsonObjectData = jsonDataTemplate % tuple(data[0])

crl = pycurl.Curl()

url = f"http://{orionHost}:{orionPort}/v2/op/update"

# curl -X GET \
# 	'http://localhost:1026/v2/entities/urn:ngsiv2:I40Asset:PLC:001' \
# 	-H 'fiware-service: opcua_car' \
# 	-H 'fiware-servicepath: /demo' \
# 	| jq
method = "POST"
header = ['Content-Type: application/json', 'fiware-service: opcua_car', 'fiware-servicepath: /demo']

print(f"curl {method} {url} -H {header} -d {jsonObjectData}")
print("\n ##### A ##### \n")

crl.setopt(crl.URL, url)
crl.setopt(crl.CUSTOMREQUEST, method)
crl.setopt(crl.HTTPHEADER, header)
crl.setopt(crl.POSTFIELDS, jsonObjectData)
crl.perform()

crl.reset()

method = "GET"

url = f"http://{orionHost}:{orionPort}/v2/entities/urn:ngsiv2:I40Asset:PLC:001"
print(url)
print("\n ##### B ##### \n")

crl.setopt(crl.URL, url)
crl.setopt(crl.CUSTOMREQUEST, method)
crl.setopt(crl.HTTPHEADER, ['fiware-service: opcua_car', 'fiware-servicepath: /demo'])

crl.perform()

crl.close()
