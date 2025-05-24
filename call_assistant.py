from app_functions.get_apps import get_installed_apps
from app_functions.get_games import get_installed_games
from app_functions.merge_installed_apps_with_steam_ids import merge_installed_apps_with_steam_ids
from messaging_functions.mail.send_email import send_email
from messaging_functions.get_phone_number import get_contact_phone_number
from messaging_functions.whatsapp.send_whatsapp_message import send_whatsapp_message
from spotify_functions.spotify_controller import main as spotify_main
import sys
from app_functions.open_app import load_apps
from app_functions.open_app import find_best_match
import subprocess
import os
from app_functions.open_app import open_app

current_action = None
current_app_match = None
context_data = {}
contact_name = None

get_installed_apps()
try:
    get_installed_games()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")
try:
    merge_installed_apps_with_steam_ids()
except Exception as e:
    print(f"Er is een fout opgetreden bij het ophalen van geïnstalleerde games: {e}")

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

    if current_action == "message":
        message = line
        send_whatsapp(contact_name, message)
        current_action = None
        contact_name = None
        continue

    if current_action == "contact_name":
        contact_name = line
        current_action = "message"
        print("Welke bericht?")
        sys.stdout.flush()
        continue
        


    if current_action == "prism":
        version = line
        command = [
            current_app_match, 
            "-l", version,
        ]
        subprocess.run(command)
        current_app_match = None
        current_action = None
        continue

    if current_action == "open_app":
        app_name = line
        apps = load_apps()
        if not apps:
            continue
        best_match = find_best_match(apps, app_name)
        if best_match:
            if apps[best_match].startswith("S:"):
                steamLink = os.getenv("STEAM_PATH") + "//Steam.exe"
                steam_id = apps[best_match].replace("S:", "")
                command_str = f'"{steamLink}" -applaunch {steam_id}'
                print(command_str)
                subprocess.run(command_str, shell=True)
                sys.stdout.flush()
                current_action = None
                continue
            if best_match == "Prism Launcher":
                current_action = "prism"
                current_app_match = apps[best_match]
                print("Welke versie?")
                sys.stdout.flush()
                continue
            print(f"Beste overeenkomst: {best_match}")
            success = open_app(apps[best_match])
            if not success:
                print("Kon geen uitvoerbaar bestand of snelkoppeling openen.")
        else:
            print("Geen overeenkomst gevonden.")
        print("VERWERKT: App geopend.")
        sys.stdout.flush()
        current_action = None
        continue

    # Speciale test string "hallo"
    if line == "hallo":
        print(f"VERWERKT: {line[::-1]}")
        sys.stdout.flush()
        continue

    # Splits input in command en optionele parameters
    parts = line.split(';')
    command = parts[0].lower()

    if command == "open":
        print("Welke app wil je openen?")
        sys.stdout.flush()
        current_action = "open_app"
        continue

    elif command == "send whatsapp message":
        current_action = "contact_name"
        print("Welke contactnaam?")
        sys.stdout.flush()
        continue

    elif command == "send email":
        send_email_func()

    elif command == "spotify":
        spotify_func()

    else:
        print(f"Onbekend commando: {line}")
        sys.stdout.flush()
