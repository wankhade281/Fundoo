from nameko.rpc import rpc

import sys

sys.path.insert(0, '/home/admin1/Demo1/PycharmProjects/fundoo')
from microserv.models import Data
import redis


class User(object):
    name = "note_service"

    @rpc
    def create_note(self, data):
        db_obj = Data()
        json_keys = list(data.keys())
        if len(json_keys) == 6:
            db_obj.put_cache(data)
            db_obj.get_cache('note_data')
            db_obj.create_entry(data)
            response = {'success': True, 'data': [], 'message': "Entry Create Successfully"}
            return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

    @rpc
    def delete_note(self, data):
        db_obj = Data()
        json_keys = list(data.keys())
        if len(json_keys) == 1:
            db_obj.delete_entry(data)
            response = {'success': True, 'data': [], 'message': "Data Delete Successfully"}
            return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

    @rpc
    def update_note(self, data):
        db_obj = Data()
        json_keys = list(data.keys())
        if len(json_keys) == 7:
            db_obj.update_entry(data)
            response = {'success': True, 'data': [], 'message': "Data Update Successfully"}
            return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response

    @rpc
    def read_note(self, data):
        db_obj = Data()
        json_keys = list(data.keys())
        if len(json_keys) == 1:
            db_obj.read_entry(data)
            response = {'success': True, 'data': [], 'message': "Data read Successfully"}
            return response
        else:
            response = {'success': False, 'data': [], 'message': "some values are missing"}
            return response
