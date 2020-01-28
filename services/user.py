import jwt
from configuration.config import Connection
from configuration.redis_connection import RedisService
from vendor.smtp import SMTP
from view.query import Query


class User:
    """Summary:- This class is used processing user input submitted in Front end(HTML)
     and store into database for registration, login and forgot password"""

    def __init__(self):
        self.mydb = Connection()

    def user_registration(self, data):
        # processing user input submitted in Front end(HTML)
        obj = Query()
        result_passwd = obj.password_validate(data)
        result_email = obj.email_validate(data['email'])
        if result_email and result_passwd:
            result = obj.email_exist(data)
            if result:
                query = "INSERT INTO users(email,password) VALUES ('" + data['email'] + "','" + data[
                    'password'] + "') "
                self.mydb.query_execute(query)
                return {'success': True, 'data': [], 'message': "Successfully Registered"}
            else:
                return {'success': False, 'data': [], 'message': "Email already exist"}
        else:
            return {'success': False, 'data': [], 'message': "not a valid email or password and cnf "
                                                             "password not match"}

    def login(self, data):
        # processing user input submitted in Front end(HTML)
        db_obj = Query()
        if db_obj.email_validate(data['email']):
            result = db_obj.user_exist(data)
            if result:
                redis_obj = RedisService()
                payload = {
                    # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=120),
                    # 'iat': datetime.datetime.utcnow(),
                    'id': result,
                    'email': data['email']
                }
                encoded_jwt = jwt.encode(payload, 'secret', algorithm='HS256').decode("UTF-8")
                redis_obj.set(result, data['email'])
                return {'success': True, 'data': [], 'token': encoded_jwt}
            else:
                return {'success': False, 'data': [], 'message': "Not a Registered User"}
        else:
            return {'success': False, 'data': [], 'message': "Email not in valid format"}

    def forget_password(self, data, version, host):
        # processing user input submitted in Front end(HTML)
        db_obj = Query()
        if db_obj.email_exist(data):
            return {'success': False, 'data': [], 'message': "Not a Register User"}
        else:
            email = data['email']
            s = SMTP()
            encoded_jwt = jwt.encode({'email': email}, 'secret', algorithm='HS256').decode("UTF-8")
            data = f"{version}://{host}/forget/?new={encoded_jwt}"
            s.send_mail(data, email)
            return {'success': True, 'data': [], 'message': "Message sent Successfully"}

    def set_password(self, email_id, data):
        # processing user input submitted in Front end(HTML)
        query = " UPDATE users SET password = '" + data['password'] + "'WHERE  email = '" + email_id + "' "
        self.mydb.query_execute(query)
        return {'success': True, 'data': [], 'message': "Password Reset Successfully"}
