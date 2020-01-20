from microservices.user import User


def test_login():
    u = User()
    data = {
        "email": "chetanwank@gmail.com",
        "password": "12345"
    }
    assert u.user_login(data) == {'success': True, 'data': [], 'message': "Login Successful"}


def test_register():
    u = User()
    data = {
        "email": "chetanwank281@gmail.com",
        "password": "12345",
        "confirm_password": '12345'
    }
    assert u.user_register(data) == {'success': False, 'data': [], 'message': "Email already exist"}


def test_forget_password():
    u = User()
    data = {
        "email": "chetanwank281@gmail.com",
    }
    assert u.forget_password(data) == {'success': False, 'data': [], 'message': "Message sent Successfully"}
