#! /usr/bin python3

from Applications import Applications
from Calendar import Calendar
from System import System

from datetime import datetime, timedelta
import os
import sys
from time import sleep, time



class Teodoro(System, Applications, Calendar):
	
	def __init__(self, names_file = "Names.txt",
				spotify_file = "Spotify.txt",
				days_file = "Days.txt", 
				months_file = "Months.txt",
				numbers_file = "Numbers.txt",
				calendarsid_file = "CalendarsID.txt"):

		self.Names = open(names_file).read().splitlines()
		self.SpotifyActions = {}
		file = open(spotify_file)
		for line in file:
			key, value = line.rstrip("\n").split(":")
			self.SpotifyActions[key] = value
		self.Days = {}
		file = open(days_file)
		for line in file:
			key, value = line.rstrip("\n").replace(" ", "").split(":")
			self.Days[key] = value
		self.Months = {}
		file = open(months_file)
		for line in file:
			key, value = line.rstrip("\n").replace(" ", "").split(":")
			self.Months[key] = value

		System.__init__(self)
		Applications.__init__(self, self.SpotifyActions)
		Calendar.__init__(self, calendarsid_file, numbers_file, self.Months)

	def __del__(self):
		self.speak("Adiós señor, que tenga un buen día")
		sys.exit() 

	def Hello(self): 
		self.speak("Hola señor, aquí estoy para lo que necesite.")
			
	def tellDay(self):
		day = str(datetime.today().weekday() + 1)
		today = datetime.today()
		number = str(today.date())
		print(self.Days[day]  + ". " + number) 
		self.speak("Hoy es " + self.Days[day]  + ", " + number[-2:] + " de " + self.Months[number[5:7]] + " de " + number[0:4]) 
	
	def tellTime(self): 
		t = datetime.now() 
		print(t.strftime('%H:%M')) 
		t = str(t)
		hour = t[11:13] 
		minutes = t[14:16] 
		self.speak("Son las" + hour + "horas y" + minutes + "minutos")     
		
		
def Take_query(Teo): 

	Teo.Hello() 
	os.system("clear")
	start = time()
	
	while(True): 
		
		end = time()
		if end-start > 120:
			os.system("clear")
			start = time()

		query = Teo.takeCommand().lower() 
		
		if ("cómo te llamas" in query) or ("cómo te puedo llamar" in query): 
			n = str()
			for name in Teo.Names:
				n += name + ", o "
			Teo.speak("Me puedes llamar " + n[:-2] + ", tu asistente fiel")
		
		elif ("hola" == query.replace(" ", "")) or ("qué tal" in query):
			Teo.Hello()
		
		elif "anímame" in query:
			Teo.speak("Venga señor, no pasa nada, aquí está Teodoro para servirle")

		elif "qué día es hoy" in query: 
			Teo.tellDay()
		
		elif "qué hora es" in query: 
			Teo.tellTime()
		
		elif "busca en google" in query:
			Teo.google(query)

		elif "busca en wikipedia" in query: 
			response = Teo.wikipedia(query)
			if response is None:
				Teo.speak("No se ha podido encontrar la página solicitada")

		elif "pon la música" in query:
			Teo.spotify("play")
		
		elif "pasa de canción" in query or "siguiente canción" in query:
			Teo.spotify("next")
		
		elif "anterior canción" in query:
			Teo.spotify("previous")
		
		elif "para la música" in query or "para spotify" in query:
			Teo.spotify("pause")
		
		elif "cierra spotify" in query or "quita la música" in query:
			Teo.spotify("stop")
			
		elif "tiempo hace" in query:
			Teo.weather(query)
		
		elif "alarma" in query:  # "(Pon una) alarma de '5 segundos/minutos/horas' de nombre 'Nombre'"
			Teo.alarm(query)
		
		elif ("eventos" in query) or ("calendario" in query) or ('tareas' in query): # "(Enséñame/muéstrame mis/mi) eventos/calendario/tareas para hoy/mañana/pasado mañana/'fecha'/esta-e/próxima-o/siguiente/X siguientes semana/semanas/mes/meses"
			Teo.getCalendar(query)
			
		elif "apaga el ordenador" in query:
			Teo.shutdown()

		elif ("suspende el ordenador" in query) or ("suspensión" in query):
			Teo.suspend()
		
		elif ("apágate" in query) or ("adiós" in query): 
			del Teo

				
if __name__ == '__main__': 

	Teo = Teodoro()

	Take_query(Teo)
