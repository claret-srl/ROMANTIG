import os
from dotenv import load_dotenv


def envArrayToString(_Array):
	output = str()
	spacing = ", "
	spacingLen = len(spacing)

	_Array = _Array.split(",")

	for element in _Array :
		element = element.strip()
		if len(element) != 0:
			output += f"'{element}'" + spacing

	if output[-spacingLen:] == spacing:
		output = output[:-spacingLen]

	return output

script_dir = os.path.dirname(__file__)

load_dotenv(script_dir + "//" + ".env")

ENDSGOOD = os.getenv('ENDSGOOD')
ENDSBAD = os.getenv('ENDSBAD')
TIMESUP = os.getenv('TIMESUP')
TIMESDOWN = os.getenv('TIMESDOWN')
TIMESTEP = os.getenv('TIMESTEP')
IDEALTIME = os.getenv('IDEALTIME')
OEE_START_DATE = os.getenv('START_DATE')
OEE_START_TIME = os.getenv('START_TIME')

result = envArrayToString(TIMESUP)
print("\n", result)

result = envArrayToString(TIMESDOWN)
print("\n", result)