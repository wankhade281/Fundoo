import os
from dotenv import load_dotenv
import mysql.connector
from email.mime.text import MIMEText
import jwt
import smtplib

load_dotenv()


class Database:  # This class is used to form a database connection
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            passwd=os.getenv("PASSWD"),
            database=os.getenv("DATABASE")
        )
        self.mycursor = self.mydb.cursor()

    def run_query(self, query):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def execute(self, query):
        self.mycursor.execute(query)
        self.mydb.commit()


class SMTP:
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
        data = f"http://localhost:9090/forget/?new={encoded_jwt}"
        msg = MIMEText(data)
        self.s.sendmail(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), email_id, msg.as_string())

    def __del__(self):
        self.s.quit()
