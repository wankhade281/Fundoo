import json


class Response:

    def __init__(self, that):
        self.Response = that

    def jsonResponse(self, status, data):
        print(self.Response, '-------->')
        self.Response.send_response(status)
        self.Response.send_header('Content-type', 'text/json')
        self.Response.end_headers()
        self.Response.wfile.write(json.dumps(data).encode())

    def html_response(self, status, data):
        self.Response.send_response(status)
        self.Response.send_header('Content-type', 'text/html')
        self.Response.end_headers()
        self.Response.wfile.write(data.encode("utf8"))

    def HTTPHandler400(self):
        pass

    def HTTPHandler500(self):
        pass