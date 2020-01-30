import PIL
from PIL.Image import Image
import jwt
from config.db_connection import Connection
from config.redis_connection import RedisService
from vendor.smtp import SMTP
from models.db_query import Query


class User:
    """Summary:- This class is used processing user input submitted in Front end(HTML)
     and store into database for registration, login and forgot password"""

    def __init__(self):
        self.mydb = Connection()

    def user_registration(self, data):
        # processing user input submitted in Front end(HTML)
        db_obj = Query()
        result = db_obj.email_exist(data)
        if result:
            q = Query()
            q.insert_query(data, table_name='users')
            return {'success': True, 'data': [], 'message': "Successfully Registered"}
        else:
            return {'success': False, 'data': [], 'message': "Email already exist"}

    def user_login(self, data):
        # processing user input submitted in Front end(HTML)
        db_obj = Query()
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

    def set_password(self, data):
        # processing user input submitted in Front end(HTML)
        q = Query()   # TODO only one object
        q.reset_password(data)
        return {'success': True, 'data': [], 'message': "Password Reset Successfully"}

    def create_pic(self, data):
        table_name = 'profile'
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            q = Query()
            q.insert_query(data=data, table_name=table_name)
            return {'success': True, 'data': [], 'message': "Pic saved Successfully"}
        else:
            return {'success': False, 'data': [], 'message': "Profile already Exist"}

    def update_pic(self, data, condition):
        db_obj = Query()
        result = db_obj.profile_exist(condition)
        if result:
            return {'success': False, 'data': [], 'message': "Profile Not Exist"}
        else:
            q = Query()
            q.update_que(data, table_name='profile', condition=condition)
            return {'success': True, 'data': [], 'message': "Profile Update Successfully"}

    def read_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            q = Query()
            val = q.read_picture(data)
            print("Image Path ---->",val[0][1])
            path = val[0][1]
            path = path[1:]
            PIL.Image.open("/home/admin1/Demo1/PycharmProjects/fundoo"+path).show()
            return {'success': True, 'data': [], 'message': "Data Read Successfully"}
        else:
            return {'success': True, 'data': [], 'message': "Data not Available"}

    def delete_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            return {'success': False, 'data': [], 'message': "Profile Not Exist"}
        else:
            q = Query()
            q.delete_picture(data)
            return {'success': True, 'data': [], 'message': "Profile Delete Successfully"}
