from Engine import Engine
from time import sleep, time
import os
import wikipedia 
import webbrowser 
import urllib.request
import re
import tools as t
import threading


window = None


class Applications(Engine):
    def __init__(self, SpotifyActions):

        self.SpotifyActions = SpotifyActions
        wikipedia.set_lang("es") 
        self.s_time_unit = t.Tools(3)	#Instancia objeto Switch
        self.s_time_unit.setSwitch_time_unit()	#Creador del switch

        self.alarmDuration = None
        self.alarmSpeech = None
        self.alarmText = None
        self.alarmFirstFlag = True
        self.alarmIndex = 1
        self.alarmWindow = None

        Engine.__init__(self, self.Names, pause_thr = 0.8)

    def spotify(self, action):
        os.system(self.SpotifyActions[action])

    def countdown(self, t, name, window):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            sleep(1)
            t -= 1
            os.system("clear")
            window = self.GUI("Countdown", text = "Alarma " + name + "  --->  " + timeformat, size = 16, prev_window = window)
        return window

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
        os.system("clear")
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


    def set_alarm(self, query, window):
        list_of_words = query.split()
        try:
            t = int(list_of_words[list_of_words.index("de") + 1])
        except:
            t = 1
        unit = list_of_words[list_of_words.index("de") + 2]
        try:
            m = self.s_time_unit.switch(unit)
        except:
            m = 60
        t *= m
        try:
            name = list_of_words[list_of_words.index("nombre") + 1]
        except:
            name = "Alarma"

        self.alarmSpeech = "Riiiiiiiiiing riiiiiiiiiing. Fin de la alarma de nombre " + name
        self.alarmText = "Fin de la alarma de nombre " + name
        self.alarmDuration = t

    def alarm(self):
        global window
        if self.alarmFirstFlag:
            t = self.alarmDuration
            self.alarmFirstFlag = False
        else:
            t = self.alarmDuration-self.alarmIndex
            self.alarmIndex = self.alarmIndex + 1
            self.alarmWindow.destroy()
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.alarmWindow = self.GUI("Countdown", text = timeformat, size = 16)

        if t:
            timer = threading.Timer(1, self.alarm)
            timer.start()
        else:    
            os.system("clear")
            self.spotify("pause")
            self.speak(self.alarmSpeech)
            self.spotify("play")	
            self.GUI("Show", text = self.alarmText, size = 16, prev_window = self.alarmWindow)
                    

