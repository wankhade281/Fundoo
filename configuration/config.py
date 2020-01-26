import os
from dotenv import load_dotenv
import mysql.connector
import smtplib

load_dotenv()


def singleton(myClass):
    instances = {}

    def get_instance(*args, **kwargs):
        if myClass not in instances:
            instances[myClass] = myClass(*args, **kwargs)
        return instances[myClass]

    return get_instance


@singleton
class Connection:  # This class is used to form a database connection
    def __init__(self, **kwargs):
        self.conn = self.connect(**kwargs)
        self.mycursor = self.conn.cursor()

    def connect(self, **kwargs):
        mydb = mysql.connector.connect(
            host=kwargs["host"],
            user=kwargs["user"],
            passwd=kwargs["passwd"],
            database=kwargs["database"],
        )
        return mydb

    def smtp(self):
        server = os.getenv("SMTP_EXCHANGE_SERVER")
        port = os.getenv("SMTP_EXCHANGE_PORT")
        s = smtplib.SMTP(server, port)
        s.starttls()
        s.login(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), os.getenv("SMTP_EXCHANGE_USER_PASSWORD"))
        return s

    def run_query(self, query):
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def query_execute(self, query):
        self.mycursor.execute(query)
        self.conn.commit()


con = Connection(host=os.getenv("HOST"),
                 user=os.getenv("USER"),
                 passwd=os.getenv("PASSWD"),
                 database=os.getenv("DATABASE"))