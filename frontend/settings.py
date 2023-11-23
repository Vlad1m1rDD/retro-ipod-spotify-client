import subprocess
import bluetooth
import spotify_manager

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def tupleToObject(t):
    return {"addr": t[0], "name": t[1]}


def findBluetoothDevices():
    devices_raw = bluetooth.discover_devices(lookup_names=True)
    print(f"{devices_raw}")
    scanned_devices = [{"addr": address, "name": name} for address, name in devices_raw]
    for device in scanned_devices:
        spotify_manager.DATASTORE.setBluetoothDevice(device)
    return scanned_devices


def findAvailablePort():
    return bluetooth.get_available_port(bluetooth.RFCOMM)


def connectToBtDevice(device, port):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    subprocess.run(["bluetoothctl", "pair", device["addr"]], text=True, check=True)
    subprocess.run(["bluetoothctl", "trust", device["addr"]], text=True, check=True)
    sock.connect((device["addr"], port))
    print("Connected to: " + device["name"])
    sock.close()
    return True
