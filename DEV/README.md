## Business
- [ ] Intregrare presso 3 clienti o lettera di intenti.
	- [ ] Zenti
	- [ ] G.Engineering
	- [ ] Laserlam
- [ ] Fee annuale per integrazione sulle macchine.
- [ ] Business Plan.

## docker-compose
- [x] mettere tutte le variabili dell .env
- [x] Check if is possible to assign .env variable to service_id and volume_id
- [ ] oee-service folder name
- [ ] debug level for all services
- [x] org.fiware
- [x] Fix unused and Mongo anonymus volumes
## services
- [x] mettere tutte le variabili dell .env

## ROSE-AP
- [ ] None instead of Null
- [ ] Pushing the img to docker hub
- [ ] Unificare nomenclatua rose-ap-OEE
- [ ] set .env in provision-device import-data
- [ ] Rimuovere pull remoto docker img rose ap, e ripristinarlo in produzione
- [ ] improve doc both github and grafana
	- [x] Mermaid
	- [x] https://github.blog/2022-05-19-math-support-in-markdown/
- [x] Add Where NAME = ngsi:v2:...:I40Asset:PLC
- [x] Removed the absurd necessity to re-build in case of .config update, (update .config > restart the service)
- [x] L'oee va calcolato on deamand ad ogni prodotto completato, per poi visualizzare a piacimento i dati potendo filtrare per prodotto, lotto, ora/giorno/mese/anno (websocket?)
- [x] Ciclo tempo non prevede l'evenienza che non entri nel ciclo la prima volta
- [x] Division by 0
- [x] Ciclo tempo assurdo
- [x] Division by 0
- [x] Non gestite le eccezzioni di connessione
- [x] Non gestite le eccezzioni di inserimento con key duplicata
- [x] CrateDB persistent (Splitted stop and delete case for services script)
- [x] Improve Grafana dashboard 
- [x] Update Grafana to 9.3.6 (latest)
- [x] Update Grafana to 9.1.3 (latest)
- [x] Update IoT-Agent to 2.0.5 (latest working)
- [x] Update to Orion 3.8.0 (latest)
- [x] Update to Orion 3.7.0000 (latest stable)
- [x] Update to Mongo 6.0.4 (latest)
- [x] Update to Mongo 4.4.18 (latest 4.xx.xx)
- [x] Update to Crate 5.1.3 (latest)
- [x] Update to Redis 7.0.8 (latest)
- [x] Services port inherit from .env file
- [x] Add waitForQuantumleap
- [x] Switch Base image of the OEE-Service to python:3.9.16-alpine3.17 (from 892.95MB to 59.35MB)
- [x] Make the PLC IP configurable in the same file as the .config of the ROSE-AP
- [x] remove duplicated setEnviroment() in services, env var are passed trough commands -e "${ENV}=ENV"
- [x] riscrivere lo script python
- [x] si possono rimuovere i WaitForCotiners visto che adesso startano in ordine?
- [x] WARN[0000] The "host" variable is not set. Defaulting to a blank string.
	- host=0.0.0.0 in .env, default host for docker services
- [x] job-working-directory: error retrieving current directory: getcwd: cannot access parent directories: No such file or directory
	- error related to the remote pull of a local docker service
- [x] Rename cmd create to pull

## Grafana
- [x] grafana\datasources\datasource.yaml db-crate host, ports, mtopcua_car
- [ ] Shared Data between dashboard
- [x] Provisioning datasurce from .env
- [x] .env table name
	- Non è possibile senza plugin di terze parti
## Phase 3
- [x] Github repository
- [ ] Step by Step Tutorial (nuova build, specificare l'origine dei dati, procesStatus, e lo switch di eventual icomponenti spedcificando l'architettura)
- [x] NGSI-V2 Naming standard for procesStatus
- [x] ID and atribute following Smart Factory Demo (https://github.com/FcoMelendez/smart_factory_demo)
- [x] Modificare il provisioning dei device e relashhionship con gli header corretti di service e servicepath
- [x] Process Mermaid Chart
- [x] Architecture Mermaid Chart

### ROSE-AP
- [] Add information on machine activation status (e.g. records and calculate OEE only when it's active).
	- the oee is computed on demand so it's only computed if production is present
	- Qualche cazzo di qualcosa deve far scendere l'aviabiliti se non c'è produzione
- [ ] Add information about reworks (parts and time).
- [ ] Add information about total OEE stats for all the production.
- [] Extend to Factory level (e.g. un elemento nel contex broker che comunica lo scheduling dei turni di lavoro)
	- Si potrebbe fare per calcolare l'oee dei turni


## RAMP in remoto
- Connessione remota RAMP




