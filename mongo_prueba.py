from pymongo import MongoClient

def get_db():
    client = MongoClient('localhost:27017')
    db = client.Knowledge_Base
    return client, db

def add_country(db):
    db.countries.insert({"name" : "Canada"})
    
def get_days(db):
    return db.General.find()

if __name__ == "__main__":

    client, db = get_db() 
    print(client.list_database_names())
    for days in get_days(db):
        print(days)
