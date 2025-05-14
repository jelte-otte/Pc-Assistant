import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from fuzzywuzzy import fuzz

load_dotenv()
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-modify-playback-state user-read-playback-state playlist-read-private"
))

# Functie om playlist te zoeken in gebruikersaccount
def find_user_playlist(sp, playlist_name, exact=True, match_threshold=80):
    try:
        user_playlists = sp.current_user_playlists()
        if not user_playlists or 'items' not in user_playlists:
            return None
        best_match = None
        best_score = 0
        
        for playlist in user_playlists['items']:
            if not playlist or 'name' not in playlist:
                continue
            name = playlist['name'].lower()
            if exact and name == playlist_name.lower():
                return playlist['uri']
            elif not exact:
                score = fuzz.ratio(name, playlist_name.lower())
                if score > best_score and score >= match_threshold:
                    best_score = score
                    best_match = playlist['uri']
        
        return best_match if not exact else None
    except Exception as e:
        print(f"Fout bij het ophalen van gebruikersplaylists: {e}")
        return None

# Functie om playlist te zoeken op Spotify (publiek)
def find_spotify_playlist(sp, playlist_name, exact=True, match_threshold=80):
    try:
        results = sp.search(q=f'"{playlist_name}"' if exact else playlist_name, type="playlist", limit=10)
        items = results.get('playlists', {}).get('items', [])
        
        if not items:
            return None
            
        if exact:
            for item in items:
                if not item or 'name' not in item:
                    continue
                if item['name'].lower() == playlist_name.lower():
                    return item['uri']
        else:
            best_match = None
            best_score = 0
            for item in items:
                if not item or 'name' not in item:
                    continue
                score = fuzz.ratio(item['name'].lower(), playlist_name.lower())
                if score > best_score and score >= match_threshold:
                    best_score = score
                    best_match = item['uri']
            return best_match
        
        return None
    except Exception as e:
        print(f"Fout bij het zoeken op Spotify: {e}")
        return None

# Hoofdlogica
try:
    playlist_name = input("Voeg hier je playlist naam in: ").strip()
    if not playlist_name:
        print("Geen playlist naam ingevoerd.")
        exit(1)
        
    match_threshold = 80  # Stel hier het gewenste percentage in (0-100)

    # Stap 1: Zoek exacte match in eigen account
    playlist_uri = find_user_playlist(sp, playlist_name, exact=True, match_threshold=match_threshold)
    if playlist_uri:
        print(f"Exacte match gevonden in jouw account: {playlist_name}")
        sp.start_playback(context_uri=playlist_uri)
    else:
        # Stap 2: Zoek ongeveer match in eigen account
        playlist_uri = find_user_playlist(sp, playlist_name, exact=False, match_threshold=match_threshold)
        if playlist_uri:
            print(f"Geen exacte match, maar wel een vergelijkbare playlist gevonden in jouw account (gelijkenis: {match_threshold}% of hoger).")
            sp.start_playback(context_uri=playlist_uri)
        else:
            # Stap 3: Zoek exacte match op Spotify
            playlist_uri = find_spotify_playlist(sp, playlist_name, exact=True, match_threshold=match_threshold)
            if playlist_uri:
                print(f"Geen match in jouw account, maar wel een exacte match gevonden op Spotify: {playlist_name}")
                sp.start_playback(context_uri=playlist_uri)
            else:
                # Stap 4: Zoek ongeveer match op Spotify
                playlist_uri = find_spotify_playlist(sp, playlist_name, exact=False, match_threshold=match_threshold)
                if playlist_uri:
                    print(f"Geen exacte match, maar wel een vergelijkbare playlist gevonden op Spotify (gelijkenis: {match_threshold}% of hoger).")
                    sp.start_playback(context_uri=playlist_uri)
                else:
                    print(f"Geen playlist gevonden die overeenkomt met '{playlist_name}' (met minimaal {match_threshold}% gelijkenis).")
except Exception as e:
    print(f"Algemene fout: {e}")