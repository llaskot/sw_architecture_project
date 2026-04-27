from email.message import EmailMessage
from aiosmtplib import send

from app.core.config import settings


class Mailer:
    def __init__(self):
        self.host = settings.mailer_host
        self.port = settings.mailer_port
        self.user = settings.mailer_user
        self.password = settings.mailer_pass

    async def send_email(self, recipient: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = f"App Support <{self.user}>"
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body)

        await send(
            msg,
            hostname=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            use_tls=True
        )