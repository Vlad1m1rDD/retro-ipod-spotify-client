import bluetooth
import spotify_manager

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def find_device_port(device_address):
    # Perform service discovery
    services = bluetooth.find_service(address=device_address)

    # Check if any services were found
    if services:
        # Print information about each service
        for service in services:
            print("Service Name:", service["name"])
            print("Host:", service["host"])
            print("Port:", service["port"])

        # Return the port of the first service (you may adjust this based on your specific use case)
        return services[0]["port"]
    else:
        print("No services found for the device.")
        return None


def find_bluetooth_devices():
    devices_raw = bluetooth.discover_devices(lookup_names=True)
    scanned_devices = [
        spotify_manager.UserBluetoothDevice({"addr": address, "name": name})
        for address, name in devices_raw
    ]
    for device in scanned_devices:
        spotify_manager.DATASTORE.setBluetoothDevice(device)
    return scanned_devices


def connect_to_bt_device(device):
    port = find_device_port(device["addr"])
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    sock.connect((device["addr"], port))
    print("Connected to: " + device["name"])
    sock.close()
    return True
