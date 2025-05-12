import os
import glob
import json
import re

def get_steam_game_ids(steam_library_path):
    steam_game_ids = {}
    # Zoek alle manifest-bestanden
    appmanifest_files = glob.glob(os.path.join(steam_library_path, "steamapps", "appmanifest_*.acf"))

    for manifest_file in appmanifest_files:
        try:
            with open(manifest_file, 'r', encoding='utf-8') as file:
                content = file.read()
                # Pak AppID en naam uit het manifest
                app_id_match = re.search(r'"appid"\s+"(\d+)"', content)
                name_match = re.search(r'"name"\s+"(.+?)"', content)

                if app_id_match and name_match:
                    app_id = app_id_match.group(1)
                    game_name = name_match.group(1)
                    steam_game_ids[game_name] = app_id
        except Exception as e:
            print(f"Fout bij manifestbestand {manifest_file}: {e}")

    return steam_game_ids

def get_installed_games():
    steam_library_path = os.getenv("STEAM_PATH")
    installed_steam_games = get_steam_game_ids(steam_library_path)

    with open(os.path.join("apps", "steam_game_ids.json"), "w", encoding="utf-8") as f:
        json.dump(installed_steam_games, f, indent=2, ensure_ascii=False)

    print(f"{len(installed_steam_games)} Steam games opgeslagen in steam_game_ids.json")

if __name__ == "__main__":
    get_installed_games()
