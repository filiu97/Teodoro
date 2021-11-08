from SpeechEngine import SpeechEngine
import os

class System(SpeechEngine):

    def __init__(self):
        SpeechEngine.__init__(self, self.Names, pause_thr = 0.8)


    def shutdown(self):
        self.speak("En seguida, que tengas un buen día")
        os.system("shutdown now -h")

    def suspend(self):
        os.system("sudo pm-suspend")