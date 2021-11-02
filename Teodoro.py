#! /usr/bin python3

import tools as t
import pyttsx3 
import speech_recognition as sr 
import webbrowser   
import datetime   
import wikipedia 
import os
import sys
from time import sleep, time
from dateutil.relativedelta import relativedelta
import datefinder
from datetime import datetime, timedelta
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import iso8601

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)

# Para hacerlo por primera vez, las credenciales
#credentials = flow.run_console()
#pickle.dump(credentials, open("token.pkl", "wb")) 

credentials = pickle.load(open("token.pkl", "rb"))  

service = build("calendar", "v3", credentials=credentials)


Names = ["Teodoro",
		 "Teo",
		]


Spotify = {"pause" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause",
		   "play" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play",
		   "next" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next",
		   "previous" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous",
		   "stop" : "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Stop"            
		}

Day_dict = {1: 'lunes', 2: 'martes',  
			3: 'miércoles', 4: 'jueves',  
			5: 'viernes', 6: 'sábado', 
			7: 'domingo'} 

Month_dict = {'01': 'enero', '02': 'febrero',
			  '03': 'marzo', '04': 'abril',
			  '05': 'mayo', '06': 'junio',
			  '07': 'julio', '08': 'agosto',
			  '09': 'septiembre', '10': 'octubre',
			  '11': 'noviembre', '12' : 'diciembre'}

Number_dict = {1: 'uno', 2: 'dos',  
			   3: 'tres', 4: 'cuatro',  
			   5: 'cinco', 6: 'seis', 
			   7: 'siete', 8: 'ocho',
			   9: 'nueve', 10: 'diez'} 

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
						audio = r.record(source, 10) 
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
	
	day = datetime.today().weekday() + 1
	today = datetime.today()
	number = str(today.date())
	
	#if day in Day_dict.keys(): 
	print(Day_dict[day]  + ". " + number) 
	speak("Hoy es " + Day_dict[day]  + ", " + number[-2:] + " de " + Month_dict[number[5:7]] + " de " + number[0:4]) 
  
  
def tellTime(): 
      
    t = str(datetime.now()) 
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
		sleep(1)
		t -= 1
		os.system("clear")
		
	os.system(Spotify["pause"])
	speak("Riiiiiiiiiing riiiiiiiiiing. Fin de la alarma de " + name)
	os.system(Spotify["play"])


def get_date_hours(date_input, time_format = "date"):

	date_obj = iso8601.parse_date(date_input)
	if time_format == "date":
		return date_obj.strftime('%H:%M del %d-%m-%Y ')
	elif time_format == "hours":
		return date_obj.strftime('%H:%M')
	elif time_format == "day_complete":
		return date_obj.strftime('%d-%m-%Y ')

def get_relative_events(duration, offset = 0, maxResults = 50):
	today = datetime.today()
	today = datetime.combine(today, datetime.min.time())
	today = today + relativedelta(days=offset)
	diff = today + relativedelta(days=duration)
	tmin = today.isoformat('T') + "Z"
	tmax = diff.isoformat('T') + "Z"
	eventsResult = service.events().list(
		calendarId='primary',
		timeMin=tmin,
		timeMax=tmax,
		maxResults=maxResults,
		singleEvents=True,
		orderBy='startTime',
	).execute()
	return eventsResult

def get_absolute_events(day_str, maxResults = 50):
	matches = list(datefinder.find_dates(day_str))
	day = matches[0]
	diff = day + relativedelta(days=1)
	tmin = day.isoformat('T') + "Z"
	tmax = diff.isoformat('T') + "Z"
	eventsResult = service.events().list(
		calendarId='primary',
		timeMin=tmin,
		timeMax=tmax,
		maxResults=maxResults,
		singleEvents=True,
		orderBy='startTime',
	).execute()
	return eventsResult


def Take_query(): 

	Hello() 
	os.system("clear")
	start = time()
	
	while(True): 
		
		end = time()
		if end-start > 120:
			os.system("clear")
			start = time()

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
		
		elif "alarma" in query:  # "(Pon una) alarma de '5 segundos/minutos/horas' de nombre 'Nombre'"
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
		

		elif ("eventos" in query) or ("calendario" in query): # "(Enséñame/muéstrame mis/mi) eventos/calendario para hoy/mañana/pasado mañana/'fecha'/esta-e/próxima-o/siguiente/X siguientes semana/semanas/mes/meses"
			start = time()
			list_of_words = query.split()

			if "semanas" in query:
				number = list_of_words[list_of_words.index("semanas") - 1]
				time_str = "las próximas " + number + " semanas"
				time_format = "date"
				key_list = list(Number_dict.keys())
				val_list = list(Number_dict.values())
				position = val_list.index(number)
				number = key_list[position]
				duration = 7*number
				eventsResult = get_relative_events(duration)

			elif "semana" in query:
				time_unit = list_of_words[list_of_words.index("semana") - 1]
				if time_unit == "esta":
					time_str = "esta semana"
					time_format = "date"
					duration = 7
					eventsResult = get_relative_events(duration)
				elif time_unit == "próxima" or time_unit == "siguiente":
					time_str = "la próxima semana"
					time_format = "date"
					duration = 7
					offset = 7
					eventsResult = get_relative_events(duration, offset)
			
			elif "meses" in query:
				number = list_of_words[list_of_words.index("meses") - 1]
				time_str = "los próximos " + number + " meses"
				time_format = "date"
				key_list = list(Number_dict.keys())
				val_list = list(Number_dict.values())
				position = val_list.index(number)
				number = key_list[position]
				duration = 30*number
				eventsResult = get_relative_events(duration)

			elif "mes" in query:
				time_unit = list_of_words[list_of_words.index("mes") - 1]
				if time_unit == "este":
					time_str = "este mes"
					time_format = "date"
					duration = 30
					eventsResult = get_relative_events(duration)
				elif time_unit == "próximo" or time_unit == "siguiente":
					time_str = "la próximo mes"
					time_format = "date"
					duration = 30
					offset = 30
					eventsResult = get_relative_events(duration, offset)

			else:
				time_unit = "para"
				if list_of_words[list_of_words.index(time_unit) + 1] == "hoy":
					time_str = "hoy"
					time_format = "hours"
					today = datetime.today()
					day_str = today.strftime("%m-%d-%Y")
					eventsResult = get_absolute_events(day_str)
				elif list_of_words[list_of_words.index(time_unit) + 1] == "mañana":
					time_str = "mañana"
					time_format = "hours"
					today = datetime.today()
					day_str = today + timedelta(days=1)
					day_str = day_str.strftime("%m-%d-%Y")
					eventsResult = get_absolute_events(day_str)
				elif list_of_words[list_of_words.index(time_unit) + 1] == "pasado":
					time_str = "pasado mañana"
					time_format = "hours"
					today = datetime.today()
					day_str = today + timedelta(days=2)
					day_str = day_str.strftime("%m-%d-%Y")
					eventsResult = get_absolute_events(day_str)
				else:
					day = list_of_words[list_of_words.index(time_unit) + 2]
					try:
						month = list_of_words[list_of_words.index(time_unit) + 4]
					except:
						today = datetime.today()
						month = today.month
					try:
						year = list_of_words[list_of_words.index(time_unit) + 6]
					except:
						today = datetime.today()
						year = today.year
					time_str = "el día " + str(day) + " de " +  str(month) + " de " + str(year)
					time_format = "hours"
					key_list = list(Month_dict.keys())
					val_list = list(Month_dict.values())
					position = val_list.index(month)
					month = key_list[position]
					day_str = str(month) + "/" + str(day) + "/" + str(year)
					eventsResult = get_absolute_events(day_str)

			if eventsResult['items']:
				speak("Tus eventos para " + time_str + " son:")
				for event in eventsResult['items']:
					if 'dateTime' in event['start'].keys():
						print("   -" + event['summary'] + " a las " + get_date_hours(event['start']['dateTime'], time_format))
					else:
						print("   -" + event['summary'] + " el día " + get_date_hours(event['start']['date'], 'day_complete'))
			else:
				speak("No tienes ningún evento para " + time_str)


			

		
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
