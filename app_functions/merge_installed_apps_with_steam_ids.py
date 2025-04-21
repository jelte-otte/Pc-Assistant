import json
import os

def merge_installed_apps_with_steam_ids():
    apps_path = os.path.join("apps", "installed_apps.json")
    steam_ids_path = os.path.join("apps", "steam_game_ids.json")

    # Check of beide bestanden bestaan
    if not os.path.exists(apps_path) or not os.path.exists(steam_ids_path):
        print("Vereiste bestanden niet gevonden.")
        return

    # Laad beide bestanden
    with open(apps_path, "r", encoding="utf-8") as f:
        installed_apps = json.load(f)

    with open(steam_ids_path, "r", encoding="utf-8") as f:
        steam_games = json.load(f)

    # Maak nieuwe dict aan met vervangen links
    updated_apps = {}
    for app_name, location in installed_apps.items():
        if app_name in steam_games:
            steam_id = steam_games[app_name]
            updated_apps[app_name] = f"S:{steam_id}"
        else:
            updated_apps[app_name] = location  # Laat origineel pad staan

    # Opslaan
    with open(apps_path, "w", encoding="utf-8") as f:
        json.dump(updated_apps, f, indent=2, ensure_ascii=False)

    print("installed_apps.json bijgewerkt met Steam App IDs waar van toepassing.")

if __name__ == "__main__":
    merge_installed_apps_with_steam_ids()
