def provisioning_ARGS(
    IOTA,
    IOTA_NORTH_PORT,
    ORION,
    ORION_PORT,
    DEVICE_BASE_ID,
    DEVICE_ID,
    DEVICE_TYPE,
    OCB_ID,
    ROSEAP_OEE,
    ROSEAP_OEE_PORT,
    QUANTUMLEAP,
    QUANTUMLEAP_PORT,
    Service,
    ServicePath,
    contentType,
):
    return [
        ##### IoT-Agent
        ##### Service Group
        ##### PLC
#         {
#             "method": "POST",
#             "service": IOTA,
#             "port": IOTA_NORTH_PORT,
#             "NGSI": "iot",
#             "endpoint": "services",
#             "path": None,
#             "header": [Service, ServicePath, contentType["json"]],
#             "payload": '''{
#     "services": [
#         {
#             "apikey": "''' + ORION + "-" + ORION_PORT + "-" + DEVICE_TYPE + "-" + '''/iot/d",
#             "cbroker": "http://''' + ORION + ":" + ORION_PORT + '''",
#             "entity_type": "''' + DEVICE_TYPE + '''",
#             "resource": "/iot/d"
#         }
#     ]
# }'''
#         },
        # ##### IoT-Agent
        # ##### Device
        # ##### urn:ngsiv2:I40Asset:PLC:001
#         {
#             "method": "POST",
#             "service": IOTA,
#             "port": IOTA_NORTH_PORT,
#             "NGSI": "iot",
#             "endpoint": "devices",
#             "path": None,
#             "header": [Service, ServicePath, contentType["json"]],
#             "payload": '''{
#     "devices": [
#         {
#             "device_id": "''' + DEVICE_ID + '''",
#             "type": "''' + DEVICE_TYPE + '''",
#             "attributes": [
#                 {
#                     "name": "''' + OCB_ID + '''",
#                     "type": "Text"
#                 }
#             ]
#         }
#     ]
# }'''
#         },
        # ##### Contex Broker
        # ##### Entity
        # ##### urn:ngsiv2:I40Asset:Area:001
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "entities",
            "path": None,
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '{"type": "Area", "id": "' + DEVICE_BASE_ID + ':Area:001"}',
        },
        # ##### Contex Broker
        # ##### Entity
        # ##### urn:ngsiv2:I40Asset:Workstation:001
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "entities",
            "path": None,
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '{"type": "Workstation", "id": "' + DEVICE_BASE_ID + ':Workstation:001"}',
        },
        # ##### Contex Broker
        # ##### Relationship
        # ##### urn:ngsiv2:I40Asset:Workstation:001
        # ##### has parent
        # ##### urn:ngsiv2:I40Asset:Area:001
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "op/update",
            "path": None,
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '''{
    "actionType": "APPEND",
    "entities": [
        {
            "id": "''' + DEVICE_BASE_ID + ''':Workstation:001",
            "type": "''' + DEVICE_TYPE + '''",
            "hasParentI40Asset": {
                "type": "Relationship",
                "value": "''' + DEVICE_BASE_ID + ''':Area:001"
            }
        }
    ]
}'''
        },
        # ##### Contex Broker
        # ##### Relationship
        # ##### urn:ngsiv2:I40Asset:PLC:001
        # ##### has parent
        # ##### urn:ngsiv2:I40Asset:Workstation:001
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "op/update",
            "path": None,
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '''{
    "actionType": "APPEND",
    "entities": [
        {
            "id": "''' + DEVICE_ID + '''",
            "type": "''' + DEVICE_TYPE + '''",
            "hasParentI40Asset": {
                "type": "Relationship",
                "value": "''' + DEVICE_BASE_ID + ''':Workstation:001"
            }
        }
    ]
}'''
        },
        # ##### Contex Broker
        # ##### Subscriptions
        # ##### on
        # ##### urn:ngsiv2:I40Asset:PLC:001 processstatus
        # ##### value changhe
        # ##### notify
        # ##### Quantumleap
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "subscriptions",
            "path": None,
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '''{
    "description": "Orion notify Quantumleap",
    "subject": {
        "entities": [
            {
                "id": "''' + DEVICE_ID + '''",
                "type": "''' + DEVICE_TYPE + '''"
            }
        ],
        "condition": {
            "attrs": ["''' + OCB_ID + '''"]
        }
    },
    "notification": {
        "http": {
            "url": "http://''' + QUANTUMLEAP + ''':'''+ QUANTUMLEAP_PORT+ '''/v2/notify"
        },
        "attrs": ["''' + OCB_ID + '''"]
    }
}''',
        },
        # ##### Contex Broker
        # ##### Subscriptions
        # ##### on
        # ##### urn:ngsiv2:I40Asset:PLC:001 processstatus
        # ##### value changhe
        # ##### notify
        # ##### OEE-Service
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "subscriptions",
            "path": None,
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '''{
    "description": "Orion notify OEE-service",
    "subject": {
        "entities": [
            {
                "id": "''' + DEVICE_ID + '''",
                "type": "''' + DEVICE_TYPE + '''"}
            ],
        "condition": {
            "attrs": ["''' + OCB_ID + '''"]
        }
    },
    "notification": {
        "http": {
            "url": "http://''' + ROSEAP_OEE + ":" + ROSEAP_OEE_PORT + '''/"
        },
        "attrs": ["''' + OCB_ID + '''"]
    }
}''',
        }
    ]
    

def update_ARGS(ORION, ORION_PORT, Service, ServicePath, contentType, DEVICE_ID, DEVICE_TYPE, _data
):
    return [
        # ##### Contex Broker
        # ##### Append Attribute
        # ##### OEE, Availability, Performance, Quality
        # ##### to
        # ##### urn:ngsiv2:I40Asset:PLC:001
        {
            "method": "POST",
            "service": ORION,
            "port": ORION_PORT,
            "NGSI": "v2",
            "endpoint": "entities" ,
            "path": DEVICE_ID + "/attrs",
            "header": [Service, ServicePath, contentType["json"]],
            "payload": '''{
    "OEE"           :    {"type": "Float", "value": '''+ str(_data[0][0])+ '''},
    "Availability"  :    {"type": "Float", "value": '''+ str(_data[0][1])+ '''},
    "Performance"   :    {"type": "Float", "value": '''+ str(_data[0][2])+ '''},
    "Quality"       :    {"type": "Float", "value": '''+ str(_data[0][3])+ '''}
}'''
        }
        # ,
        # {
        #     "method": "POST",
        #     "service": ORION,
        #     "port": ORION_PORT,
        #     "NGSI": "v2",
        #     "endpoint": "op/update",
        #     "path": None,
        #     "header": [Service, ServicePath, contentType["json"]],
        #     "payload": '''
        #         {
        #             "actionType": "append",
        #             "entities": [
        #                 {
        #                     "id"            :    "''' + DEVICE_ID + '''",
        #                     "type"          :    "''' + DEVICE_TYPE + '''",
        #                     "OEE"           :    {"type": "Float", "value": '''+ str(_data[0][0])+ '''},
        #                     "Availability"  :    {"type": "Float", "value": '''+ str(_data[0][1])+ '''},
        #                     "Performance"   :    {"type": "Float", "value": '''+ str(_data[0][2])+ '''},
        #                     "Quality"       :    {"type": "Float", "value": '''+ str(_data[0][3])+ '''}
        #                 }
        #             ]
        #         }
        #     ''',
        # }
        # ,
        # {
        #     'method'    :    'GET',
        #     'service'   :    ORION,
        #     'port'      :    ORION_PORT,
        #     'NGSI'      :    'v2',
        #     'endpoint'  :    'entities',
        #     'path'      :    DEVICE_ID,
        #     'header'    :    [Service, ServicePath],
        #     'payload'   :    None
        # }
    ]
