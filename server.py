import os
from http.server import HTTPServer
from routes import Routes

server = HTTPServer((os.getenv("SERVER_HOST_IP_ADDRESS"), int(os.getenv('SERVER_HOST_PORT'))), Routes)
print(f"httpd server start on {os.getenv('SERVER_HOST_IP_ADDRESS')}:{int(os.getenv('SERVER_HOST_PORT'))}")
server.serve_forever()
