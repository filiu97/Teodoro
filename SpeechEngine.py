import speech_recognition as sr 
import pyttsx3 


class SpeechEngine():

    def __init__(self, Names, pause_thr = 0.8):
        
        self.Names = Names
        r = sr.Recognizer()
        r.pause_threshold = pause_thr
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
    
    def speak(self, audio): 
        engine = pyttsx3.init()
        engine.setProperty('voice', 'spanish')
        engine.setProperty('rate', 165)
        engine.say(audio)
        engine.runAndWait() 

    def takeCommand(self): 

        r = sr.Recognizer()

        with sr.Microphone() as source:
            audio = r.record(source, 3)
            try:
                Query = r.recognize_google(audio, language='es-ES')
                for name in self.Names:
                    if (Query.find(name)) != -1:
                        self.speak("¿Si?")
                        print("Reconociendo")
                        audio = r.record(source, 10) 
                        try:
                            Request = r.recognize_google(audio, language='es-ES')
                            print("Usted ha dicho:", Request)
                            return Request
                        except:
                            return "nada"			
                return "nada"
            except: 
                return "nada"

    def repeat(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                print('Escuchando') 
                audio = r.record(source, 10)
                try: 
                    return r.recognize_google(audio, language='es-ES')
                except:
                    self.speak("No he reconocido lo que ha dicho, lo siento")
                    return None
            except:
                return None