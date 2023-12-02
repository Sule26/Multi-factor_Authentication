from email.message import EmailMessage
from twilio.rest import Client
from loguru import logger
import smtplib
import pyotp
import ssl
import os


def generate_key() -> str:
    return pyotp.random_base32()


class Authy:
    def generate_code(self, key: str, email: str) -> str:
        self.totp = pyotp.TOTP(s=key)
        self.totp_authy = self.totp.provisioning_uri(name=email, issuer_name="Uerj Multi-Factor Authentication")
        logger.debug(f"{self.totp.now()=}")
        return self.totp_authy

    def verify_code(self, key: str, code: str) -> bool:
        if hasattr(Authy, "totp"):
            return self.totp.verify(code)

        self.totp = pyotp.TOTP(s=key)
        return self.totp.verify(code)


class Email:
    EMAIL_SENDER = str(os.environ.get("EMAIL"))
    EMAIL_PASSWORD = str(os.environ.get("EMAIL_PASSWORD"))
    SUBJECT = "Code"

    def generate_code(self, key: str) -> str:
        self.totp = pyotp.TOTP(s=key, interval=60)
        logger.debug(f"{self.totp.now()=}")
        return self.totp.now()

    def send_message(self, key: str, email_receiver: str) -> None:
        em = EmailMessage()
        em["From"] = self.EMAIL_SENDER
        em["To"] = email_receiver
        em["subject"] = self.SUBJECT
        em.set_content(self.generate_code(key))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(user=self.EMAIL_SENDER, password=self.EMAIL_PASSWORD)
            smtp.sendmail(self.EMAIL_SENDER, email_receiver, em.as_string())

    def verify_code(self, key: str, code: str) -> bool:
        if hasattr(Email, "totp"):
            return self.totp.verify(code)

        self.totp = pyotp.TOTP(s=key, interval=60)
        return self.totp.verify(code)


class SMS:
    ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE = os.environ.get("TWILIO_PHONE")
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    def generate_code(self, key: str) -> str:
        self.totp = pyotp.TOTP(s=key, interval=60)
        logger.debug(f"{self.totp.now()=}")
        return self.totp.now()

    def send_sms(self, key: str, phone_receiver: str) -> None:
        self.CLIENT.messages.create(
            from_=self.TWILIO_PHONE, body=self.generate_code(key), to=phone_receiver
        )

    def verify_code(self, key: str, code: str) -> bool:
        if hasattr(SMS, "totp"):
            return self.totp.verify(code)

        self.totp = pyotp.TOTP(s=key, interval=60)
        return self.totp.verify(code)
