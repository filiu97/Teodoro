import speech_recognition as sr 
import pyttsx3 
from tkinter import *
from time import sleep, time
import requests


class Engine():

    def __init__(self, Names, pause_thr = 0.8):
        
        self.Names = Names
        r = sr.Recognizer()
        r.pause_threshold = pause_thr
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
        self.voiceEngine = pyttsx3.init()
        self.defaultVoice = 'spanish+m3'
        self.defaultWisperVoice = 'spanish+whisper'
        self.defaultRate = 180
        self.maxVoices = 7
        self.voiceEngine.setProperty('voice', self.defaultVoice)
        self.voiceEngine.setProperty('rate', self.defaultRate)
    
    def internetCheck(self):
        url = "http://www.google.com"
        timeout = 5
        try:
            requests.get(url, timeout=timeout)
            return 0
        except (requests.ConnectionError, requests.Timeout) as exception:
            text = "No tiene acceso \na Internet"
            return text

    def speak(self, audio): 
        self.voiceEngine.say(audio)
        self.voiceEngine.runAndWait() 

    def takeCommand(self): 

        r = sr.Recognizer()

        while 1:
            with sr.Microphone() as source:
                audio = r.record(source, 3)
                try:
                    Query = r.recognize_google(audio, language='es-ES')
                    for name in self.Names:
                        if (Query.find(name)) != -1:
                            self.speak("¿Si?")
                            window = self.GUI("Status", "Reconociendo...")
                            audio = r.record(source, 10) 
                            try:
                                Request = r.recognize_google(audio, language='es-ES')
                                return Request, window
                            except:
                                return None, None		
                    return None, None
                except: 
                    continue

    def repeat(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                window = self.GUI("Status", "Reconociendo...")
                audio = r.record(source, 10)
                try: 
                    Request = r.recognize_google(audio, language='es-ES')
                    return Request, window
                except:
                    self.speak("No he reconocido lo que ha dicho, lo siento")
                    return None, None
            except:
                return None, None

    def GUI(self, action, text = None, size = 24, 
            image = None, geometry = "400x200", 
            prev_window = None):
        
        if prev_window is not None or action == "Close":
            prev_window.destroy()
            if action == "Close":
                return

        window = Tk()
        window.geometry(geometry)
        window.configure(bg = "LightSkyBlue1")
        window.title("Teodoro " + action)
        window.resizable(False, True)
        font1 = "Times New Roman"
        font2 = "Helvetica"

        if action == "Status":
            label = Label(
                window,
                text=text,
                font=(font1, size, "bold"),
                padx=0,
                pady=0,
                bg='LightSkyBlue1'
                )
            label.pack(expand=True)
            window.update()
            return window
            
        elif action == "Show":
            label = Label(
                window,
                text=text,
                font=(font1, size, "bold"),
                padx=0,
                pady=0,
                bg='LightSkyBlue1'
            )
            cls_label = Label(
                window,
                text="Cierre esta ventana para continuar",
                font=(font2, 10, "bold"),
                padx=0,
                pady=0,
                bg='LightSkyBlue1'
                )
            label.pack(expand=True)
            cls_label.pack(expand=True)
            window.mainloop()

        elif action == "Image":
            canvas = Canvas(window, width = 1500, height = 800)      
            canvas.pack()      
            img = PhotoImage(file=image)      
            canvas.create_image(20,20, anchor=NW, image=img) 
            window.mainloop()

        elif action == "GetCalendar":
            f = Frame(window)
            canvas = Canvas(f, width="800", height="800")
            scroll = Scrollbar(f, orient = "vertical", command=canvas.yview)
            scroll_frame = Frame(canvas)
            f_close = Frame(window)

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all"),
                    bg = "LightSkyBlue1"
                )
            )

            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scroll.set)

            label = Label(
                scroll_frame,
                text=text,
                font=(font1, size, "bold"),
                padx=0,
                pady=0,
                bg='LightSkyBlue1'
                )
            cls_label = Label(
                f_close,
                text="Cierre esta ventana para continuar",
                font=(font2, 12, "bold"),
                padx=0,
                pady=0,
                bg='LightSkyBlue1'
                )
            f_close.pack(side=BOTTOM)
            f.pack(side=TOP)
            canvas.pack(side=LEFT, fill="both")
            scroll.pack(side=RIGHT, fill="y")
            label.pack()
            cls_label.pack()
            window.mainloop()

        elif action == "SetCalendar":
            frame1 = Frame(window)
            frame1.pack()
            label = Label(
                window,
                text="¿Quieres añadir una descripción \ny localización a tu evento",
                font=(font1, 12, "bold"),
                padx=0,
                pady=0,
                bg='LightSkyBlue1'
                )
            label.pack()

            frame2 = Frame(window)
            frame2.pack()
            Label(frame2, text="Description",font=(font1, 12, "bold")).grid(row=0, column=0, sticky=W)
            desc_entry = Entry(frame2)
            desc_entry.grid(row=0, column=1, sticky=W)
            description = str(desc_entry.get())
            Label(frame2, text="Location",font=(font1, 12, "bold")).grid(row=1, column=0, sticky=W)
            loc_entry = Entry(frame2)
            loc_entry.grid(row=1, column=1, sticky=W)
            location = str(loc_entry.get())

            frame3 = Frame(window)
            frame3.pack()
            b1 = Button(frame3,text=" Ok ",command=lambda:window.destroy())
            b1.pack(expand = True)

            window.mainloop()

            return description, location
