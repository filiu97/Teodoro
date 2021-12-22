#! /usr/bin python3

from Applications import Applications
from Calendar import Calendar
from System import System

from datetime import datetime, timedelta
import os
import sys
from time import sleep, time
import threading


class Teodoro(System, Applications, Calendar):
	
	def __init__(self,
				bdc_path = "BdC/",
				names_file = "Names.txt",
				spotify_file = "Spotify.txt",
				days_file = "Days.txt", 
				months_file = "Months.txt",
				numbers_file = "Numbers.txt",
				calendarsid_file = "CalendarsID.txt",
				commands_file = "Commands.txt",
				del_speak = True):

		self.Names = open(bdc_path + names_file).read().splitlines()
		self.SpotifyActions = {}
		file = open(bdc_path + spotify_file)
		for line in file:
			key, value = line.rstrip("\n").split("_")
			self.SpotifyActions[key] = value
		self.Days = {}
		file = open(bdc_path + days_file)
		for line in file:
			key, value = line.rstrip("\n").replace(" ", "").split(":")
			self.Days[key] = value
		self.Months = {}
		file = open(bdc_path + months_file)
		for line in file:
			key, value = line.rstrip("\n").replace(" ", "").split(":")
			self.Months[key] = value
		
		file = open(bdc_path + commands_file)
		self.Commands = eval(file.read())

		self.del_speak = del_speak

		System.__init__(self)
		Applications.__init__(self, self.SpotifyActions)
		Calendar.__init__(self, bdc_path, calendarsid_file, numbers_file, self.Months)

	def __del__(self):
		if self.del_speak:
			self.speak("Adiós señor, que tenga un buen día")
			sys.exit() 

	def tellNames(self):
		n = str()
		text = str()
		for name in self.Names:
			n += name + ", o "
			text += name + "\n"
		speech = "Me puedes llamar " + n[:-2] + ", tu asistente fiel"
		return speech, text

	def Hello(self, window = None): 
		if window is not None:
			self.GUI("Close", prev_window=window)
		self.speak("Hola señor, aquí estoy para lo que necesite.")
		
	def tellDay(self):
		day = str(datetime.today().weekday() + 1)
		today = datetime.today()
		number = str(today.date())
		speech = "Hoy es " + self.Days[day]  + ", " + number[-2:] + " de " + self.Months[number[5:7]] + " de " + number[0:4]
		text = self.Days[day] + ", " +  number[-2:] + " de\n" + self.Months[number[5:7]] + " de " + number[0:4]
		return speech, text
	
	def tellTime(self): 
		t = datetime.now() 
		text = t.strftime('%H:%M')
		t = str(t)
		hour = t[11:13] 
		minutes = t[14:16] 
		speech = "Son las" + hour + "horas y" + minutes + "minutos"
		return speech, text  

	def getAction(self, query, window = None):

		if bool([match for match in self.Commands["Name"] if(match in query)]): 
			speech, text = self.tellNames()
			self.speak(speech) 
			self.GUI("Show", text = text, prev_window = window)
			return None
		
		elif bool([match for match in self.Commands["Greetings"] if(match in query)]):	
			self.Hello(window)
			return None
		
		elif bool([match for match in self.Commands["Cheer up"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			self.speak("Ánimo señor, no se preocupe")
			return None

		elif bool([match for match in self.Commands["Secret"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)
			
			self.voiceEngine.setProperty('voice', self.defaultWisperVoice)
			self.speak("""En realidad, soy un extraterreste en misión oficial,
			para poder estudiar a los humanos y observar su comportamiento""")
			self.voiceEngine.setProperty('voice', self.defaultVoice)
			
			return None

		elif bool([match for match in self.Commands["Today"] if(match in query)]): 
			speech, text = self.tellDay()
			self.speak(speech) 
			self.GUI("Show", text = text, prev_window = window)
			return None
		
		elif bool([match for match in self.Commands["Time"] if(match in query)]): 
			speech, text = self.tellTime()
			self.speak(speech)
			self.GUI("Show", text = text, prev_window = window) 
			return None
		
		elif bool([match for match in self.Commands["Google"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			self.google(query)
			return None

		elif bool([match for match in self.Commands["Wikipedia"] if(match in query)]): 
			if window is not None:
				self.GUI("Close", prev_window=window)

			response = self.wikipedia(query)
			if response is None:
				self.speak("No se ha podido encontrar la página solicitada")
			return None

		elif bool([match for match in self.Commands["Youtube"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)
				
			self.youtube(query)
			return None

		elif bool([match for match in self.Commands["Play"] if(match in query)]):
			self.spotify("play", window)
			return None
		
		elif bool([match for match in self.Commands["Next"] if(match in query)]):
			self.spotify("next", window)
			return None
		
		elif bool([match for match in self.Commands["Previous"] if(match in query)]):
			self.spotify("previous", window)
			return None
		
		elif bool([match for match in self.Commands["Pause"] if(match in query)]):
			self.spotify("pause", window)
			return None
		
		elif bool([match for match in self.Commands["Stop"] if(match in query)]):
			self.spotify("stop", window)
			return None

		elif bool([match for match in self.Commands["Song"] if(match in query)]):
			speech, text = self.spotify("song")
			self.speak(speech)
			self.GUI("Show", text = text, size = 16, prev_window = window) 
			return None
			
		elif bool([match for match in self.Commands["Weather"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			speech, image = self.weather(query)
			self.speak(speech)
			os.system("display " + image + ".png")
			# self.GUI("Image", image = image + ".png", geometry = "1750X1000", prev_window = window)
			return None
		
		elif bool([match for match in self.Commands["Alarm"] if(match in query)]):  # "(Pon una) alarma de '5 segundos/minutos/horas' de nombre 'Nombre'"
			if window is not None:
				self.GUI("Close", prev_window=window)

			t, speech, text = self.setAlarm(query)
			timer = threading.Timer(t, self.alarm(speech, text))
			timer.start()
			return None
		
		elif bool([match for match in self.Commands["GetCalendar"] if(match in query)]): # "(Enséñame/muéstrame mis/mi) eventos/calendario/tareas para hoy/mañana/pasado mañana/'fecha'/esta-e/próxima-o/siguiente/X siguientes semana/semanas/mes/meses"
			speech, text = self.getCalendar(query)
			if speech != None:
				self.speak(speech)
				self.GUI("GetCalendar", text = text, size = 12, geometry = "800x200", prev_window = window)
			else:
				self.speak("Credenciales actualizadas")
			return None

		elif bool([match for match in self.Commands["SetCalendar"] if(match in query)]): # "Crear/crea/creame/hacer/haz/hazme un evento para hoy/mañana/pasado mañana/'fecha' a las X de nombre X "
			self.setCalendar(query, window)
			return None
			
		elif bool([match for match in self.Commands["Shutdown"] if(match in query)]):
			self.shutdown()
			return None

		elif bool([match for match in self.Commands["Suspend"] if(match in query)]):
			self.suspend()
			return None
		
		elif bool([match for match in self.Commands["Restart"] if(match in query)]):
			self.restart()
			return None

		elif bool([match for match in self.Commands["Nothing"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			self.voiceEngine.setProperty('voice', self.defaultWisperVoice)
			self.speak("Vale, aquí no ha pasado nada")
			self.voiceEngine.setProperty('voice', self.defaultVoice)
			return None
		
		elif bool([match for match in self.Commands["Del"] if(match in query)]): 
			del self
			return None

		else:
			self.speak("Lo siento, no te he entendido")
			return -1
		
		
def takeQuery(Teo): 

	Teo.Hello() 
	os.system("clear")
	
	while(True): 

		query, window = Teo.takeCommand()
		if query is not None:
			query = query.lower()
			response = Teo.getAction(query, window)
			if response is not None:
				Teo.speak("¿Puede repetir su petición?")
				query = Teo.repeat()
				Teo.getAction(query)
		
				
if __name__ == '__main__': 
	Teo = Teodoro()
	takeQuery(Teo)
