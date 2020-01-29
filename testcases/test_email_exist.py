import jwt

from models.db_query import Query

q = Query()


def test_user_exist():
    data = {'email': 'chetanwankhade281@gmail.com', 'password': 'chetan123'}
    encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
    assert q.user_exist(encoded_jwt) == True
