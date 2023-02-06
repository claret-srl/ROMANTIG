import os
import configparser


# Configuration
script_dir = os.path.dirname(__file__)
path = script_dir + "//" + "oee_conf.config"

config = configparser.ConfigParser()

try:
	print("[INFO] Reading configuration."+ "\n")
	config.read(path)
	print("[INFO] Successful configuration file reading."+ "\n")
	try:
		upTimeStates = config["PROCESS"]["upTimeStates"].split(",")
		downTimeStates = config["PROCESS"]["downTimeStates"].split(",")

		endStates = config["PROCESS"]["endStates"].split(",")
		startStates = config["PROCESS"]["startStates"].split(",")

		goodEnd = config["PROCESS"]["goodEnd"].split(",")
		badEnd = config["PROCESS"]["badEnd"].split(",")

		idealTime = float(config["OEE"]["idealTime_ppm"]) / 60
		timestep = int(config["OEE"]["timestep"])

	except Exception as e:
		print("[ERROR] Reading configuration file fail:\n" + e + "\n")

except Exception as e:
	print("[ERROR] Reading configuration file fail:\n" + e + "\n")

# print(type(upTimeStates))
# print(upTimeStates)

print("(" + ', '.join(upTimeStates) + ")")
print("(" + ', '.join(downTimeStates) + ")")