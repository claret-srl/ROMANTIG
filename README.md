# ROMANTIG ROSE-AP OEE Calculator


This ROSE-AP is intended as a microservice for automatic OEE, and related metrics, calculation. The service works by connecting to a [Crate database](https://crate.io/) on port 4200, where information about the status of your target process are stored by [Orion](https://fiware-orion.readthedocs.io/en/master/) and [QuantumLeap](https://quantumleap.readthedocs.io/en/latest/) services.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Example](#example)
- [Troubleshooting](#troubleshooting)

## Background
OEE (Overall Equipment Effectiveness) is a metric used in industrial applications to measure the effectiveness and efficiency of a manufacturing process. It is calculated by multiplying the three factors of Availability, Performance, and Quality.

Availability refers to the percentage of time a machine is available to run, taking into account scheduled and unscheduled downtime. Performance measures the actual output of the machine versus its maximum potential output. Quality assesses the percentage of good product produced versus the total number of products produced.

Measuring OEE is important in industrial applications as it provides a comprehensive view of the efficiency of the manufacturing process. By understanding the factors that contribute to inefficiencies, organizations can identify areas for improvement, increase production, and reduce costs. Additionally, OEE is a key indicator of the overall competitiveness of a company, as it is directly tied to production output and profitability.

## Install

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

## Usage
Make the `./services` script executable
```
sudo chmod +x ./services
```
Build the Docker image for the OEE microservice:
```
sudo ./services build
```
To pull all images:
```
./services pull
```
To apply settings and start all the services in the containers run:
```
sudo ./services start
```
Now you can open Grafana on [localhost:3000](localhost:3000) (`user:admin` `password:admin`) and select predefined "Process Status" dashboard to visualiza OEE live data. You can freely add plots and other tables by using the "add new panel" function of Grafana. Below an example:

![grafana_oee](img/dashboard.png)

## Example
Our example use-case scenario is based on an automated welding robotic system which performs several tasks. At first, a stereometric scanner individuates the 3D pose estimate of target pipes, then the robot arm proceeds to pick those and place them in front of a torch, where they will be welded. Once welded, the system proceeds to perform a quality control check to validate the welding: if the check succeeds, the pipe is placed in the final bin; if the check fail, welding is performed again and the QC control the pipe a second time. If the check fails twice in a row, the pipe is discarded. 

The process cycle and the respective up and down time states are shown below:

```mermaid
flowchart LR
    Picking --> Welding --> QC
    QC -- Good Part --> Placing
    QC --> Rework --> QC
    QC -- Bad Part --> Trashing
    Placing & Trashing --> Idle --> Picking

classDef Gainsboro fill:Gainsboro,stroke:#333,color:#333

class Picking,Placing,QC,Welding,upTime,Idle,Trashing,Rework,QC_Rework Gainsboro

linkStyle 0,1,2 stroke:lightgreen,border-color:lightgreen;
linkStyle 3,4,5,6,7,8 stroke:LightCoral;
```

In general, we suggest you to adopt a state space representation similar to the one above for your target process, in order to clearly highlight every step in the cycle and attribute it the correct value for up or down time. The state representation (the onthology of the system) should not be too detailed (i.e. too many states) or too general (i.e. one or two states) because of unnecessary additional workload or possible loss of information.

As it can be seen in the docker-compose file, the PLC responsible for controlling our process is directly connected to Orion Context Broker through the [IoT Agent for OPC-UA](https://iotagent-opcua.readthedocs.io/en/latest/) servers, which is used to write the process states directly on the CrateDB (through QuantumLeap) where they will be read and processed by our OEE calculator.

# Architecture

This application builds on the components and dummy IoT devices created in
[previous tutorials](https://github.com/FIWARE/tutorials.IoT-Agent/). It will use three FIWARE components: the
[Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/), the
[IoT Agent for Ultralight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/), and
[QuantumLeap](https://smartsdk.github.io/ngsi-timeseries-api/) .

Therefore the overall architecture will consist of the following elements:

-   The **FIWARE Generic Enablers**:

    -   The FIWARE [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) which will receive requests
        using [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2)
    -   The FIWARE [IoT Agent for Ultralight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/) which will
        receive northbound measurements from the dummy IoT devices in
        [Ultralight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual)
        format and convert them to [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) requests for the
        context broker to alter the state of the context entities
    -   FIWARE [QuantumLeap](https://quantumleap.readthedocs.io/en/latest/) subscribed to context changes and persisting
        them into a **CrateDB** database

-   A [MongoDB](https://www.mongodb.com/) database:

    -   Used by the **Orion Context Broker** to hold context data information such as data entities, subscriptions and
        registrations
    -   Used by the **IoT Agent** to hold device information such as device URLs and Keys

-   A [CrateDB](https://crate.io/) database:

    -   Used as a data sink to hold time-based historical context data
    -   offers an HTTP endpoint to interpret time-based data queries

-   A **Context Provider**: - A webserver acting as set of
    [dummy IoT devices](https://github.com/FIWARE/tutorials.IoT-Sensors/tree/NGSI-v2) using the
    [Ultralight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual)
    protocol running over HTTP. - Note the **Stock Management Frontend** and **Context Provider NGSI** proxy are not
    used in this tutorial.

Since all interactions between the elements are initiated by HTTP requests, the entities can be containerized and run
from exposed ports.

The overall architecture can be seen below:

```mermaid
  flowchart TD
    Welder[Welder]
    Robot[Robot]
    QC[Quality Control]
    Device[Device]
    PLC[PLC]
    IoT-Agent[IoT-Agent]:::Cyan
    Orion[Orion \n Context Broker]:::DarkBlue
    Quantumleap[Quantum \n Leap]:::DarkBlue
    ROSE-AP(ROSE-AP \n RomanTIG):::Claret
    Redis[(RedisDB)]
    Mongo[(MongoDB)]
    Crate[(CrateDB)]
    Grafana[Grafana]:::Grafana

    Orion & IoT-Agent <--27017:27017---> Mongo
    ROSE-AP <--1026:1026--> Orion
    Quantumleap <--6379:6379--> Redis
    Welder & Robot & QC & Device <--PROFINET--> PLC <--OPC-UA--> IoT-Agent <--4041:4041--> Orion <--8668:8668--> Quantumleap
    Grafana <--4200:4200--> Crate
    ROSE-AP  & Quantumleap <--4200:4200--> Crate
    
classDef DarkBlue fill:#233C68,stroke:#333,color:#FFF
classDef Cyan fill:#45D3DD,stroke:#333,color:#333
classDef Gainsboro fill:Gainsboro,stroke:#333,color:#333
classDef Grafana fill:#333,Stroke:#282828,color:#FCB35F
classDef Claret fill:#0999D0,Stroke:#F8F8F8,color:#F8F8F8

class Crate,Mongo,Redis,Welder,Robot,QC,Device,PLC Gainsboro
```

# Prerequisites

## Docker and Docker Compose

To keep things simple all components will be run using [Docker](https://www.docker.com). **Docker** is a container
technology which allows to different components isolated into their respective environments.

-   To install Docker on Windows follow the instructions [here](https://docs.docker.com/docker-for-windows/)
-   To install Docker on Mac follow the instructions [here](https://docs.docker.com/docker-for-mac/)
-   To install Docker on Linux follow the instructions [here](https://docs.docker.com/install/)

**Docker Compose** is a tool for defining and running multi-container Docker applications. A series of
[YAML files](https://raw.githubusercontent.com/Fiware/tutorials.Time-Series-Data/master/docker-compose.yml) are used to
configure the required services for the application. This means all container services can be brought up in a single
command. Docker Compose is installed by default as part of Docker for Windows and Docker for Mac, however Linux users
will need to follow the instructions found [here](https://docs.docker.com/compose/install/)

You can check your current **Docker** and **Docker Compose** versions using the following commands:

```console
docker-compose -v
docker version
```

Please ensure that you are using Docker version 20.10 or higher and Docker Compose 1.29 or higher and upgrade if
necessary.

# Troubleshooting

If the following error will appear creating or starting the container
```
/bin/bash^M: bad interpreter: No such file or directory
```
Please use the utility `dos2unix` to convert the text files from DOS/Mac to Unix enviroment, install dos2unix on CentOS/Fedora/RHEL
```
sudo yum update
sudo yum install dos2unix
```
or in Ubuntu/Debian:
```
sudo apt update
sudo apt install dos2unix
```
Then run the following command, in the root directory, to convert all the text files from DOS/Mac to Unix enviroment 
```
dos2unix ./.env ./docker-compose.yml ./import-data ./provision-devices ./services
```

## CrateDB

If the CrateDB container crashes after startup, run the following command:
```
sudo sysctl vm.max_map_count=262144
```
This setting in included in the script case `sudo ./services up`.

## Redis

If the Redis container crashes after startup, run the following command:
```
sudo sysctl vm.overcommit_memory=1
```
This setting in included in the script case `sudo ./services up`.
