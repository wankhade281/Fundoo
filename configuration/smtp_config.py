import os
import smtplib
from email.mime.text import MIMEText
import jwt
from dotenv import load_dotenv

load_dotenv()


class smtp:
    def __init__(self):
        self.server = os.getenv("SMTP_EXCHANGE_SERVER")
        self.port = os.getenv("SMTP_EXCHANGE_PORT")
        self.s = smtplib.SMTP(self.server, self.port)

    def start(self):
        self.s.starttls()

    def login(self):
        self.s.login(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), os.getenv("SMTP_EXCHANGE_USER_PASSWORD"))

    def send_mail(self, email_id):
        encoded_jwt = jwt.encode({'email': email_id}, 'secret', algorithm='HS256').decode("UTF-8")
        data = f"http://localhost:8080/forget/?new={encoded_jwt}"
        msg = MIMEText(data)
        self.s.sendmail(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), email_id, msg.as_string())

    def __del__(self):
        self.s.quit()
