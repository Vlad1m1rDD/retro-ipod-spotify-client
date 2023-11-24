import os
import subprocess
from time import sleep
import bluetooth
import spotify_manager
import pexpect
import time

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


# def find_device_port(device_address):
#     # Perform service discovery
#     services = bluetooth.find_service(address=device_address)

#     # Check if any services were found
#     if services:
#         # Print information about each service
#         for service in services:
#             print("Service Name:", service["name"])
#             print("Host:", service["host"])
#             print("Port:", service["port"])

#         # Return the port of the first service (you may adjust this based on your specific use case)
#         return services[0]["port"]
#     else:
#         print("No services found for the device.")
#         return None


# def pair_and_connect(device_address):
#     port = 1
#     print("Trying to connect")
#     # Pairing
#     try:
#         # Try to initiate pairing
#         print(f"Attempting to pair with {device_address}")
#         print(f"Paired and trusted with {device_address}")

#         # Connecting
#         sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#         try:
#             sock.connect((device_address, port))
#             print(f"Connected to {device_address} on port {port}")

#             # Your communication logic goes here

#         except bluetooth.BluetoothError as e:
#             print(f"Error connecting to {device_address}: {str(e)}")

#         finally:
#             sock.close()

#     except bluetooth.btcommon.BluetoothError as e:
#         print(f"Failed to pair with {device_address}: {str(e)}")


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

    target_name = device_address  # Replace with the name of your target device
    scan_and_connect(target_name)

    print("Connected to: " + device["name"])
    return True


# def run_command(command, expected_prompt=None, timeout=30):
#     try:
#         process = pexpect.spawn(command, timeout=timeout)
#         if expected_prompt:
#             process.expect(expected_prompt)
#         output = process.before.decode()
#         process.close()
#         return output
#     except Exception as e:
#         print(f"Error running command: {e}")
#         return None


def scan_and_connect(target_device_name):
    nearby_devices = bluetooth.discover_devices(lookup_names=True)

    found_device = None
    for addr, name in nearby_devices:
        print(f"Found device: {name} ({addr})")
        if target_device_name in name:
            found_device = addr
            break

    if found_device:
        print(f"Device '{target_device_name}' found. Pairing and connecting...")
        port = find_device_port(found_device)
        if port:
            try:
                server_sock.connect((target_device_name, port))
            except bluetooth.BluetoothError as e:
                print(f"Error connecting to {target_device_name}: {str(e)}")

            finally:
                server_sock.close()

        else:
            print(f"Unable to find a suitable port for device '{target_device_name}'.")
    else:
        print(f"Device with name '{target_device_name}' not found.")


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
