import cgi

import jwt

from configuration.smtp_config import smtp
from model.query import DatabaseManage
from view.response import Response


class FormDetails:
    """Summary:- This class is used processing user input submitted in Front end(HTML)
     and store into database for registration, login and forgot password"""
    def register(self):
        try:    # processing user input submitted in Front end(HTML)
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            responce_data = {'success': True, 'data': [], 'message': ""}
            data = {'email': form['email'].value, 'password': form['password'].value,
                    'confirm_password': form['confirm_password'].value}
            db_obj = DatabaseManage()
            result_passwd = db_obj.password_validate(data)
            result_email = db_obj.email_validate(data['email'])
            if result_email and result_passwd:
                result = db_obj.email_exist(data)
                if result:
                    db_obj.registration(data)
                    responce_data.update({'success': True, 'data': [], 'message': "Successfully Registered"})
                    Response(self).jsonResponse(status=200, data=responce_data)
                else:
                    responce_data.update({'success': False, 'data': [], 'message': "Email already exist"})
                    Response(self).jsonResponse(status=404, data=responce_data)
            else:
                responce_data.update({'success': False, 'data': [], 'message': "not a valid email or password and cnf "
                                                                               "password not match"})
                Response(self).jsonResponse(status=404, data=responce_data)
        except KeyError:
            print()

        # data = {'email': form['email'].value, 'password': form['password'].value,
        #         'confirm_password': form['confirm_password'].value}
        # my_db_obj = db_manage()
        # my_db_obj.registration(data)
        # self._set_headers()
        # self.wfile.write(self._html("Register!"))

    def login(self):
        try:
            # processing user input submitted in Front end(HTML)
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            data = {'email': form['email'].value, 'password': form['password'].value}
            db_obj = DatabaseManage()
            encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
            responce_data = {'message': encoded_jwt}
            if db_obj.email_validate(data['email']):
                result = db_obj.user_exist(encoded_jwt)
                if result:
                    responce_data.update({'success': False, 'data': [], 'message': "Not a Registered User"})
                    Response(self).jsonResponse(status=404, data=responce_data)
                else:
                    responce_data.update({'message': encoded_jwt})
                    Response(self).jsonResponse(status=200, data=responce_data)
            else:
                responce_data.update({'success': False, 'data': [], 'message': "Email not in valid format"})
                Response(self).jsonResponse(status=404, data=responce_data)
        except KeyError:
            print()

    def forget_password(self):
        # processing user input submitted in Front end(HTML)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        responce_data = {'success': True, 'data': [], 'message': ""}
        data = {'email': form['email'].value}
        db_obj = DatabaseManage()
        if db_obj.email_exist(data):
            responce_data.update({'success': False, 'data': [], 'message': "Not a Register User"})
            Response(self).jsonResponse(status=404, data=responce_data)
        else:
            s = smtp()
            s.start()  # start TLS for security
            s.login()  # Authentication and login
            s.send_mail(form['email'].value)  # sending the mail
            # smtp(form['email'].value)
            responce_data.update({'success': True, 'data': [], 'message': "Message send Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)

    def set_password(self, email_id):
        # processing user input submitted in Front end(HTML)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        responce_data = {'success': True, 'data': [], 'message': ""}
        form_keys = list(form.keys())
        data = {'password': form['password'].value}
        db_obj = DatabaseManage()
        if len(form_keys) < 2:
            responce_data.update({'success': False, 'data': [], 'message': "some values are missing"})
            Response(self).jsonResponse(status=404, data=responce_data)
        else:
            db_obj.update_password(email_id, data['password'])
            responce_data.update({'success': True, 'data': [], 'message': "Password Reset"})
            Response(self).jsonResponse(status=404, data=responce_data)

    def create(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        responce_data = {'success': True, 'data': [], 'message': ""}
        form_keys = list(form.keys())
        data = {'Title': form['Title'].value, 'Description': form['Description'].value, 'Colour': form['Colour'].value, 'isPinned': form['isPinned'].value, 'isArchive': form['isArchive'].value, 'isTrash': form['isTrash'].value}
        db_obj = DatabaseManage()
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
        data = {'id':form['id'].value,'Title': form['Title'].value, 'Description': form['Description'].value, 'Colour': form['Colour'].value, 'isPinned': form['isPinned'].value, 'isArchive': form['isArchive'].value, 'isTrash': form['isTrash'].value}
        db_obj = DatabaseManage()
        if len(form_keys) == 7:
            db_obj.update_entry(data)
            responce_data.update({'success': True, 'data': [], 'message': "Data Update Successfully"})
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
        db_obj = DatabaseManage()
        if len(form_keys) == 1:
            db_obj.delete_entry(data)
            responce_data.update({'success': True, 'data': [], 'message': "Data Delete Successfully"})
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
        db_obj = DatabaseManage()
        if len(form_keys) == 1:
            db_obj.read_entry(data)
            responce_data.update({'success': True, 'data': [], 'message': "Data read Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)
        else:
            responce_data.update({'success': False, 'data': [], 'message': "some values are missing"})
            Response(self).jsonResponse(status=404, data=responce_data)
