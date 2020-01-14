"""
    service_1
    ~~~~~~~~~
    Example of http GET extension
"""
import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http

# from login_details import login


class HttpService(object):
    name = "user_services"

    login_service = RpcProxy('login_service')

    @http('GET', '/register/<username>')
    def get_method(self, request, username):
        print(username)
        third = u"received request for register: {}".format(request.get_data(as_text=True))
        return json.dumps({'value': third})

    @http('GET', '/login')
    def get_method(self, request):
        print(request)
        return self.login_service

