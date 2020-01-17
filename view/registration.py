import cgi

import jwt

from configuration.connection import SMTP
from model.query import Data
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
            db_obj = Data()
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
            db_obj = Data()
            encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
            response_data = {'message': encoded_jwt}
            if db_obj.email_validate(data['email']):
                result = db_obj.user_exist(encoded_jwt)
                if result:
                    response_data.update({'success': False, 'data': [], 'message': "Not a Registered User"})
                    Response(self).jsonResponse(status=404, data=response_data)
                else:
                    response_data.update({'success': True, 'data': [], 'message': "Login Successful"})
                    Response(self).jsonResponse(status=200, data=response_data)
            else:
                response_data.update({'success': False, 'data': [], 'message': "Email not in valid format"})
                Response(self).jsonResponse(status=404, data=response_data)
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
        response_data = {'success': True, 'data': [], 'message': ""}
        data = {'email': form['email'].value}
        db_obj = Data()
        if db_obj.email_exist(data):
            response_data.update({'success': False, 'data': [], 'message': "Not a Register User"})
            Response(self).jsonResponse(status=404, data=response_data)
        else:
            s = SMTP()
            s.start()  # start TLS for security
            s.login()  # Authentication and login
            s.send_mail(form['email'].value)  # sending the mail
            # smtp(form['email'].value)
            response_data.update({'success': True, 'data': [], 'message': "Message sent Successfully"})
            Response(self).jsonResponse(status=200, data=response_data)

    def set_password(self, email_id):
        # processing user input submitted in Front end(HTML)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        response_data = {'success': True, 'data': [], 'message': ""}
        form_keys = list(form.keys())
        data = {'password': form['password'].value}
        db_obj = Data()
        if len(form_keys) < 2:
            response_data.update({'success': False, 'data': [], 'message': "some values are missing"})
            Response(self).jsonResponse(status=404, data=response_data)
        else:
            db_obj.update_password(email_id, data['password'])
            response_data.update({'success': True, 'data': [], 'message': "Password Reset Successfully"})
            Response(self).jsonResponse(status=404, data=response_data)
