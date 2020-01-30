from config.db_connection import Connection


class Query:
    """Summary:- This class is used to form connection with the database and perform operation check
    entry into the database
    """
    def __init__(self):  # This function is used to form a connection with database
        self.mydb = Connection()

    def user_exist(self, data):
        # This function is used to check valid user  using sql query for login according return true or false value
        query = "SELECT * from users where email = '" + data['email'] + "' and password = '" + data['password'] + "'"
        result = self.mydb.run_query(query)
        if result:
            user_id = result[0][0]
            return user_id
        else:
            return False

    def email_exist(self, data):  # This function is used to check email already exist in database using sql query
        query = "SELECT email from users where email = '" + data['email'] + "'"
        result = self.mydb.run_query(query)
        if len(result):
            return False
        else:
            return True

    def profile_exist(self, data):
        # This function is used to check user is exist or not and return a true and false value
        query = "SELECT * from profile where user_id='" + data['user_id'] + "'"
        result = self.mydb.run_query(query)
        if len(result):
            return False
        else:
            return True

    def insert_query(self, data, table_name=None):
        column = []
        rows_values = []
        val = []
        for key, value in data.items():
            column.append(key)
            rows_values.append("%s")
            val.append(value)
        print(column)
        print(rows_values)
        print(val)
        column = ', '.join(column)
        val_ = ', '.join(['%s'] * len(val))
        query ='''INSERT INTO %s (%s) VALUES (%s)''' % (table_name, column, val_)
        print(query)
        self.mydb.query_execute(query=query,value=val)

    def read_que(self, data, table_name=None):
        terms = ' AND '.join(f'{key} = %s' for key in data)
        query = 'SELECT * FROM %s '%table_name + terms
        args = (data.values())
        print(terms,"-->>terms")
        print(query,"-->>query")
        print(args,"-->>args")
        column = []
        rows_values = []
        val = []
        for key1, value in data.items():
            column.append(key1)
            rows_values.append("%s")
            val.append(value)
        print(column, "-->>column")
        print(rows_values, "-->>row")
        print(val, "-->>val")
        result = self.mydb.run_query(query=query, value=val)
        print(result)
        return result

    def update_que(self, data, table_name=None, condition=None):
        column = []
        rows_values = []
        val = []
        for key, value in data.items():
            column.append(key)
            rows_values.append("%s")
            val.append(value)
        column1 = []
        rows_values1 = []
        val1 = []
        for key1, value1 in condition.items():
            column1.append(key1)
            rows_values1.append("%s")
            val1.append(value1)
        terms = ' , '.join(f'{key} = %s' for key in data)
        query = 'UPDATE %s SET ' % table_name + terms + ' WHERE %s = %s' % (column1[0], val1[0])
        self.mydb.query_execute(query=query, value=val)

    # def delete(self, data):


    def reset_password(self, data):
        query = " UPDATE users SET password = '" + data['password'] + "'WHERE  email = '" + data['email'] + "' "
        self.mydb.query_execute(query)


    def update_picture(self, data):
        query = "UPDATE profile SET profile_path='" + data['profile_path'] + "'WHERE  user_id = '" + data[
            'user_id'] + "'"
        self.mydb.query_execute(query)

    def read_picture(self, data):
        query = "SELECT * FROM profile WHERE user_id = '" + data['user_id'] + "'"
        result = self.mydb.run_query(query)
        return result

    def delete_picture(self, data):
        query = "DELETE FROM profile WHERE user_id = '" + data['user_id'] + "'"
        self.mydb.query_execute(query)


    def update_query(self, data):
        query = "UPDATE notes SET Title = '" + data['Title'] + "',Description = '" + data[
            'Description'] + "',Colour = '" + data['Colour'] + "',isPinned = '" + data[
                    'isPinned'] + "', isArchive = '" + data['isArchive'] + "', isTrash = '" + data[
                    'isTrash'] + "' WHERE  user_id = " + data['user_id'] + ""
        self.mydb.query_execute(query)

    def read_query(self, data):
        query = "SELECT * FROM notes WHERE user_id = '" + data['user_id'] + "'"
        entry = self.mydb.run_query(query)
        return entry

    def delete_query(self, data):
        query = "DELETE FROM notes WHERE user_id = " + data['user_id'] + ""
        self.mydb.query_execute(query)
