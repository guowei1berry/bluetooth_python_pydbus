import pydbus
import time
import requests

bus = pydbus.SystemBus()

# print("bus",bus)

adapter = bus.get('org.bluez', '/org/bluez/hci0')
# print("adapter",adapter)
# print("diradapter",dir(adapter))

# print("address",adapter.Address) #hci0	84:C5:A6:D4:0C:C3
# print("Name",adapter.Name)
mngr = bus.get('org.bluez', '/')
print("mngr",dir(mngr))


def list_connected_devices():
    mngd_objs = mngr.GetManagedObjects()

    # for item in mngd_objs.items():
    #     print("item",item)
    for key, value in mngd_objs.items():
        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_3C'):
            # print(">>>>>>>",key, '->', value)
            first = value
        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_3D'):
            # print(">>>>>>>",key, '->', value)
            second = value
        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_01'):
            # print(">>>>>>>",key, '->', value)
            third = value
        if (key =='/org/bluez/hci0/dev_AC_23_3F_71_05_00'):
            # print(">>>>>>>",key, '->', value)
            fourth = value

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

    # print("values",first,second,third,fourth)
    r = requests.post('http://localhost:8000/post', json={"first": first})
    print("status",r.status_code)
    print("ok", r.ok)
    print("text", r.text)
    print("resp",r)

    thisdict = {
                "msg" : "advData",
                "gmac" : "1c:69:7a:62:cd:e4",#"YOUR_GATEWAY_MAC_HERE",
                "readings" : [
                             {
                                "dmac" : "AC_23_3F_71_05_3C",
                                "type" : 4,
                                "rssi" : -42,
                                "refpower" : 197,
                                "time" : "2022-10-25 04:15:00"
                            },
                            {
                                "dmac" : "AC_23_3F_71_05_3D",
                                "type" : 4,
                                "rssi" : -42,
                                "refpower" : 197,
                                "time" : "2022-10-25 04:15:00"
                            },
                            {
                                "dmac" : "AC_23_3F_71_05_01",
                                "type" : 4,
                                "rssi" : -42,
                                "refpower" : 197,
                                "time" : "2022-10-25 04:15:00"
                            },
                            {
                                "dmac" : "AC_23_3F_71_05_00",
                                "type" : 4,
                                "rssi" : -42,
                                "refpower" : 197,
                                "time" : "2022-10-25 04:15:00"
                            }
                            ]
                }   

if __name__ == '__main__':

    for x in range(1): 
        list_connected_devices()
        
        #time.sleep(3)

# sudo bluetoothctl
# agent on
# default-agent
# scan on