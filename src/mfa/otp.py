import qrcode
import pyotp
import os


class OTP:
    def generate_code(self) -> str:
        totp = pyotp.TOTP(s=os.environ.get("PYOTP_KEY"), interval=300)
        return totp.now()

    def generate_authenticator(self, username, email) -> None:
        authy = pyotp.totp.TOTP(os.environ.get("PYOTP_KEY")).provisioning_uri(
            name=email, issuer_name="Uerj Multi-Factor Authentication"
        )
        qrcode.make(authy).save(f"{username}.png")
