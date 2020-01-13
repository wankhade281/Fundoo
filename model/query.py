import base64
import re

import jwt


from configuration.db_connection import Database


class DatabaseManage:
    """Summary:- This class is used to form connection with the database and perform operation update, add and check
    entry into the database
    """

    def __init__(self):  # This function is used to form a connection with database
        self.mydbobj = Database()

    def registration(self, data):  # This function is used to store a registration entry into database using sql command
        query = "INSERT INTO tblRegistration(email,password) VALUES ('" + data['email'] + "','" + data[
            'password'] + "') "
        self.mydbobj.execute(query)

    def email_exist(self, data):  # This function is used to check email already exist in database using sql query
        query = "SELECT email from tblRegistration where email = '" + data['email'] + "'"
        result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

    def user_exist(self, data):
        result = jwt.decode(data, 'secret', algorithms=['HS256'])
        # This function is used to check valid user  using sql query for login according return true or false value
        query = "SELECT * from tblRegistration where email = '" + result['some']['email'] + "' and password = '" + \
                result['some']['password'] + "'"
        result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

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

    def update_password(self, email, data):  # This function is used to update a password in database using sql query
        query = " UPDATE tblRegistration SET password = '" + data + "'WHERE  email = '" + email + "' "
        self.mydbobj.execute(query)

    def create_tbl(self, data):
        print("inside  query")
        query = "CREATE TABLE " + data + "(Id INT NOT NULL AUTO_INCREMENT, Title VARCHAR(50) NOT NULL, " \
                                         "Description VARCHAR(500) NOT NULL, Colour VARCHAR(12) NOT NULL, " \
                                         "isPinned BINARY NULL DEFAULT 0, isArchive BINARY NULL DEFAULT 0, " \
                                         "isTrash BINARY NULL DEFAULT 0, PRIMARY KEY (ID)) "
        self.mydbobj.execute(query)

    def create_entry(self, data):
        print(data)
        query = "INSERT INTO crudoperation1 (Title, Description, Colour, isPinned, isArchive, isTrash) VALUES ('" + \
                data[
                    'Title'] + "', '" + data['Description'] + "', '" + data['Colour'] + "', '" + data[
                    'isPinned'] + "', '" + data[
                    'isArchive'] + "', '" + data['isTrash'] + "')"
        self.mydbobj.execute(query)
        print("Entry create Successfully")

    def update_entry(self, data):
        query = "UPDATE crudoperation1 SET Title = '" + data['Title'] + "',Description = '" + data[
            'Description'] + "',Colour = '" + data['Colour'] + "',isPinned = '" + data[
                    'isPinned'] + "', isArchive = '" + data['isArchive'] + "', isTrash = '" + data[
                    'isTrash'] + "' WHERE  id = " + data['id'] + ""
        self.mydbobj.execute(query)
        print("Data update Successfully")

    def delete_entry(self, data):
        query = "DELETE FROM crudoperation1 WHERE id = " + data['id'] + ""
        self.mydbobj.execute(query)
        print("Entry delete Successfully")

    def read_entry(self, data):
        # query = "SELECT * FROM crudoperation1"
        query = "SELECT * FROM crudoperation1 WHERE id = '" + data['id'] + "'"
        entry = self.mydbobj.run_query(query)
        print(entry)

    def profile_exist(self, data):
        image = base64.b64encode(data['profile'])
        valid_image = image.decode("utf-8")
        query = "SELECT * from profilepic where Image = '" + valid_image + "'"
        result = self.mydbobj.run_query(query)
        print(result)
        if len(result):
            return False
        else:
            return True
        pass

    def create_profile(self, data):
        image = base64.b64encode(data['profile'])
        valid_image = image.decode("utf-8")
        query = "INSERT INTO profilepic(Image) VALUES('"+valid_image+"')"
        self.mydbobj.execute(query)
        print("Entry create Successfully")

    def update_profile(self, oldimage, newimage):
        image = base64.b64encode(oldimage)
        oldimage1 = image.decode("utf-8")
        image = base64.b64encode(newimage)
        newimage1 = image.decode("utf-8")
        query = "UPDATE profilepic SET Image = '" + oldimage1 + "' WHERE  Image = '" + newimage1 + "'"
        self.mydbobj.execute(query)
        print("Data update Successfully")

    def delete_profile(self, data):
        query = "DELETE FROM profilepic WHERE Image = '" + data['profile'] + "'"
        self.mydbobj.execute(query)
        print("Entry delete Successfully")

    def read_profile(self):
        query = "SELECT * FROM profilepic "
        result = self.mydbobj.run_query(query)
        for x in result:
            print(x)
        print("Entry read Successfully")

    def read_all(self, data):
        query = "SELECT * FROM crudoperation1 WHERE " + data + "=1 "
        result = self.mydbobj.run_query(query)
        for x in result:
            print(x)
        print("Entry read Successfully")
