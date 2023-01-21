## Misc
- [x] CrateDB persistent (Splitted stop and delete case for services script)
- [x] Improve Grafana dashboard (https://github.blog/2022-05-19-math-support-in-markdown/)
- [x] Update Grafana to 9.1.3 (latest)
- [x] Update IoT-Agent to 2.0.5 (latest)
- [x] Update to Orion 3.7.0000 (latest stable)
- [x] Update to Mongo 4.4.18
- [x] Update to Crate 5.1.3 (latest)
- [x] Update to Redis 7.0.8 (latest)
- [x] Services port inherit from .env file
- [ ] Make the PLC IP configurable
- [ ] set .env in provision-device import-data
- [ ] riscrivere lo script python
## Phase 3
- [x] Github repository
- [ ] Step by Step Tutorial (nuova build, specificare l'origine dei dati, procesStatus, e lo switch di eventual icomponenti spedcificando l'architettura)
- [ ] NGSI-V2 Naming standard for procesStatus
- [ ] ID and atribute following Smart Factory Demo (https://github.com/FcoMelendez/smart_factory_demo)
### ROSE-AP
- [ ] Add information on machine activation status (e.g. records and calculate OEE only when it's active).
	- Provision the information about hte schedule production to know when in planned production on the microservice. (https://www.machinemetrics.com/blog/oee-ooe-teep)
- [ ] Add information about reworks (parts and time).
- [ ] Add information about total OEE stats for all the production.
- [ ] Extend to Factory level (e.g. un elemento nel contex broker che comunica lo scheduling dei turni di lavoro)


## RAMP in remoto
- Connessione remota RAMP

## Business
- Intregrare presso 2 clienti o lettera di intenti.
- Fee annuale per integrazione sulle macchine.

## Architettura
![Architettura](img/architettura.png)

## Mermaid
```mermaid
flowchart TD
    A[Start] --> B{Is it?}
    B -- Yes --> C[OK]
    C --> D[Rethink]
    D --> B
    B -- No ----> E[End]
```
