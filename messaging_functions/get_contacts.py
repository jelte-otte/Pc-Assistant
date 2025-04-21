import json
import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

load_dotenv()
BASE_DIR = os.path.dirname(__file__)
CREDENTIALS_DIR = os.getenv('CREDENTIALS_FOLDER')
CONTACTS_DIR = os.getenv('CONTACTS_FOLDER')

CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(CREDENTIALS_DIR, 'token.json')
JSON_FILE = os.path.join(CONTACTS_DIR, 'contacts.json')

os.makedirs(CREDENTIALS_DIR, exist_ok=True)
os.makedirs(CONTACTS_DIR, exist_ok=True)

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_contacts():
    creds = get_credentials()
    service = build('people', 'v1', credentials=creds)

    print("Fetching contacts from Google...")
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,phoneNumbers'
    ).execute()

    contacts = []
    for person in results.get('connections', []):
        names = person.get('names', [])
        numbers = person.get('phoneNumbers', [])
        if names and numbers:
            name = names[0].get('displayName', '')
            phone = numbers[0].get('value', '').replace(' ', '').replace('-', '')
            contacts.append({'name': name, 'phone': phone})
    return contacts

def save_to_json(contacts):
    with open(JSON_FILE, 'w', encoding='utf-8') as jsonfile:
        json.dump(contacts, jsonfile, indent=2, ensure_ascii=False)
    print(f"{len(contacts)} contacts saved to {JSON_FILE}")

def get_contacts():
    contacts = fetch_contacts()
    save_to_json(contacts)

if __name__ == '__main__':
    get_contacts()
