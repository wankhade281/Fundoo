import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from view.profile import Profile, ListingPages
from view.route import openfile, store_data
from model.query import Data


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
            Data.read(self)
        elif self.path == '/profile/read':
            Profile.read_pic(self)
        else:
            openfile(self)

    def do_PUT(self):
        ListingPages.isTrash(self)
        if self.path == '/api/note':
            Data.update(self)
        elif self.path == '/profile/update':
            Profile.update_pic(self)

    def do_DELETE(self):
        if self.path == '/api/note':
            Data.delete(self)
        elif self.path == '/profile/delete':
            Profile.delete_pic(self)

    def do_POST(self):  # do database operations with posted data
        if self.path == "/api/note":
            Data.create(self)
        elif self.path == '/profile/create':
            Profile.create_pic(self)
        else:
            store_data(self)


server = HTTPServer((os.getenv("SERVER_HOST_IP_ADDRESS"), int(os.getenv('SERVER_HOST_PORT'))), Server)
print(f"httpd server start on {os.getenv('SERVER_HOST_IP_ADDRESS')}:{int(os.getenv('SERVER_HOST_PORT'))}")
server.serve_forever()
