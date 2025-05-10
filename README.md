# Personal Python Assistant

This is a personal assistant for Windows built with Python, similar to Google Assistant or Siri. It allows you to open applications, send WhatsApp messages through Selenium with a headless browser, and automatically sync your Google contacts via the Google API.

## Features

- Detects and opens all installed applications and games on your PC
- Links locally installed games to their corresponding Steam IDs
- Sends WhatsApp messages through WhatsApp Web using a headless browser
- (Planned) Sends emails via your configured contacts
- Fully configurable through a `.env` file

## Project Structure

```plaintext
.
├── app_functions/
│   ├── get_apps.py
│   ├── get_games.py
│   ├── open_app.py
│   └── merge_installed_apps_with_steam_ids.py
├── deprecated_functions/
│   ├── connect_to_phone.py
│   ├── send_whatsapp_message.py
│   └── unlock_phone.py
├── hierTestenWij/
│   └── get_microphone_names.py
├── main_functions/
│   ├── commands.py
│   └── listener.py
├── messaging_functions/
│   ├── get_contacts.py
│   ├── get_phone_number.py
│   ├── whatsapp/
│   │   └── send_whatsapp_message.py
│   └── mail/
│       └── send_email.py
├── call_assistant.py
├── requirements.txt
├── .env
└── example.env
```

## Setup

1. Clone this repository.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on the provided `example.env` and configure the paths and credentials accordingly.

## Notes

- This project is in early development and maintained by non-professional programmers, so bugs and limitations are expected.
- There is no front-end (GUI) yet. All interaction currently happens through the command line.
- Contact syncing via Google API is functional but requires manual setup and credentials.
- Voice recognition is planned but not yet implemented.
- Email sending is not functional yet — placeholder only.

---

## Feedback & Contribution

Feedback is welcome. Feel free to report issues or suggest improvements via GitHub.

Good luck using the assistant!
