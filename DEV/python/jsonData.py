import json
from collections import namedtuple
from json import JSONEncoder

def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())

#Assume you received this JSON response

Availability = 0.4
Performance = 0.3
Quality = 0.2
Oee = 0.1

studentJsonData = "{'actionType': 'append','entities': [{'id': 'urn:ngsiv2:I40Asset:PLC:001','type': 'PLC','Availability': {'type': 'Float','value':" + Availability + "},'Performance': {'type': 'Float','value':" + Performance + "},'Quality': {'type': 'Float','value':" + Quality + "},'OEE': {'type': 'Float','value':" + Oee + "}}]}"

# Parse JSON into an object with attributes corresponding to dict keys.
student = json.loads(studentJsonData, object_hook=customStudentDecoder)

print("After Converting JSON Data into Custom Python Object")
print(student.rollNumber, student.name)