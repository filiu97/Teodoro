from pymongo import MongoClient
import gridfs
import base64
from io import BytesIO
from PIL import Image
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime

def get_db():
    client = MongoClient("mongodb+srv://filiu:teodoro@teodoro.ocpsz.mongodb.net/KnowledgeBase?retryWrites=true&w=majority")
    db = client.KnowledgeBase
    fs = gridfs.GridFS(db)
    return client, db, fs

if __name__ == "__main__":

    client, db, fs = get_db() 
    # applications = []
    # calendar = []
    # general = []
    # for collection in db.list_collection_names():
    #     if collection == "Applications":
    #         for element in db[collection].find({}):
    #             applications.append(element)
    #     elif collection == "Calendar":
    #         for element in db[collection].find({}):
    #             calendar.append(element)
    #     elif collection == "General":
    #         for element in db[collection].find({}):
    #             general.append(element)

    # SpotifyActions = applications[0]["SpotifyActions"]
    # # CalendarsID = calendar[0]["CalendarsID"]
    # # Numbers = calendar[0]["Numbers"]
    # Time = general[0]["Time"]
    # Names = general[0]["Names"]
    # Commands = general[1]["Commands"]

    # print("Commands" in general[1])

    # file = "Filiu.jpg"
    # with open(file, 'rb') as f:
    #     contents = base64.b64encode(f.read())
    # fs.put(contents, filename="filiu")

    # file = "/home/filiu/Teodoro/Teodoro_Calling.mp3"
    # with open(file, 'rb') as f:
    #     contents = base64.b64encode(f.read())
    # fs.put(contents, filename="audio")

    # image = fs.find_one({"filename":"filiu"})
    # bytedata = image.read()
    # ima_IO = BytesIO(base64.b64decode(bytedata))
    # img_PIL = Image.open(ima_IO)
    # img_PIL.show()

    # audio = fs.find_one({"filename":"audio"})
    # bytedata = audio.read()

    # aud_IO = BytesIO(base64.b64decode(bytedata))
    # song = AudioSegment.from_file(aud_IO, format="mp3")
    # play(song)



    # new_rem = {"nombre": "Caca", "día": "2022-03-17", "hora": "19:23"}
    # db["Reminders"].insert_one(new_rem)

    # while True:
    #     t = datetime.now() 
    #     hour = t.strftime('%H:%M')
    #     today = datetime.today()
    #     number = str(today.date())
    #     reminders = []
    #     for collection in db.list_collection_names():
    #         if collection == "Reminders":
    #             for element in db[collection].find({}):
    #                 reminders.append(element)
    #     if not len(reminders):
    #         print("caca")
    #     for rem in range(len(reminders)):
    #         if reminders[rem]["día"] == number and reminders[rem]["hora"] <= hour:
    #             print("Recordatorio " + reminders[rem]["nombre"])
    #             del_rem = {"hora" : reminders[rem]["hora"]}
    #             db["Reminders"].delete_one(del_rem)
    #             break



    # users = []
    # for collection in db.list_collection_names():
    #     if collection == "Users":
    #         for element in db[collection].find({}):
    #             users.append(element)
    # User = db["Users"].find_one({"Nombre": "filiu"})
    # print(User)
    # User.pop("_id")
    # for k, v in User.items():
    #     print(k, v)

    # field = "caca"
    # attribute = "marrón"
    # name2find = { "Nombre": "carlos" }
    # newvalues = { "$set": { field : attribute } }

    # db["Users"].update_one(name2find, newvalues)





    # applications = []
    # for collection in db.list_collection_names():
    #     if collection == "Applications":
    #         for element in db[collection].find({}):
    #             applications.append(element)
    
    # SpotifyActions = applications[0]["SpotifyActions"]
    # MathOperations = applications[0]["MathOperations"]

    # number_1 = 5
    # number_2 = 5

    # print(eval(MathOperations["add"]["operation"]))

    # print(len(MathOperations))

    # print(MathOperations.keys())

    # query = "5 * 5"

    # for key in MathOperations.keys():
    #     if MathOperations[key]["keyword"] in query:
    #         print(eval(MathOperations[key]["operation"]))

    # info = db["Users"].find_one({"nombre": "filiu"}, {"_id":0, "_CalendarsID":1, "_PhoneFunctions":1})
    # CalendarsID = info["_CalendarsID"]
    # PhoneFunctions = info["_PhoneFunctions"]
    # print(CalendarsID)
    # print(PhoneFunctions)


    # field = ["caca", "pedo"]
    # attribute = ["espesa", "contundente"]
    # name2find = { "nombre": "usuario" }
    # for i in range(len(field)):
    #     newvalues = { "$set": { field[i] : attribute[i] } }
    #     db["Users"].update_one(name2find, newvalues)

   
    # db["Users"].insert_one({"nombre" : "caca", "_CalendarsID" : {"personal" : None, "trello" : None}, "_PhoneFunctions":False, "_salt":"salt", "_hash":"hash"})
    # newvalues = { "$set": { "_CalendarsID" : {"personal" : None, "trello" : None}, "_salt":"salt", "_hash":"hash" } }
    # db["Users"].update_one("caca", newvalues)

    text = "caca"
    text1 = "blanda"
    field = [text]
    attribute = [text1]

    name2find = {"nombre": "filiu"}
    for i in range(len(field)):
        newvalues = {"$set": {field[i]: attribute[i]}}
        db["Users"].update_one(name2find, newvalues)