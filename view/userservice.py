import cgi
import jwt
from .utils import Utility
from services.notes import Note
from services.users import User


class UserData:

    def user_register(self):
        try:  # processing user input submitted in Front end(HTML)
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            data = {'email': form['email'].value, 'password': form['password'].value,
                    'confirm_password': form['confirm_password'].value}
            obj = Utility()
            u = User()
            result_passwd = obj.password_validate(data)
            result_email = obj.email_validate(data['email'])
            data = {'email': form['email'].value, 'password': form['password'].value
                    }
            if result_email and result_passwd:
                response = u.user_registration(data)
                return response
            else:
                return {'success': True, 'data': [], 'message': "Not a valid Email"}
        except KeyError:
            print()

    def user_login(self):
        try:
            # processing user input submitted in Front end(HTML)
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            data = {'email': form['email'].value, 'password': form['password'].value}
            obj = Utility()
            u = User()
            if obj.email_validate(data['email']):
                response = u.user_login(data)
                return response
            else:
                return {'success': True, 'data': [], 'message': "Not a valid Email"}
        except KeyError:
            print()

    def forget_pass(self, version):
        # processing user input submitted in Front end(HTML)
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            version = version.split('/')[0]
            host = self.headers['Host']
            data = {'email': form['email'].value}
            obj = Utility()
            u = User()
            if obj.email_validate(data['email']):
                response = u.forget_password(data, version, host)
                return response
            else:
                return {'success': True, 'data': [], 'message': "Not a valid Email"}
        except KeyError:
            print()

    def reset_pass(self):
        from urllib.parse import urlparse, parse_qs
        query_comp = parse_qs(urlparse(self.path).query)
        token = query_comp["token"][0]
        token = jwt.decode(token, "secret", algorithm='HS256')
        try:
            # processing user input submitted in Front end(HTML)
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            data = {'email': token['email'], 'password': form['password'].value}
            obj = Utility()
            u = User()
            if obj.email_validate(data['email']):
                response = u.set_password(data)
                return response
            else:
                return {'success': True, 'data': [], 'message': "Not a valid Email"}
        except KeyError:
            print()

    def create_note(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            user_id = payload['id']
            data = {'Title': form['Title'].value, 'Description': form['Description'].value,
                    'Colour': form['Colour'].value,
                    'isPinned': form['isPinned'].value, 'isArchive': form['isArchive'].value,
                    'isTrash': form['isTrash'].value, 'user_id': str(user_id)}
            n = Note()
            response = n.create_note(data)
            return response
        except KeyError:
            print()

    def update_note(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            user_id = str(payload['id'])
            data = {'Title': form['Title'].value, 'Description': form['Description'].value,
                    'Colour': form['Colour'].value, 'isPinned': form['isPinned'].value,
                    'isArchive': form['isArchive'].value, 'isTrash': form['isTrash'].value, 'user_id': user_id}
            n = Note()
            response = n.update_note(data)
            return response
        except KeyError:
            print()

    def delete_note(self):
        try:
            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            user_id = payload['id']
            data = {'user_id': str(user_id)}
            n = Note()
            response = n.delete_note(data)
            return response
        except KeyError:
            print()

    def read_note(self):
        try:
            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            user_id = payload['id']
            data = {'user_id': str(user_id)}
            n = Note()
            response = n.read_note(data)
            return response
        except KeyError:
            print()

    def create_profile(self):
        try:
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                form = cgi.FieldStorage(fp=self.rfile,
                                        headers=self.headers,
                                        environ={'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': self.headers['Content-Type'],
                                                 })
                filename = form['upfile'].filename
                data = form['upfile'].file.read()
                open("./media/%s" % filename, "wb").write(data)
                token = self.headers['token']
                payload = jwt.decode(token, "secret", algorithms='HS256')
                user_id = str(payload['id'])
                profile_data = {
                    'profile_path': f'./media/{filename}',
                    'user_id': user_id
                }
                u = User()
                response = u.create_pic(profile_data)
                return response
        except KeyError:
            print()

    def update_profile(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            user_id = str(payload['id'])
            data = {'profile_path': form['profile_path'].value, 'user_id': user_id}
            u = User()
            response = u.update_pic(data)
            return response
        except KeyError:
            print()

    def read_profile(self):
        try:
            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            user_id = str(payload['id'])
            data = {'user_id': user_id}
            u = User()
            response = u.read_pic(data)
            return response
        except KeyError:
            print()

    def delete_profile(self):
        try:
            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            user_id = str(payload['id'])
            data = {'user_id': user_id}
            u = User()
            response = u.delete_pic(data)
            return response
        except KeyError:
            print()

    def openfile(self):
        if self.path == '/register':
            with open('template/registration.html', 'r') as f:
                html_string_register = f.read()
            self.wfile.write(self._html(html_string_register))
        elif self.path == '/login':
            with open('template/login.html', 'r') as f:
                html_string_login = f.read()
                self.wfile.write(self._html(html_string_login))
        elif self.path == '/forget':
            with open('template/forget_password.html', 'r') as f:
                html_string_forget_password = f.read()
                self.wfile.write(self._html(html_string_forget_password))
        elif 'new' in self.path:
            from urllib.parse import urlparse, parse_qs
            query_comp = parse_qs(urlparse(self.path).query)
            token = query_comp["new"][0]
            with open('template/reset.html', 'r') as f:
                html_string_reset = f.read()
                output = html_string_reset.format(result=token)
                self.wfile.write(self._html(output))
        else:
            with open('template/error.html', 'r') as f:
                html_string_error = f.read()
                self.wfile.write(self._html(html_string_error))
