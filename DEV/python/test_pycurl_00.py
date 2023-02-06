import pycurl

Availability = 0.4
Performance = 0.3
Quality = 0.2
Oee = 0.1

jsonData = '{"actionType": "append","entities": [{"id": "urn:ngsiv2:I40Asset:PLC:001","type": "PLC","Availability": {"type": "Float","value":' + str(Availability) + '},"Performance": {"type": "Float","value":' + str(Performance) + '},"Quality": {"type": "Float","value":' + str(Quality) + '},"OEE": {"type": "Float","value":' + str(Oee) + '}}]}'


# print(jsonData)

crl = pycurl.Curl()
crl.setopt(crl.URL,"http://localhost:1026/v2/op/update")
# crl.setopt(crl.URL,"http://localhost:1026/version")
# crl.setopt(crl.CUSTOMREQUEST, "GET")
crl.setopt(crl.CUSTOMREQUEST, "POST")
# crl.setopt(crl.HTTPHEADER, 'Content-Type: application/json')
crl.setopt(crl.HTTPHEADER, ['Content-Type: application/json'])
crl.setopt(crl.POSTFIELDS, jsonData)
crl.perform()
crl.close()