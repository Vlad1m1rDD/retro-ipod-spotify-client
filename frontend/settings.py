import subprocess
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


def pair_and_connect(device_address, port):
    print("Trying to connect")
    try:
        # Launch bluetoothctl as a subprocess
        bluetoothctl_process = subprocess.Popen(
            ["bluetoothctl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )

        # Send commands to bluetoothctl
        commands = [
            "pairable on\n",
            f"pair {device_address}\n",
            f"trust {device_address}\n",
            f"connect {device_address}\n",
            "exit\n",
        ]

        for command in commands:
            bluetoothctl_process.stdin.write(command)
            bluetoothctl_process.stdin.flush()

        # Close the process and wait for it to finish
        bluetoothctl_process.communicate()

    except Exception as e:
        print(f"Failed to pair with {device_address}: {str(e)}")


def find_bluetooth_devices():
    devices_raw = bluetooth.discover_devices(lookup_names=True)
    scanned_devices = [{"addr": address, "name": name} for address, name in devices_raw]
    for device in scanned_devices:
        spotify_manager.DATASTORE.setBluetoothDevice(device)
    return scanned_devices


def connect_to_bt_device(device):
    device_address = device["addr"]
    print(f"device: {device}")
    # port = find_device_port(device_address)
    # if port is not None:
    pair_and_connect(device_address, 1)
    # else:
    #     print(f"Unable to determine the port for the device {device_address}")

    print("Connected to: " + device["name"])
    return True
