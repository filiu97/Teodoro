from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://filiu:teodoro@teodoro.ocpsz.mongodb.net/KnowledgeBase?retryWrites=true&w=majority")
    db = client.KnowledgeBase
    return client, db

if __name__ == "__main__":

    client, db = get_db() 
    applications = []
    calendar = []
    general = []
    for collection in db.list_collection_names():
        if collection == "Applications":
            applications = db[collection].find({})
        elif collection == "Calendar":
            calendar = db[collection].find({})
        else:
            for element in db[collection].find({}):
                general.append(element)

    SpotifyActions = applications[0]["SpotifyActions"]
    CalendarsID = calendar[0]["CalendarsID"]
    Numbers = calendar[0]["Numbers"]
    Time = general[0]["Time"]
    Names = general[0]["Names"]
    Commands = general[1]["Commands"]
    print(SpotifyActions["play"])
    print(CalendarsID["personal"])
    print(Numbers)
    print(Time["Months"])
    print(Names)
    print(Commands["Name"])
