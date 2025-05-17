import smtplib
from email.message import EmailMessage

# Inloggegevens (vervang deze nooit hardcoded in productie)
EMAIL_ADDRESS = "mymailingservice@mail.com"
EMAIL_PASSWORD = "p2FdAU7ELkKA3GT"

def send_mail(to_address, subject, body):
    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.mail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"Mail verzonden naar {to_address}")
    except Exception as e:
        print(f"Fout bij verzenden: {e}")

# Voorbeeldgebruik
if __name__ == "__main__":
    send_mail("ontvanger@example.com", "Testonderwerp", "Dit is een testbericht via Mail.com SMTP.")
