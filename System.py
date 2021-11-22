from Engine import Engine
import os

class System(Engine):

    def __init__(self):
        Engine.__init__(self, self.Names, pause_thr = 0.8)


    def shutdown(self):
        self.speak("En seguida, que tengas un buen día")
        os.system("shutdown now -h")

    def suspend(self):
        os.system("sudo pm-suspend")