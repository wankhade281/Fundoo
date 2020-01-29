from http.server import BaseHTTPRequestHandler
from auth.login_authenticate import is_authenticated
from services.notes import Note
from view.response import Response
from view.userservice import UserData


class Routes(BaseHTTPRequestHandler):  # This class is used to perform operations related to http request
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = message
        return content.encode("utf8")

    @is_authenticated
    def do_GET(self):
        n = Note()
        if self.path == '/api/note':
            response = UserData.read_note(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/profile/read':
            response = UserData.read_profile(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/ispinned':
            response = n.isPinned(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/istrash':
            response = n.isTrash(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/isarchive':
            response = n.isArchieve(self)
            Response(self).jsonResponse(status=200, data=response)
        else:
            self._set_headers()
            UserData.openfile(self)

    @is_authenticated
    def do_PUT(self):
        if self.path == '/api/note':
            response = UserData.update_note(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/profile/update':
            response = UserData.update_profile(self)
            Response(self).jsonResponse(status=200, data=response)

    @is_authenticated
    def do_DELETE(self):
        if self.path == '/api/note':
            response = UserData.delete_note(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/profile/delete':
            response = UserData.delete_profile(self)
            Response(self).jsonResponse(status=200, data=response)

    @is_authenticated
    def do_POST(self):  # do database operations with posted data
        if self.path == "/api/note":
            response = UserData.create_note(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/profile/create':
            response = UserData.create_profile(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == "/register":
            response = UserData.user_register(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == "/login":
            response = UserData.user_login(self)
            Response(self).jsonResponse(status=200, data=response)
        elif self.path == '/login/forget':
            data = self.protocol_version
            response = UserData.forget_pass(self, data)
            Response(self).jsonResponse(status=200, data=response)
        elif 'new' in self.path:
            response = UserData.reset_pass(self)
            Response(self).jsonResponse(status=200, data=response)