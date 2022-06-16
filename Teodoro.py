#! /usr/bin python3

from Applications import Applications
from Calendar import Calendar
from System import System

from datetime import datetime, timedelta
import os
import sys
from time import time
import threading
from pymongo import MongoClient
import gridfs
import base64
from io import BytesIO
from PIL import Image
import socket
import webbrowser
import bcrypt


class Teodoro(System, Applications, Calendar):

    """ Clase Teodoro.

    Esta clase hereda de todas las demás para poder hacer uso de las funcionalidades 
    implementadas en las demás clases. Contiene las funcionalidades básicas de comunicación común con el
    usuario, además de contener el bucle de acción del sistema. Supone la clase principal del asistente, 
    en el que se inicia la base de conocimiento del asistente a través de la conexión con MongoDB.

    Funcionalidades:
        - Login del usuario.
        - Saludo.
        - Enunciado de los nombres por los que responde el asistente.
        - Enunciado del día actual.
        - Enunciado de la hora actual.
        - Acciones sobre los usuarios:
            > Crear nuevo.
            > Cambiar de usuario.
            > Eliminar usuario.
        - Incorporación de nueva información sobre el usuario actual.
        - Lógica de la ejecución de todas las funcionalidades del sistema.

    Args:
            - System (class): Superclase que contiene las funcionalidades relacionadas con el control del ordenador.
            - Applications (class): Superclase que contiene las funcionalidades relacionadas con el control de
            aplicación como búsquedas web, alarmas y recordatorios, control de la música, conexión con el teléfono...
            - Calendar (class): Superclase que contiene las funcionalidades relacionadas con el control del calendario
            del usuario.
    """

#   ******************  __init__ y __del__  ******************

    def __init__(self, default_name = "Teodoro", default_user = "filiu", del_speak = True):
        """
        Función de inicialización todos los atributos y parámetros de la clase Teodoro. Además, como esta clase
        es hija de otras clases, es en esta función de inicialización donde se instancia estas clases.
        En esta función se produce:
            - Extracción de la clave para acceder a la base de conocimiento en MongoDB.
            - Inicialización de la base de conocimiento.
            - Login del usuario.
            - Extracción de datos de la base de conocimiento.
                · General:
                    > Names.
                    > Time: 
                        * Days.
                        * Months.
                    > Numbers.
                    > Commands.
                · Applications:
                    > Spotify Actions.
                    > Math Operations.
            - Inicialización de las funcionalidades asociadas al teléfono móvil del usuario.
            - Instanciación de las superclases de las que hereda la clase Teodoro.

        Args:
            default_name (str, optional): El nombre del asistente por defecto del sistema. Defaults to "Teodoro".
            default_user (str, optional): El nombre del usuario por defecto del sistema. Defaults to "filiu".
            del_speak (bool, optional): Flag para permitir la salida de audio al terminar la ejecución del sistema. Defaults to True.
        """
        # Recepción argumentos
        self.del_speak = del_speak
        self.default_user = default_user
        self.default_name = default_name

        # Extracción de la clave de la base de conocimiento de MongoDB.
        # Debe estar guardada en un archivo oculto del sistema de nombre "MongoDBKey"
        file = open(".MongoDBKey", 'r')
        mongo_key = file.read()
        file.close()

        # Inicialización de la base de conocimiento
        self.client = MongoClient(mongo_key)
        self.db = self.client.KnowledgeBase
        self.fs = gridfs.GridFS(self.db)

        # Definición de campos del usuario por defecto
        self.__defaultUser = "usuario"
        self.__defaultSalt = "$2b$12$rPkLBpwSB34yL8nrlg21uu"
        self.__defaultHash = "$2b$12$rPkLBpwSB34yL8nrlg21uuqHjoeJdQheW6dtnYggqvUbvJFRZ0T/C"
        self.__CalendarsID = {"personal": None, "trello": None}
        self.__PhoneFunctions = False

        # Proceso de *Login* del usuario
        self.Login(self.default_user)

        # Obtención de datos de la base de conocimiento
        response = self.ExtractKnowledgeBase(self.default_name)

        # Errores por falta de información en la Base de Conocimiento
        if response == -1:
            self.__del__()
        elif response == 1:
            self.GUI("Show", text="Funcionalidad 'Today' no disponible.\nCompruebe la Base de Concimiento")
        elif response == 2:
            self.GUI("Show", text="Funcionalidades 'Today', 'getCalendar'\n y 'setCalendar' no disponibles.\nCompruebe la Base de Concimiento")
        elif response == 3:
            self.GUI("Show", text="Funcionalidades 'Reminder', 'Math', \n'getCalendar' y 'setCalendar'.\nCompruebe la Base de Concimiento")
        elif response == 4:
            self.GUI("Show", text="Funcionalidades de control de Spotify\n no disponibles.\n Compruebe la Base de Conocimiento")
        elif response == 5:
            self.GUI("Show", text="Funcionalidades 'Math' no disponible.\nCompruebe la Base de Concimiento")

        # Frases de error
        self.Error = "Usted no tiene permiso \npara acceder a estas funcionalidades"
        self.SpotifyError = "Ha habido algún \nproblema con Spotify"

        # Instanciación de las superclases de las que hereda la clase Teodoro
        System.__init__(self)  # System
        Applications.__init__(self, self.SpotifyActions, self.MathOperations, self.Numbers)  # Applications
        Calendar.__init__(self, self.CalendarsID, self.Numbers, self.Months)  # Calendar

    def __del__(self):
        """
        Función destructor de la clase Teodoro. En ella se comprueba si Teodoro está autorizado a emitir una frase de despedida o no, 
        y se termina el programa.
        """
        if self.del_speak:
            self.speak("Adiós " + self.User + ", que tenga un buen día")
        sys.exit()


#   ******************  Login  ******************

    def Login(self, default_user, first = True):
        """
        Función que realiza la lógica de inicio de un usuario

        Args:
            default_user (str): Nombre del usuario por defecto
            first (boolean, optional): Flag que indica si el login se realiza el principio del programa o no. Defaults to True.
        Returns:
            speech (str): Cadena de texto que contiene la frase que debe pronunciar el sistema.
            text (str): Cadena de texto que contiene la frase que debe mostrar el sistema.
        """
        name, password, phone = self.GUI("Login", text = default_user)
        try:
            info = self.db["Users"].find_one(
                {"nombre": name}, {"_id": 0, "_salt": 1, "_hash": 1})
            mySalt = info["_salt"].encode('utf-8')
            myHash = info["_hash"].encode('utf-8')
            password = password.encode('utf-8')
            newHash = bcrypt.hashpw(password, mySalt)
            if myHash == newHash:
                self.GUI(
                    "Show", "Inicialización correcta.\nBienvenido " + name + "!")
                self.User = name
                info = self.db["Users"].find_one(
                    {"nombre": name}, {"_id": 0, "_CalendarsID": 1, "_PhoneFunctions": 1})
                self.CalendarsID = info["_CalendarsID"]
                self.PhoneFunctions = info["_PhoneFunctions"]
            elif first == True:
                self.User = self.__defaultUser
                self.GUI("Show", "Has inicializado como \n " +
                        self.User + ".\nBienvenido!")
                info = self.db["Users"].find_one(
                    {"nombre": self.User}, {"_id": 0, "_CalendarsID": 1, "_PhoneFunctions": 1})
                self.CalendarsID = info["_CalendarsID"]
                self.PhoneFunctions = info["_PhoneFunctions"]
            else:
                speech = "No se ha podido realizar el cambio de usuario"
                text = "Operación denegada"
                return speech, text
        except:
            if first == True:
                self.User = self.__defaultUser
                self.GUI("Show", "Has inicializado como \n " +
                        self.User + ".\nBienvenido!")
                info = self.db["Users"].find_one(
                    {"nombre": self.User}, {"_id": 0, "_CalendarsID": 1, "_PhoneFunctions": 1})
                self.CalendarsID = info["_CalendarsID"]
                self.PhoneFunctions = info["_PhoneFunctions"]
            else:
                speech = "No se ha podido realizar el cambio de usuario"
                text = "Operación denegada"
                return speech, text

         # Inicialización de las funcionalides relacionadas con el teléfono móvil del usuario
        if phone.get() and self.PhoneFunctions:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(("", 50000))
            self.sock.setblocking(0)
            # Macro de inicialización
            self.macroTeodoro = "https://trigger.macrodroid.com/66e970ab-dfed-4d8a-9e54-00ecf148d064/Teodoro"
            webbrowser.open(self.macroTeodoro)


#   ******************  Extracción de información básica de la Base de Conocimiento  ******************

    def ExtractKnowledgeBase(self, default_name):
        """
        Función que extrae la información básica de la base de conocimiento para el correcto funcionamiento del sistema.
        En concreto, extrae información de las colecciones:
            - *General*:
                > *Names*. Si no existe, el programa pone como nombre por defecto "Teodoro".
                > *Days*. Si no existe, funcionalidad *Today* no disponible.
                > *Months*. Si no existe, funcionalidades *Today*, *getCalendar* y *setCalendar* no disponibles.
                > *Numbers*. Si no existe, funcionalidades *Reminder*, *Math*, *getCalendar* y *setCalendar* no disponibles.
                > *Commands*. Si no existe, se termina la ejecución del programa.
            - *Applications*:
                > *SpotifyActions*. Si no existe, funcionalidades relacionadas con Spotify no disponibles.
                > *MathOperations*. Si no existe, funcionalidad *Math* no disponible.

        Args:
            default_name (str): El nombre del asistente por defecto del sistema.

        Returns:
            response (int): Variable de verificación de ejecución correcta.
        """
        # General
        general = []
        for collection in self.db.list_collection_names():
            if collection == "General":
                for element in self.db[collection].find({}):
                    general.append(element)
        common = general[0]
        commands = general[1]

        # Names
        if "Names" in common:
            self.Names = common["Names"]  
        else:
            self.Names = default_name

        response = 0 # Por defecto, no hay ningún fallo en la Base de Conocimiento
            
        # Days and Months
        keys = []
        for i in range(len(common["Time"]["Days"])):
            keys.append(str(i+1))
        if "Days" in common["Time"]:
            self.Days = dict(zip(keys, common["Time"]["Days"]))
        else:
            self.Days = None
            response = 1
        keys = []
        for i in range(len(common["Time"]["Months"])):
            keys.append(str(i+1))
        if "Months" in common["Time"]:
            self.Months = dict(zip(keys, common["Time"]["Months"])) 
        else:
            self.Months = None
            response = 2

        # Numbers
        if "Numbers" in common:
            self.Numbers = common["Numbers"]  
        else:
            self.Numbers = None
            response = 3

        # Commands
        if "Commands" in commands:
            self.Commands = commands["Commands"]  
        else:
            response = -1

        # Applications
        applications = []
        for collection in self.db.list_collection_names():
            if collection == "Applications":
                for element in self.db[collection].find({}):
                    applications.append(element)

        # Spotify Actions
        if "SpotifyActions" in applications[0]:
            self.SpotifyActions = applications[0]["SpotifyActions"]
        else:
            self.SpotifyActions = None
            response = 4
        
        # Math Operations
        if "MathOperations" in applications[0]:
            self.MathOperations = applications[0]["MathOperations"]
        else:
            self.MathOperations = None
            response = 5
        
        return response


#   ******************  Funcionalides de comunicación comunes  ******************

    def Hello(self, window = None):  
        """        
        Función que pronuncia el mensaje de bienvenida al sistema.

        Args:
            window (tkinter.Tk, optional): Ventana de la interfaz de usuario. Defaults to None.
        """
        if window is not None:
            self.GUI("Close", prev_window = window)
        self.speak("Hola " + self.User + ", aquí estoy para lo que necesite.")

    def tellNames(self):       
        """
        Función que extrae los nombres posibles por los que el usuario puede invocar al sistema.

        Returns:
            speech (str): Cadena de texto que contiene la frase que debe pronunciar el sistema.
            text (str): Cadena de texto que contiene la frase que debe mostrar el sistema.
        """
        n = str()
        text = str()
        for name in self.Names:
            n += name + ", o "
            text += name + "\n"
        speech = "Me puedes llamar " + n[:-2] + ", tu asistente fiel"
        return speech, text

    def tellDay(self):
        """
        Función que devuelve el día actual al usuario.

        Returns:
            speech (str): Cadena de texto que contiene la frase que debe pronunciar el sistema.
            text (str): Cadena de texto que contiene la frase que debe mostrar el sistema.
        """
        day = str(datetime.today().weekday() + 1)
        today = datetime.today()
        number = str(today.date())
        speech = "Hoy es " + self.Days[day] + ", " + number[-2:] + \
            " de " + self.Months[number[6:7]] + " de " + number[0:4]
        text = self.Days[day] + ", " + number[-2:] + " de\n" + \
            self.Months[number[6:7]] + " de " + number[0:4]
        return speech, text

    def tellTime(self):
        """
        Función que devuelve la hora actual al usuario.

        Returns:
            speech (str): Cadena de texto que contiene la frase que debe pronunciar el sistema.
            text (str): Cadena de texto que contiene la frase que debe mostrar el sistema.
        """
        t = datetime.now()
        text = t.strftime('%H:%M')
        t = str(t)
        hour = t[11:13]
        minutes = t[14:16]
        speech = "Son las" + hour + "horas y" + minutes + "minutos"
        return speech, text


#   ******************  Funcionalidades sobre los usuarios  ******************

    def actionUser(self, action, name):   
        """
        Función que realiza acciones sobre los usuarios del sistema. En concreto, existen tres posibles acciones:
            - Nuevo usuario (*new*): Crea un nuevo usuario "vacío", es decir, con los parámetros por defecto y con
                                     el nombre que el usuario desee.
            - Cambiar de usuario (*change*): Cambia de usuario actual. Para ello, el sistema pide un luego *Login*.
            - Eliminar un usuario (*remove*): Elimina por completo un usuario de la base de conocimiento.

        Args:
            action (str): Acción que la función debe realizar (*new*, *change* o *remove*).
            name (str): Nombre del usuario que se desea crear, al que se desea cambiar o que se desea eliminar.

        Returns:
            speech (str): Cadena de texto que contiene la frase que debe pronunciar el sistema.
            text (str): Cadena de texto que contiene la frase que debe mostrar el sistema.
        """
        if action == "new":
            self.db["Users"].insert_one({"nombre": name, "_CalendarsID": self.__CalendarsID,
                                        "_PhoneFunctions": self.__PhoneFunctions, "_salt": self.__defaultSalt, "_hash": self.__defaultHash})
            speech = "Nuevo usuario creado"
            text = "Nuevo usuario de nombre: " + name + "\ncreado correctamente"

        elif action == "change":
            speech, text = self.Login(name, first = False)

        elif action == "remove":
            name2find = {"nombre": name}
            self.db["Users"].delete_one(name2find)
            speech = "Usuario borrado"
            text = "Usuario: " + name + " borrado"

        return speech, text

    def newUserInfo(self, field, attribute):   
        """
        Función que realiza la actualización de un usuario con un nuevo campo y atributo en la base de conocimiento.

        Args:
            field (str, array of str): Nombre o nombres de los campos que se desean incluir.
            attribute (str, array of str): Nombre o nombres de los atributos de ese/esos nuevos campos.

        Returns:
            speech (str): Cadena de texto que contiene la frase que debe pronunciar el sistema.
            text (str): Cadena de texto que contiene la frase que debe mostrar el sistema.
        """
        name2find = {"nombre": self.User}
        for i in range(len(field)):
            newvalues = {"$set": {field[i]: attribute[i]}}
            self.db["Users"].update_one(name2find, newvalues)
        speech = "Nueva información guardada"
        text = "Información guardada"
        return speech, text


#   ******************  Ejecución de funcionalidades  ******************

    def getAction(self, query, window=None):
        """
        Función principal de la ejecución de funcionalidades. En ella se verifica la entrada por voz de las peticiones que el usuario realiza
        al asistente. Está compuesta por una red de de if-elif-else extensa en la que implementan todas las funcionalidades
        del sistema. 

        Args:
            query (str): Cadena de texto que contiene la petición del usuario.
            window (tkinter.Tk, optional): Ventana de la interfaz de usuario. Defaults to None.

        Returns:
            (response) (int): Variable de verificación de ejecución correcta.
        """
        
        if bool([match for match in self.Commands["Name"] if(match in query)]):             # Funcionalidad *Name*
            speech, text = self.tellNames()                                                 # Llamada al método *tellNames*
            self.speak(speech)                                                              # Enunciar *speech*
            self.GUI("Show", text = text, prev_window = window)                             # Mostrar *text*
            response = 0    
            return response

        elif bool([match for match in self.Commands["Greetings"] if(match in query)]):      # Funcionalidad *Greetings*
            self.Hello(window)                                                              # Llamada al método *Hello*
            response = 0
            return response

        elif bool([match for match in self.Commands["Cheer up"] if(match in query)]):       # Funcionalidad *Cheer up*
            if window is not None:                                                          # Cierre de ventana anterior
                self.GUI("Close", prev_window=window)

            self.speak("Ánimo" + self.User + ", no se preocupe")                            # Enunciar frase
            response = 0
            return response

        elif bool([match for match in self.Commands["Secret"] if(match in query)]):         # Funcionalidad *Secret*
            if window is not None:                                                          # Cierre de ventana anterior
                self.GUI("Close", prev_window=window)

            currentVoice = self.voiceEngine.getProperty('voice')
            self.voiceEngine.setProperty('voice', self.defaultWisperVoice)                  # Cambio de voz del asistente
            self.speak("""En realidad, soy un extraterreste en misión oficial,  
			para poder estudiar a los humanos y observar su comportamiento""")              # Enunciar frase
            self.voiceEngine.setProperty('voice', currentVoice)                             # Vuelta a la voz anterior
            response = 0
            return response

        elif bool([match for match in self.Commands["Today"] if(match in query)]):          # Funcionalidad *Today*
            if self.Days and self.Months:
                speech, text = self.tellDay()                                               # Llamada al método *tellDay*
                self.speak(speech)                                                          # Enunciar *speech*
                self.GUI("Show", text = text, prev_window = window)                         # Mostrar *text*
            else:
                self.GUI("Show", text = self.Error, prev_window = window)                   # Mostrar error
            response = 0
            return response

        elif bool([match for match in self.Commands["Time"] if(match in query)]):           # Funcionalidad *Time*
            speech, text = self.tellTime()                                                  # Llamada al método *tellTime*
            self.speak(speech)                                                              # Enunciar *speech*
            self.GUI("Show", text=text, prev_window=window)                                 # Mostrar *text*
            response = 0
            return response

        elif bool([match for match in self.Commands["Users"] if(match in query)]):          # Funcionalidad *Users* REVISAR
            if window is not None:                                                          # Cierre de ventana anterior
                self.GUI("Close", prev_window=window)

            list_of_words = query.split()
            name = list_of_words[list_of_words.index("nombre") + 1]
            if "nuevo" in list_of_words:
                action = "new"
            elif "cambiar" in list_of_words:
                action = "change"
            elif "eliminar" in list_of_words or "borrar" in list_of_words:
                action = "remove"
            speech, text = self.actionUser(action, name)
            self.speak(speech)
            self.GUI("Show", text=text)
            response = 0
            return response

        elif bool([match for match in self.Commands["NewInformation"] if(match in query)]): # Funcionalidad *NewInformation* REVISAR
            if window is not None:
                self.GUI("Close", prev_window=window)

            self.speak(
                "Perfecto, dime primero cómo vamos a llamar esta nueva información")
            field, window = self.repeat()
            if isinstance(field, tuple):
                field = " ".join(field)
            if field == "contraseña":
                if self.User != "usuario":
                    password = self.GUI("Text", "secret", prev_window=window)
                    password = password.encode('utf-8')
                    salt = bcrypt.gensalt()
                    newHash = bcrypt.hashpw(password, salt)
                    field = ["_salt", "_hash"]
                    attribute = [salt.decode("utf-8"), newHash.decode("utf-8")]
                else:
                    speech = "No puedes darle contraseña al usuario por defecto"
                    text = "Operación denegada"
                    self.speak(speech)
                    self.GUI("Show", text=text)
                    response = 0
                    return response
            else:
                self.speak(
                    "Bien, y ahora dime qué quieres que apunte sobre " + field)
                attribute, window = self.repeat()
                if isinstance(attribute, tuple):
                    attribute = " ".join(attribute)
            speech, text = self.newUserInfo(field, attribute)
            self.speak(speech)
            self.GUI("Show", text=text)
            response = 0
            return response

        elif bool([match for match in self.Commands["Information"] if(match in query)]):    # Funcionalidad *Information* REVISAR
            if window is not None:
                self.GUI("Close", prev_window=window)

            try:
                image = self.fs.find_one({"filename": self.User})
                bytedata = image.read()
                ima_IO = BytesIO(base64.b64decode(bytedata))
                img_PIL = Image.open(ima_IO)
                img_PIL.show()
            except:
                self.speak(
                    "Parece que no tienes una foto asociada a tu usuario")

            info = self.db["Users"].find_one({"nombre": self.User}, {
                                             "_id": 0, "_salt": 0, "_hash": 0, "_CalendarsID": 0, "_PhoneFunctions": 0})
            self.speak("Lo que sé de ti es: ")
            for k, v in info.items():
                self.speak(k + v)
            response = 0
            return response

        elif bool([match for match in self.Commands["ChangeVoice"] if(match in query)]):    # Funcionalidad *ChangeVoice* REVISAR
            self.speak("Perfecto. Tiene " + str(Teo.maxVoices) +
                       "voces para poder elegir")                                           # Frase inicial
            speech, text = self.changeVoice()                                               # Llamada al método *changeVoice*
            self.speak(speech)                                                              # Enunciar *speech*
            self.GUI("Show", text=text, prev_window=window)                                 # Mostrar *text*
            response = 0
            return response

        elif bool([match for match in self.Commands["Google"] if(match in query)]):         # Funcionalidad *Google* REVISAR
            if window is not None:                                                          # Cierre ventana anterior
                self.GUI("Close", prev_window=window)

            self.google(query)                                                              # Llamada al método *google*
            response = 0
            return response

        elif bool([match for match in self.Commands["Wikipedia"] if(match in query)]):      # Funcionalidad *Wikipedia* REVISAR
            if window is not None:                                                          # Cierre de ventana anterior
                self.GUI("Close", prev_window=window)

            response = self.wikipedia(query)                                                
            if response is None:
                self.speak("No se ha podido encontrar la página solicitada")
            return response

        elif bool([match for match in self.Commands["Youtube"] if(match in query)]):        # Funcionalidad *Youtube* REVISAR
            if window is not None:                                                          # Cierre ventana anterior
                self.GUI("Close", prev_window=window)

            self.youtube(query)                                                             # Llamada al método *youtube*
            response = 0
            return response

        elif bool([match for match in self.Commands["Play"] if(match in query)]):           # Funcionalidad *Play*
            if self.SpotifyActions:                                                         
                response = self.spotify("play", window)                                     # Llamada al método *spotify*
                if response == 256:                                                         
                    self.GUI("Show", text=self.SpotifyError)                                # Mostrar error
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar *text*
                response = 0
            return response

        elif bool([match for match in self.Commands["Next"] if(match in query)]):           # Funcionalidad *Next*
            if self.SpotifyActions:                                                         
                response = self.spotify("next", window)                                     # Llamada al método *spotify*
                if response == 256:                                                         
                    self.GUI("Show", text=self.SpotifyError)                                # Mostrar error
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar *text*
                response = 0
            return response

        elif bool([match for match in self.Commands["Previous"] if(match in query)]):       # Funcionalidad *Previous*
            if self.SpotifyActions:                                                         
                response = self.spotify("previous", window)                                 # Llamada al método *spotify*
                if response == 256:                                                         
                    self.GUI("Show", text=self.SpotifyError)                                # Mostrar error
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar *text*
                response = 0
            return response

        elif bool([match for match in self.Commands["Pause"] if(match in query)]):          # Funcionalidad *Pause*
            if self.SpotifyActions:                                                         
                response = self.spotify("pause", window)                                    # Llamada al método *spotify*
                if response == 256:                                                         
                    self.GUI("Show", text=self.SpotifyError)                                # Mostrar error
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar *text*
                response = 0
            return response

        elif bool([match for match in self.Commands["Stop"] if(match in query)]):           # Funcionalidad *Stop*
            if self.SpotifyActions:                                                         
                response = self.spotify("stop", window)                                     # Llamada al método *spotify*
                if response == 256:                                                         
                    self.GUI("Show", text=self.SpotifyError)                                # Mostrar error
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar *text*
                response = 0
            return response

        elif bool([match for match in self.Commands["Song"] if(match in query)]):           # Funcionalidad *Song*
            if self.SpotifyActions:                                                         
                response = self.spotify("song", window)                                     # Llamada al método *spotify*
                if response == 256:                                                         
                    self.GUI("Show", text=self.SpotifyError)                                # Mostrar error
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar *text*
                response = 0
            return response

        elif bool([match for match in self.Commands["Weather"] if(match in query)]):        # Funcionalidad *Weather* REVISAR
            if window is not None:
                self.GUI("Close", prev_window=window)

            speech, place = self.weather(query)
            self.speak(speech)
            os.system("display " + place + ".png")
            # self.GUI("Image", image = place + ".png", geometry = "1750X1000", prev_window = window)
            response = 0
            return response
 
        elif bool([match for match in self.Commands["Alarm"] if(match in query)]):          # Funcionalidad *Alarm* REVISAR
            # "(Pon una) alarma de '5 segundos/minutos/horas' de nombre 'Nombre'"
            if window is not None:                                                          # Cierre ventana anterior
                self.GUI("Close", prev_window=window)

            t, speech, text = self.setAlarm(query)                                          # Llamada al método *setAlarm*
            timer = threading.Timer(t, self.alarm, args=(speech, text))                     # Inicialización temporizador
            timer.start()                                                                   # Inicio temporizador    
            response = 0
            return response

        elif bool([match for match in self.Commands["Reminder"] if(match in query)]):       # Funcionalidad *Reminder* REVISAR
            # "(Crea un) recordatorio de nombre 'Nombre' para el 'Día' a las 'Hora'"
            if self.Numbers:
                speech, text = self.setReminder(query)                                      # Llamada al método *setReminder*
                self.speak(speech)                                                          # Enunciar *speech*
                self.GUI("Show", text=text, prev_window=window)                             # Mostrar *text
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar error
            response = 0
            return response
 
        elif bool([match for match in self.Commands["Math"] if(match in query)]):           # Funcionalidad *Math* REVISAR
            # "Cuánto da/Cuánto es/Calcula/Calcular/Calcúlame *operación matemática como suena*"
            if self.Numbers and self.MathOperations:            
                speech, text = self.mathOperation(query)                                    # Llamada al método *mathOperation*
                self.speak(speech)                                                          # Enunciar *speech*
                self.GUI("Show", text=text, prev_window=window)                             # Mostrar *text*
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar error
            response = 0
            return response
 
        elif bool([match for match in self.Commands["Phone"] if(match in query)]):          # Funcionalidad *Phone*
            # Encuentra mi teléfono/móvil (y similares)
            if window is not None:                                                          # Cierre ventana anterior  
                self.GUI("Close", prev_window=window)

            if self.macroPhone:
                speech = self.findPhone()                                                   # Llamada al método *findPhone*
                self.speak(speech)                                                          # Enunciar *speech*
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar error
            response = 0
            return response

        elif bool([match for match in self.Commands["GetCalendar"] if(match in query)]):    # Funcionalidad *GetCalendar* REVISAR
            # "(Enséñame/muéstrame mis/mi) eventos/calendario/tareas para hoy/mañana/pasado mañana/'fecha'/esta-e/próxima-o/siguiente/X siguientes semana/semanas/mes/meses"
            if self.CalendarsID and self.Months and self.Numbers:   
                speech, text = self.getCalendar(query)                                      # Llamada al método *getCalendar*
                if speech == -1:
                    self.GUI("Show", text="Petición incorrecta", prev_window=window)        # Mostrar error en la petición
                    response = -1
                elif speech != None:
                    self.speak(speech)                                                      # Enunciar *speech*
                    self.GUI("GetCalendar", text=text, size=12,
                             geometry="800x600", prev_window=window)                        # Mostrar *text*
                    response = 0
                else:
                    self.speak("Credenciales actualizadas")                                 # Enunciar actualización de credenciales
                    response = 0
                return response
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar error
                response = 0
                return response

        elif bool([match for match in self.Commands["SetCalendar"] if(match in query)]):    # Funcionalidad *SetCalendar* REVISAR
            # "Crear/crea/creame/hacer/haz/hazme un evento para hoy/mañana/pasado mañana/'fecha' a las X de nombre X "
            if self.CalendarsID and self.Months and self.Numbers:
                speech, text = self.setCalendar(query, window)                              # Llamada al método *setCalendar*
                if speech == -1:
                    self.GUI("Show", text="Petición incorrecta", prev_window=window)        # Mostrar error en la petición
                    response = -1
                else:
                    self.speak(speech)                                                      # Enunciar *speech*
                    self.GUI("Show", text=text, prev_window=window)                         # Mostrar *text*
                    response = 0
                return response
            else:
                self.GUI("Show", text=self.Error, prev_window=window)                       # Mostrar error
                response = 0
                return response

        elif bool([match for match in self.Commands["Shutdown"] if(match in query)]):       # Funcionalidad *Shutdown* REVISAR
            self.shutdown()                                                                 # Llamada al método *shutdown*
            response = 0
            return response

        elif bool([match for match in self.Commands["Suspend"] if(match in query)]):        # Funcionalidad *Suspend* REVISAR
            self.suspend()                                                                  # Llamada al método *suspend*
            response = 0
            return response

        elif bool([match for match in self.Commands["Restart"] if(match in query)]):        # Funcionalidad *Restart* REVISAR
            self.restart()                                                                  # Llamada al método *restart*
            response = 0
            return response

        elif bool([match for match in self.Commands["Nothing"] if(match in query)]):        # Funcionalidad *Nothing*
            if window is not None:                                                          
                self.GUI("Close", prev_window=window)                                       # Cierre ventana anterior

            currentVoice = self.voiceEngine.getProperty('voice')                            
            self.voiceEngine.setProperty('voice', self.defaultWisperVoice)                  # Cambio de voz del asistente
            self.speak("Vale, aquí no ha pasado nada")                                      # Enunciar frase
            self.voiceEngine.setProperty('voice', currentVoice)                             # Vuelta a la voz anterior
            response = 0
            return response

        elif bool([match for match in self.Commands["Del"] if(match in query)]):            # Funcionalidad *Del*
            del self                                                                        # Terminar sistema
            response = 0
            return response

        else:
            self.speak("Lo siento, no te he entendido")                                     # Enunciar frase
            response = 0
            return response


#   ******************  Bucle principal del sistema  ******************

def takeQuery(Teo):
    """ 
    Función principal del sistema. Contiene un bucle infinito en el cual se realizan las siguientes acciones:
        - Comprobación de acceso a internet. Si no se tiene acceso, el sistema no puede funcionar.
        - Recepción de comandos por parte del usuario.
        - Ejecución de funcionalid asociada al comando del usuario.
        - Lógica de comprobación de recordatorios y del teléfono móvil de usuario.

    Args:
        Teo (class): Instancia de la clase Teodoro.
    """
    # Inicialización del sistema
    Teo.Hello()                                                 # Saludo inicial
    os.system("clear")                                          # Limpieza de terminal
    lastsave = time()                                           # Inicialización tiempo de chequeo

    # Bucle principal
    while(True):
        internetOk = Teo.internetCheck()                        # Llamada al método *internetCheck*
        if internetOk != 0:                                     # COMPROBACIÓN ACCESO A INTERNET
            Teo.GUI("Show", text=internetOk)                    # Mostrar error
            del Teo                                             # Terminar sistema
        else:
            query, window = Teo.takeCommand()                   # Llamada al método *takeCommand*
            if query != None:                                   # PETICIÓN REALIZADA
                query = query.lower()
                response = Teo.getAction(query, window)         # Llamada al método *getAction*
                if response != 0:                               # ERROR EN LA PETICIÓN
                    if window is not None:
                        Teo.GUI("Close", prev_window=window)    # Cierre ventana anterior
                    Teo.speak("¿Puede repetir su petición?")    # Enunciar frase
                    query, window = Teo.repeat()                # Llamada al método *repeat*
                    Teo.getAction(query, window)                # Llamada al método *getAction*
            elif time() - lastsave > 60:                        # PETICIÓN NO REALIZADA / COMPROBACIÓN TIEMPO DE CHEQUEO
                speech, text = Teo.checkReminder()              # Llamada al método *checkReminder*
                if speech != None:
                    Teo.speak(speech)                           # Enunciar *speech*
                    Teo.GUI("Show", text=text)                  # Mostrar *text*
                if Teo.PhoneFunctions:                          
                    Teo.checkPhone()                            # Llamada al método *checkPhone*
                lastsave = time()                               # Reseteo del tiempo de chequeo


if __name__ == '__main__':

    Teo = Teodoro()  # Instanciación de la clase Teodoro
    takeQuery(Teo)   # Llamada a la función principal del sistema
