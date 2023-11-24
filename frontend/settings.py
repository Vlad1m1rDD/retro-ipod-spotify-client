import os
import subprocess
from time import sleep
import bluetooth
import spotify_manager
import pexpect
import time

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def find_bluetooth_devices():
    devices_raw = bluetooth.discover_devices(lookup_names=True)
    scanned_devices = [{"addr": address, "name": name} for address, name in devices_raw]
    for device in scanned_devices:
        spotify_manager.DATASTORE.setBluetoothDevice(device)
    return scanned_devices


def connect_to_bt_device(device):
    # device_address = device["addr"]
    print(f"device: {device}")

    # pair_and_connect(device_address, 1)

    target_name = device["name"]  # Replace with the name of your target device
    target_address = find_device_address(target_name)

    if target_address:
        print(f"Device '{target_name}' found at address {target_address}.")
        pair_and_connect(target_address)
    else:
        print(f"Device with name '{target_name}' not found.")

    print("Connected to: " + device["name"])
    return True


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    return output.decode(), error.decode()


def find_device_address(target_device_name):
    # Start Bluetooth scanning
    run_command("sudo hcitool scan > /tmp/bt_scan_results &")

    # Wait for the scan to complete
    time.sleep(10)

    # Read the scan results
    output, _ = run_command("cat /tmp/bt_scan_results")

    # Check if the desired device is in the scan results
    target_device_address = None
    for line in output.split("\n"):
        if target_device_name in line:
            target_device_address = line.split()[0]
            break

    # Clean up temporary files
    run_command("rm /tmp/bt_scan_results")

    return target_device_address


def pair_and_connect(device_address):
    try:
        # Pair with the device
        run_command(f"sudo hcitool cc {device_address}")

        # Connect to the device
        run_command(f"sudo hcitool auth {device_address}")

        print(f"Successfully paired and connected to device {device_address}")

        # Add your communication logic here

    except Exception as e:
        print(f"Error pairing/connecting to device {device_address}: {str(e)}")
