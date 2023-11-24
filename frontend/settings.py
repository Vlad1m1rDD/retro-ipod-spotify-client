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
    device_address = device["addr"]
    print(f"device: {device}")

    pair_and_connect(device_address, 1)

    print("Connected to: " + device["name"])
    return True


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    return output.decode(), error.decode()


def pair_and_connect(device_address):
    try:
        # Pair with the device
        run_command(f"sudo bluetoothctl pair {device_address}")

        # Trust with the device
        run_command(f"sudo bluetoothctl trust {device_address}")

        # Connect to the device
        run_command(f"sudo bluetoothctl connect {device_address}")

        print(f"Successfully paired and connected to device {device_address}")

        # Add your communication logic here

    except Exception as e:
        print(f"Error pairing/connecting to device {device_address}: {str(e)}")
