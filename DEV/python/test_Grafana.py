import os
import json

script_dir = os.path.dirname(__file__)

CRATE_SCHEMA = os.getenv("CRATE_SCHEMA")  # mtopcua_car
CRATE_TABLE = os.getenv("CRATE_TABLE")  # etdevice
CRATE_TABLE_DEVICE = os.getenv("CRATE_TABLE_DEVICE")  # etdevice
CRATE_TABLE_DURATION = os.getenv("CRATE_TABLE_DURATION")  # etprocessduration
CRATE_TABLE_OEE = os.getenv("CRATE_TABLE_OEE")  # etoee

replacesGrafana = {
    "mtopcua_car": CRATE_SCHEMA,
	"process_status_oee": CRATE_TABLE_OEE,
	"etplc": CRATE_TABLE_DEVICE
}

def replace_in_string(replaces, dirSurce, dirTarget):
	with open(f"{script_dir}\{dirSurce}", "r") as inputFile:
		GrafanaConfiguration = inputFile.read()

	for key, value in replaces.items():
		GrafanaConfiguration = GrafanaConfiguration.replace(key, value.lower())

	with open(f"{script_dir}\{dirTarget}", "w") as outputFile:
		outputFile.write(GrafanaConfiguration)

replace_in_string(replacesGrafana, "..\\grafana\\dashboards\\dashboard.src", "..\\grafana\\dashboards\\dashboard.json")