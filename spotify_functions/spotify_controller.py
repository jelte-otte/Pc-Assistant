import os
import socket
import time
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fuzzywuzzy import fuzz
from app_functions.open_app import find_best_match, load_apps, open_app

# === Spotify authenticatie ===
load_dotenv()
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-modify-playback-state user-read-playback-state playlist-read-private"
))

# === Hulp: Apps openen ===
def open_spotify_app():
    apps = load_apps()
    if not apps:
        print("Geen apps geladen.")
        return False

    best_match = find_best_match(apps, "Spotify")
    if best_match:
        print(f"Openen van Spotify via: {best_match}")
        return open_app(apps[best_match])
    else:
        print("Spotify niet gevonden in app-lijst.")
        return False

# === Apparatenbeheer ===
def ensure_active_device(sp):
    pc_name = socket.gethostname().lower()
    devices = sp.devices().get('devices', [])
    pc_device = next((d['id'] for d in devices if fuzz.ratio(d['name'].lower(), pc_name) >= 90), None)

    if not pc_device:
        if open_spotify_app():
            time.sleep(5)
            devices = sp.devices().get('devices', [])
            pc_device = next((d['id'] for d in devices if fuzz.ratio(d['name'].lower(), pc_name) >= 90), None)

    if pc_device:
        sp.transfer_playback(device_id=pc_device, force_play=False)
        time.sleep(1)
        return pc_device
    return None

# === Zoekfunctionaliteit ===
def find_playlist_uri(sp, query, match_threshold=80):
    user_playlists = sp.current_user_playlists()

    # 1. Exacte match in eigen bibliotheek
    for playlist in user_playlists.get('items', []):
        if playlist['name'].strip().lower() == query.strip().lower():
            return playlist['uri'], playlist['name'], "(exact match in library)"

    # 2. Fuzzy match in eigen bibliotheek
    best_match = None
    best_score = 0
    best_name = ""
    for playlist in user_playlists.get('items', []):
        score = fuzz.ratio(playlist['name'].strip().lower(), query.strip().lower())
        if score > best_score and score >= match_threshold:
            best_score = score
            best_match = playlist['uri']
            best_name = playlist['name']
    if best_match:
        return best_match, best_name, "(fuzzy match in library)"

    # 3. Exact match op Spotify
    results = sp.search(q=f'"{query}"', type="playlist", limit=10)
    for playlist in results.get('playlists', {}).get('items', []):
        if playlist['name'].strip().lower() == query.strip().lower():
            return playlist['uri'], playlist['name'], "(exact match on Spotify)"

    # 4. Fuzzy match op Spotify
    best_match = None
    best_score = 0
    best_name = ""
    for playlist in results.get('playlists', {}).get('items', []):
        score = fuzz.ratio(playlist['name'].strip().lower(), query.strip().lower())
        if score > best_score and score >= match_threshold:
            best_score = score
            best_match = playlist['uri']
            best_name = playlist['name']
    if best_match:
        return best_match, best_name, "(fuzzy match on Spotify)"

    return None, None, "No match found"


def find_track_uri(sp, query, match_threshold=80):
    results = sp.search(q=f'"{query}"', type="track", limit=10)
    for track in results.get('tracks', {}).get('items', []):
        if track['name'].strip().lower() == query.strip().lower():
            return track['uri'], track['name'], "(exact match)"
    best_match = None
    best_score = 0
    best_name = ""
    for track in results.get('tracks', {}).get('items', []):
        score = fuzz.ratio(track['name'].strip().lower(), query.strip().lower())
        if score > best_score and score >= match_threshold:
            best_score = score
            best_match = track['uri']
            best_name = track['name']
    if best_match:
        return best_match, best_name, "(fuzzy match)"
    if not best_match:
        print("Geen goede match gevonden. Suggesties:")
    for track in results.get('tracks', {}).get('items', []):
        print(f"- {track['name']}")

    return None, None, "No match found"

# === Hoofdprogramma ===
def main():
    try:
        action = input("Play playlist or song? (playlist/song): ").strip().lower()
        if action not in ['playlist', 'song']:
            print("Invalid choice.")
            return
        name = input(f"Name of the {action}: ").strip()
        if not name:
            print("No name provided.")
            return

        device_id = ensure_active_device(sp)
        if not device_id:
            print("No active device found.")
            return

        if action == "playlist":
            uri, actual_name, info = find_playlist_uri(sp, name)
            if uri:
                print(f"Playing {actual_name} {info}")
                sp.start_playback(device_id=device_id, context_uri=uri)
            else:
                print("No playlist found.")
        else:
            uri, actual_name, info = find_track_uri(sp, name)
            if uri:
                print(f"Playing {actual_name} {info}")
                sp.start_playback(device_id=device_id, uris=[uri])
            else:
                print("No track found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
