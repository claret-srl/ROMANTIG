def append_ARGS(_data):
    return {
        "actionType": "append",
        "entities": [
            {
                "id"			:	"urn:ngsiv2:I40Asset:PLC:001",
                "type"			:	"PLC",
                "OEE"			:	{"type": "Float", "value": _data[0][0]},
                "Availability"	:	{"type": "Float", "value": _data[0][1]},
                "Performance"	:	{"type": "Float", "value": _data[0][2]},
                "Quality"		:	{"type": "Float", "value": _data[0][3]},
            }
        ],
    }
