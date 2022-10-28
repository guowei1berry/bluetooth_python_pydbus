import pydbus
import time
import requests
from measureDist import calculateRefpower 
from datetime import datetime,timezone
import json
import random
from paho.mqtt import client as mqtt_client
now_utc = datetime.now(timezone.utc)
print(now_utc)

bus = pydbus.SystemBus()

# print("bus",bus)

adapter = bus.get('org.bluez', '/org/bluez/hci0')
# print("adapter",adapter)
# print("diradapter",dir(adapter))

# print("address",adapter.Address) #hci0	84:C5:A6:D4:0C:C3
mngr = bus.get('org.bluez', '/')
print("mngr",dir(mngr))


def retrieveData(val):
    device = val["org.bluez.Device1"]
    rssi = val["org.bluez.Device1"]["RSSI"]
    manufacturerData = val["org.bluez.Device1"]["ManufacturerData"][76]
    refPower = manufacturerData[len(manufacturerData)-1 ]
    return {"RSSI":rssi , "refPower":refPower }


def list_connected_devices():
    mngd_objs = mngr.GetManagedObjects()

    # for item in mngd_objs.items():
    #     print("item",item)
    for key, value in mngd_objs.items():
        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_3C'):
            # # print(">>>>>>>",key, '->', value)
            firstDevice = value["org.bluez.Device1"]
            data =retrieveData(value)
            first_rssi = data["RSSI"]
            first_refPower = data["refPower"]
            first_calculate = calculateRefpower(first_rssi,first_refPower)
            # print("firstDevice",firstDevice)
            # print("firstrssi",first_rssi)
            # print("first_refPower",first_refPower)
            # print("first_calculate",first_calculate)
            
        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_3D'):
            # print(">>>>>>>",key, '->', value)
            secondDevice = value["org.bluez.Device1"]
            data =retrieveData(value)
            second_rssi = data["RSSI"]
            second_refPower = data["refPower"]
            second_calculate = calculateRefpower(second_rssi,second_refPower)
            # print("secondDevice",secondDevice)
            # print("second_rssi",second_rssi)
            # print("second_refPower",second_refPower)
            # print("second_calculate",second_calculate)


        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_01'):
            # print(">>>>>>>",key, '->', value)
            thirdDevice = value["org.bluez.Device1"]
            data =retrieveData(value)
            third_rssi = data["RSSI"]
            third_refPower = data["refPower"]
            third_calculate = calculateRefpower(third_rssi,third_refPower)
            # print("thirdDevice",thirdDevice)
            # print("third_rssi",third_rssi)
            # print("third_refPower",third_refPower)
            # print("third_calculate",third_calculate)

        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_00'):
            # print(">>>>>>>",key, '->', value)
            forthDevice = value["org.bluez.Device1"]
            data =retrieveData(value)
            forth_rssi = data["RSSI"]
            forth_refPower = data["refPower"]
            forth_calculate = calculateRefpower(forth_rssi,forth_refPower)
            # print("forthDevice",forthDevice)
            # print("forth_rssi",forth_rssi)
            # print("forth_refPower",forth_refPower)
            # print("forth_calculate",forth_calculate)

    # keys = list(mngd_objs)
    # print("mngd_objs",mngd_objs)
    # print("mngd_objs[1]",keys[1000])
    # print("mngd_objs",mngd_objs[1])

    for path in mngd_objs:
        con_state = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected', False)
        # print("con_state",con_state)
        if con_state:
            # print("con_state",con_state)
            addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
            name = mngd_objs[path].get('org.bluez.Device1', {}).get('Name')
            print(f'Device {name} [{addr}] is connected')


    thisdict = {
                # "step": step,
                "msg" : "advData",
                "gmac" : "1c:69:7a:62:cd:e4",#"YOUR_GATEWAY_MAC_HERE",
                "readings" : [
                             {
                                "dmac" : "AC_23_3F_71_05_3C",
                                "type" : 4,
                                "rssi" : first_rssi,
                                "refpower" : first_refPower,
                                "time" : now_utc
                            },
                            {
                                "dmac" : "AC_23_3F_71_05_3D",
                                "type" : 4,
                                "rssi" : second_rssi,
                                "refpower" : second_refPower,
                                "time" : now_utc
                            },
                            {
                                "dmac" : "AC_23_3F_71_05_01",
                                "type" : 4,
                                "rssi" : third_rssi,
                                "refpower" : third_refPower,
                                "time" : now_utc
                            },
                            {
                                "dmac" : "AC_23_3F_71_05_00",
                                "type" : 4,
                                "rssi" : forth_rssi,
                                "refpower" : forth_refPower,
                                "time" : now_utc
                            }
                            ]
                }  
    # # print("values",first,second,third,fourth)
    print("thisdict",json.dumps(thisdict, indent=4, sort_keys=True, default=str))
    return thisdict
    # r = requests.post('http://localhost:8000/post', json={"thisdict": json.dumps(thisdict, indent=4, sort_keys=True, default=str)})
    # r = requests.post('http://jarvis-mqtt.viatick.com/jarvis/ble/du.guowei17/reading', json={"thisdict": json.dumps(thisdict, indent=4, sort_keys=True, default=str)})
    # print("status",r.status_code)
    # print("ok", r.ok)
    # print("text", r.text)
    # print("resp",r) 
#################################### MQTT CONNECT ############################################
broker = 'jarvis-mqtt.viatick.com'
port = 1883
topic = "jarvis/ble/du.guowei17/reading"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        data_Call = list_connected_devices() 
        msg = f"messages: {msg_count}"
        print("data_Call",data_Call)
        result = client.publish(topic, str(data_Call))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':

    # for x in range(1):
    try:
        run()
        # step = 0
        # while True:
        #     step += 1
        #     list_connected_devices()  
        #     time.sleep(0.5)
    except KeyboardInterrupt:
        pass 

        


# sudo bluetoothctl ##need to run this before scanning
# agent on
# default-agent
# scan on