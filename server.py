import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from auth.user_authenticate import is_authenticated
from view.routes import UserData


class Server(BaseHTTPRequestHandler):  # This class is used to perform operations related to http request
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = message
        return content.encode("utf8")

    @is_authenticated
    def do_GET(self):
        if self.path == '/api/note':
            UserData.read_note(self)
        elif self.path == '/profile/read':
            UserData.read_profile(self)
        else:
            self._set_headers()
            UserData.openfile(self)

    @is_authenticated
    def do_PUT(self):
        if self.path == '/api/note':
            UserData.update_note(self)
        elif self.path == '/profile/update':
            UserData.update_profile(self)
        elif self.path == '/istrash':
            UserData.store_data(self)

    @is_authenticated
    def do_DELETE(self):
        if self.path == '/api/note':
            UserData.delete_note(self)
        elif self.path == '/profile/delete':
            UserData.delete_profile(self)

    @is_authenticated
    def do_POST(self):  # do database operations with posted data
        if self.path == "/api/note":
            UserData.create_note(self)
        elif self.path == '/profile/create':
            UserData.create_profile(self)
        else:
            data = self.protocol_version
            UserData.store_data(self, data)


server = HTTPServer((os.getenv("SERVER_HOST_IP_ADDRESS"), int(os.getenv('SERVER_HOST_PORT'))), Server)
print(f"httpd server start on {os.getenv('SERVER_HOST_IP_ADDRESS')}:{int(os.getenv('SERVER_HOST_PORT'))}")
server.serve_forever()
