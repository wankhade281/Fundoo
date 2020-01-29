from config.db_connection import Connection
from config.redis_connection import RedisService
from models.db_query import Query


class Note:
    def __init__(self):  # This function is used to form a connection with database
        self.mydbobj = Connection()
        self.r = RedisService()

    def create_note(self, data):
        if self.r.get(data['user_id']):
            form_keys = list(data.keys())
            if len(form_keys) == 7:
                q = Query()
                q.insert_query(data=data, table_name='notes')
                print("Entry Created Successfully")
                return {'success': True, 'data': [], 'message': "Entry Create Successfully"}
            else:
                return {'success': False, 'data': [], 'message': "some values are missing"}
        else:
            return {'success': False, 'data': [], 'message': "not a valid user"}

    def update_note(self, data):
        if self.r.get(data['user_id']):
            form_keys = list(data.keys())
            if len(form_keys) == 7:
                q = Query()
                q.update_query()
                return {'success': True, 'data': [], 'message': "Data Update Successfully"}
            else:
                return {'success': False, 'data': [], 'message': "some values are missing"}
        else:
            return {'success': False, 'data': [], 'message': "Not a valid user"}

    def read_note(self, data):
        if self.r.get(data['user_id']):
            form_keys = list(data.keys())
            if len(form_keys) == 1:
                q = Query()
                entry = q.update_query()
                if len(entry):
                    return {'success': True, 'data': [], 'message': "Data read Successfully"}
                else:
                    return {'success': False, 'data': [], 'message': "Data is not available for user"}
            else:
                return {'success': False, 'data': [], 'message': "some values are missing"}
        else:
            return {'success': False, 'data': [], 'message': "Not a valid user"}

    def delete_note(self, data):
        if self.r.get(data['user_id']):
            form_keys = list(data.keys())
            if len(form_keys) == 1:
                q = Query()
                q.delete_query(data)
                print("Entry delete Successfully")
                return {'success': True, 'data': [], 'message': "Data Delete Successfully"}
            else:
                return {'success': False, 'data': [], 'message': "some values are missing"}
        else:
            return {'success': False, 'data': [], 'message': "Not a valid user"}

    def isArchieve(self):
        query = "SELECT * FROM notes WHERE " 'isArchive' "=1 "
        result = self.mydbobj.run_query(query)
        for x in result:
            print(x)
        return {'success': True, 'data': [], 'message': "Data Read Successfully"}

    def isPinned(self):
        query = "SELECT * FROM notes WHERE " 'isPinned' "=1 "
        result = self.mydbobj.run_query(query)
        for x in result:
            print(x)
        return {'success': True, 'data': [], 'message': "Data Read Successfully"}

    def isTrash(self):
        if self.path == '/istrash':
            query = "SELECT * FROM notes WHERE " 'isTrash' "=1"
            result = self.mydbobj.run_query(query)
            for x in result:
                print(x)
            return {'success': True, 'data': [], 'message': "Data Read Successfully"}
