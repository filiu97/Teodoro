from Engine import Engine
from time import sleep, time
import os
import wikipedia 
import webbrowser 
import urllib.request
import re
import tools as t
import threading
import subprocess as sp
from datetime import datetime, timedelta


class Applications(Engine):
    def __init__(self, db):

        self.applications = []
        for collection in db.list_collection_names():
            if collection == "Applications":
                for element in db[collection].find({}):
                    self.applications.append(element)
        
        self.SpotifyActions = self.applications[0]["SpotifyActions"]

        wikipedia.set_lang("es") 
        self.s_time_unit = t.Tools(3)	#Instancia objeto Switch
        self.s_time_unit.setSwitch_time_unit()	#Creador del switch

        Engine.__init__(self, self.Names, pause_thr = 0.8)

    def spotify(self, action, window = None):
        if window is not None:
            self.GUI("Close", prev_window=window)
        if action == "status":
            return sp.getoutput(self.SpotifyActions[action])
        elif action == "song":
            title = sp.getoutput(self.SpotifyActions["title"])
            album = sp.getoutput(self.SpotifyActions["album"])
            artist = sp.getoutput(self.SpotifyActions["artist"])
            speech = "Es " + title + ", del album " + album + ", de " + artist
            text = "Canción: " + title + "\n" + "Album: " + album + "\n" + "Artista: " + artist
            return speech, text
        else:
            status = os.system(self.SpotifyActions[action])
            if action == "previous":
                os.system(self.SpotifyActions[action])
            return status

    def google(self, query):
        words = query.split()
        if words[-1] == "google":
            query = words[1]
        else:
            query = words[-1]
        webbrowser.open("https://www.google.es/search?q=" + query)

    def wikipedia(self, query):
        words = query.split()
        if words[-1] == "wikipedia":
            query = words[1]
        else:
            query = words[-1]
        try:
            page = wikipedia.page(query)
            webbrowser.open(page.url)
        except wikipedia.DisambiguationError as e:
            self.speak("Múltiples opciones para " + query)
            print(e.options)
            self.speak("¿Cuál desea consultar?")
            repeated = self.repeat()
            if repeated is None:
                return None
            else:
                page = wikipedia.page(repeated)
                webbrowser.open(page.url)
                return 1

    def youtube(self, query):    
        words = query.split()
        if words[-1] == "youtube":
            query = words[1]
        else:
            query = words[-1]
        if "busca" in query:
            webbrowser.open("https://www.youtube.com/results?search_query=" + query.replace(" ", "+"))
        else:
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query.replace(" ", "+"))
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            webbrowser.open("https://www.youtube.com/watch?v=" + video_ids[0])

    def weather(self, query):
        query = query.partition("en")
        place = str(query[2]).replace(" ","")
        os.system("curl http://es.wttr.in/" + place + ".png --output '" + place + ".png'")
        weather = os.popen("curl http://es.wttr.in/"+ place).read()
        #os.system("clear")
        i = weather.find("+") or weather.find("-")
        try:
            temp = float(weather[i:i+3])
        except:
            temp = float(weather[i:i+2])
        i = weather.find("/") + 10
        desc = str()
        while weather[i] != " ":
            desc = desc + weather[i]
            i+=1
        speech = "En " + place + ",  está " + desc + " y hace " + str(temp) + " grados."
        return speech, place

    def setAlarm(self, query):
        list_of_words = query.split()
        try:
            t = int(list_of_words[list_of_words.index("de") + 1])
        except:
            t = 1
        try:
            unit = list_of_words[list_of_words.index("de") + 2]
            m = self.s_time_unit.switch(unit)
        except:
            m = 60
        t *= m
        try:
            name = list_of_words[list_of_words.index("nombre") + 1]
        except:
            name = "Alarma"

        speech = "Riiiiiiiiiing riiiiiiiiiing. Fin de la alarma de cinco minutos. " + name
        text = "Fin de la alarma \n " + name
        return t, speech, text

    def alarm(self, speech, text):
        if self.spotify("status") == "Playing":
            self.spotify("pause")
            self.speak(speech)
            self.spotify("play")
        else:
            self.speak(speech)
        self.GUI("Show", text = text, size = 16)
    
    def setReminder(self, query):
        list_of_words = query.split()
        try:
            name = list_of_words[list_of_words.index("nombre") + 1]
        except:
            name = "Recordatorio"
        try:
            hour = list_of_words[list_of_words.index("las") + 1]
            # if list_of_words[list_of_words.index(hour) + 3] == "tarde":
        except:
            speech = "No has especificado una hora concreta"
            text = "Debes especificar una hora concreta"
            return speech, text
        try:
            day = list_of_words[list_of_words.index("para") + 1]
            today = datetime.today().date()
            if day == "hoy":
                day = str(today)
            elif day == "mañana":
                day = str(today + timedelta(days=1))
            elif day == "pasado mañana":
                day = str(today + timedelta(days=2))
            # CUALQUIER FECHA
        except:
            day = str(datetime.today().date())
        
        new_rem = {"nombre": name, "día": day, "hora": hour}
        self.db["Reminders"].insert_one(new_rem)

        speech = "Recordatorio creado"
        text = "Recordatorio de nombre: " + name + " creado correctamente"
        return speech, text

    def checkReminder(self):
        t = datetime.now() 
        hour = t.strftime('%H:%M')
        today = datetime.today()
        number = str(today.date())
        reminders = []
        for collection in self.db.list_collection_names():
            if collection == "Reminders":
                for element in self.db[collection].find({}):
                    reminders.append(element)
        if not len(reminders):
            speech = None
            text = None
        else:
            for rem in range(len(reminders)):
                if reminders[rem]["día"] == number and reminders[rem]["hora"] <= hour:
                    speech = "Tienes un recordatorio para esta hora de nombre " + reminders[rem]["nombre"]
                    text = "Recordatorio " + reminders[rem]["nombre"]
                    del_rem = {"hora" : reminders[rem]["hora"]}
                    self.db["Reminders"].delete_one(del_rem)
                else:
                    speech = None
                    text = None
        
        return speech, text



