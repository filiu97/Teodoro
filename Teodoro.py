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
				calendarsid_file = "CalendarsID.txt",
				commands_file = "Commands.txt"):

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
		
		file = open(commands_file)
		self.Commands = eval(file.read())

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
		
		if bool([match for match in Teo.Commands["Name"] if(match in query)]): 
			n = str()
			for name in Teo.Names:
				n += name + ", o "
			Teo.speak("Me puedes llamar " + n[:-2] + ", tu asistente fiel")
		
		elif bool([match for match in Teo.Commands["Greetings"] if(match in query)]):
			Teo.Hello()
		
		elif bool([match for match in Teo.Commands["Cheer up"] if(match in query)]):
			Teo.speak("Venga señor, no pasa nada, aquí está Teodoro para servirle")

		elif bool([match for match in Teo.Commands["Today"] if(match in query)]): 
			Teo.tellDay()
		
		elif bool([match for match in Teo.Commands["Time"] if(match in query)]): 
			Teo.tellTime()
		
		elif bool([match for match in Teo.Commands["Google"] if(match in query)]):
			Teo.google(query)

		elif bool([match for match in Teo.Commands["Wikipedia"] if(match in query)]): 
			response = Teo.wikipedia(query)
			if response is None:
				Teo.speak("No se ha podido encontrar la página solicitada")

		elif bool([match for match in Teo.Commands["Play"] if(match in query)]):
			Teo.spotify("play")
		
		elif bool([match for match in Teo.Commands["Next"] if(match in query)]):
			Teo.spotify("next")
		
		elif bool([match for match in Teo.Commands["Previous"] if(match in query)]):
			Teo.spotify("previous")
		
		elif bool([match for match in Teo.Commands["Pause"] if(match in query)]):
			Teo.spotify("pause")
		
		elif bool([match for match in Teo.Commands["Stop"] if(match in query)]):
			Teo.spotify("stop")
			
		elif bool([match for match in Teo.Commands["Weather"] if(match in query)]):
			Teo.weather(query)
		
		elif bool([match for match in Teo.Commands["Alarm"] if(match in query)]):  # "(Pon una) alarma de '5 segundos/minutos/horas' de nombre 'Nombre'"
			Teo.alarm(query)
		
		elif bool([match for match in Teo.Commands["GetCalendar"] if(match in query)]): # "(Enséñame/muéstrame mis/mi) eventos/calendario/tareas para hoy/mañana/pasado mañana/'fecha'/esta-e/próxima-o/siguiente/X siguientes semana/semanas/mes/meses"
			Teo.getCalendar(query)
			
		elif bool([match for match in Teo.Commands["Shutdown"] if(match in query)]):
			Teo.shutdown()

		elif bool([match for match in Teo.Commands["Suspend"] if(match in query)]):
			Teo.suspend()
		
		elif bool([match for match in Teo.Commands["Del"] if(match in query)]): 
			del Teo

				
if __name__ == '__main__': 

	Teo = Teodoro()

	Take_query(Teo)
