from app_functions import merge_installed_apps_with_steam_ids
from app_functions import open_app
from app_functions.get_apps import get_installed_apps
from app_functions.get_games import get_installed_games
from app_functions.open_app import open_requested_app
from messaging_functions.whatsapp.send_whatsapp_message import send_whatsapp_message
from messaging_functions.import_contacts import convert_vcf_to_json
from messaging_functions.mail.send_email import send_email
from messaging_functions.get_phone_number import get_contact_phone_number
from messaging_functions.whatsapp.send_whatsapp_message import send_whatsapp_message
from messaging_functions.import_contacts import convert_vcf_to_json

from messaging_functions.whatsapp.send_whatsapp_message import send_whatsapp_message
from messaging_functions.import_contacts import convert_vcf_to_json


get_installed_apps()
convert_vcf_to_json()
try:
    get_installed_games()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")
try:
    merge_installed_apps_with_steam_ids()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")

def open_app_input(keyword):
    if keyword == "open":
        open_app()

def send_whatsapp_message_input(keyword):
    if keyword == "send whatsapp message":
        try:
            contact_name = input("Enter the contact name: ").strip()
            phone_number = get_contact_phone_number(contact_name)

            if not phone_number:
                print("No matching contact found.")
                return
            else:
                message = input("What message do you want to send? ").strip()
                send_whatsapp_message(phone_number, message)
        except Exception as e:
            print(f"An error occurred while sending a whatsapp message: {e}")
def send_email_input(keyword):
    if keyword == "send email":
        print("important note: this functions does NOT work with basic authentication and a free microsoft account.")
        try:
            to_email = input("Enter the recipient's email address: ").strip()
            subject = input("Enter the email subject: ").strip()
            body = input("Enter the email body: ").strip()
            send_email(to_email, subject, body)
        except Exception as e:
            if "basic authentication is disabled" in str(e):
                print("Basic authentication is disabled. Please check your SMTP settings.")
            print(f"An error occurred while sending an email: {e}")

while True:
    text = input("Type 'open' to open an app: ").strip()

    if text == "open":
        open_app_input(text)
    elif text == "send whatsapp message":
        send_whatsapp_message_input(text)
    elif text == "send email":
        send_email_input(text);