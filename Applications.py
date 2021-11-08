from SpeechEngine import SpeechEngine
from time import sleep, time
import os
import wikipedia 
import webbrowser 
import tools as t




class Applications(SpeechEngine):
    def __init__(self, SpotifyActions):

        self.SpotifyActions = SpotifyActions
        wikipedia.set_lang("es") 
        self.s_time_unit = t.Tools(3)	#Instancia objeto Switch
        self.s_time_unit.setSwitch_time_unit()	#Creador del switch

        SpeechEngine.__init__(self, self.Names, pause_thr = 0.8)

    def spotify(self, action):
        os.system(self.SpotifyActions[action])

    def countdown(self, t, name):
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print("alarma " + name + "  --->  " + timeformat, end="\r")
            sleep(1)
            t -= 1
            os.system("clear")
            
        self.spotify("pause")
        self.speak("Riiiiiiiiiing riiiiiiiiiing. Fin de la alarma de " + name)
        self.spotify("play")

    def google(self, query):
        query = query.partition("google")
        self.speak("Abriendo Google")
        webbrowser.open("https://www.google.es/search?q=" + query[2])

    def wikipedia(self, query):
        query = query.partition("wikipedia")
        try:
            page = wikipedia.page(query[2])
    #	    result = wikipedia.summary(query[2], sentences = 4)
            webbrowser.open(page.url)
    #		self.speak("Según Wikipedia, ") 
    #		self.speak(result)
        except wikipedia.DisambiguationError as e:
            self.speak("Múltiples opciones para " + query[2])
            print(e.options)
            self.speak("¿Cuál desea consultar?")
            repeated = self.repeat()
            if repeated is None:
                return None
            else:
                page = wikipedia.page(repeated)
#			    result = wikipedia.summary(query[2], sentences = 4)
                webbrowser.open(page.url)
#				self.speak("Según Wikipedia, ") 
#				self.speak(result)

    def weather(self, query):
        query = query.partition("en")
        place = str(query[2]).replace(" ","")
        os.system("curl http://es.wttr.in/" + place + ".png --output '" + place + ".png'")
        weather = os.popen("curl http://es.wttr.in/"+ place).read()
        i = weather.find("+" or "-")
        try:
            temp = float(weather[i:i+3])
        except:
            temp = float(weather[i:i+2])
        i = weather.find("/") + 10
        desc = str()
        while weather[i] != " ":
            desc = desc + weather[i]
            i+=1
        self.speak("En " + place + ",  está " + desc + " y hace " + str(temp) + " grados.")
        os.system("display " + place + ".png")


    def alarm(self, query):
        list_of_words = query.split()
        try:
            t = int(list_of_words[list_of_words.index("de") + 1])
        except:
            t = 1
        unit = list_of_words[list_of_words.index("de") + 2]
        m = self.s_time_unit.switch(unit)
        t *= m
        name = list_of_words[list_of_words.index("nombre") + 1]
        self.countdown(t,name)

                   

