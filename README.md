# ROMANTING ROSE-AP OEE Calculator


This ROSE-AP is intended as a microservice for automatic OEE, and related metrics, calculation. The service works by connecting to a [Crate database](https://crate.io/) on port 4200, where information about the status of your target process are stored by [Orion](https://fiware-orion.readthedocs.io/en/master/) and [QuantumLeap](https://quantumleap.readthedocs.io/en/latest/) services.


## Configuration

In order to compute the OEE, the service must know if each possible process state that is found on CrateDB has to be considered an up-time or a down-time state. To do so, please change the `oee_conf.config` file found in the `oee_service` folder, prior to building the image of the service. You have to set the following variables:

```
[PROCESS]
upTimeStates = ["upTimeStateName1","upTimeStateName2",...,"upTimeStateNameN"] #These represents the states to be considered as up-time
downTimeStates = ["downTimeStateName1","downTimeStateName2",...,"downTimeStateNameN"]#These represents the states to be considered as down-time
endStates =["upTimeStateNameN","downTimeStateNameN",...] #Subset of either upTimeStates, downTimeStates or both. These represents the possibly multiple final states of the process
goodEnd =["endStatesName1",...] #Subset of endStates, these represents the final states in which an item is successfully created
badEnd =["endStatesName2",...] #Subset of endStates, these represents the final states in which an item is defective or faulty and has to be discarded

[OEE]
timestep = 300 #The timestep granularity (integer) for the resulting OEE metrics, in seconds
idealTime_ppm = 5 #The theoretical maximum piece per minute rate (integer) that the process is able to deliver in ideal conditions (note: this ppm value cannot be lower than the actual process output rate as this represents a theoretical upper bound) 
```

Be sure that the name of the states written in the config file perfectly match those that are written by your process to the CrateDB, so that the microservice can correctly identify them.

## Setup

navigate to oee-service folder and build the image for the OEE microservice:

```
  cd oee-service

  docker build -t rose-ap-oee .
```
Go back to the main folder and make the `./services` script executable
```
  cd ..
  sudo chmod +x ./services
```
Run  `sudo ./services create` to create all images, then run `./services start` to start the containers.

Now you can open Grafana on `localhost:3000` and select predefined "Process Status" dashboard to visualiza OEE live data. You can freely add plots and other tables by using the "add new panel" function of Grafana.

## Example

Our example use-case scenario is based on an automated welding robotic system which performs several tasks. At first, a stereometric scanner individuates the 3D pose estimate of target pipes, then the robot arm proceeds to pick those and place them in front of a torch, where they will be welded. Once welded, the system proceeds to perform a quality control check to validate the welding: if the check succeeds, the pipe is placed in the final bin; if the check fail, welding is performed again and the QC control the pipe a second time. If the check fails twice in a row, the pipe is discarded. 

The process cycle and the respective up and down time states are shown below:

![mockup_cycle](https://user-images.githubusercontent.com/35039520/185942765-a7667e8e-95bb-45d6-b462-54c7703aeb46.png)

In general, we suggest you to adopt a state space representation similar to the one above for your target process, in order to clearly highlight every step in the cycle and attribute it the correct value for up or down time. The state representation (the onthology of the system) should not be too detailed (i.e. too many states) or too general (i.e. one or two states) because of unnecessary additional workload or possible loss of information.

<<<<<<< HEAD
As it can be seen in the docker-compose file, the PLC responsible for controlling our process is directly connected to Orion Context Broker through the [IoT Agent for OPC-UA](https://iotagent-opcua.readthedocs.io/en/latest/) servers, which is used to write the process states directly on the CrateDB (through QuantumLeap) where they will be read and processed by our OEE calculator. 
=======
As it can be seen in the docker-compose file, the PLC responsible for controlling our process is directly connected to Orion Context Broker through the [IoT Agent for OPC-UA](https://iotagent-opcua.readthedocs.io/en/latest/) servers, which is used to write the process states directly on the CrateDB (through QuantumLeap) where they will be read and processed by our OEE calculator. 
>>>>>>> f202b0460152975509df9dcac2632c381f0fb5d9
