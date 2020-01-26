import re
import jwt
from configuration.config import Connection


class Query:
    """Summary:- This class is used to form connection with the database and perform operation update, add and check
    entry into the database
    """
    def __init__(self):  # This function is used to form a connection with database
        self.mydbobj = Connection()

    def email_exist(self, data):  # This function is used to check email already exist in database using sql query
        query = "SELECT email from user where email = '" + data['email'] + "'"
        result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

    def user_exist(self, data):
        # This function is used to check valid user  using sql query for login according return true or false value
        query = "SELECT * from user where email = '" + data['email'] + "' and password = '" + data['password'] + "'"
        result = self.mydbobj.run_query(query)
        user_id = result[0][0]
        email = result[0][1]
        print(user_id, "----------------->>>>>>>>>>")
        print(email, "----------------->>>>>>>>>>")
        if user_id:
            return user_id
        else:
            return False

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

    def profile_exist(self, data):
        query = "SELECT * from profile where Image = '" + data['profile'] + "'"
        result = self.mydbobj.run_query(query)
        print(result)
        if len(result):
            return False
        else:
            return True

