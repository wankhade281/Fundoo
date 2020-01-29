from models.db_query import Query
from view.userservice import User
q = Query()
u = User()

def test_register():
    data = {
        "email": "chetanwank281@gmail.com",
        "password": "12345",
        "confirm_password": '12345'
    }
    assert u.user_registration(data) == {'success': False, 'data': [], 'message': "Email already exist"}


def test_email_exist():
    data = {
        "email": "chetanwank281@gmail.com",
    }
    assert q.email_exist(data) == False


def test_user_exist():
    data = {
        "email": "chetk281@gmail.com",
        "password": "12345"
    }
    assert q.user_exist(data) == False


def test_email_validate():
    email = "chetanwankhade281@gmail.com"
    assert q.email_validate(email) == True


def test_password_validate():
    data = {
        "password": "12345",
        "confirm_password": '12345'
    }
    assert q.password_validate(data) == True

def test_user_registration():
    data = {
        "email": "chetanwafaafnk281@gmail.com",
        "password": "12345"
    }
    assert u.user_login(data) == {'success': False, 'data': [], 'message': "Not a Registered User"}

# def test_forget_password():
#     data = {
#         "email": "chetanwank281@gmail.com"
#     }
#     version = 'HTTP'
#     host = 'localhost'
#     assert u.forget_password(data, version, host) == {'success': True, 'data': [], 'message': "Message sent Successfully"}