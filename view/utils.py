import re

from config.db_connection import Connection


class Utility:
    def __init__(self):
        self.mydb = Connection()

    def email_validate(self, email):
        # This function is used to check email is in valid format or not and return true or false value
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    def password_validate(self, data):
        # This function is used to check psw and cnf psw is in valid or not and return true and false value
        if data['password'] == data['confirm_password']:
            return True
        else:
            return False