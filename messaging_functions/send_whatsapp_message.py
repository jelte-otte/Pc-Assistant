import os
import subprocess
import time
from messaging_functions.connect_to_phone import connect_adb_wirelessly
from messaging_functions.connect_to_phone import connect_adb_via_usb
from messaging_functions.unlock_phone import unlock_device


def send_whatsapp_message(phone_number, message, device_id=None, connectivity_method=os.getenv('CONNECTIVITY_METHOD')):

    if connectivity_method == "wireless":
        connect_adb_wirelessly(os.getenv('PHONE_IP'))
    elif connectivity_method == "usb":
        device_id = connect_adb_via_usb(os.getenv('DEVICE_ID'))
    
    # Controleer of scherm vergrendeld is
    check_cmd = ["adb"]
    if device_id:
        check_cmd += ["-s", device_id]
    check_cmd += ["shell", "dumpsys", "window"]

    try:
        output = subprocess.check_output(check_cmd, encoding='utf-8')
        if "mDreamingLockscreen=true" in output:
            unlock_device(device_id)
    except subprocess.CalledProcessError as e:
        print("Fout bij controleren vergrendeling:", e)
        return

    # Open WhatsApp met bericht
    message_encoded = message.replace(" ", "%20")
    wa_url = f"https://wa.me/{phone_number}?text={message_encoded}"

    start_cmd = ["adb"]
    if device_id:
        start_cmd += ["-s", device_id]
    start_cmd += [
        "shell", "am", "start",
        "-a", "android.intent.action.VIEW",
        "-d", wa_url
    ]

    try:
        subprocess.run(start_cmd, check=True)
        print(f"Chat geopend voor {phone_number}")
    except subprocess.CalledProcessError as e:
        print("Fout bij openen van WhatsApp:", e)
        return

    time.sleep(2.3)

    # Simuleer Enter
    send_cmd = ["adb"]
    if device_id:
        send_cmd += ["-s", device_id]
    send_cmd += ["shell", "input", "keyevent", "66"]

    try:
        subprocess.run(send_cmd, check=True)
        print("Bericht verzonden.")
        power_off_cmd = ["adb"]
        if device_id:
            power_off_cmd += ["-s", device_id]
        power_off_cmd += ["shell", "input", "keyevent", "223"]

        try:
            subprocess.run(power_off_cmd, check=True)
            print("Scherm uitgeschakeld.")
        except subprocess.CalledProcessError as e:
            print("Fout bij uitschakelen van scherm:", e)
    except subprocess.CalledProcessError as e:
        print("Fout bij verzenden van bericht:", e)
