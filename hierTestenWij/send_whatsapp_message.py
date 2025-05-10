import os
import json
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Configuratie ===
SESSION_DIR = os.path.abspath("selenium_whatsapp_session")
SESSION_FLAG = os.path.join(SESSION_DIR, "session_initialized.flag")
load_dotenv()
contacts_path = os.getenv("CONTACTS_FILE_PATH")

# === Hulpfuncties ===
def start_driver(headless: bool) -> webdriver.Chrome:
    options = Options()
    options.headless = headless
    options.add_argument(f"--user-data-dir={SESSION_DIR}")
    options.add_argument("--profile-directory=Default")
    return webdriver.Chrome(options=options)

def qr_code_present(driver: webdriver.Chrome) -> bool:
    try:
        driver.find_element(By.XPATH, '//canvas[@aria-label="Scan this QR code to link a device!"]')
        return True
    except NoSuchElementException:
        return False

def wait_until_qr_scanned(driver: webdriver.Chrome):
    print("Wachten tot QR-code gescand is...")
    while qr_code_present(driver):
        time.sleep(2)
    print("QR-code succesvol gescand.")
    with open(SESSION_FLAG, "w") as f:
        f.write("initialized")
    time.sleep(5)

# === Contactgegevens laden ===
if not contacts_path or not os.path.exists(contacts_path):
    print("Fout: contacts.json-pad niet gevonden in .env.")
    exit(1)

with open(contacts_path, "r", encoding="utf-8") as f:
    contacts = json.load(f)

target_name = input("Voer de naam van de contactpersoon in: ").strip()
contact = next((c for c in contacts if c["name"].lower() == target_name.lower()), None)

if not contact:
    print(f"Contact met naam '{target_name}' niet gevonden.")
    exit(1)

phone_number = contact["phone"]
message = f"Hallo {contact['name']}, dit is een automatisch bericht."

# === WhatsApp Web Sessiebeheer ===
first_time = not os.path.exists(SESSION_FLAG)
driver = None

if first_time:
    driver = start_driver(headless=False)
    driver.get("https://web.whatsapp.com")
    time.sleep(5)
    wait_until_qr_scanned(driver)
    driver.quit()
    driver = start_driver(headless=True)
else:
    driver = start_driver(headless=True)
    driver.get("https://web.whatsapp.com")
    time.sleep(10)
    if qr_code_present(driver):
        print("Sessie verlopen. QR vereist. Herstart in GUI-modus.")
        driver.quit()
        if os.path.exists(SESSION_FLAG):
            os.remove(SESSION_FLAG)
        driver = start_driver(headless=False)
        driver.get("https://web.whatsapp.com")
        time.sleep(5)
        wait_until_qr_scanned(driver)
        driver.quit()
        driver = start_driver(headless=True)

# === Bericht versturen ===
chat_url = f"https://web.whatsapp.com/send?phone={phone_number.replace('+', '')}"
driver.get(chat_url)

try:
    message_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]'))
    )
    message_box.click()
    time.sleep(0.3)
    message_box.send_keys(message)
    time.sleep(0.5)

    # Wacht op de knop en klik via JS
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send"]'))
    )
    driver.execute_script("arguments[0].click();", send_button)

    print(f"Bericht verzonden naar {contact['name']}.")
    time.sleep(5)
except Exception as e:
    print(f"Fout bij invoeren of verzenden: {e}")