import base64
import cgi
import re
import jwt
import redis

from configuration.connection import Database
from view.response import Response


class Data:
    """Summary:- This class is used to form connection with the database and perform operation update, add and check
    entry into the database
    """

    def __init__(self):  # This function is used to form a connection with database
        self.mydbobj = Database()
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def registration(self, data):  # This function is used to store a registration entry into database using sql command
        query = "INSERT INTO user(email,password) VALUES ('" + data['email'] + "','" + data[
            'password'] + "') "
        self.mydbobj.execute(query)

    def email_exist(self, data):  # This function is used to check email already exist in database using sql query
        query = "SELECT email from user where email = '" + data['email'] + "'"
        result = self.mydbobj.run_query(query)
        if len(result):
            return False
        else:
            return True

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
        query = " UPDATE user SET password = '" + data + "'WHERE  email = '" + email + "' "
        self.mydbobj.execute(query)

    def create_tbl(self, data):
        query = "CREATE TABLE " + data + "(Id INT NOT NULL AUTO_INCREMENT, Title VARCHAR(50) NOT NULL, " \
                                         "Description VARCHAR(500) NOT NULL, Colour VARCHAR(12) NOT NULL, " \
                                         "isPinned BINARY NULL DEFAULT 0, isArchive BINARY NULL DEFAULT 0, " \
                                         "isTrash BINARY NULL DEFAULT 0, PRIMARY KEY (ID)) "
        self.mydbobj.execute(query)

    def create_entry(self, data):
        print(data)
        query = "INSERT INTO note (Title, Description, Colour, isPinned, isArchive, isTrash) VALUES ('" + \
                data[
                    'Title'] + "', '" + data['Description'] + "', '" + data['Colour'] + "', '" + data[
                    'isPinned'] + "', '" + data[
                    'isArchive'] + "', '" + data['isTrash'] + "')"
        self.mydbobj.execute(query)
        print("Entry create Successfully")

    def update_entry(self, data):
        query = "UPDATE note SET Title = '" + data['Title'] + "',Description = '" + data[
            'Description'] + "',Colour = '" + data['Colour'] + "',isPinned = '" + data[
                    'isPinned'] + "', isArchive = '" + data['isArchive'] + "', isTrash = '" + data[
                    'isTrash'] + "' WHERE  id = " + data['id'] + ""
        self.mydbobj.execute(query)
        print("Data update Successfully")

    def delete_entry(self, data):
        query = "DELETE FROM note WHERE id = " + data['id'] + ""
        self.mydbobj.execute(query)
        print("Entry delete Successfully")

    def read_entry(self, data):
        # query = "SELECT * FROM new_table"
        query = "SELECT * FROM note WHERE id = '" + data['id'] + "'"
        entry = self.mydbobj.run_query(query)
        print(entry)

    def read_all(self, data):
        query = "SELECT * FROM note WHERE " + data + "=1 "
        result = self.mydbobj.run_query(query)
        for x in result:
            print(x)
        print("Entry read Successfully")

    def profile_exist(self, data):
        image = base64.b64encode(data['profile'])
        valid_image = image.decode("utf-8")
        query = "SELECT * from profile where Image = '" + valid_image + "'"
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
        query = "INSERT INTO profile(Image) VALUES('"+valid_image+"')"
        self.mydbobj.execute(query)
        print("Entry create Successfully")

    def update_profile(self, oldimage, newimage):
        image = base64.b64encode(oldimage)
        oldimage1 = image.decode("utf-8")
        image = base64.b64encode(newimage)
        newimage1 = image.decode("utf-8")
        query = "UPDATE profile SET Image = '" + oldimage1 + "' WHERE  Image = '" + newimage1 + "'"
        self.mydbobj.execute(query)
        print("Data update Successfully")

    def delete_profile(self, data):
        query = "DELETE FROM profile WHERE Image = '" + data['profile'] + "'"
        self.mydbobj.execute(query)
        print("Entry delete Successfully")

    def read_profile(self):
        query = "SELECT * FROM profile "
        result = self.mydbobj.run_query(query)
        for x in result:
            print(x)
        print("Entry read Successfully")

    def create(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        responce_data = {'success': True, 'data': [], 'message': ""}
        form_keys = list(form.keys())
        data = {'Title': form['Title'].value, 'Description': form['Description'].value, 'Colour': form['Colour'].value,
                'isPinned': form['isPinned'].value, 'isArchive': form['isArchive'].value,
                'isTrash': form['isTrash'].value}
        db_obj = Data()
        if len(form_keys) == 6:
            db_obj.create_entry(data)
            responce_data.update({'success': True, 'data': [], 'message': "Entry Create Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)
        else:
            responce_data.update({'success': False, 'data': [], 'message': "some values are missing"})
            Response(self).jsonResponse(status=404, data=responce_data)

    def update(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        responce_data = {'success': True, 'data': [], 'message': ""}
        form_keys = list(form.keys())
        data = {'id': form['id'].value, 'Title': form['Title'].value, 'Description': form['Description'].value,
                'Colour': form['Colour'].value, 'isPinned': form['isPinned'].value,
                'isArchive': form['isArchive'].value, 'isTrash': form['isTrash'].value}
        db_obj = Data()
        if len(form_keys) == 7:
            db_obj.update_entry(data)
            responce_data.update({'success': True, 'data': [], 'message': "Data Update Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)
        else:
            responce_data.update({'success': False, 'data': [], 'message': "some values are missing"})
            Response(self).jsonResponse(status=404, data=responce_data)

    def read(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        responce_data = {'success': True, 'data': [], 'message': ""}
        form_keys = list(form.keys())
        data = {'id': form['id'].value}
        db_obj = Data()
        if len(form_keys) == 1:
            db_obj.read_entry(data)
            responce_data.update({'success': True, 'data': [], 'message': "Data read Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)
        else:
            responce_data.update({'success': False, 'data': [], 'message': "some values are missing"})
            Response(self).jsonResponse(status=404, data=responce_data)

    def delete(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        responce_data = {'success': True, 'data': [], 'message': ""}
        form_keys = list(form.keys())
        data = {'id': form['id'].value}
        db_obj = Data()
        if len(form_keys) == 1:
            db_obj.delete_entry(data)
            responce_data.update({'success': True, 'data': [], 'message': "Data Delete Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)
        else:
            responce_data.update({'success': False, 'data': [], 'message': "some values are missing"})
            Response(self).jsonResponse(status=404, data=responce_data)

    def put_cache(self, data):
        self.r.hmset("note_data", data)

    def get_cache(self, data):
        x = self.r.hgetall(data)
        print(x)
        return x