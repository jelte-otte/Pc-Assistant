import os
import subprocess
import json
from fuzzywuzzy import fuzz
import win32com.client

def load_apps():
    path = os.path.join("apps", "installed_apps.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{path} niet gevonden. Start eerst get_apps.py.")
        return {}

def find_best_match(apps, user_input):
    best_match = None
    highest_score = 0
    for app_name in apps:
        score = fuzz.ratio(user_input.lower(), app_name.lower())
        if score > highest_score:
            highest_score = score
            best_match = app_name
            if score == 100:
                break
    return best_match if highest_score >= 80 else None

def open_app(path_or_cmd):
    if path_or_cmd.startswith("shell:AppsFolder"):
        subprocess.run(['explorer', path_or_cmd], shell=True)
        return True
    if path_or_cmd.lower().endswith('.lnk') and os.path.isfile(path_or_cmd):
        os.startfile(path_or_cmd)
        return True
    if os.path.isfile(path_or_cmd) and path_or_cmd.lower().endswith('.exe'):
        subprocess.Popen(path_or_cmd)
        return True
    if os.path.isdir(path_or_cmd):
        for file in os.listdir(path_or_cmd):
            if file.lower().endswith(".exe"):
                subprocess.Popen(os.path.join(path_or_cmd, file))
                return True
    return False

def resolve_lnk(lnk_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(lnk_path)
    return shortcut.Targetpath

def open_requested_app():
    apps = load_apps()
    if not apps:
        return

    user_input = input("Welke app wil je openen? ").strip().lower()
    best_match = find_best_match(apps, user_input)

    if best_match:
        if apps[best_match].startswith("S:"):
            steamLink = apps["Steam"]
            steam_id = apps[best_match].replace("S:", "")
            command = [
                "start", "",
               f"{steamLink}", 
                "-applaunch", steam_id,
            ]
            print(command)
            subprocess.run(command, shell=True)
            return
        if best_match == "Prism Launcher":
            version = input("welke versie?")
            command = [
                resolve_lnk(apps[best_match]), 
                "-l", version,
            ]
            subprocess.run(command)
        print(f"Beste overeenkomst: {best_match}")
        success = open_app(apps[best_match])
        if not success:
            print("Kon geen uitvoerbaar bestand of snelkoppeling openen.")
    else:
        print("Geen overeenkomst gevonden.")

if __name__ == "__main__":
    open_requested_app()
