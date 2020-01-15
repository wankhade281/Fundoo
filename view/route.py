import jwt

from view.profile import ListingPages
from view.registration import FormDetails
from view.response import Response


def openfile(self):
    l = ListingPages
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
    elif self.path == '/isarchive':
        l.isArchieve(self)
    else:
        with open('template/error.html', 'r') as f:
            html_string_error = f.read()
            self.wfile.write(self._html(html_string_error))


def store_data(self):
    l = ListingPages
    obj = FormDetails
    if self.path == "/register":
        obj.register(self)
    elif self.path == "/login":
        obj.login(self)
    elif self.path == '/login/forget':
        obj.forget_password(self)
    elif self.path == '/ispinned':
        l.isPinned(self)
    elif 'new' in self.path:
        from urllib.parse import urlparse, parse_qs
        query_comp = parse_qs(urlparse(self.path).query)
        token = query_comp["token"][0]
        token = jwt.decode(token, "secret", algorithm='HS256')
        obj.set_password(self, token['email'])
    else:
        responce_data = {'success': False, 'data': [], 'message': "Invalid URL"}
        Response(self).jsonResponse(status=404, data=responce_data)
