```mermaid
flowchart TD
flowchart
    Idle --> Picking --> Welding --> QC
    QC -- Rework --> Welding
    QC -- Bad Part --> Trashing --> Idle
    QC -- Good Part --> Placing --> Idle

classDef upTime fill:lightgreen,stroke:#333,color:#333
classDef downTime fill:LightCoral,stroke:#333,color:#333
classDef upDownTime fill:#f7dc6f,stroke:#333,color:#333

class Picking,Welding,Placing upTime
class Idle,Trashing,Rework downTime
class QC upDownTime
```
