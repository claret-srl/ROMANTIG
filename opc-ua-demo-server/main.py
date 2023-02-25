import asyncio, logging, random, os, time

from asyncua import Server
from dotenv import load_dotenv


script_dir = os.path.dirname(__file__)

load_dotenv(script_dir + "//" + ".env")

LOG_LEVEL = os.getenv("LOG_LEVEL")  # debug

OPCUA_PORT = os.getenv("OPCUA_PORT")  # 4840

OCB_ID_PROCESS = os.getenv("OCB_ID_PROCESS")  # processStatus
OCB_ID_MACHINE = os.getenv("OCB_ID_MACHINE")  # machineStatus

OPCUA_ID_PROCESS = os.getenv("OPCUA_ID_PROCESS")  # ns=4;i=198
OPCUA_ID_MACHINE = os.getenv("OPCUA_ID_MACHINE")  # ns=4;i=339

print(LOG_LEVEL)


async def main():

    _logger = logging.getLogger(__name__)

    # setup the server
    server = Server()
    await server.init()

    server.set_endpoint(f"opc.tcp://0.0.0.0:{OPCUA_PORT}/")

    # # set up the namespace, not really necessary but should as spec
    # uri = "https://examples.freeopcua.github.io"

    # # default namespace, is unused since variable are set matching the same nemeSpace and Id of the real PLC
    # ns = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
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

    _logger.info("Starting server...")

    async with server:

        cycleCounter = 1
        CycleCounterToSwitch = 2
        pseudoRandom = 75

        while True:

            processStates = ["Idle", "In Picking", "In Welding", "In QC"]
            # machineState = await machineStatusVar.get_value()

            if cycleCounter % CycleCounterToSwitch == 0:

                # oldMachineStatusVar = await machineStatusVar.get_value()
                # newMachineStatusVar = not oldMachineStatusVar

                await machineStatusVar.write_value(False)
                _logger.info("Set value of %s to %s", machineStatusVar, "False")
                
                await asyncio.sleep(random.randint(4, 7))
                
                await machineStatusVar.write_value(True)
                _logger.info("Set value of %s to %s", machineStatusVar, "True")
                
                cycleCounter += 1
                               
            else:
                for status in processStates:

                    if status == "In Placing" or status == "In Trashing":
                        cycleCounter += 1

                    elif status == "In QC":
                        nextStatus = ["In Placing", "In Reworking"]
                        processStates.append(nextStatus[round(random.randint(0, pseudoRandom) / pseudoRandom)])

                    elif status == "In Reworking":
                        nextStatus = "In QC from rework"
                        processStates.append(nextStatus)

                    elif status == "In QC from rework":
                        nextStatus = ["In Placing", "In Trashing"]
                        processStates.append(nextStatus[round(random.randint(0, pseudoRandom) / pseudoRandom)])

                    await asyncio.sleep(random.randint(4, 7))
                    await processStatusVar.write_value(status)
                    _logger.info("Set value of %s to %s", processStatusVar, status)

                    # print(f"""\ncycleCounter:  [{cycleCounter}]\nprocessStatus: [{status}]\nmachineStatus: [{machineState}]""")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=False)
