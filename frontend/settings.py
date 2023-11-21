import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def findBluetoothDevices():
    devices = (bluetooth.discover_devices(lookup_names=True),)
    # print(devices)
    listDevices = []
    index = 0
    for device in devices:
        listDevices[index] = {"addr": device[0], "name": device[1]}
        index = index + 1
    print(listDevices)
    return listDevices


def findAvailablePort():
    return bluetooth.get_available_port(bluetooth.RFCOMM)


def connectToBtDevice(device, port):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((device["addr"], port))
    print("Connected to: " + device["name"])
    sock.close()
    return True
