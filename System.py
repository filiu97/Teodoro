from Engine import Engine
import os
from time import sleep

class System(Engine):

    def __init__(self):
        Engine.__init__(self, self.Names, pause_thr = 0.8)


    def shutdown(self, test=False):
        self.speak("En seguida, que tengas un buen día")
        if test:
            sleep(5)
        else:
            os.system("shutdown now -h")

    def suspend(self, test=False):
        self.speak("Perfecto, suspendiendo el equipo")
        if test:
            sleep(5)
        else:
            os.system("sudo pm-suspend")

    def restart(self, test=False):
        self.speak("Perfecto, reiniciando el equipo")
        if test:
            sleep(5)
        else:
            os.system("shutdown now -r")