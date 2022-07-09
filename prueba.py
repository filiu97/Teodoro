import os
import shlex
from time import sleep
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build
import pickle
import datefinder
from datetime import datetime, time, timedelta
import color

# trello = 'qonfs68h23u3uct5656hlrscusfeiale@import.calendar.google.com'
# personal = 'karlosfiliu97@gmail.com'

# scopes = ['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)

# Para hacerlo por primera vez, las credenciales
# credentials = flow.run_console()
# pickle.dump(credentials, open("token.pkl", "wb")) 

# credentials = pickle.load(open("token.pkl", "rb"))  

# service = build("calendar", "v3", credentials=credentials)
# result = service.calendarList().list().execute()
# print(result)
# calendar_id = result['items'][0]['id']
# print(calendar_id)
# result = service.events().list(calendarId=calendar_id).execute()
# print(result['items'][0])

# def create_event(start_time_str, summary, duration=1, description=None, location=None):
#     matches = list(datefinder.find_dates(start_time_str))
#     if len(matches):
#         start_time = matches[0]
#         end_time = start_time + timedelta(hours = duration)
                
#     event = {
#         'summary': summary,
#         'location': location,
#         'description': description,
#         'start': {
#             'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
#             'timeZone': 'Europe/Madrid',
#         },
#         'end': {
#             'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
#             'timeZone': 'Europe/Madrid',
#         },
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 10},
#             ],
#         },
#     }
    
#     return service.events().insert(calendarId=personal, body=event, sendNotifications=True).execute()

# create_event('11/10/2021 12:30pm',"Prueba")


# from dateutil.relativedelta import relativedelta

# # Get events
# today = datetime.today()
# d = 7
# diff = today + relativedelta(days=d)
# tmin = today.isoformat('T') + "Z"
# tmax = diff.isoformat('T') + "Z"
# maxResults = 50
# eventsResult = service.events().list(
#     calendarId=personal,
#     timeMin=tmin,
#     timeMax=tmax,
#     maxResults=maxResults,
#     singleEvents=True,
#     orderBy='startTime',
# ).execute()


# import iso8601

# def get_date(date_input):

#     date_obj = iso8601.parse_date(date_input)
#     return date_obj.strftime('%H:%M del %d-%m-%Y ')


# print("Tus eventos de los próximos " + str(d) + " días son:")

# # Get the list of colors
# colors = service.colors().get().execute()



# for event in eventsResult['items']:
#     if 'dateTime' in event['start'].keys():
#         print("   -" + event['summary'] + " a las " + get_date(event['start']['dateTime']))
#     else:
#         print("   -" + event['summary'] + " el día " + get_date(event['start']['date']))



# def get_hours(date_input):

#     date_obj = iso8601.parse_date(date_input)
#     return date_obj.strftime('%H:%M')

# day_str = "2021/11/02"
# matches = list(datefinder.find_dates(day_str))

# day = matches[0]
# diff = day + relativedelta(days=1)
# tmin = day.isoformat('T') + "Z"
# tmax = diff.isoformat('T') + "Z"
# eventsResult = service.events().list(
#     calendarId='karlosfiliu97@gmail.com',
#     timeMin=tmin,
#     timeMax=tmax,
#     maxResults=maxResults,
#     singleEvents=True,
#     orderBy='startTime',
# ).execute()

# print("Tus eventos para el día " + str(day.strftime("%d-%m-%Y")) + " son:")

# for event in eventsResult['items']:
#     if 'dateTime' in event['start'].keys():
#         print("   -" + event['summary'] + " a las " + get_hours(event['start']['dateTime']))
#     else:
#         print("   -" + event['summary'] + " el día " + event['start']['date'])



# List = open("Names.txt").read().splitlines()
# print(List)

# Prueba = {}
# file = open("Prueba.txt")
# prueba = eval(file.read())
# print(prueba)
# print(type(prueba))
# query = "Hola Teodoro, dime, cómo te llamas"
# print(bool([match for match in prueba["Nombre"] if(match in query)]))


# import webbrowser 

# webbrowser.open("http://youtube.com")

# import urllib.request
# import re

# search_keyword="caca de mono"
# html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword.replace(" ", "+"))
# video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
# print("https://www.youtube.com/watch?v=" + video_ids[0])
# webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])

# from tkinter import *


# window = Tk()
# window.geometry("400x200")
# window.configure(bg = "LightSkyBlue1")
# window.title("Teodoro Prueba")
# window.resizable(False, True)
# font1 = "Times New Roman"
# font2 = "Helvetica"


# global description, location
# # frame1 = Frame(window)
# # frame1.pack()
# label = Label(
#     window,
#     text="¿Quieres añadir una descripción \ny localización a tu evento",
#     font=(font1, 12, "bold"),
#     padx=0,
#     pady=0,
#     bg='LightSkyBlue1'
#     )
# label.pack()

# global desc

# def enter(desc):
#     desc = desc_entry.get()
#     window.destroy()

# # frame2 = Frame(window)
# # frame2.pack()
# Label(window, text="Description",font=(font1, 12, "bold")).pack()
# # description = StringVar()
# desc_entry = Entry(window)
# desc_entry.bind('<Return>',enter)
# desc_entry.pack()
# # desc_entry.grid(row=0, column=1, sticky=W)
# Label(window, text="Location",font=(font1, 12, "bold")).pack()
# # location = StringVar()
# loc_entry = Entry(window)
# loc_entry.pack()

# # frame3 = Frame(window)
# # frame3.pack()
# # b1 = Button(window,text=" Ok ",command=lambda:window.destroy()).pack()

# window.mainloop()

# print(desc)
# print(loc)


# from time import sleep, time
# import os

# import threading

# i = 0
# first = True

# def countdown(t = 60, name = 'prueba'):

#     global first, i

#     if first:
#         t_ = t
#         first = False
#     else:
#         t_ = t-i
#         i = i + 1
#     mins, secs = divmod(t_, 60)
#     timeformat = '{:02d}:{:02d}'.format(mins, secs)
#     os.system("clear")
#     print("Alarma " + name + "  --->  " + timeformat)
#     if t_:
#         timer2 = threading.Timer(1, countdown)
#         timer2.start()
#     else:
#         fin()


# def fin(name = 'prueba'):

#     os.system("clear")
#     print("Alarma " + name + "  --->  Finalizada!")


# timer1 = threading.Timer(1, countdown)
# timer1.start()

# import subprocess as sp

# prueba = sp.getoutput('''dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'PlaybackStatus'|egrep -A 1 "string"|cut -b 26-|cut -d '"' -f 1|egrep -v ^$''')

# print(prueba)

# import pyttsx3

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for voice in voices:
#     print("Voice: %s" % voice.name)
#     print(" - ID: %s" % voice.id)
#     print(" - Languages: %s" % voice.languages)
#     print(" - Gender: %s" % voice.gender)
#     print(" - Age: %s" % voice.age)
#     print("\n")
# engine.setProperty('rate', 180)
# engine.setProperty('voice', 'spanish+m3')

# engine.say('Hola, ¿cómo estás?')
# engine.runAndWait()




# import webbrowser 


# status = webbrowser.open("https://www.google.es/search?q=" + "caca")
# print(status)

# import os
# from time import sleep

# os.system("nmcli radio wifi off")
# sleep(10)
# os.system("nmcli radio wifi on")

# from Teodoro import Teodoro

# test = Teodoro(del_speak=False)
# for command in test.Commands.keys():
#     query = test.Commands[command][0]
#     if query != 'apaga el ordenador' and query != 'suspende el ordenador' and query != 'reinicia el ordenador':
#         print(query)

# f = 5
# print(type(f) == int)


# import webbrowser 

# status = webbrowser.open("https://trigger.macrodroid.com/66e970ab-dfed-4d8a-9e54-00ecf148d064/Teodoro")
# print(status)


import webbrowser 
import socket

webbrowser.open("https://trigger.macrodroid.com/66e970ab-dfed-4d8a-9e54-00ecf148d064/emergency_call")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("",50000))
sock.setblocking(0)
status = None
while status == None:
    try:
        data, _ = sock.recvfrom(1024)
        code = data.decode("utf-8")
        if code == 'c':
            sleep(10)
            print("Ok")
            status = 1
    except:
        status = None

# number = str(datetime.today().date())
# print(number)
# t = datetime.now() 
# text = t.strftime('%H:%M')
# print(text)
# hour = "01:22" 
# hour = hour.replace(hour[:2], str(int(hour[:2]) + 12))
# print(hour)

# import telegram_send
# telegram_send.send(messages=["UNLOCK_MOBILE 14335"])




# import speech_recognition as sr 
# import pyttsx3 

# r = sr.Recognizer()
# r.pause_threshold = 0.8
# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source)
# voiceEngine = pyttsx3.init()
# defaultVoice = 'spanish+m3'
# defaultWisperVoice = 'spanish+whisper'
# defaultRate = 180
# maxVoices = 7
# voiceEngine.setProperty('voice', defaultVoice)
# voiceEngine.setProperty('rate', defaultRate)
# Names = {"Teodoro", "Teo"}

# def takeCommand(): 

#     r = sr.Recognizer()

#     while 1:
#         with sr.Microphone() as source:
#             audio = r.record(source, 3)
#             try:
#                 Query = r.recognize_google(audio, language='es-ES')
#                 for name in Names:
#                     if (Query.find(name)) != -1:
#                         speak("¿Si?")
#                         audio = r.record(source, 10) 
#                         try:
#                             Request = r.recognize_google(audio, language='es-ES')
#                             return Request
#                         except:
#                             return None		
#                 return None
#             except: 
#                 return None

#     def speak(audio): 
#         voiceEngine.say(audio)
#         voiceEngine.runAndWait()

# while(1):
#     query = takeCommand()
#     if query is not None:
#         print(query)


# import webbrowser 

# macroEmergencyCall = "https://trigger.macrodroid.com/66e970ab-dfed-4d8a-9e54-00ecf148d064/emergency_call"
# webbrowser.open(macroEmergencyCall)

# import bcrypt

# password = b'k1rl4sf3l35'

# # Generate salt
# mySalt = bcrypt.gensalt()
# print(mySalt)

# # Hash password
# hash = bcrypt.hashpw(password, mySalt)
# print(hash)

# print(bcrypt.checkpw(b"k1rl4sf3l35", b'$2b$12$8grSVALUCAUkbq.7JR8Ahex58CUZsAlSEoIJYIv0Ojgbv.3wwDnLy'))

# from gtts import gTTS 
# from playsound import playsound 
# v =gTTS(text="Hola, ¿qué tal estás?",lang="es",slow=False) 
# v.save("name.mp3") 
# playsound("name.mp3")

# file = open(".MongoDBKey", 'r')
# mongo_key = file.read()
# print(mongo_key)
# file.close()

# import json
#f = open("Commands.json",'r')
#json_object = json.loads(f)
#json_formatted_str = json.dumps(json_object, indent=2)
#print(json_formatted_str)

# query  ="alarma de nombre caca de la vaca"
# list_of_words = query.split()

# name = ' '.join(list_of_words[list_of_words.index("nombre")+1:])
# print(name)

# name = query.partition("nombre")
# print(name[2])


# print(str(datetime.today().date()))
# print(datetime.strptime('20/6/22', '%d/%m/%y').date() > datetime.strptime('19/6/22', '%d/%m/%y').date())


# start_time_str = "el día " + str(21) + " de " +  str(6) + " de " + str(2022) + " a las 10:30"
# # start_time_str = "21/6/22 10:30"
# duration = 2

# matches = list(datefinder.find_dates(start_time_str))
# if len(matches):
#     start_time = matches[0]
#     end_time = start_time + timedelta(hours = duration)

# print(start_time)
# print(end_time)


# f = open(".prueba", "x")
# f.close()

# webbrowser.open(".prueba")


# f = open(".log", "w")
# f.write(str(datetime.today().date()))
# f.close()



# f = open(".log", "r")
# last_connection = f.read()

# if str(datetime.today().date()) == last_connection:
#     print("Yeah")
# else:
#     print("No")
# f.close()
