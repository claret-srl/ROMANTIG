import os, time, random, asyncio

from asyncua import Server
from dotenv import load_dotenv


script_dir = os.path.dirname(__file__)

load_dotenv(script_dir + "//" + ".env")

OPCUA_PORT = os.getenv("OPCUA_PORT")  # 4840

OCB_ID_PROCESS = os.getenv("OCB_ID_PROCESS")  # processStatus
OCB_ID_MACHINE = os.getenv("OCB_ID_MACHINE")  # machineStatus

OPCUA_ID_PROCESS = os.getenv("OPCUA_ID_PROCESS")  # ns=4;i=198
OPCUA_ID_MACHINE = os.getenv("OPCUA_ID_MACHINE")  # ns=4;i=339

async def main():

    # setup the server
    server = Server()
    await server.init()

    server.set_endpoint(f"opc.tcp://0.0.0.0:{OPCUA_PORT}/")

    # # set up the namespace, not really necessary but should as spec
    # uri = "https://examples.freeopcua.github.io"

    # # default namespace, is unused since variable are set matching the same nemeSpace and Id of the real PLC
    # ns = await server.register_namespace(uri)

    parentObj = await server.nodes.objects.add_object("ns=4;i=1", "DIH_Welding")

    # Set Variables matching the same nemeSpace and Id of the real PLC
    processStatusVar = await parentObj.add_variable(
        OPCUA_ID_PROCESS, OCB_ID_PROCESS, "Idle"
    )
    machineStatusVar = await parentObj.add_variable(
        OPCUA_ID_MACHINE, OCB_ID_MACHINE, True
    )

    # Set variable to be writable by clients
    await processStatusVar.set_writable()
    await machineStatusVar.set_writable()

    async with server:

        cycleCounter = 1
        CycleToSwitch = 10
        pseudoRandom = 75
        alreadyEntered = False

        while True:

            processStates = ["Idle", "In Picking", "In Welding", "In QC"]

            for status in processStates:

                if status == "In Placing" or status == "In Trashing":
                    cycleCounter += 1
                    alreadyEntered = False

                elif status == "In QC":
                    nextStatus = ["In Placing", "In Reworking"]
                    processStates.append(nextStatus[round(random.randint(0, pseudoRandom) / pseudoRandom)])

                elif status == "In Reworking":
                    nextStatus = "In QC from rework"
                    processStates.append(nextStatus)

                elif status == "In QC from rework":
                    nextStatus = ["In Placing", "In Trashing"]
                    processStates.append(nextStatus[round(random.randint(0, pseudoRandom) / pseudoRandom)])

                print(f"Set value of {processStatusVar} to {status}")
                await processStatusVar.write_value(status)
                await asyncio.sleep(random.randint(2, 4))

                if cycleCounter % CycleToSwitch == 0:
                    if not alreadyEntered:
                        alreadyEntered = True
                        print(f"Set value of {processStatusVar} to Offline")
                        await processStatusVar.write_value("Offline")
                        await asyncio.sleep(random.randint(120, 180))


if __name__ == "__main__":
    asyncio.run(main(), debug=False)
