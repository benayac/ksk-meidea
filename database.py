import pymongo
import dns
from secrets import *

class Database():
    def __init__(self):
        client = pymongo.MongoClient(DATABASEURL)
        self.db = client.meIDEA
    
    def insert_data(self, data):
        result = self.db.emails.insert_one(data)
        print('Created {}'.format(result.inserted_id))

    def is_data_available(self, data):
        if(self.db.emails.count_documents(data) >= 1):
            return True
        else:
            return False