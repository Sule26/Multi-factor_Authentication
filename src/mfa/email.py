from email.message import EmailMessage
from .otp import OTP
import os
import ssl
import smtplib


class Email:
    EMAIL_SENDER = os.environ.get("EMAIL")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    SUBJECT = "Code"

    def send_message(self, email_receiver: str) -> None:
        em = EmailMessage()
        em["From"] = self.EMAIL_SENDER
        em["To"] = email_receiver
        em["subject"] = self.SUBJECT
        em.set_content(OTP.generate_code)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context) as smtp:
            smtp.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
            smtp.sendmail(self.EMAIL_SENDER, email_receiver, em.as_string())
