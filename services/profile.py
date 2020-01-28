import PIL
from PIL.Image import Image
from configuration.config import Connection
from view.query import Query


class Profile:
    def __init__(self):
        self.mydb = Connection()

    def create_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            query = "INSERT INTO profile(profile_path, user_id)VALUES('" + data['profile_path'] + "','" + data[
                'user_id'] + "')"
            self.mydb.query_execute(query)
            return {'success': True, 'data': [], 'message': "Pic saved Successfully"}
        else:
            return {'success': False, 'data': [], 'message': "Profile already Exist"}

    def read_pic(self, data):
        query = "SELECT * FROM profile WHERE user_id = '" + data['user_id'] + "'"
        result = self.mydb.run_query(query)
        if result:
            print("Image Path ---->",result[0][1])
            path = result[0][1]
            path = path[1:]
            PIL.Image.open("/home/admin1/Demo1/PycharmProjects/fundoo"+path).show()
            return {'success': True, 'data': [], 'message': "Data Read Successfully"}
        else:
            return {'success': True, 'data': [], 'message': "Data not Available"}

    def update_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            return {'success': False, 'data': [], 'message': "Profile Not Exist"}
        else:
            query = "UPDATE profile SET profile_path='" + data['profile_path'] + "'WHERE  user_id = '" + data[
                'user_id'] + "'"
            self.mydb.query_execute(query)
            return {'success': True, 'data': [], 'message': "Profile Update Successfully"}

    def delete_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            return {'success': False, 'data': [], 'message': "Profile Not Exist"}
        else:
            query = "DELETE FROM profile WHERE user_id = '" + data['user_id'] + "'"
            self.mydb.query_execute(query)
            return {'success': True, 'data': [], 'message': "Profile Delete Successfully"}


class ListingPages:
    def __init__(self):
        self.mydb = Connection()

    def isArchieve(self):
        query = "SELECT * FROM notes WHERE " 'isArchive' "=1 "
        result = self.mydb.run_query(query)
        for x in result:
            print(x)
        return {'success': True, 'data': [], 'message': "Data Read Successfully"}

    def isPinned(self):
        query = "SELECT * FROM notes WHERE " 'isPinned' "=1 "
        result = self.mydb.run_query(query)
        for x in result:
            print(x)
        return {'success': True, 'data': [], 'message': "Data Read Successfully"}

    def isTrash(self):
        if self.path == '/istrash':
            responce_data = {'success': True, 'data': [], 'message': ""}
            query = "SELECT * FROM notes WHERE " 'isTrash' "=1"
            result = self.mydb.run_query(query)
            for x in result:
                print(x)
            return {'success': True, 'data': [], 'message': "Data Read Successfully"}
