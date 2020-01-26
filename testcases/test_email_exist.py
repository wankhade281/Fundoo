import jwt

from microservices.models import Data


def test_user_exist():
    d = Data()
    data = {'email': 'chetanwankhade281@gmail.com', 'password': 'chetan123'}
    encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
    assert d.user_exist(encoded_jwt) == True
