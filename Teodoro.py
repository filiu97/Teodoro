#! /usr/bin python3

from Applications import Applications
from Calendar import Calendar
from System import System

from datetime import datetime, timedelta
import os
import sys
from time import process_time, sleep, time
import threading
from pymongo import MongoClient
import gridfs
import base64
from io import BytesIO
from PIL import Image
import socket
import webbrowser 


class Teodoro(System, Applications, Calendar):
	
	def __init__(self,
				mongo_key = "mongodb+srv://filiu:teodoro@teodoro.ocpsz.mongodb.net/KnowledgeBase?retryWrites=true&w=majority",
				del_speak = True):
		

		self.client = MongoClient(mongo_key)
		self.db = self.client.KnowledgeBase
		self.fs = gridfs.GridFS(self.db)

		self.general = []
		for collection in self.db.list_collection_names():
			if collection == "General":
				for element in self.db[collection].find({}):
					self.general.append(element)

		self.Names = self.general[0]["Names"]

		keys = []
		for i in range(len(self.general[0]["Time"]["Days"])):
			keys.append(str(i+1))
		self.Days = dict(zip(keys,self.general[0]["Time"]["Days"]))

		keys = []
		for i in range(len(self.general[0]["Time"]["Months"])):
			keys.append(str(i+1))
		self.Months = dict(zip(keys,self.general[0]["Time"]["Months"]))
	
		self.Numbers = self.general[0]["Numbers"]

		self.Commands = self.general[1]["Commands"]

		self.users = []
		for collection in self.db.list_collection_names():
			if collection == "Users":
				for element in self.db[collection].find({}):
					self.users.append(element)
		self.User = self.users[0]["Nombre"]

		self.applications = []
		for collection in self.db.list_collection_names():
			if collection == "Applications":
				for element in self.db[collection].find({}):
					self.applications.append(element)
        
		self.SpotifyActions = self.applications[0]["SpotifyActions"]
		self.MathOperations = self.applications[0]["MathOperations"]

		self.calendar = []
		for collection in self.db.list_collection_names():
			if collection == "Calendar":
				for element in self.db[collection].find({}):
					self.calendar.append(element)
		
		self.CalendarsID = self.calendar[0]["CalendarsID"]

		self.del_speak = del_speak

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(("",50000))
		self.sock.setblocking(0)
		self.macroTeodoro = "https://trigger.macrodroid.com/66e970ab-dfed-4d8a-9e54-00ecf148d064/Teodoro"
		webbrowser.open(self.macroTeodoro)

		System.__init__(self)
		Applications.__init__(self, self.SpotifyActions, self.MathOperations, self.Numbers)
		Calendar.__init__(self, self.CalendarsID, self.Numbers, self.Months)

	def __del__(self):
		if self.del_speak:
			self.speak("Adiós " + self.User + ", que tenga un buen día")
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
		self.speak("Hola " + self.User + ", aquí estoy para lo que necesite.")
		
	def tellDay(self):
		day = str(datetime.today().weekday() + 1)
		today = datetime.today()
		number = str(today.date())
		speech = "Hoy es " + self.Days[day]  + ", " + number[-2:] + " de " + self.Months[number[6:7]] + " de " + number[0:4]
		text = self.Days[day] + ", " +  number[-2:] + " de\n" + self.Months[number[6:7]] + " de " + number[0:4]
		return speech, text
	
	def tellTime(self): 
		t = datetime.now() 
		text = t.strftime('%H:%M')
		t = str(t)
		hour = t[11:13] 
		minutes = t[14:16] 
		speech = "Son las" + hour + "horas y" + minutes + "minutos"
		return speech, text  
		
	def actionUser(self, action, name2find, name):
		if action == "new":
			self.db["Users"].insert_one(name2find)
			speech = "Nuevo usuario creado"
			text = "Nuevo usuario de nombre: " + name + " creado correctamente"
		elif action == "change":
			self.User = self.db["Users"].find_one(name2find)["Nombre"]
			speech = "Cambio de usuario realizado"
			text = "Nuevo usuario: " + name
		elif action == "remove":
			self.db["Users"].delete_one(name2find)
			speech = "Usuario borrado"
			text = "Usuario: " + name + " borrado"
		return speech, text
	
	def newUserInfo(self, field, attribute):
		name2find = { "Nombre": self.User }
		newvalues = { "$set": { field : attribute } }
		self.db["Users"].update_one(name2find, newvalues)
		speech = "Nueva información guardada"
		text = "Información: " + field + ":" + attribute + " guardada"
		return speech, text


	def getAction(self, query, window = None):

		if bool([match for match in self.Commands["Name"] if(match in query)]): 
			speech, text = self.tellNames()
			self.speak(speech) 
			self.GUI("Show", text = text, prev_window = window)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Greetings"] if(match in query)]):	
			self.Hello(window)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Cheer up"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			self.speak("Ánimo" + self.User + ", no se preocupe")
			response = 0
			return response

		elif bool([match for match in self.Commands["Secret"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)
			
			self.voiceEngine.setProperty('voice', self.defaultWisperVoice)
			self.speak("""En realidad, soy un extraterreste en misión oficial,
			para poder estudiar a los humanos y observar su comportamiento""")
			self.voiceEngine.setProperty('voice', self.defaultVoice)
			response = 0
			return response

		elif bool([match for match in self.Commands["Today"] if(match in query)]): 
			speech, text = self.tellDay()
			self.speak(speech) 
			self.GUI("Show", text = text, prev_window = window)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Time"] if(match in query)]): 
			speech, text = self.tellTime()
			self.speak(speech)
			self.GUI("Show", text = text, prev_window = window) 
			response = 0
			return response

		elif bool([match for match in self.Commands["Users"] if(match in query)]):
			list_of_words = query.split()
			name = list_of_words[list_of_words.index("nombre") + 1]
			name2find = {"Nombre": name}
			if "nuevo" in list_of_words:
				action = "new"
			elif "cambiar" in list_of_words:
				action = "change"
			elif "eliminar" in list_of_words or "borrar" in list_of_words:
				action = "remove"
			speech,text = self.actionUser(action, name2find, name)
			self.speak(speech)
			self.GUI("Show", text = text, prev_window = window)
			response = 0
			return response

		elif bool([match for match in self.Commands["NewInformation"] if(match in query)]):
			self.speak("Perfecto, dime primero cómo vamos a llamar esta nueva información")
			field, window = self.repeat()
			if isinstance(field, tuple):
				field = " ".join(field)
			self.speak("Bien, y ahora dime qué quieres que apunte sobre " + field)
			attribute, window = self.repeat()
			if isinstance(attribute, tuple):
				attribute = " ".join(attribute)
			speech, text = self.newUserInfo(field, attribute)
			self.speak(speech)
			self.GUI("Show", text = text, prev_window = window)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Information"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)
			
			try:
				image = self.fs.find_one({"filename" : self.User})
				bytedata = image.read()
				ima_IO = BytesIO(base64.b64decode(bytedata))
				img_PIL = Image.open(ima_IO)
				img_PIL.show()
			except:
				self.speak("Parece que no tienes una foto asociada a tu usuario")

			info = self.db["Users"].find_one({"Nombre": self.User})
			info.pop("_id")
			self.speak("Lo que sé de ti es: ")
			for k, v in info.items():
				self.speak(k + v)
			response = 0
			return response

		elif bool([match for match in self.Commands["ChangeVoice"] if(match in query)]):
			self.speak("Perfecto. Tiene " + str(Teo.maxVoices) + "voces para poder elegir")
			speech, text = self.changeVoice()
			self.speak(speech)
			self.GUI("Show", text = text, prev_window = window) 
			response = 0
			return response

		elif bool([match for match in self.Commands["Google"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			self.google(query)
			response = 0
			return response

		elif bool([match for match in self.Commands["Wikipedia"] if(match in query)]): 
			if window is not None:
				self.GUI("Close", prev_window=window)

			response = self.wikipedia(query)
			if response is None:
				self.speak("No se ha podido encontrar la página solicitada")
			response = 0
			return response

		elif bool([match for match in self.Commands["Youtube"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)
				
			self.youtube(query)
			response = 0
			return response

		elif bool([match for match in self.Commands["Play"] if(match in query)]):
			response = self.spotify("play", window)
			if response == 256:
				self.speak("Ha habido algún problema con Spotify")
			return response
		
		elif bool([match for match in self.Commands["Next"] if(match in query)]):
			response = self.spotify("next", window)
			if response == 256:
				self.speak("Ha habido algún problema con Spotify")
			return response
		
		elif bool([match for match in self.Commands["Previous"] if(match in query)]):
			self.spotify("previous", window)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Pause"] if(match in query)]):
			self.spotify("pause", window)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Stop"] if(match in query)]):
			self.spotify("stop", window)
			response = 0
			return response

		elif bool([match for match in self.Commands["Song"] if(match in query)]):
			speech, text = self.spotify("song")
			self.speak(speech)
			self.GUI("Show", text = text, size = 16, prev_window = window) 
			response = 0
			return response
			
		elif bool([match for match in self.Commands["Weather"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			speech, image = self.weather(query)
			self.speak(speech)
			os.system("display " + image + ".png")
			# self.GUI("Image", image = image + ".png", geometry = "1750X1000", prev_window = window)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Alarm"] if(match in query)]):  # "(Pon una) alarma de '5 segundos/minutos/horas' de nombre 'Nombre'"
			if window is not None:
				self.GUI("Close", prev_window=window)

			t, speech, text = self.setAlarm(query)
			timer = threading.Timer(t, self.alarm, args=(speech, text))
			timer.start()
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Reminder"] if(match in query)]):  # "(Crea un) recordatorio de nombre 'Nombre' para el 'Día' a las 'Hora'"
			speech, text = self.setReminder(query)
			self.speak(speech)
			self.GUI("Show", text = text, size = 16, prev_window = window) 
			response = 0
			return response

		elif bool([match for match in self.Commands["Math"] if(match in query)]):  # "Cuánto da/Cuánto es/Calcula/Calcular/Calcúlame *operación matemática como suena*"
			list_of_words = query.split()
			operation = None
			for key in self.MathOperations.keys():
				if self.MathOperations[key]["keyword"] in query:
					operation = self.MathOperations[key]["operation"]
					if self.MathOperations[key]["keyword"] == "elevado":
						number_1 = list_of_words[list_of_words.index("elevado") - 1]
						if list_of_words[list_of_words.index("elevado") + 2] == "cuadrado":
							number_2 = "2"
						elif list_of_words[list_of_words.index("elevado") + 2] == "cubo":
							number_2 = "3"
						else:
							number_2 = list_of_words[list_of_words.index("elevado") + 2]
					elif self.MathOperations[key]["keyword"] == "raíz cuadrada" or self.MathOperations[key]["keyword"] == "raíz cúbica":
						number_1 = list_of_words[list_of_words.index("raíz") + 3]
						number_2 = "-1"
					else:
						number_1 = list_of_words[list_of_words.index(self.MathOperations[key]["keyword"]) - 1]
						number_2 = list_of_words[list_of_words.index(self.MathOperations[key]["keyword"]) + 1]
			if operation == None:
				self.speak("Lo siento, no puedo realizar esa operación")
				response = 0
				return response
	
			key_list = list(self.Numbers.keys())
			val_list = list(self.Numbers.values())
			try:
				position = val_list.index(number_1)
				number_1 = int(key_list[position])
			except:
				number_1 = int(number_1)
			try:
				position = val_list.index(number_2)
				number_2 = int(key_list[position])
			except:
				number_2 = int(number_2)

			speech, text = self.mathOperation(operation, number_1, number_2)
			self.speak(speech)
			self.GUI("Show", text = text, size = 16, prev_window = window) 
			response = 0
			return response

		elif bool([match for match in self.Commands["Phone"] if(match in query)]): # Encuentra mi teléfono/móvil (y similares)
			if window is not None:
				self.GUI("Close", prev_window=window)
			speech = self.findPhone()
			self.speak(speech)
			response = 0
			return response

		elif bool([match for match in self.Commands["GetCalendar"] if(match in query)]): # "(Enséñame/muéstrame mis/mi) eventos/calendario/tareas para hoy/mañana/pasado mañana/'fecha'/esta-e/próxima-o/siguiente/X siguientes semana/semanas/mes/meses"
			speech, text = self.getCalendar(query)
			if speech == -1:
				self.GUI("Show", text="Petición incorrecta", prev_window=window)
				response = -1
			elif speech != None:
				self.speak(speech)
				self.GUI("GetCalendar", text = text, size = 12, geometry = "800x200", prev_window = window)
				response = 0
			else:
				self.speak("Credenciales actualizadas")
				response = 0
			return response

		elif bool([match for match in self.Commands["SetCalendar"] if(match in query)]): # "Crear/crea/creame/hacer/haz/hazme un evento para hoy/mañana/pasado mañana/'fecha' a las X de nombre X "
			response = self.setCalendar(query, window)
			return response
			
		elif bool([match for match in self.Commands["Shutdown"] if(match in query)]):
			self.shutdown()
			response = 0
			return response

		elif bool([match for match in self.Commands["Suspend"] if(match in query)]):
			self.suspend()
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Restart"] if(match in query)]):
			self.restart()
			response = 0
			return response

		elif bool([match for match in self.Commands["Nothing"] if(match in query)]):
			if window is not None:
				self.GUI("Close", prev_window=window)

			self.voiceEngine.setProperty('voice', self.defaultWisperVoice)
			self.speak("Vale, aquí no ha pasado nada")
			self.voiceEngine.setProperty('voice', self.defaultVoice)
			response = 0
			return response
		
		elif bool([match for match in self.Commands["Del"] if(match in query)]): 
			del self
			response = 0
			return response

		else:
			response = "Lo siento, no te he entendido"
			self.speak(response)
			return response
		
		
def takeQuery(Teo): 

	Teo.Hello() 
	os.system("clear")
	lastsave = 0
	
	while(True): 
		
		internetOk = Teo.internetCheck()
		if internetOk != 0:
			Teo.GUI("Show", text = internetOk)
			del Teo
		else:
			query, window = Teo.takeCommand()
			if query != None:
				query = query.lower()
				response = Teo.getAction(query, window)
				if response != 0:
					Teo.GUI("Close", prev_window = window)
					Teo.speak("¿Puede repetir su petición?")
					query, window = Teo.repeat()
					Teo.getAction(query, window)
			elif time() - lastsave > 60:
				speech, text = Teo.checkReminder()
				if speech != None:
					Teo.speak(speech)
					Teo.GUI("Show", text = text)
				Teo.checkPhone()
				lastsave = time()
		
				
if __name__ == '__main__':

	Teo = Teodoro()
	takeQuery(Teo)
	