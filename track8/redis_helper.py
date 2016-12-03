import json

import redis
import datetime
from django_redis import get_redis_connection

class RedisHelper(object):
    #__metaclass__ = Singleton

    def __init__(self, ):
        self.redis_connection = get_redis_connection('default').connection_pool
        self.redis_client_object = redis.Redis(connection_pool=self.redis_connection)

    def get_key(self, obj_type, obj_name):
        return obj_type + ":" + obj_name

    def create_tag(self, tag_name):
        key = self.get_key("tag", tag_name)
        self.redis_client_object.zadd(key, tag_name, 0)

    def increment_tag_count(self, tag_name, related_tag_name):
        key = self.get_key("tag", tag_name)
        self.redis_client_object.zincrby(key, related_tag_name, 1)

    def get_related_tags(self, tag_name, limit, offset):
        key = self.get_key("tag", tag_name)
        data = self.redis_client_object.zrevrangebyscore(key, "+inf", "-inf", start=offset, num=limit)
        return data
        

    def add_tag_playlist(playlist_id, tag_name):
        key = self.get_key("playlist:tag", tag_name)
        self.redis_client_object.sadd(key,playlist_id)

    def get_playlists_for_tag(tag_name)
        key = self.get_key("playlist:tag", tag_name)
        data = self.redis_client_object.smembers(key)
        return data

    

