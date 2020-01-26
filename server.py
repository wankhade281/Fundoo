import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from view.utils import is_authenticated
from view.registration import Formdata


class Server(BaseHTTPRequestHandler):  # This class is used to perform operations related to http request
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = message
        return content.encode("utf8")

    def do_GET(self):
        self._set_headers()
        if self.path == '/api/note':
            Formdata.read_note(self)
        elif self.path == '/profile/read':
            Formdata.read_profile(self)
        else:
            Formdata.openfile(self)

    def do_PUT(self):
        if self.path == '/api/note':
            Formdata.update_note(self)
        elif self.path == '/profile/update':
            Formdata.update_profile(self)
        elif self.path == '/istrash':
            Formdata.store_data(self)

    def do_DELETE(self):
        if self.path == '/api/note':
            Formdata.delete_note(self)
        elif self.path == '/profile/delete':
            Formdata.delete_profile(self)

    @is_authenticated
    def do_POST(self):  # do database operations with posted data
        if self.path == "/api/note":
            Formdata.create_note(self)
        elif self.path == '/profile/create':
            Formdata.create_profile(self)
        else:
            Formdata.store_data(self)


server = HTTPServer((os.getenv("SERVER_HOST_IP_ADDRESS"), int(os.getenv('SERVER_HOST_PORT'))), Server)
print(f"httpd server start on {os.getenv('SERVER_HOST_IP_ADDRESS')}:{int(os.getenv('SERVER_HOST_PORT'))}")
server.serve_forever()
