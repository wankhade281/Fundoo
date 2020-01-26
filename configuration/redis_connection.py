import os
import redis


class RedisService:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        r = redis.Redis(host=os.getenv('REDIS_HOST'),
                        port=os.getenv('REDIS_PORT'),
                        db=os.getenv('REDIS_DB'),
                        password=os.getenv('REDIS_PASSWD'))
        return r

    def set(self, key, value):
        self.conn.set(key, value)

    def get(self, key):
        value = self.conn.get(key)
        return value

    def disconnect(self):
        self.conn.close()

# con = RedisService(host=os.getenv('REDIS_HOST'),
#                    port=os.getenv('REDIS_PORT'),
#                    db=os.getenv('REDIS_DB'),
#                    password=os.getenv('REDIS_PASSWD'))
