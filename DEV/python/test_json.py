import json

data = [[1,2,3,4]]


DataTemplateDict = {
  "actionType": "append",
  "entities": [
	{
	  "id": "urn:ngsiv2:I40Asset:PLC:001",
	  "type": "PLC",
	  "OEE": {
		"type": "Float",
		"value": data[0][0]
	  },
	  "Availability": {
		"type": "Float",
		"value": data[0][1]
	  },
	  "Performance": {
		"type": "Float",
		"value": data[0][2]
	  },
	  "Quality": {
		"type": "Float",
		"value": data[0][3]
	  }
	}
  ]
}

DataTemplateJson = json.dumps(DataTemplateDict, indent=2)

print(json.dumps(DataTemplateJson, indent=2))