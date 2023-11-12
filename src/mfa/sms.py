from twilio.rest import Client
from .otp import OTP
from loguru import logger
import os


class SMS:
    ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
    AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms(self, phone_receiver) -> None:
        message = self.CLIENT.messages.create(
            from_=os.environ.get("TWILIO_PHONE"), body=OTP.generate_code(), to=phone_receiver
        )
        # logger.debug(message.sid)
