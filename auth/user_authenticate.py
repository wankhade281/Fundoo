import jwt
from configuration.redis_connection import RedisService
from view.response import Response


def response(success=False, message='something went wrong', data=[]):
    response = {'success': success,
                "message": message,
                "data": data, }
    return response


def is_authenticated(method):
    def authenticate_user(self):
        """this function is used to decode and check whether the user is authorized user or not:param catch:
        True:return:"""
        try:
            if self.path in ['/api/note','/profile/create','/profile/delete','/profile/update','/profile/read']:
                token = self.headers['token']
                payload = jwt.decode(token, "secret", algorithms='HS256')
                id = payload['id']
                redis_obj = RedisService()
                token = redis_obj.get(id)
                if token is None:
                    raise ValueError("You Need To Login First")
                return method(self)
            elif self.path in ['/login','/register','/forget','/login/forget']:
                return method(self)
            elif 'new' in self.path:
                return method(self)
        except jwt.ExpiredSignatureError:
            res = response(message="Signature expired. Please log in again.")
            Response(self).jsonResponse(status=404, data=res)
        except jwt.DecodeError:
            res = response(message="DecodeError")
            Response(self).jsonResponse(status=404, data=res)
        except jwt.InvalidTokenError:
            res = response(message="InvalidTokenError")
            Response(self).jsonResponse(status=404, data=res)
    return authenticate_user
