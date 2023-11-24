import subprocess
import bluetooth
import spotify_manager
import pexpect

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)


def run_cmd(command: str):
    """Execute shell commands and return STDOUT"""
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    return stdout.decode("utf-8")


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


def run_bluetoothctl_commands(commands):
    try:
        # Spawn bluetoothctl process
        bluetoothctl_process = pexpect.spawn("bluetoothctl")

        # Send commands
        for command in commands:
            bluetoothctl_process.sendline(command)

        # Wait for the process to finish
        bluetoothctl_process.expect(pexpect.EOF, timeout=10)

    except Exception as e:
        print(f"Error running bluetoothctl commands: {str(e)}")


def pair_and_connect(device_address, port):
    print("Trying to connect")
    # Pairing
    try:
        # Try to initiate pairing
        # print(f"Attempting to pair with {device_address}")
        print(run_cmd("bluetoothctl agent on"))
        print(run_cmd("bluetoothctl default-agent"))
        print(run_cmd("bluetoothctl pair {device_address}"))
        print(run_cmd("bluetoothctl connect {device_address}"))
        print(run_cmd("bluetoothctl info {device_address}"))
        # print(f"Paired and trusted with {device_address}")

        # Connecting
        # sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        # try:
        #     sock.connect((device_address, port))
        #     print(f"Connected to {device_address} on port {port}")

        #     # Your communication logic goes here

        # except bluetooth.BluetoothError as e:
        #     print(f"Error connecting to {device_address}: {str(e)}")

        # finally:
        #     sock.close()

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
    commands = [
        "power on",
        "pairable on",
        "discoverable on",
        "agent on",
        "scan on",
        f"pair {device_address}",  # Replace {device_address} with the actual address
        f"trust {device_address}",  # Replace {device_address} with the actual address
        f"connect {device_address}",  # Replace {device_address} with the actual address
    ]
    print(f"device: {device}")
    # port = find_device_port(device_address)
    # if port is not None:
    # pair_and_connect(device_address, 1)
    run_bluetoothctl_commands(commands)
    # else:
    #     print(f"Unable to determine the port for the device {device_address}")

    print("Connected to: " + device["name"])
    return True
