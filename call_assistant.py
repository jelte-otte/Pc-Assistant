from app_functions.get_apps import get_installed_apps
from app_functions.get_games import get_installed_games
from app_functions.open_app import open_requested_app
from app_functions.merge_installed_apps_with_steam_ids import merge_installed_apps_with_steam_ids
from messaging_functions.mail.send_email import send_email
from messaging_functions.get_phone_number import get_contact_phone_number
from messaging_functions.whatsapp.send_whatsapp_message import send_whatsapp_message
from spotify_functions.spotify_controller import main as spotify_main
import sys

get_installed_apps()
try:
    get_installed_games()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")
try:
    merge_installed_apps_with_steam_ids()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")

def open_app():
    open_requested_app()
    print("VERWERKT: App geopend")
    sys.stdout.flush()

def send_whatsapp(contact_name, message):
    phone_number = get_contact_phone_number(contact_name)
    if not phone_number:
        print("No matching contact found.")
    else:
        send_whatsapp_message(phone_number, message)
        print(f"VERWERKT: WhatsApp bericht gestuurd naar {contact_name}")
    sys.stdout.flush()

def send_email_func():
    send_email()
    print("VERWERKT: Email verzonden")
    sys.stdout.flush()

def spotify_func():
    spotify_main()
    print("VERWERKT: Spotify gestart")
    sys.stdout.flush()

while True:
    line = sys.stdin.readline()
    if not line:
        break
    line = line.strip()

    # Speciale test string "hallo"
    if line == "hallo":
        print(f"VERWERKT: {line[::-1]}")
        sys.stdout.flush()
        continue

    # Splits input in command en optionele parameters
    parts = line.split(';')
    command = parts[0].lower()

    if command == "open":
        open_app()

    elif command == "send whatsapp message":
        # Verwacht: send whatsapp message;contact_name;message
        if len(parts) < 3:
            print("Fout: 'send whatsapp message' vereist contactnaam en bericht.")
            sys.stdout.flush()
            continue
        contact_name = parts[1]
        message = parts[2]
        send_whatsapp(contact_name, message)

    elif command == "send email":
        send_email_func()

    elif command == "spotify":
        spotify_func()

    else:
        print(f"Onbekend commando: {line}")
        sys.stdout.flush()
