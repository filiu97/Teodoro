from Engine import Engine
import os

class System(Engine):

    def __init__(self):
        Engine.__init__(self, self.Names, pause_thr = 0.8)


    def shutdown(self):
        self.speak("En seguida, que tengas un buen día")
        os.system("shutdown now -h")

    def suspend(self):
        self.speak("Perfecto, suspendiendo el equipo")
        os.system("sudo pm-suspend")

    def restart(self):
        self.speak("Perfecto, reiniciando el equipo")
        os.system("shutdown now -r")