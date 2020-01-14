import cgi
from view.response import Response
from model.query import DatabaseManage


class Profile:
    def create_pic(self):
        if self.path == '/profile/create':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            responce_data = {'success': True, 'data': [], 'message': ""}
            data = {'profile': form['profile'].value}
            db_obj = DatabaseManage()
            result = db_obj.profile_exist(data)
            if result:
                db_obj.create_profile(data)
                responce_data.update({'success': True, 'data': [], 'message': "Pic saved Successfully"})
                Response(self).jsonResponse(status=200, data=responce_data)
            else:
                responce_data.update({'success': False, 'data': [], 'message': "Profile already Exist"})
                Response(self).jsonResponse(status=404, data=responce_data)

    def read_pic(self):
        if self.path == '/profile/read':
            responce_data = {'success': True, 'data': [], 'message': ""}
            db_obj = DatabaseManage()
            db_obj.read_profile()
            responce_data.update({'success': True, 'data': [], 'message': "Data Read Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)

    def update_pic(self):
        if self.path == '/profile/update':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            responce_data = {'success': True, 'data': [], 'message': ""}
            data = {'profile': form['profile'].value, 'newprofile': form['newprofile'].value}
            db_obj = DatabaseManage()
            result = db_obj.profile_exist(data)
            if result:
                responce_data.update({'success': False, 'data': [], 'message': "Profile Not Exist"})
                Response(self).jsonResponse(status=404, data=responce_data)
            else:
                db_obj.update_profile(data['profile'], data['newprofile'])
                responce_data.update({'success': True, 'data': [], 'message': "Profile Update Successfully"})
                Response(self).jsonResponse(status=200, data=responce_data)

    def delete_pic(self):
        if self.path == '/profile/delete':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            responce_data = {'success': True, 'data': [], 'message': ""}
            data = {'profile': form['profile'].value}
            db_obj = DatabaseManage()
            result = db_obj.profile_exist(data)
            if result:
                responce_data.update({'success': False, 'data': [], 'message': "Profile Not Exist"})
                Response(self).jsonResponse(status=404, data=responce_data)
            else:
                db_obj.delete_profile(data)
                responce_data.update({'success': True, 'data': [], 'message': "Profile Delete Successfully"})
                Response(self).jsonResponse(status=200, data=responce_data)


class ListingPages:
    def isArchieve(self):
        responce_data = {'success': True, 'data': [], 'message': ""}
        db_obj = DatabaseManage()
        db_obj.read_all('isArchive')
        responce_data.update({'success': True, 'data': [], 'message': "Data Read Successfully"})
        Response(self).jsonResponse(status=200, data=responce_data)

    def isPinned(self):
        responce_data = {'success': True, 'data': [], 'message': ""}
        db_obj = DatabaseManage()
        db_obj.read_all('isPinned')
        responce_data.update({'success': True, 'data': [], 'message': "Data Read Successfully"})
        Response(self).jsonResponse(status=200, data=responce_data)

    def isTrash(self):
        if self.path == '/istrash':
            responce_data = {'success': True, 'data': [], 'message': ""}
            db_obj = DatabaseManage()
            db_obj.read_all('isTrash')
            responce_data.update({'success': True, 'data': [], 'message': "Data Read Successfully"})
            Response(self).jsonResponse(status=200, data=responce_data)