from pymongo import MongoClient
import gridfs
import base64
from io import BytesIO
from PIL import Image
from pydub import AudioSegment
from pydub.playback import play

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
    #         applications = db[collection].find({})
    #     elif collection == "Calendar":
    #         calendar = db[collection].find({})
    #     else:
    #         for element in db[collection].find({}):
    #             general.append(element)

    # SpotifyActions = applications[0]["SpotifyActions"]
    # CalendarsID = calendar[0]["CalendarsID"]
    # Numbers = calendar[0]["Numbers"]
    # Time = general[0]["Time"]
    # Names = general[0]["Names"]
    # Commands = general[1]["Commands"]
    # print(SpotifyActions["play"])
    # print(CalendarsID["personal"])
    # print(Numbers)
    # print(Time["Months"])
    # print(Names)
    # print(Commands["Name"])

    # file = "/home/filiu/Imágenes/Spotify-logo-2015.png"
    # with open(file, 'rb') as f:
    #     contents = base64.b64encode(f.read())
    # fs.put(contents, filename="image")

    # file = "/home/filiu/Teodoro/Teodoro_Calling.mp3"
    # with open(file, 'rb') as f:
    #     contents = base64.b64encode(f.read())
    # fs.put(contents, filename="audio")

    image = fs.find_one({"filename":"image"})
    bytedata = image.read()

    ima_IO = BytesIO(base64.b64decode(bytedata))
    img_PIL = Image.open(ima_IO)
    img_PIL.show()

    audio = fs.find_one({"filename":"audio"})
    bytedata = audio.read()

    aud_IO = BytesIO(base64.b64decode(bytedata))
    song = AudioSegment.from_file(aud_IO, format="mp3")
    play(song)