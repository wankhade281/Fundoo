import jwt

from view.query import Query
from view.registration import User


def test_register():
    f = User()
    data = {
        "email": "chetanwank281@gmail.com",
        "password": "12345",
        "confirm_password": '12345'
    }
    assert f.register(data) == {'success': False, 'data': [], 'message': "Email already exist"}


def test_email_exist():
    d = Query()
    data = {
        "email": "chetanwank281@gmail.com",
    }
    assert d.email_exist(data) == False


def test_user_exist():
    d = Query()
    data = {
        "email": "chetanwank281@gmail.com",
        "password": "12345"
    }
    encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
    assert d.user_exist(encoded_jwt) == False


def test_email_validate():
    d = Query()
    email = "chetanwankhade281@gmail.com"
    assert d.email_validate(email) == True


def test_password_validate():
    d = Query()
    data = {
        "password": "12345",
        "confirm_password": '12345'
    }
    assert d.password_validate(data) == True
