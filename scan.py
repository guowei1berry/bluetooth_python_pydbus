import pydbus

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
        # print("item",item)
    for key, value in mngd_objs.items():
        if (key =='/org/bluez/hci0/dev_DD_33_04_13_2F_AC'):
            print("Here",key, '->', value)
    
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

if __name__ == '__main__':
    list_connected_devices()


# sudo bluetoothctl
# agent on
# default-agent
# scan on