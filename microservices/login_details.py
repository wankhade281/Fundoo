from nameko.rpc import rpc


class login(object):
    name = 'login_service'

    @rpc
    def log(self):
        username = self.args.get('username', '')
        print(username)
        pwd = self.args.get('pwd', '')
        print(pwd)
        print("inside login operation")
        return "login successful"
