```mermaid
graph TD
    A[Christmas] -->|Get money| B(Go shopping)
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
	<i class="fa-duotone fa:fa-ethernet"></i>
```

```mermaid
  flowchart TD
    Welder[fa:fa-broom Welder]:::Cyan
    Robot[fa:fa-robot Robot]:::Cyan
    QC[fa:fa-video QC]:::Cyan
    Device[fa:fa-ethernet Device]:::Cyan
    PLC[fa:fa-microchip PLC]:::Cyan
    IoT-Agent[fa:fa-network-wired IoT-Agent]:::Cyan
    Orion[Orion \n Context Broker]:::DarkBlue
    Quantumleap[Quantum \n Leap]:::DarkBlue
    ROSE-AP(fa:fa-wand-magic-sparkles \n ROSE-AP \n RomanTIG):::ROSE-AP
    Redis[(fa:fa-server \n RedisDB)]
    Mongo[(fa:fa-server \n MongoDB)]
    Crate[(fa:fa-server \n CrateDB)]
    Grafana[fa:fa-chart-line \n Grafana]


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
classDef ROSE-AP fill:#F8F8F8,Stroke:#0999D0,color:#0999D0

class Crate,Mongo,Redis Gainsboro
class Grafana Grafana
```

classDef upTime fill:lightgreen,stroke:#333,color:#333
classDef downTime fill:LightCoral,stroke:#333,color:#333
classDef upDownTime fill:#f7dc6f,stroke:#333,color:#333

class Picking,Placing,upTime upTime
class Idle,Trashing,Rework,downTime downTime
class QC,Welding upDownTime
```
```mermaid
flowchart LR
    subgraph Legend
    downTime[Down Time]
    upTime[Up Time]
    end
    
    subgraph Flow Chart Compact
    Idle --> Picking --> Welding --> QC
    QC -- Rework --> Welding
    QC -- Bad Part --> Trashing --> Idle
    QC -- Good Part --> Placing --> Idle
    end


classDef upTime fill:lightgreen,stroke:#333,color:#333
classDef downTime fill:LightCoral,stroke:#333,color:#333
classDef upDownTime fill:#f7dc6f,stroke:#333,color:#333

class Picking,Placing,upTime upTime
class Idle,Trashing,Rework,downTime downTime
class QC,Welding upDownTime
```
