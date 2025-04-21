import json
from difflib import get_close_matches
import unicodedata

def normalize(text: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def get_contact_phone_number(name_input: str) -> str | None:
    with open("contacts/contacts.json", "r", encoding="utf-8") as f:
        contacts = json.load(f)

    normalized_input = normalize(name_input)
    name_map = {normalize(c['name']): c for c in contacts}

    matches = get_close_matches(normalized_input, list(name_map.keys()), n=1, cutoff=0.85)

    if not matches:
        print(f"No close match found for '{name_input}'.")
        return None

    matched_contact = name_map[matches[0]]
    print(f"Found contact: {matched_contact['name']}")
    return matched_contact['phone'].replace("+", "").replace(" ", "").replace("-", "")
