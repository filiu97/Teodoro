import pytest
from Teodoro import Teodoro
import os

class Tests:


    #ENG-6
    def test_ENG_6(self):
        test = Teodoro(del_speak=False)
        os.system("clear")
        # query, window = test.takeCommand()

        print("  - ENG-6: ")
        del test

    #SYS-3
    def test_SYS_3(self):
        test = Teodoro(del_speak=False)

        print(" - SYS-3: ")
        del test

    #APP-1
    def test_APP_1(self):
        test = Teodoro(del_speak=False)


        print(" - APP-1: ")
        del test

    #APP-5
    def test_APP_5(self):
        test = Teodoro(del_speak=False)
        query = "Qué tiempo hace en Murcia"
        speech, image = test.weather(query)
        print(" - APP-5: ")
        print("           Teodoro says: '" + speech + "'")
        print("           Image title: '" + image + "'") #Cambiar a leer el formato del place, y que sea .png
        del test

    #APP-13
    def test_APP_13(self):
        test = Teodoro(del_speak=False)


        print(" - APP-13: ")
        del test

    #CAL-3
    def test_CAL_3(self):
        test = Teodoro(del_speak=False)
        

        print(" - CAL-3: ")
        del test
    #TEO-1
    def test_TEO_1(self):
        test = Teodoro(del_speak=False)
        speech, text = test.tellNames()
        assert all(name in speech for name in ["Teodoro", "Teo"]), " - TEO-1: speech value has not all allowed names"
        assert all(name in text for name in ["Teodoro", "Teo"]),  "           text value has not all allowed names"
        print(" - TEO-1: Allowed names was set correctly")
        print("           Teodoro response is: '" + speech + "'")
        del test

    #TEO-4
    def test_TEO_4(self):
        test = Teodoro(del_speak=False)
        query = ""
        response = test.getAction(query)
        assert response != None, " - TEO-4: Teodoro has done some functionality"
        print(" - TEO-4: Teodoro has no functionality for a empty query")
        print("           Teodoro response is: '" + response + "'")

    #TEO-5
    def test_TEO_5(self):
        test = Teodoro(del_speak=False)
        

        print(" - TEO-5: ")
        del test

    #REND-4
    def test_REND_4(self):
        test = Teodoro(del_speak=False)


        print(" - REND-4: ")
        del test
    
    
# ENG-6. Teodoro debe realizar la identificación de llamada a Teodoro. Se debe reconocer cuando el usuario llama al asistente mediante 
# las palabras claves de nombres especificados en la BdC (Apéndice C, Names.txt). El usuario tendrá acceso a la base de datos, 
# pudiendo customizar los diferentes nombres a los que responde Teodoro.

# SYS-2. (3 o 4, son muy parecidos). Apagado (Suspensión o Reinicio) del equipo en menos de 10 segundos. 
# Tras realizarse la secuencia de apagado (suspensión o reinicio) y tras la ejecución del comando, el equipo debe apagarse 
# (suspender o reiniciarse) en menos de 10 segundos.

# APP-1. Teodoro debe tener acceso a Spotify. El usuario debe acceder a una cuenta de Spotify ya registrada para que Teodoro pueda 
# realizar las funcionalidades descritas. Se requiere que la aplicación de Spotify se encuentre abierta y con un usuario registrado, 
# en el caso que no se cumplan estas condiciones, Teodoro volverá a escucha activa de 3 segundos sin realizar ninguna funcionalidad.

# APP-5. Teodoro debe tener acceso a una API en la red con soporte para el terminal para
# consulta del tiempo. Según la localización que el usuario consulte por voz, se accederá a los
# datos del clima de dicha localización.

# APP-13. Las aplicaciones Youtube, Spotify, Wikipedia y Tiempo Atmosférico requieren de conectividad a internet. Si el equipo no tiene 
# conectividad no se podrá tener acceso a dichas funcionalidad y Teodoro se lo indicará al usuario por medio de la funcionalidad SHOW de la 
# GUI (Apéndice D, GUI).

# CAL-3. Teodoro debe mostrar eventos dentro de Google Calendar hasta una fecha concreta. Esta fecha irá desde el día actual a los 
# próximos “X” meses. En el caso que el usuario no indique la duración (Apéndice E.7.1, GetCalendar), Teodoro volverá al bloque de 
# escucha activa de 10 segundos y se lo indicará por pantalla por medio de la funcionalidad SHOW de la GUI (Apéndice D, GUI)

# TEO-1. Teodoro debe informar al usuario de los nombres que se debe utilizar para comunicarse con él.

# TEO-4. Teodoro debe pedir al usuario una repetición de la petición en caso de no contener ninguna palabra clave o de no entenderse

# TEO-5. Teodoro debe poder despedirse y acabar su proceso.

# REND-4. El asistente debe tardar un máximo de 35 segundos desde que el usuario trata de comunicarse hasta que la tarea es ejecutada.