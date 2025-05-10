from app_functions.get_apps import get_installed_apps
from app_functions.get_games import get_installed_games
from app_functions.open_app import open_requested_app
from app_functions.merge_installed_apps_with_steam_ids import merge_installed_apps_with_steam_ids
from messaging_functions.get_contacts import get_contacts
from messaging_functions.mail.send_email import send_email
from messaging_functions.get_phone_number import get_contact_phone_number
from messaging_functions.whatsapp.send_whatsapp_message import send_whatsapp_message



get_installed_apps()
try:
    get_installed_games()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")
try:
    merge_installed_apps_with_steam_ids()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")
try:
    get_contacts()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")

def open_app(keyword):
    if keyword == "open":
        open_requested_app()

def send_message(keyword):
    if keyword == "send whatsapp message":
        contact_name = input("Enter the contact name: ").strip()
        phone_number = get_contact_phone_number(contact_name)

        if not phone_number:
            print("No matching contact found.")
            return
        else:
            message = input("What message do you want to send? ").strip()
            send_whatsapp_message(phone_number, message)

    elif keyword == "send email":
        send_email()

while True:
    text = input("Type 'open' to open an app: ").strip()

    if text == "open":
        open_app(text)
    elif text == "send whatsapp message":
        send_message(text)