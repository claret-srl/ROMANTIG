from crate import client
from datetime import datetime
import configparser
import time
import pycurl

config = configparser.ConfigParser()
config.read("oee_conf.config")

# PROCESS
upTimeStates = config["PROCESS"]["upTimeStates"]
downTimeStates = config["PROCESS"]["downTimeStates"]
endStates = config["PROCESS"]["endStates"]
goodEnd = config["PROCESS"]["goodEnd"]
badEnd = config["PROCESS"]["badEnd"]

# OEE
idealTime = float(config["OEE"]["idealTime_ppm"]) / 60
timestep = int(config["OEE"]["timestep"])

# ####################################################
# #
# # TIME STEP OVERRIDE
# #
# timestep = 10

print("Timestep is {} seconds".format(timestep))

print("Connection to CrateDB in progress.")

# ####################################################
# #
# # HOST OVERRIDE
# #
# crateDBhost = "localhost"
crateDBhost = "crate-db"

connection_device = client.connect(crateDBhost + ":" + "4200", error_trace=True)
cursor = connection_device.cursor()
print("Connection to CrateDB succesful.")
cursor.execute(
    "create table if not exists mtopcua_car.oee (start_date timestamp primary key, end_date timestamp, num_prod int, num_good int, num_bad int, up_time float, down_time float, availability float, performance float, quality float, oee float);"
)

start_time = datetime.now()
dt_obj = datetime.now()
end_block_time = datetime.now()
end_time = datetime.now() # Aggiunto perchè viene dichiarato nel ciclo IF, e se non entra da errore.
begin_block_time = datetime.now() # Aggiunto perchè viene dichiarato nel ciclo IF, e se non entra da errore.

while True:
    print("Loop")
    now_time = datetime.now()
    if (now_time - end_block_time).seconds > timestep:

        query_wakeup = "SELECT time_index, processstatus FROM mtopcua_car.etdevice"
        cursor.execute(query_wakeup)
        
        query = "SELECT time_index, processstatus FROM mtopcua_car.etdevice WHERE time_index BETWEEN {} and {} ORDER BY time_index ASC LIMIT 100;".format(
            end_block_time.timestamp(),
            datetime.now().timestamp()
        )
        cursor.execute(query)
        

        records = []
        records = cursor.fetchall()

        process_list = []
        total_upTime, total_downTime, total_produce, total_good, total_bad = (
            0,
            0,
            0,
            0,
            0,
        )
        for i, row in enumerate(records):
            dt_obj = datetime.fromtimestamp(row[0] / 1000)
            processStatus = row[-1]
            if i > 0:
                start_time = old_dt_obj
                end_time = dt_obj
                process_length = (end_time - start_time).total_seconds()
                down_up_time = "downTime" if old_status in downTimeStates else "upTime"
                up_time = process_length if down_up_time == "upTime" else 0
                down_time = process_length if down_up_time == "downTime" else 0

                total_upTime += up_time
                total_downTime += down_time

                total_produce += 1 if old_status in endStates else 0
                total_good += 1 if old_status in goodEnd else 0
                total_bad += 1 if old_status in badEnd else 0

            else:
                begin_block_time = dt_obj
            old_dt_obj = dt_obj
            old_status = processStatus

        start_time = datetime.now()
        end_block_time = end_time

        try:
            availability = total_upTime / (total_upTime + total_downTime)
        except:
            print("No time not yet detected.")
            availability = 0

        try:
            performance = total_produce / (total_upTime * idealTime)
        except:
            print("No time not yet detected.")
            performance = 0
        
        try:
            quality = total_good / total_produce
        except:
            print("No products in this period")
            quality = 0

        oee = availability * performance * quality

        save_data = (
            begin_block_time.timestamp(),
            end_block_time.timestamp(),
            total_produce,
            total_good,
            total_bad,
            total_upTime,
            total_downTime,
            availability,
            performance,
            quality,
            oee,
        )

        cursor.execute("""INSERT INTO mtopcua_car.oee (start_date, end_date, num_prod,num_good,num_bad, up_time, down_time, availability, performance, quality, oee) VALUES (?, ?, ?, ?,?,?,?,?,?,?,?)""", save_data)

        # print("start block: {}, end block: {}, total upTime: {}, total downTime: {}, total produce: {}".format(begin_block_time,end_block_time,total_upTime,total_downTime,total_produce))

        print("5-min Availability is {:.2f}%".format(availability * 100))
        print("5-min Performance is {:.2f}%".format(performance * 100))
        print("5-min Quality is {:.2f}%".format(quality * 100))
        print("5-min OEE is {:.2f}%".format(oee * 100))
        
        jsonData = '{"actionType": "append","entities": [{"id": "urn:ngsiv2:I40Asset:PLC:001","type": "PLC","Availability": {"type": "Float","value":' + str(availability) + '},"Performance": {"type": "Float","value":' + str(performance) + '},"Quality": {"type": "Float","value":' + str(quality) + '},"OEE": {"type": "Float","value":' + str(oee) + '}}]}'

        # print(jsonData)

        crl = pycurl.Curl()
        # ####################################################
		# #
		# # LOCALHOST OVERRIDE
		# #
        # crl.setopt(crl.URL,"http://localhost:1026/v2/op/update")
        crl.setopt(crl.URL,"http://orion:1026/v2/op/update")
        crl.setopt(crl.CUSTOMREQUEST, "POST")
        crl.setopt(crl.HTTPHEADER, ['Content-Type: application/json'])
        crl.setopt(crl.POSTFIELDS, jsonData)
        crl.perform()
        crl.close()

    # time.sleep(timestep / 100)  # TO BE REMOVED
    time.sleep(1) # TO BE REMOVED