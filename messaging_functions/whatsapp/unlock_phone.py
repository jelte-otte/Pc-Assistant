import os
import subprocess
from dotenv import load_dotenv
import time

load_dotenv()
PIN = os.getenv("DEVICE_PIN")

def unlock_device(device_id=None):
    if not PIN:
        print("Geen pincode opgegeven in .env (DEVICE_PIN)")
        return

    cmd = ["adb"]
    if device_id:
        cmd += ["-s", device_id]

    try:
        # Scherm aan
        subprocess.run(cmd + ["shell", "input", "keyevent", "224"], check=True)
        time.sleep(1)

        # Swipe omhoog (voor ontgrendelscherm)
        subprocess.run(cmd + ["shell", "input", "swipe", "300", "1000", "300", "500"], check=True)
        time.sleep(1)

        # Pincode invoeren
        for digit in PIN:
            subprocess.run(cmd + ["shell", "input", "text", digit], check=True)
            time.sleep(0.1)

        # Bevestigen met Enter
        subprocess.run(cmd + ["shell", "input", "keyevent", "66"], check=True)
        print("Toestel ontgrendeld.")
    except subprocess.CalledProcessError as e:
        print("Fout bij ontgrendelen:", e)
