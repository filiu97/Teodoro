
# ENG-6. Teodoro debe realizar la identificación de llamada a Teodoro. Se debe reconocer cuando el usuario llama al asistente mediante 
# las palabras claves de nombres especificados en la BdC (Apéndice C, Names.txt). El usuario tendrá acceso a la base de datos, 
# pudiendo customizar los diferentes nombres a los que responde Teodoro.

# SYS-3. Suspensión del equipo en menos de 10 segundos. 
# Tras realizarse la secuencia de suspensión y tras la ejecución del comando, el equipo debe suspender en menos de 10 segundos.

# APP-1. Teodoro debe tener acceso a Spotify. El usuario debe acceder a una cuenta de Spotify ya registrada para que Teodoro pueda 
# realizar las funcionalidades descritas. Se requiere que la aplicación de Spotify se encuentre abierta y con un usuario registrado, 
# en el caso que no se cumplan estas condiciones, Teodoro volverá a escucha activa de 3 segundos sin realizar ninguna funcionalidad.

# APP-6. Teodoro debe poder guardar la imagen proporcionada por la API de consulta del tiempo.
# Debe mostrar por pantalla el tiempo de la localización consultada mediante la GUI Image.
# (Apéndice D, GUI). En el caso que el usuario durante la consulta no especifique correctamente la
# localización (Apéndice E.6.1, Weather), Teodoro se lo indicará por pantalla por medio de la
# funcionalidad SHOW de la GUI (Apéndice D, GUI).

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


import pytest
from Teodoro import Teodoro
import os
from playsound import playsound
from time import sleep, time


class Tests:

    #ENG-6
    def test_ENG_6(self):
        test = Teodoro(del_speak=False)
        os.system("clear")
        print("\n------------------------ ENG-6 ------------------------------")
        print("Playing Teodoro_Calling.mp3...")
        playsound('Teodoro_Calling.mp3', block = False)
        print("Calling Teodoro...")
        query, window = test.takeCommand()
        window.destroy()
        assert query == 'hola', "Teodoro has not recognized query correctly"
        print("Teodoro has recognized query correctly")
        print("Query is: " + query)
        del test

    #SYS-3
    def test_SYS_3(self):
        print("\n------------------------ SYS-3 ------------------------------")
        test = Teodoro(del_speak=False)
        t_start = time()
        test.suspend(test = True)
        t_end = time()
        t = t_end-t_start
        assert t < 10, "t = " + "{:.2f}".format(t) + " s. Teodoro has not satisfied suspension requirement"
        print("t = " + "{:.2f}".format(t) + " s. Teodoro has satisfied suspension requirement")
        del test

    #APP-1
    def test_APP_1(self):
        print("\n------------------------ APP-1 ------------------------------")
        test = Teodoro(del_speak=False)
        query = "pon la música"
        response = test.getAction(query)
        assert response == 256, 'Teodoro has not answered correctly'
        print("Not access to Spotify: Teodoro has answered correctly")

        os.popen("spotify")
        print("Abriendo Spotify...")
        sleep(5)
        query = "pon la música"
        response = test.getAction(query)
        assert response == 0, 'Teodoro has not answered correctly'
        print("Play: Teodoro has answered correctly")

        query = "qué canción es esta"
        response = test.getAction(query)
        assert response == 0, 'Teodoro has not answered correctly'
        print("Song: Teodoro has answered correctly")

        query = "pasa de canción"
        response = test.getAction(query)
        assert response == 0, 'Teodoro has not answered correctly'
        print("Next: Teodoro has answered correctly")
        sleep(5)
        
        query = "canción anterior"
        response = test.getAction(query)
        assert response == 0, 'Teodoro has not answered correctly'
        print("Previous: Teodoro has answered correctly")
        sleep(5)

        query = "para la música"
        response = test.getAction(query)
        assert response == 0, 'Teodoro has not answered correctly'
        print("Pause: Teodoro has answered correctly")

        query = "quita la música"
        response = test.getAction(query)
        assert response == 0, 'Teodoro has not answered correctly'
        print("Stop: Teodoro has answered correctly")
        del test

    #APP-6
    def test_APP_6(self):
        print("\n------------------------ APP-6 ------------------------------")
        test = Teodoro(del_speak=False)
        query = "Qué tiempo hace en Madrid"
        image = "Madrid.png"
        if os.path.isfile(image) == True:
            os.remove(image)
        test.getAction(query)
        assert os.path.isfile(image) == True, "Teodoro has not saved weather image correctly"
        print("Teodoro has saved weather image correctly")
        del test

    #APP-13
    def test_APP_13(self):
        print("\n------------------------ APP-13 ------------------------------")
        print("Turning off wifi connection...")
        os.system("nmcli radio wifi off")
        test = Teodoro(del_speak=False)
        internetOk = test.internetCheck()
        assert internetOk != 0, "Teodoro has not correctly detected the non-connection to Internet"
        print("Teodoro has correctly detected the non-connection to Internet")
        print("Turning on wifi connection...")
        os.system("nmcli radio wifi on")
        test.GUI("Show", text = internetOk)
            

    #CAL-3
    def test_CAL_3(self):
        print("\n------------------------ CAL-3 ------------------------------")
        test = Teodoro(del_speak=False)
        response = test.getAction("Dime mis eventos para hoy")
        response += test.getAction("Dime mis eventos para mañana")
        response += test.getAction("Dime mis eventos para pasado mañana")
        response += test.getAction("Dime mis eventos para el 30 de diciembre")
        response += test.getAction("Dime mis eventos de esta semana")
        response += test.getAction("Dime mis eventos para los próximos tres meses")
        error = test.getAction("Dime mis eventos")
        assert response == 0, "Teodoro has not correctly get user's events"
        assert error == -1, "Teodoro has not correctly solve error in user's query"
        print("Teodoro has correctly got user's events")
        print("Teodoro has correctly solved error in user's query")
        del test

    #TEO-1
    def test_TEO_1(self):
        print("\n------------------------ TEO-1 ------------------------------")
        test = Teodoro(del_speak=False)
        speech, text = test.tellNames()
        assert all(name in speech for name in ["Teodoro", "Teo"]), "speech value has not all allowed names"
        assert all(name in text for name in ["Teodoro", "Teo"]),  "text value has not all allowed names"
        print("Allowed names was set correctly")
        test.speak(speech)
        print("Teodoro response is: \n" + text)
        del test

    #TEO-4
    def test_TEO_4(self):
        print("\n------------------------ TEO-4 ------------------------------")
        test = Teodoro(del_speak=False)
        query = ""
        response = test.getAction(query)
        assert type(response) != int, "Teodoro has done some functionality"
        print("Teodoro has no functionality for an empty query")
        print("Teodoro response is: '" + response + "'")

    #TEO-5
    def test_TEO_5(self):
        print("\n------------------------ TEO-5 ------------------------------")
        test = Teodoro()
        del test
        check = "test" in locals()
        assert check == False, "Teodoro has not deleted itself correctly"
        print("Teodoro has deleted itself correctly")
        
    #REND-4
    def test_REND_4(self):
        print("\n------------------------ REND-4 ------------------------------")
        test = Teodoro(del_speak=False)
        t = []
        for command in test.Commands.keys():
            query = test.Commands[command][0]
            if query != 'apaga el ordenador' and query != 'suspende el ordenador' and query != 'reinicia el ordenador':
                t_start = time()
                test.getAction(test.Commands[command][0])
                t_end = time()
                t.append(t_end-t_start)
                print(command + " functionality -> t = " + "{:.2f}".format(t_end-t_start) + " s")

        assert max(t) < 35, "Max time = " + "{:.2f}".format(max(t)) + " s. Teodoro has not satisfied the performance requirement"
        print("Max time = " + "{:.2f}".format(max(t)) + " s. Teodoro has satisfied the performance requirement")
    
