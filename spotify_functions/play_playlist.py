import os
import socket
import subprocess
import time
from fuzzywuzzy import fuzz
import json

# Jouw bestaande open_app functies
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

# Algemene zoekfunctie voor hergebruik
def search_spotify_item(sp, query, search_type, exact=True, match_threshold=80):
    try:
        if search_type == "playlist":
            # Zoek in gebruikersplaylists
            if exact:
                user_playlists = sp.current_user_playlists()
                if user_playlists and 'items' in user_playlists:
                    for playlist in user_playlists['items']:
                        if not playlist or 'name' not in playlist:
                            continue
                        if playlist['name'].lower() == query.lower():
                            return playlist['uri']
            # Zoek publiek op Spotify
            results = sp.search(q=f'"{query}"' if exact else query, type="playlist", limit=10)
            items = results.get('playlists', {}).get('items', [])
        elif search_type == "track":
            # Zoek alleen publiek op Spotify voor tracks
            results = sp.search(q=f'"{query}"' if exact else query, type="track", limit=10)
            items = results.get('tracks', {}).get('items', [])
        else:
            return None
        
        if not items:
            return None
            
        if exact:
            for item in items:
                if not item or 'name' not in item:
                    continue
                if item['name'].lower() == query.lower():
                    return item['uri']
        else:
            best_match = None
            best_score = 0
            for item in items:
                if not item or 'name' not in item:
                    continue
                score = fuzz.ratio(item['name'].lower(), query.lower())
                if score > best_score and score >= match_threshold:
                    best_score = score
                    best_match = item['uri']
            return best_match
        
        return None
    except Exception as e:
        print(f"Error while searching {search_type} on Spotify: {e}")
        return None

# Functie om een playlist af te spelen
def play_playlist(sp, playlist_name, device_id, match_threshold=80):
    # Stap 1: Zoek exacte match in eigen account
    playlist_uri = search_spotify_item(sp, playlist_name, "playlist", exact=True, match_threshold=match_threshold)
    if playlist_uri:
        print(f"Found exact match in your account: {playlist_name}")
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        return True
    
    # Stap 2: Zoek ongeveer match in eigen account
    playlist_uri = search_spotify_item(sp, playlist_name, "playlist", exact=False, match_threshold=match_threshold)
    if playlist_uri:
        print(f"Found no exact match, but found a similar playlist in your account: {playlist_name}")
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        return True
    
    # Stap 3: Zoek exacte match op Spotify
    playlist_uri = search_spotify_item(sp, playlist_name, "playlist", exact=True, match_threshold=match_threshold)
    if playlist_uri:
        print(f"No match in your account, but found an exact match on Spotify: {playlist_name}")
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        return True
    
    # Stap 4: Zoek ongeveer match op Spotify
    playlist_uri = search_spotify_item(sp, playlist_name, "playlist", exact=False, match_threshold=match_threshold)
    if playlist_uri:
        print(f"No exact match, but found a similar playlist on Spotify: {playlist_name}")
        sp.start_playback(device_id=device_id, context_uri=playlist_uri)
        return True
    
    print(f"No playlist found for the name '{playlist_name}'")
    return False

# Functie om een nummer af te spelen
def play_song(sp, song_name, device_id, match_threshold=80):
    # Zoek exacte match voor het nummer
    song_uri = search_spotify_item(sp, song_name, "track", exact=True, match_threshold=match_threshold)
    if song_uri:
        print(f"Found exact match for song: {song_name}")
        sp.start_playback(device_id=device_id, uris=[song_uri])
        return True
    
    # Zoek ongeveer match voor het nummer
    song_uri = search_spotify_item(sp, song_name, "track", exact=False, match_threshold=match_threshold)
    if song_uri:
        print(f"Found no exact match, but found a similar song: {song_name}")
        sp.start_playback(device_id=device_id, uris=[song_uri])
        return True
    
    print(f"No song found for the name '{song_name}'")
    return False

