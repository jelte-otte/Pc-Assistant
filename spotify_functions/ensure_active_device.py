import socket
import time
from fuzzywuzzy import fuzz
from spotify_functions import open_spotify_app

def ensure_active_device(sp):
    try:
        # Haal de naam van de huidige pc op
        pc_name = socket.gethostname().lower()
        print(f"PC name: {pc_name}")
        
        devices = sp.devices()
        if not devices or not devices.get('devices'):
            print("No devices found. Trying to open Spotify...")
            if not open_spotify_app():
                return None
            devices = sp.devices()
        
        pc_device = None
        for device in devices.get('devices', []):
            device_name = device['name'].lower()
            # Zoek naar een apparaat dat overeenkomt met de pc-naam
            if device_name == pc_name or fuzz.ratio(device_name, pc_name) >= 90:
                pc_device = device['id']
                break
        
        if not pc_device:
            print("No device matching PC name found. Trying to open Spotify and retry...")
            if not open_spotify_app():
                return None
            devices = sp.devices()
            for device in devices.get('devices', []):
                device_name = device['name'].lower()
                if device_name == pc_name or fuzz.ratio(device_name, pc_name) >= 90:
                    pc_device = device['id']
                    break
        
        if pc_device:
            print(f"Activating PC device: {pc_device}")
            sp.transfer_playback(device_id=pc_device, force_play=False)
            time.sleep(1)  # Geef tijd om te activeren
            return pc_device
        
        print("No devices available or PC device not found. Please ensure Spotify is open.")
        return None
    except Exception as e:
        print(f"Error while checking/activating device: {e}")
        return None