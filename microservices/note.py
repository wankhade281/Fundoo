from nameko.rpc import rpc

import sys

sys.path.insert(0, '/home/admin1/Demo1/PycharmProjects/fundoo')
from microservices.models import Data


class User(object):
    name = "note_service"

    @rpc
    def create_note(self, data):
        db_obj = Data()
        data_id = data['id']
        json_keys = list(data.keys())
        if len(json_keys) == 7:
            if db_obj.get_cache(data_id):
                response = {'success': True, 'data': [], 'message': "Entry already available"}
                return response
            else:
                db_obj.put_cache(data, data_id)
                db_obj.create_entry(data)
                response = {'success': True, 'data': [], 'message': "Entry Create Successfully"}
                return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

    @rpc
    def delete_note(self, data):
        db_obj = Data()
        data_id = data['id']
        json_keys = list(data.keys())
        if len(json_keys) == 1:
            if len(db_obj.get_keys(data_id)):
                db_obj.del_cache(data_id)
                db_obj.delete_entry(data)
                response = {'success': True, 'data': [], 'message': "Entry Delete Successfully"}
                return response
            else:
                response = {'success': True, 'data': [], 'message': "Entry not available"}
                return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

    @rpc
    def update_note(self, data):
        db_obj = Data()
        json_keys = list(data.keys())
        data_id = data['id']
        if len(json_keys) == 7:
            if db_obj.get_cache(data_id):
                db_obj.put_cache(data, data_id)
                db_obj.update_entry(data)
                response = {'success': True, 'data': [], 'message': "Data Update Successfully"}
                return response
            else:
                response = {'success': True, 'data': [], 'message': "Entry not available"}
                return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

    @rpc
    def read_note(self, data):
        db_obj = Data()
        json_keys = list(data.keys())
        data_id = data['id']
        if len(json_keys) == 1:
            if len(db_obj.get_keys(data_id)):
                x = db_obj.get_cache(data_id)
            response = {'success': True, 'data': [], 'message': "Data read Successfully"}
            return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response
