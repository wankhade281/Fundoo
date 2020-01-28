import os
import smtplib
from email.mime.text import MIMEText


class SMTP:
    def __init__(self):
        self.con = self.connect()

    def connect(self):
        server = os.getenv("SMTP_EXCHANGE_SERVER")
        port = os.getenv("SMTP_EXCHANGE_PORT")
        s = smtplib.SMTP(server, port)
        s.starttls()
        s.login(os.getenv("SMTP_EXCHANGE_USER_LOGIN"),os.getenv("SMTP_EXCHANGE_USER_PASSWORD"))
        return s

    def send_mail(self, data, email):
        msg = MIMEText(data)
        self.con.sendmail(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), email, msg.as_string())
        self.con.quit()