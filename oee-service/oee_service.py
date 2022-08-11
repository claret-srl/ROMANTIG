from crate import client
from datetime import datetime,timedelta
import configparser
import time


config = configparser.ConfigParser()
config.read('oee_conf.config')
upTimeStates = config['PROCESS']['upTimeStates']
downTimeStates = config['PROCESS']['downTimeStates']
endStates = config['PROCESS']['endStates']

goodEnd = config['PROCESS']['goodEnd']
badEnd = config['PROCESS']['badEnd']
idealTime = float(config['OEE']['idealTime_ppm'])/60
timestep = int(config['OEE']['timestep'])

print('timestep is {} seconds'.format(timestep))

print("preparing connection")
connection_device = client.connect("crate-db:4200/")
cursor_oee = connection_device.cursor()
print("connection succesful")
cursor_oee.execute("create table if not exists mtopcua_car.oee (start_date timestamp primary key, end_date timestamp, num_prod int, num_good int, num_bad int, up_time float, down_time float, availability float, performance float, quality float, oee float);")
# cursor_oee.arraysize = 20
# get all records
start_time = datetime.now()

dt_obj = datetime.now()
end_block_time= datetime.now()

while True:
    now_time = datetime.now()
    if (now_time-end_block_time).seconds > timestep:
        # time.sleep(1)
        query = "SELECT time_index, processstatus FROM mtopcua_car.etdevice WHERE time_index BETWEEN {} and {} ORDER BY time_index ASC LIMIT 100;".format(end_block_time.timestamp(),datetime.now().timestamp())
        query2 = "SELECT time_index, processstatus FROM mtopcua_car.etdevice"
        records = []
        ## first query is truncated for some reason ##
        cursor_oee.execute(query2)
        records2 = cursor_oee.fetchone()
        # print(records2, len(records2))
        
        cursor_oee.execute(query)
        # get all records
        records = cursor_oee.fetchall()
        # print(records, len(records))
        
        process_list=[]
        total_upTime,total_downTime,total_produce,total_good,total_bad = 0,0,0,0,0
        for i,row in enumerate(records):
            dt_obj = datetime.fromtimestamp(row[0]/1000)
            processStatus = row[-1]
            if i>0:
                start_time = old_dt_obj
                end_time = dt_obj
                process_length = (end_time-start_time).total_seconds()
                down_up_time = "downTime" if old_status in downTimeStates else "upTime"
                up_time = process_length if down_up_time == "upTime" else 0
                down_time = process_length if down_up_time == "downTime" else 0

                total_upTime += up_time
                total_downTime += down_time

                total_produce += 1 if old_status in endStates else 0
                total_good +=1 if old_status in goodEnd else 0
                total_bad +=1 if old_status in badEnd else 0
                
            else:
                begin_block_time = dt_obj
            old_dt_obj = dt_obj
            old_status = processStatus

        start_time=datetime.now()
        # time.sleep(1)
        end_block_time = end_time+timedelta(seconds=1)

        availability = total_upTime/(total_upTime+total_downTime)
        performance = total_produce/(total_upTime * idealTime)
        try:
            quality = total_good/total_produce
        except:
            print('no products in this period')
            quality = 1

        oee = availability*performance*quality
        save_data = (begin_block_time.timestamp(),end_block_time.timestamp(),total_produce,total_good,total_bad,total_upTime,total_downTime,availability,performance,quality,oee)

        cursor_oee.execute("""INSERT INTO mtopcua_car.oee (start_date, end_date, num_prod,num_good,num_bad, up_time, down_time, availability, performance, quality, oee) VALUES (?, ?, ?, ?,?,?,?,?,?,?,?)""",
                            save_data)

        # print("start block: {}, end block: {}, total upTime: {}, total downTime: {}, total produce: {}".format(begin_block_time,end_block_time,total_upTime,total_downTime,total_produce))
        
        print("5-min Availability is {:.2f}%".format(availability*100))
        print("5-min Performance is {:.2f}%".format(performance*100))
        print("5-min Quality is {:.2f}%".format(quality*100)) 
        print("5-min OEE is {:.2f}%".format(oee*100)) 

        