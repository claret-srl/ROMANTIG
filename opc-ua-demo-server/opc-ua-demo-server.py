import asyncio
import logging
import random
import os

from asyncua import Server
from dotenv import load_dotenv


script_dir = os.path.dirname(__file__)

load_dotenv(script_dir + "//" + ".env")

LOG_LEVEL = os.getenv("LOG_LEVEL")  # debug

DEMO_SERVER = os.getenv("DEMO_SERVER")  # opc-ua-demo-server
DEMO_SERVER_PORT = os.getenv("DEMO_SERVER_PORT")  # 4880

OCB_ID_process = os.getenv("OCB_ID_process")  # processStatus
OCB_ID_machine = os.getenv("OCB_ID_machine")  # machineStatus

IOTA_OPCUA_ID_process = os.getenv("IOTA_OPCUA_ID_process")  # ns=4;i=198
IOTA_OPCUA_ID_machine = os.getenv("IOTA_OPCUA_ID_machine")  # ns=4;i=339


async def main():

    _logger = logging.getLogger(__name__)

    # setup the server
    server = Server()
    await server.init()

    server.set_endpoint(f"opc.tcp://0.0.0.0:{DEMO_SERVER_PORT}/")

    # # set up the namespace, not really necessary but should as spec
    # uri = "https://examples.freeopcua.github.io"

    # # default namespace, is unused since variable are set matching the same nemeSpace and Id of the real PLC
    # ns = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    parentObj = await server.nodes.objects.add_object("ns=4;i=1", "DIH_Welding")

    # Set Variables matching the same nemeSpace and Id of the real PLC
    processStatusVar = await parentObj.add_variable(
        IOTA_OPCUA_ID_process, OCB_ID_process, "Idle"
    )
    machineStatusVar = await parentObj.add_variable(
        IOTA_OPCUA_ID_machine, OCB_ID_machine, True
    )

    # Set variable to be writable by clients
    await processStatusVar.set_writable()
    await machineStatusVar.set_writable()

    _logger.info("Starting server...")

    async with server:

        cycleCounter = 0

        while True:

            processStates = ["Idle", "In Picking", "In Welding", "In QC"]

            for status in processStates:
                print(
                    f"""
                    cycleCounter:  [{cycleCounter}]
                    processStatus: [{status}]
                    machineStatus: [{await machineStatusVar.get_value()}]
                    -------------
                """
                )
                # print(f"\nprocessStates are: {processStates}")

                if status == "In Placing" or status == "In Trashing":
                    cycleCounter += 1
                    if cycleCounter % 2 == 0:
                        oldValue = await machineStatusVar.get_value()
                        await machineStatusVar.write_value(not oldValue)
                    break

                elif status == "In QC":
                    nextStatus = ["In Placing", "In Reworking"]
                    processStates.append(nextStatus[random.randint(0, 1)])

                elif status == "In Reworking":
                    nextStatus = "In QC from rework"
                    processStates.append(nextStatus)

                elif status == "In QC from rework":
                    nextStatus = ["In Trashing", "In Placing"]
                    processStates.append(nextStatus[random.randint(0, 1)])

                await asyncio.sleep(random.randint(2, 4))
                await processStatusVar.write_value(status)

                # _logger.info("Set value of %s to %s", processStatusVar, status)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(), debug=False)
