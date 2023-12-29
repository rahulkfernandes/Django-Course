import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class MongoController:
    def __init__(self):
        self.client = self.connect_to_client()
        self.drinks_db = self.client['drinks']

    def connect_to_client(self):
        client = MongoClient(
            f'mongodb://{os.environ["CLIENT_ADDR"]}:{os.environ["CLIENT_PORT"]}/',
            username=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
        if client is None:
            raise Exception('Cannot access Database Server!')

        return client
    
    def insert_drink(self, document, drink_type):
        try:
            self.drinks_db[drink_type].insert_one(document)
            return 1
        except:
            return 0
    
    def get_drink(self, name, drink_type):
        drink = self.drinks_db[drink_type].find_one({'_id': name})
        if drink is None:
            return 0
        else:
            return drink
    
    def update_drink(self, document, drink_type):
        try:
            self.drinks_db[drink_type].update_one(
                {'_id': document['_id']},
                {
                    '$set': {
                        'description': document['description']
                    }
                }
            )
            return 1
        except Exception as e:
            print(e)
            return 0

if __name__ == "__main__":
    remote = MongoController()
    remote.insert_drink({'_id':'test','description': 'info'}, 'Soda')
    drink_detail = remote.get_drink('test', 'Soda')
    print(drink_detail)
    remote.update_drink({'_id':'test','description': 'Very Nice'}, 'Soda')