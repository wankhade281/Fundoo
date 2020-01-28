from configuration.config import Connection
from configuration.redis_connection import RedisService


class Note:
    def __init__(self):  # This function is used to form a connection with database
        self.mydbobj = Connection()
        self.r = RedisService()

    def create_note(self, data):
        if self.r.get(data['user_id']):
            form_keys = list(data.keys())
            if len(form_keys) == 7:
                query = "INSERT INTO notes (Title, Description, Colour, isPinned, isArchive, isTrash, user_id) VALUES "\
                        "('" + data['Title'] + "', '" + data['Description'] + "', '" + data['Colour'] + "', '" + data[
                            'isPinned'] + "', '" + data['isArchive'] + "', '" + data['isTrash'] + "', '"+data['user_id']+"')"
                self.mydbobj.query_execute(query)
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
                query = "UPDATE notes SET Title = '" + data['Title'] + "',Description = '" + data[
                    'Description'] + "',Colour = '" + data['Colour'] + "',isPinned = '" + data[
                            'isPinned'] + "', isArchive = '" + data['isArchive'] + "', isTrash = '" + data[
                            'isTrash'] + "' WHERE  user_id = " + data['user_id'] + ""
                self.mydbobj.query_execute(query)
                return {'success': True, 'data': [], 'message': "Data Update Successfully"}
            else:
                return {'success': False, 'data': [], 'message': "some values are missing"}
        else:
            return {'success': False, 'data': [], 'message': "Not a valid user"}

    def read_note(self, data):
        if self.r.get(data['user_id']):
            form_keys = list(data.keys())
            if len(form_keys) == 1:
                query = "SELECT * FROM notes WHERE user_id = '" + data['user_id'] + "'"
                entry = self.mydbobj.run_query(query)
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
                query = "DELETE FROM notes WHERE user_id = " + data['user_id'] + ""
                self.mydbobj.query_execute(query)
                print("Entry delete Successfully")
                return {'success': True, 'data': [], 'message': "Data Delete Successfully"}
            else:
                return {'success': False, 'data': [], 'message': "some values are missing"}
        else:
            return {'success': False, 'data': [], 'message': "Not a valid user"}
