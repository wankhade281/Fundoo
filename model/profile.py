from configuration.config import Connection
from view.query import Query
from view.response import Response


class Profile:
    def __init__(self):
        self.mydb = Connection()

    def create_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            query = "INSERT INTO profile(Image) VALUES('" + data['profile'] + "')"
            self.mydb.query_execute(query)
            return {'success': True, 'data': [], 'message': "Pic saved Successfully"}
        else:
            return {'success': False, 'data': [], 'message': "Profile already Exist"}

    def read_pic(self, data):
        query = "SELECT * FROM profile WHERE id = '" + data['id'] + "'"
        result = self.mydb.run_query(query)
        for x in result:
            print(x)
        return {'success': True, 'data': [], 'message': "Data Read Successfully"}

    def update_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            return {'success': False, 'data': [], 'message': "Profile Not Exist"}
        else:
            query = "UPDATE profile SET Image = '" + data['profile'] + "' WHERE  id = '" + data['id'] + "'"
            self.mydb.query_execute(query)
            return {'success': True, 'data': [], 'message': "Profile Update Successfully"}

    def delete_pic(self, data):
        db_obj = Query()
        result = db_obj.profile_exist(data)
        if result:
            return {'success': False, 'data': [], 'message': "Profile Not Exist"}
        else:
            query = "DELETE FROM profile WHERE Image = '" + data['profile'] + "'"
            self.mydb.query_execute(query)
            return {'success': True, 'data': [], 'message': "Profile Delete Successfully"}


class ListingPages:
    def __init__(self):
        self.mydb = Connection()

    def isArchieve(self):
        query = "SELECT * FROM note WHERE " 'isArchive' "=1 "
        result = self.mydb.run_query(query)
        for x in result:
            print(x)
        return {'success': True, 'data': [], 'message': "Data Read Successfully"}

    def isPinned(self):
        query = "SELECT * FROM note WHERE " 'isPinned' "=1 "
        result = self.mydb.run_query(query)
        for x in result:
            print(x)
        return {'success': True, 'data': [], 'message': "Data Read Successfully"}

    def isTrash(self):
        if self.path == '/istrash':
            responce_data = {'success': True, 'data': [], 'message': ""}
            query = "SELECT * FROM note WHERE " 'isTrash' "=1"
            result = self.mydb.run_query(query)
            for x in result:
                print(x)
            responce_data.update({'success': True, 'data': [], 'message': "Data Read Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)