import jwt
from view.query import Query
from view.routes import User
q = Query()


def test_register():
    f = User()
    data = {
        "email": "chetanwank281@gmail.com",
        "password": "12345",
        "confirm_password": '12345'
    }
    assert f.user_registration(data) == {'success': False, 'data': [], 'message': "Email already exist"}


def test_email_exist():
    data = {
        "email": "chetanwank281@gmail.com",
    }
    assert q.email_exist(data) == False


def test_user_exist():
    data = {
        "email": "chetanwank281@gmail.com",
        "password": "12345"
    }
    encoded_jwt = jwt.encode({'some': data}, 'secret', algorithm='HS256').decode("UTF-8")
    assert q.user_exist(encoded_jwt) == False


def test_email_validate():
    email = "chetanwankhade281@gmail.com"
    assert q.email_validate(email) == True


def test_password_validate():
    data = {
        "password": "12345",
        "confirm_password": '12345'
    }
    assert q.password_validate(data) == True
