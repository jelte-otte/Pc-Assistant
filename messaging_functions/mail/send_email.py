import os
import smtplib
from email.message import EmailMessage
import dotenv
from messaging_functions.mail.smpt_config import SMTP_CONFIG

def get_smtp_settings(email):
    domain = email.split('@')[-1]
    return SMTP_CONFIG.get(domain)

def send_email(subject, body, to_email):
    dotenv.load_dotenv()
    from_email = os.getenv('FROM_EMAIL')
    from_password = os.getenv('FROM_PASSWORD').strip()
    print("Email:", from_email)
    print("Password:", from_password)
    smtp_settings = get_smtp_settings(from_email)
    if smtp_settings is None:
        raise ValueError(f"SMTP-instellingen onbekend voor domein '{from_email.split('@')[-1]}'")

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    port = smtp_settings['port']
    server = smtp_settings['server']

    if port == 465:
        with smtplib.SMTP_SSL(server, port) as smtp:
            smtp.login(from_email, from_password
)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(server, port) as smtp:
            smtp.starttls()
            smtp.login(from_email, from_password)
            smtp.send_message(msg)
