from dotenv import load_dotenv
from spotify_functions import play_playlist
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os

load_dotenv()
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-modify-playback-state user-read-playback-state playlist-read-private"
))

def play_something():
    try:
        action = input("Do you want to play a playlist or a song? (playlist/song): ").strip().lower()
        if action not in ['playlist', 'song']:
            print("Invalid action. Please choose 'playlist' or 'song'.")
            exit(1)
        
        name = input(f"Put here the name of the {action}: ").strip()
        if not name:
            print(f"No {action} name submitted.")
            exit(1)
            
        match_threshold = 80  # Stel hier het gewenste percentage in (0-100)

        # Zorg ervoor dat er een actief apparaat is
        device_id = ensure_active_device(sp)
        if not device_id:
            print("Cannot activate a device. Script stopped.")
            exit(1)

        # Voer de juiste actie uit
        if action == 'playlist':
            play_playlist(sp, name, device_id, match_threshold)
        else:  # action == 'song'
            play_song(sp, name, device_id, match_threshold)

    except Exception as e:
        print(f"General error: {e}")