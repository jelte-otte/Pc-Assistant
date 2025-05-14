import time
from app_functions.open_app import find_best_match, load_apps, open_app


def open_spotify_app():
    try:
        apps = load_apps()
        if not apps:
            print("Geen apps geladen. Kan Spotify niet openen.")
            return False
        best_match = find_best_match(apps, "Spotify")
        if best_match:
            print("Opening Spotify...")
            success = open_app(apps[best_match])
            if success:
                time.sleep(5)  # Wacht even zodat Spotify kan opstarten
                return True
            else:
                print("Kon Spotify niet openen.")
                return False
        else:
            print("Spotify niet gevonden in de lijst van apps.")
            return False
    except Exception as e:
        print(f"Error while opening Spotify: {e}")
        return False
