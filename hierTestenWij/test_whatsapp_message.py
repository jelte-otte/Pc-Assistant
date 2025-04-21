import os
import subprocess
from hierTestenWij.connect_to_phone import connect_adb_wirelessly
from hierTestenWij.connect_to_phone import connect_adb_via_usb

def send_whatsapp_message(phone_number, message, device_id=None, connectivity_method="usb"):

    if connectivity_method == "wireless":
        connect_adb_wirelessly(os.getenv('PHONE_IP'))
    elif connectivity_method == "usb":
        device_id = connect_adb_via_usb(os.getenv('DEVICE_ID'))
    
    message_encoded = message.replace(" ", "%20")
    wa_url = f"https://wa.me/{phone_number}?text={message_encoded}"

    cmd = [
        "adb"
    ]
    if device_id:
        cmd += ["-s", device_id]

    cmd += [
        "shell", "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", wa_url
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Chat geopend voor {phone_number}")
    except subprocess.CalledProcessError as e:
        print("Fout bij openen van WhatsApp:", e)
