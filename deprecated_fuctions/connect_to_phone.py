import subprocess
from dotenv import load_dotenv

load_dotenv()

def connect_adb_wirelessly(ip, maxAttempts=3):
    attempts = 0
    subprocess.run(["adb", "disconnect"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Disconnected all devices.")
    
    while attempts < maxAttempts:
        result = subprocess.run(["adb", "connect", ip], capture_output=True, text=True)
        if "connected" in result.stdout.lower():
            print(result.stdout.strip())
            print("Connected to phone via wireless ADB.")
            return ip  # Geef IP terug als device-id
        else:
            print(result.stdout.strip())
            print(f"Attempt {attempts + 1} failed. Retrying...")
            attempts += 1

def connect_adb_via_usb(device_id=None):
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")[1:]  # skip header

    # Verzamel alle USB-device ID's
    connected_devices = [
        line.split()[0]
        for line in lines
        if "device" in line and not line.startswith("List") and ":" not in line  # filter wireless devices
    ]

    if not connected_devices:
        print("No ADB device found over USB.")
        return None

    if device_id and device_id in connected_devices:
        print(f"Connected to phone via USB ADB ({device_id})")
        return device_id

    # Geen specifiek device gevraagd of opgegeven ID niet gevonden
    selected = connected_devices[0]
    print(f"Connected to phone via USB ADB ({selected})")
    return selected
