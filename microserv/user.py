import sys
sys.path.insert(0, '/home/admin1/Demo1/PycharmProjects/fundoo')
from microserv.models import Data
import jwt
from nameko.rpc import rpc, RpcProxy
from microserv.config import SMTP


class User(object):
    name = "data_service"

    log_service = RpcProxy('log_service')

    # @rpc
    # def user_login(self, data):
    #     print(data)
    #     return self.log_service.login_details(data)

    @rpc
    def user_login(self, data):
        db_obj = Data()
        encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
        if db_obj.email_validate(data['email']):
            result = db_obj.user_exist(encoded_jwt)
            if result:
                response = {'success': False, 'data': [], 'message': "Not a Register User"}
                return response
            else:
                response = {'success': True, 'data': [], 'message': "Login Successful"}
                return response
        else:
            response = {'success': False, 'data': [], 'message': "Email not in valid format"}
            return response
            # return self.log_service.login_details(data)

    @rpc
    def user_register(self, data):
        db_obj = Data()
        result_passwd = db_obj.password_validate(data)
        result_email = db_obj.email_validate(data['email'])
        if result_email and result_passwd:
            result = db_obj.email_exist(data)
            if result:
                db_obj.registration(data)
                response = {'success': True, 'data': [], 'message': "Successfully Registered"}
                return response
            else:
                response = {'success': False, 'data': [], 'message': "Email already exist"}
                return response
        else:
            response = {'success': False, 'data': [], 'message': "not a valid email or password and cnf "
                                                                 "password not match"}
            return response
        # return self.log_service.login_details(data)

    @rpc
    def forget_password(self, data):
        db_obj = Data()
        if db_obj.email_exist(data):
            response = {'success': False, 'data': [], 'message': "Not a Register User"}
            return response
        else:
            s = SMTP()
            s.start()  # start TLS for security
            s.login()  # Authentication and login
            s.send_mail(data['email'])  # sending the mail
            response = {'success': False, 'data': [], 'message': "Message sent Successfully"}
            return response
