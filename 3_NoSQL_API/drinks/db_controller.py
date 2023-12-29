import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps, loads

load_dotenv()

class MongoController:
    def __init__(self):
        self.client = self.connect_to_client()
        self.drinks_db = self.client['Drinks']

    def connect_to_client(self):
        client = MongoClient(
            f'mongodb://{os.environ["CLIENT_ADDR"]}:{os.environ["CLIENT_PORT"]}/',
            username=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD']
        )
        if client is None:
            raise Exception('Cannot access Database Server!')

        return client
    
    def insert_drink(self, drink_type, document):
        try:
            self.drinks_db[drink_type].insert_one(document)
            return 1
        except:
            return 0
    
    def get_drink(self, drink_type, id):
        drink = self.drinks_db[drink_type].find_one({'_id': id})
        if drink is None:
            return 0
        else:
            return drink
    
    def get_by_type(self, drink_type):
        drinks = self.drinks_db[drink_type].find()
        if drinks is None:
            return 0
        else:
            reformatted_drinks = {drink_type: loads(dumps(drinks))}
            return reformatted_drinks

    def update_drink(self, drink_type, document):
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
        except:
            return 0

    def delete_drink(self, drink_type, id):
        self.drinks_db[drink_type].delete_one({'_id': id})

if __name__ == "__main__":
    remote = MongoController()
    print("Initialize DB")
    remote.insert_drink('Soda', {'_id':'Orange','description': 'Carbonated orange drink'})