
from email.message import EmailMessage
from twilio.rest import Client
from loguru import logger
import smtplib
import pyotp
import ssl
import os


class OTP:
    def generate_code(self) -> str:
        self.totp = pyotp.TOTP(s="base32secret3232", interval=300)
        code = self.totp.now()
        return code

    def generate_authenticator(self, email) -> None:
        authy = pyotp.totp.TOTP(os.environ.get("PYOTP_KEY")).provisioning_uri(
            name=email, issuer_name="Uerj Multi-Factor Authentication"
        )
        return authy

    def verify(self, code) -> bool:
        return self.totp.verify(code)


class Email:
    EMAIL_SENDER = os.environ.get("EMAIL")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    SUBJECT = "Code"
    OTP = OTP()

    
    def get(self):
        logger.debug(self.EMAIL_SENDER)
        logger.debug(self.EMAIL_PASSWORD)


    def send_message(self, email_receiver: str) -> None:
        em = EmailMessage()
        em["From"] = self.EMAIL_SENDER
        em["To"] = email_receiver
        em["subject"] = self.SUBJECT
        self.current_code = self.OTP.generate_code()
        em.set_content(self.current_code)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(self.EMAIL_SENDER, self.EMAIL_PASSWORD)
            smtp.sendmail(self.EMAIL_SENDER, email_receiver, em.as_string())



class SMS:
    ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
    OTP = OTP()

    def send_sms(self, phone_receiver) -> None:
        self.current_code = self.OTP.generate_code()
        message = self.CLIENT.messages.create(
            from_=os.environ.get("TWILIO_PHONE"), body=self.current_code, to=phone_receiver
        )
        # logger.debug(message.sid)

