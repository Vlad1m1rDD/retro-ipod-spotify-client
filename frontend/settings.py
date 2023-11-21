import bluetooth


def findBluetoothDevices():
    return list(
        bluetooth.discover_devices(lookup_names=True),
    )


def findAvailablePorts():
    return list(bluetooth.get_available_port(bluetooth.RFCOMM))


def connectToBtDevice(device, port):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((device["addr"], port))
    print("Connected to: " + device["name"])
    sock.close()
    return True
