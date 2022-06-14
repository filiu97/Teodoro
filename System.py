
from Engine import Engine

import os
from time import sleep

class System(Engine):
    """ Clase System.

    Clase que contiene las funcionalidades:
        - Control de ordenador:
            > Suspender.
            > Apagar.
            > Reiniciar

    Args:
            - Engine (class): Superclase que contiene las funcionalidades relacionadas con el control del reconocimiento y
            la emisión de voz, la comprobación de la conexión a Internet del usuario, cambio de voz del asistente y la interfaz
            gráfica de usuario (GUI) 
    """
    def __init__(self):
        """
        Función de inicialización de la clase System. Se instancia la superclase Engine, de la que se heredan todos sus atributos 
        y métodos.
        """
        Engine.__init__(self, self.Names, pause_thr = 0.8)

    def shutdown(self, test = False):
        """
        Función que realiza el apagado del ordenador.

        Args:
            test (bool, optional): Bandera para el "falseado" de la funcionalidad para su testeo. Defaults to False.
        """
        self.speak("Perfecto, que tengas un buen día")
        if test:
            sleep(5)
        else:
            os.system("shutdown now -h")

    def suspend(self, test = False):
        """
        Función que realiza el apagado del ordenador.

        Args:
            test (bool, optional): Bandera para el "falseado" de la funcionalidad para su testeo. Defaults to False.
        """
        self.speak("Perfecto, suspendiendo el equipo")
        if test:
            sleep(5)
        else:
            os.system("sudo pm-suspend")

    def restart(self, test = False):
        """
        Función que realiza el apagado del ordenador.

        Args:
            test (bool, optional): Bandera para el "falseado" de la funcionalidad para su testeo. Defaults to False.
        """
        self.speak("Perfecto, reiniciando el equipo")
        if test:
            sleep(5)
        else:
            os.system("shutdown now -r")