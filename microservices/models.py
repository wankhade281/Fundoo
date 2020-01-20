import re
import jwt
import redis
from nameko.rpc import rpc

from microservices.config import Database, SMTP


class Data:
    """Summary:- This class is used to form connection with the database and perform operation update, add and check
    entry into the database
    """
    name = "data_service"

    def __init__(self):  # This function is used to form a connection with database
        self.mydbobj = Database()
        self.st = SMTP()
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    @rpc
    def registration(self, data):  # This function is used to store a registration entry into database using sql command
        query = "INSERT INTO user(email,password) VALUES ('" + data['email'] + "','" + data[
            'password'] + "') "
        self.mydbobj.execute(query)

    @rpc
    def email_exist(self, data):  # This function is used to check email already exist in database using sql query
        query = "SELECT email from user where email = '" + data['email'] + "'"
        result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

    @rpc
    def user_exist(self, data):
        # This function is used to check valid user  using sql query for login according return true or false value
        result = jwt.decode(data, 'secret', algorithms=['HS256'])
        query = "SELECT * from user where email = '" + result['some']['email'] + "' and password = '" + \
                result['some']['password'] + "'"
        result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

    @rpc
    def email_validate(self, email):
        # This function is used to check email is in valid format or not and return true or false value
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    @rpc
    def password_validate(self, data):
        # This function is used to check psw and cnf psw is in valid or not and return true and false value
        if data['password'] == data['confirm_password']:
            return True
        else:
            return False

    @rpc
    def update_password(self, email, data):  # This function is used to update a password in database using sql query
        query = " UPDATE user SET password = '" + data + "'WHERE  email = '" + email + "' "
        self.mydbobj.execute(query)

    @rpc
    def create_entry(self, data):
        print(data)
        query = "INSERT INTO note (Title, Description, Colour, isPinned, isArchive, isTrash) VALUES ('" + \
                data[
                    'Title'] + "', '" + data['Description'] + "', '" + data['Colour'] + "', '" + data[
                    'isPinned'] + "', '" + data[
                    'isArchive'] + "', '" + data['isTrash'] + "')"
        self.mydbobj.execute(query)
        print("Entry create Successfully")

    @rpc
    def update_entry(self, data):
        query = "UPDATE note SET Title = '" + data['Title'] + "',Description = '" + data[
            'Description'] + "',Colour = '" + data['Colour'] + "',isPinned = '" + data[
                    'isPinned'] + "', isArchive = '" + data['isArchive'] + "', isTrash = '" + data[
                    'isTrash'] + "' WHERE  id = " + data['id'] + ""
        self.mydbobj.execute(query)
        print("Data update Successfully")

    @rpc
    def delete_entry(self, data):
        query = "DELETE FROM note WHERE id = " + data['id'] + ""
        self.mydbobj.execute(query)
        print("Entry delete Successfully")

    @rpc
    def read_entry(self, data):
        # query = "SELECT * FROM new_table"
        query = "SELECT * FROM note WHERE id = '" + data['id'] + "'"
        entry = self.mydbobj.run_query(query)
        print(entry)

    @rpc
    def put_cache(self, data, data_id):
        self.r.hmset(data_id, data)

    @rpc
    def get_cache(self, data_id):
        x = self.r.hgetall(data_id)
        print(x)
        return x

    @rpc
    def del_cache(self, data_id):
        self.r.hdel(data_id, len(data_id))

    @rpc
    def get_keys(self, data_id):
        return self.r.hkeys(data_id)
