import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def findBluetoothDevices():
    devices = (bluetooth.discover_devices(lookup_names=True),)
    return list({"addr": devices[0], "name": devices[1]})


def findAvailablePort():
    return bluetooth.get_available_port(bluetooth.RFCOMM)


def connectToBtDevice(device, port):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((device["addr"], port))
    print("Connected to: " + device["name"])
    sock.close()
    return True
