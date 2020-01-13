import os
from dotenv import load_dotenv
import mysql.connector

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
