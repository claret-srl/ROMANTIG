import pycurl
  
jsonData = '{"actionType": "append","entities": [{"id": "urn:ngsiv2:I40Asset:PLC:001","type": "PLC","Availability": {"type": "Float","value":' + str(availability) + '},"Performance": {"type": "Float","value":' + str(performance) + '},"Quality": {"type": "Float","value":' + str(quality) + '},"OEE": {"type": "Float","value":' + str(oee) + '}}]}'

# print(jsonData)

crl = pycurl.Curl()
crl.setopt(crl.URL,"http://localhost:1026/v2/op/update")
crl.setopt(crl.CUSTOMREQUEST, "POST")
crl.setopt(crl.HTTPHEADER, ['Content-Type: application/json'])
crl.setopt(crl.POSTFIELDS, jsonData)
crl.perform()
crl.close()