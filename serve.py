import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from view.profile import Profile, ListingPages
from view.registration import FormDetails
from view.route import openfile, store_data


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
        openfile(self)

    def do_PUT(self):
        FormDetails.update(self)
        Profile.update_pic(self)
        ListingPages.isTrash(self)

    def do_DELETE(self):
        FormDetails.delete(self)
        Profile.delete_pic(self)

    def do_POST(self):
        # do database operations with posted data
       store_data(self)


server = HTTPServer((os.getenv("SERVER_HOST_IP_ADDRESS"), int(os.getenv('SERVER_HOST_PORT'))), Server)
print(f"httpd server on {os.getenv('SERVER_HOST_IP_ADDRESS')}:{int(os.getenv('SERVER_HOST_PORT'))}")
server.serve_forever()