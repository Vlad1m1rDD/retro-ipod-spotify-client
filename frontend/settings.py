import os
import subprocess
from time import sleep
import bluetooth
import spotify_manager
import pexpect
import time

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


def pair_and_connect(device_address):
    port = 1
    print("Trying to connect")
    # Pairing
    try:
        # Try to initiate pairing
        print(f"Attempting to pair with {device_address}")
        print(f"Paired and trusted with {device_address}")

        # Connecting
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            sock.connect((device_address, port))
            print(f"Connected to {device_address} on port {port}")

            # Your communication logic goes here

        except bluetooth.BluetoothError as e:
            print(f"Error connecting to {device_address}: {str(e)}")

        finally:
            sock.close()

    except bluetooth.btcommon.BluetoothError as e:
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

    # pair_and_connect(device_address, 1)

    if __name__ == "__main__":
        target_name = device_address  # Replace with the name of your target device
        scan_and_connect(target_name)

    print("Connected to: " + device["name"])
    return True


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    return output.decode(), error.decode()


def scan_and_connect(target_device_name):
    # Start bluetoothctl
    run_command("bluetoothctl")

    # Send commands to bluetoothctl
    run_command("scan on")

    found_device = None

    # Scan for devices
    while True:
        output, _ = run_command("devices")
        devices = output.strip().split("\n")

        for device in devices:
            print(f"found device", device)
            if target_device_name in device:
                found_device = device.split()[1]
                break

        if found_device:
            break

        # Sleep for a while before checking again
        time.sleep(5)

    # Stop scanning
    run_command("scan off")

    # Pair and connect
    if found_device:
        run_command(f"pair {found_device}")
        run_command(f"trust {found_device}")
        run_command(f"connect {found_device}")
        run_command("exit")
    else:
        print(f"Device with name '{target_device_name}' not found.")
