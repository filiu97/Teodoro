#! /usr/bin python3

import tools as t
import pyttsx3 
import speech_recognition as sr 
import webbrowser   
import datetime   
import wikipedia 
import os
import sys
import time

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle


Names = ["Teodoro",
		 "Teo",
		 "subnormal",
		 "imbécil",
		 "gilipollas"
		]

Spotify = {"pause" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause",
		   "play" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play",
		   "next" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next",
		   "previous" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous",
		   "stop" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop"            
		}

Day_dict = {1: 'Lunes', 2: 'Martes',  
			3: 'Miércoles', 4: 'Jueves',  
			5: 'Viernes', 6: 'Sábado', 
			7: 'Domingo'} 

Month_dict = {'01': 'Enero', '02': 'Febrero',
			  '03': 'Marzo', '04': 'Abril',
			  '05': 'Mayo', '06': 'Junio',
			  '07': 'Julio', '08': 'Agosto',
			  '09': 'Septiembre', '10': 'Octubre',
			  '11': 'Noviembre', '12' : 'Diciembre'}

s_time_unit = t.Tools(3)	#Instancia objeto Switch
s_time_unit.setSwitch_time_unit()	#Creador del switch


def takeCommand(): 

	r = sr.Recognizer()

	with sr.Microphone() as source:
#		try:
#			print('Escuchando') 
			audio = r.record(source, 3)

			try: 
#				Query = r.recognize_google(audio, language='es-ES')
#				for name in Names:
#					if (Query.find(name)) != -1:
#						print("Reconociendo") 
#						Request = Query.partition(name)
#						print("Usted ha dicho:", Request[2])
#						return Request[2]
				
				Query = r.recognize_google(audio, language='es-ES')
				for name in Names:
					if (Query.find(name)) != -1:
						speak("¿Si?")
						print("Reconociendo")
						audio = r.record(source, 5) 
#						Request = Query.partition(name)
						try:
							Request = r.recognize_google(audio, language='es-ES')
							print("Usted ha dicho:", Request)
							return Request
						except:
							return "nada"
				
				return "nada"
	
			except: 
				return "nada"
#		except:
#			return "nada"

def speak(audio): 
	engine = pyttsx3.init()
	engine.setProperty('voice', 'spanish')
	engine.setProperty('rate', 165)
	engine.say(audio)
	engine.runAndWait() 
  
def tellDay():
	
	day = datetime.datetime.today().weekday() + 1
	today = datetime.datetime.today()
	number = str(today.date())
	
	#if day in Day_dict.keys(): 
	print(Day_dict[day]  + ". " + number) 
	speak("Hoy es " + Day_dict[day]  + ", " + number[-2:] + " de " + Month_dict[number[5:7]] + " de " + number[0:4]) 
  
  
def tellTime(): 
      
    t = str(datetime.datetime.now()) 
    print(t) 
    hour = t[11:13] 
    minutes = t[14:16] 
    speak("Son las" + hour + "horas y" + minutes + "minutos")     
  
def Hello(): 
	speak("Hola señor, aquí estoy para lo que necesite.")
	wikipedia.set_lang("es") 
	r = sr.Recognizer()
#	r.energy_threshold = 4000end="\r"
#	r.dynamic_energy_threshold = True
	r.pause_threshold = 0.8
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		
		
def countdown(t, name):
	while t:
		mins, secs = divmod(t, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		print("alarma " + name + "  --->  " + timeformat, end="\r")
		time.sleep(1)
		t -= 1
		os.system("clear")
		
	os.system(Spotify["pause"])
	speak("Riiiiiiiiiing riiiiiiiiiing. Fin de la alarma de " + name)
	os.system(Spotify["play"])


def Take_query(): 

	Hello() 
	
	while(True): 
		
		os.system("clear")
		
		query = takeCommand().lower() 
		
		if ("cómo te llamas" in query) or ("cómo te puedo llamar" in query): 
			n = str()
			for name in Names:
				n += name + ", o "
			speak("Me puedes llamar " + n[:-2] + ", tu asistente fiel")
		
		elif ("hola" == query.replace(" ", "")) or ("qué tal" in query) or ("reiníciate" in query):
			Hello()
		
		elif "anímame" in query:
			speak("Venga señor, no pasa nada, aquí está Teodoro para servirle")
		
		elif "busca en google" in query:
			query = query.partition("google")
			speak("Abriendo Google")
			webbrowser.open("https://www.google.es/search?q=" + query[2])
		
		elif "qué día es hoy" in query: 
			tellDay()
		
		elif "qué hora es" in query: 
			tellTime()
		
		elif "pon la música" in query:
			os.system(Spotify["play"])
		
		elif "pasa de canción" in query or "siguiente canción" in query:
			os.system(Spotify["next"])
		
		elif "anterior canción" in query:
			os.system(Spotify["previous"])
		
		elif "para la música" in query or "para spotify" in query:
			os.system(Spotify["pause"])
		
		elif "cierra spotify" in query or "quita la música" in query:
			os.system(Spotify["stop"])
		
		elif "busca en wikipedia" in query: 
			query = query.partition("wikipedia") 
			try:
				page = wikipedia.page(query[2])
#				result = wikipedia.summary(query[2], sentences = 4)
				webbrowser.open(page.url)
#				speak("Según Wikipedia, ") 
#				speak(result)
			except wikipedia.DisambiguationError as e:
				speak("Múltiples opciones para " + query[2])
				print(e.options)
				speak("¿Cuál desea consultar?")
				r = sr.Recognizer()
				with sr.Microphone() as source:
					try:
						print('Escuchando') 
						audio = r.record(source, 10)
						try: 
							query = r.recognize_google(audio, language='es-ES')
							page = wikipedia.page(query)
#							result = wikipedia.summary(query[2], sentences = 4)
							webbrowser.open(page.url)
#							speak("Según Wikipedia, ") 
#							speak(result)
						except:
							speak("No he reconocido lo que ha dicho, lo siento")
							break
					except:
						break
		
		elif "tiempo hace" in query:
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
			speak("En " + place + ",  está " + desc + " y hace " + str(temp) + " grados.")
			os.system("display " + place + ".png")
		
		elif "alarma" in query:
			list_of_words = query.split()
			try:
				t = int(list_of_words[list_of_words.index("de") + 1])
			except:
				t = 1
			unit = list_of_words[list_of_words.index("de") + 2]
			m = s_time_unit.switch(unit)
			t *= m
			name = list_of_words[list_of_words.index("nombre") + 1]
			countdown(t,name)
		
		
		elif ("apágate" in query) or ("adiós" in query): 
			speak("Adiós señor, que tenga un buen día")
			sys.exit() 
		
		elif "apaga el ordenador" in query:
			speak("En seguida, que tengas un buen día")
			os.system("shutdown now -h")

		elif ("suspende el ordenador" in query) or ("suspensión" in query):
			os.system("sudo pm-suspend")

			

			
		elif "prueba" in query:
			
			continue
				
if __name__ == '__main__': 
      
    Take_query()
