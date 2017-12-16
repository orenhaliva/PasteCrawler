from datetime import datetime

from tinydb import TinyDB
from tinydb_serialization import SerializationMiddleware, Serializer

from crawler.config import DBConfig
from crawler.utils.singleton import Singleton


class DateTimeSerializer(Serializer):
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime(self.DATE_FORMAT)

    def decode(self, s):
        return datetime.strptime(s, self.DATE_FORMAT)


class DB(object, metaclass=Singleton):
    def __init__(self):
        serialization = SerializationMiddleware()
        serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
        self.connection = TinyDB(DBConfig.PATH_TO_DB, storage=serialization)
