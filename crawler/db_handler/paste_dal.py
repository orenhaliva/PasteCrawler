from crawler.db_handler.db import DB
from crawler.db_handler.paste import Paste


class PasteDal(object):
    def __init__(self):
        self.db = DB().connection

    def insert(self, paste: 'Paste'):
        self.db.insert(paste.__dict__)

    def get(self):
        data = self.db.all()
        return [Paste(**obj) for obj in data]
