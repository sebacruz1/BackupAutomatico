from email.message import EmailMessage
import smtplib, ssl
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

msg = EmailMessage()
msg.set_content("Backup Realizado! .")

msg['Subject'] = "Backup Realizado con éxito"
msg['From'] = EMAIL
msg['To'] = EMAIL_DESTINO

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)

