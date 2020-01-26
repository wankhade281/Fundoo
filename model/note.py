from configuration.config import Connection


class Note:
    def __init__(self):  # This function is used to form a connection with database
        self.mydbobj = Connection()

    def create_note(self, data):
        form_keys = list(data.keys())
        if len(form_keys) == 6:
            query = "INSERT INTO note (Title, Description, Colour, isPinned, isArchive, isTrash) VALUES ('" + \
                    data[
                        'Title'] + "', '" + data['Description'] + "', '" + data['Colour'] + "', '" + data[
                        'isPinned'] + "', '" + data[
                        'isArchive'] + "', '" + data['isTrash'] + "')"
            self.mydbobj.query_execute(query)
            print("Entry Created Successfully")
            return {'success': True, 'data': [], 'message': "Entry Create Successfully"}
        else:
            return {'success': False, 'data': [], 'message': "some values are missing"}

    def update_note(self, data):
        form_keys = list(data.keys())
        if len(form_keys) == 7:
            query = "UPDATE note SET Title = '" + data['Title'] + "',Description = '" + data[
                'Description'] + "',Colour = '" + data['Colour'] + "',isPinned = '" + data[
                        'isPinned'] + "', isArchive = '" + data['isArchive'] + "', isTrash = '" + data[
                        'isTrash'] + "' WHERE  id = " + data['id'] + ""
            self.mydbobj.query_execute(query)
            print("Data update Successfully")
            return {'success': True, 'data': [], 'message': "Data Update Successfully"}
        else:
            return {'success': False, 'data': [], 'message': "some values are missing"}

    def read_note(self, data):
        form_keys = list(data.keys())
        if len(form_keys) == 1:
            query = "SELECT * FROM note WHERE id = '" + data['id'] + "'"
            entry = self.mydbobj.run_query(query)
            print(entry)
            return {'success': True, 'data': [], 'message': "Data read Successfully"}
        else:
            return {'success': False, 'data': [], 'message': "some values are missing"}

    def delete_note(self, data):
        form_keys = list(data.keys())
        if len(form_keys) == 1:
            query = "DELETE FROM note WHERE id = " + data['id'] + ""
            self.mydbobj.query_execute(query)
            print("Entry delete Successfully")
            return {'success': True, 'data': [], 'message': "Data Delete Successfully"}
        else:
            return {'success': False, 'data': [], 'message': "some values are missing"}
