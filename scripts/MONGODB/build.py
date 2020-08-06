from pymongo import MongoClient

from functions import csv_to_dict, make_collections, confirm_creation

client = MongoClient("localhost", 27017)
db = client["scheduler_db"]

# Initialize the mongo database
## confirm collections exist
if __name__ == "__main__":
    if set(db.list_collection_names()) != set(['users', 'locations', 'shifts']):
        #prep data
        list_of_dicts = csv_to_dict()
        #make collections via mass insert
        db = make_collections(db, list_of_dicts)
        #check collections' and db existence
        confirm_creation(client, db)
    else:
       #check collections' and db existence
        confirm_creation(client, db)

