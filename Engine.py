
import speech_recognition as sr 
import pyttsx3 
from tkinter import *
from tkinter import scrolledtext
from tkinter import font
import requests


class Engine():

    def __init__(self, Names, pause_thr = 1):
        
        self.Names = Names
        r = sr.Recognizer()
        r.pause_threshold = pause_thr
        # r.energy_threshold = 4000
        # r.dynamic_energy_adjustment_ratio = 1
        # with sr.Microphone() as source:
        #     r.adjust_for_ambient_noise(source)
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
                # audio = r.record(source, 3)
                # r.adjust_for_ambient_noise(source)
                audio = r.listen(source, phrase_time_limit = 3)
                try:
                    Query = r.recognize_google(audio, language='es-ES')
                    for name in self.Names:
                        if (Query.find(name)) != -1:
                            self.speak("¿Si?")
                            window = self.GUI("Status", "Reconociendo...")
                            # audio = r.record(source, 10)
                            audio = r.listen(source, phrase_time_limit = 10) 
                            try:
                                Request = r.recognize_google(audio, language='es-ES')
                                return Request, window
                            except:
                                self.GUI("Close", prev_window = window)
                                return None, None		
                    return None, None
                except: 
                    return None, None

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

    def changeVoice(self):
        r = sr.Recognizer()
        window = self.GUI("Status", "Sí -> confirmar \n No -> siguiente voz \n Cualquier cosa \n -> voz por defecto")
        i = 1
        change = False
        while i <= self.maxVoices:
            newVoice = "spanish+m" + str(i)
            self.voiceEngine.setProperty('voice', newVoice)
            self.speak("Esta es una prueba de voz. ¿Le gusta?")
            with sr.Microphone() as source:
                audio = r.listen(source, phrase_time_limit = 3)
                try:
                    Query = r.recognize_google(audio, language='es-ES')
                    if Query == "si":
                        change = True
                        break
                    elif Query == "no":
                        i = i+1
                        continue
                    else:
                        self.voiceEngine.setProperty('voice', self.defaultRate)
                        break
                except:
                    self.speak = "Por favor, pruebe otra vez"
                    continue
        if i > self.maxVoices:
            text = "Se mantiene la voz anterior"
            speech = "No ha seleccionado niguna de las voces disponibles. Se mantiene la voz anterior"
        elif change:
            text = "Voz cambiada"
            speech = "Ha cambiado la voz correctamente"
        else:
            text = "Voz por defecto"
            speech = "Ha elegido al voz por defecto"

        self.GUI("Close", prev_window = window)

        return speech, text



    def get_SetCalendar_entry(self, desc_entry, loc_entry):
        global description, location
        description = desc_entry.get("1.0", "1000.1000")
        location = str(loc_entry.get())

    def get_Login_entry(self, name_entry, pwd_entry):
        global name, password
        name = str(name_entry.get())
        password = str(pwd_entry.get())

    def get_Text_entry(self, text_entry):
        global info
        info = str(text_entry.get())  

    def GUI(self, action, text = None, size = 16, 
            image = None, geometry = "400x200", 
            prev_window = None):
        
        if prev_window is not None or action == "Close":
            prev_window.destroy()
            if action == "Close":
                return

        window = Tk()
        window.geometry(geometry)
        # bg_img = PhotoImage(file = "bg.png")
        bg = "gainsboro"
        window.configure(bg = bg)
        window.title("Teodoro " + action)
        window.resizable(False, False)
        font1 = "bitstream charter"
        font2 = "Helvetica"
        close_label = "Cierre esta ventana para continuar"
        ok_button = "ok.png"

        # label = Label(
        #     window,
        #     image=bg_img
        # )
        # label.place(x=0, y=0)

        if action == "Login":
            
            label = Label(
                window,
                text = "Bienvenido!",
                font = (font1, size, "bold"),
                padx = 0,
                pady = 10,
                bg = bg
                )
            label.pack()

            frame1 = Frame(
                window,
                bg = bg
            )
            frame1.pack()

            Label(
                frame1, 
                text = "Nombre de usuario", 
                font = (font1, size-4, "bold"),
                padx = 10,
                pady = 5,
                bg=bg).grid(row=0, column=0, sticky=W)

            name_entry = Entry(
                frame1,
                font = (font1, size-6),
                width = 30)
            name_entry.grid(
                row = 0, 
                column = 1,
                sticky = W)
            if text:
                name_entry.insert(0, text)

            Label(
                frame1, 
                text = "Contraseña", 
                font = (font1, size-4, "bold"),
                padx = 10,
                pady = 5,
                bg=bg).grid(row=1, column=0, sticky=W)
        
            pwd_entry = Entry(
                frame1,
                font = (font1, size-6),
                show = "*",
                width = 30)
            pwd_entry.grid(
                row = 1, 
                column = 1,
                sticky = W)

            phone = IntVar()
            Checkbutton(
                frame1,
                text = " Usar funcionalidades móvil", 
                pady = 10,
                variable = phone).grid(row = 2, column = 1, sticky = W)


            # frame2 = Frame(
            #     window,
            #     bg = bg
            # )
            # frame2.pack()

            # Label(
            #     frame2,
            #     text = close_label,
            #     font = (font2, size-6, "bold"),
            #     padx = 0,
            #     pady = 10,
            #     bg = bg).grid(column=0, row=2)

            frame3 = Frame(
                window,
                bg = bg
            )
            frame3.pack()
            b1 = Button(
                frame3,
                command = lambda: [self.get_Login_entry(name_entry, pwd_entry), window.destroy()])
            img = PhotoImage(file = ok_button)
            b1.config(image = img)
            b1.pack()

            window.mainloop()

            return name, password, phone

        elif action == "Status":
            label = Label(
                window,
                text = text,
                font = (font1, size, "bold"),
                padx = 0,
                pady = 0,
                bg = bg
                )
            label.pack(expand = True)
            window.update()
            return window
            
        elif action == "Show":

            label = Label(
                window,
                text = text,
                font = (font1, size, "bold"),
                padx = 0,
                pady = 25,
                bg = bg
            )

            cls_label = Label(
                window,
                text = close_label,
                font = (font2, 10, "bold"),
                padx = 0,
                pady = 0,
                bg = bg
                )

            b1 = Button(
                window,
                command = lambda: window.destroy())
            img = PhotoImage(file = ok_button)
            b1.config(image = img)

            label.pack(expand = True)
            cls_label.pack(expand = True)
            b1.pack(expand = True)

            window.mainloop()

        elif action == "Image":
            canvas = Canvas(window, width = 1500, height = 800)      
            canvas.pack()      
            img = PhotoImage(file=image)      
            canvas.create_image(20,20, anchor=NW, image=img) 
            window.mainloop()

        elif action == "GetCalendar":
            
            label = Label(
                window,
                text = "Estos son sus eventos",
                font = (font1, size, "bold"),
                padx = 0,
                pady = 20,
                bg = bg
            )
            label.pack()

            frame1 = Frame(
                window,
                bg = bg
            )
            frame1.pack()
        
            text_area = scrolledtext.ScrolledText( 
                frame1,
                font = (font1, size-1),
                width = 75, 
                height = 22,
                wrap = WORD)
                
            text_area.grid(column = 0)
            text_area.insert(INSERT, text)
            text_area.configure(state ='disabled')

            frame2 = Frame(
                window,
                bg = bg
            )
            frame2.pack()

            Label(
                frame2,
                text = close_label,
                font = (font2, 10, "bold"),
                padx = 0,
                pady = 20,
                bg = bg).grid(column = 0, row = 1)

            frame3 = Frame(
                window,
                bg = bg
            )
            frame3.pack()
            b1 = Button(
                frame3,
                command = lambda: window.destroy())
            img = PhotoImage(file = ok_button)
            b1.config(image = img)
            b1.pack()

            window.mainloop()

        elif action == "SetCalendar":

            Label(
                window,
                text = "¿Quieres añadir una descripción y localización a tu evento?",
                font = (font1, size, "bold"),
                padx = 10,
                pady = 30,
                bg = bg).pack()

            frame1 = Frame(
                window,
                bg = bg)
            frame1.pack()

            Label(
                frame1, 
                text = "Descripción", 
                font = (font1, size, "bold"),
                padx = 10,
                pady = 20,
                bg = bg).grid(row = 0, column = 0, sticky = W)
            
            desc_entry = scrolledtext.ScrolledText( 
                frame1,
                font = (font1, size-6),
                width = 50, 
                height = 10,
                wrap = WORD)

            desc_entry.grid(
                row = 0, 
                column = 1,
                sticky = W)

            Label(
                frame1, 
                text = "Localización", 
                font = (font1, size, "bold"),
                padx = 10,
                pady = 20,
                bg = bg).grid(row = 1, column = 0, sticky = W)
        
            loc_entry = Entry(
                frame1,
                font = (font1, size-6),
                width = 50)
            loc_entry.grid(
                row = 1, 
                column = 1,
                sticky = W)

            frame2 = Frame(
                window,
                bg = bg
            )
            frame2.pack()

            Label(
                frame2,
                text = close_label,
                font = (font2, 10, "bold"),
                padx = 0,
                pady = 5,
                bg = bg).grid(column = 0, row = 1)

            frame3 = Frame(
                window,
                pady = 0,
                bg = bg).pack()
            b1 = Button(
                frame3,
                command = lambda: [self.get_SetCalendar_entry(desc_entry, loc_entry), window.destroy()])
            img = PhotoImage(file = ok_button)
            b1.config(image=img)
            b1.pack(expand = True)

            window.mainloop()

            return description, location

        elif action == "Text":
            
            label = Label(
                window,
                text = "Introduce aquí el texto",
                font = (font1, size, "bold"),
                padx = 0,
                pady = 10,
                bg = bg
                )
            label.pack()

            frame1 = Frame(
                window,
                bg = bg,
                pady = 15
            )
            frame1.pack()

            if text == "secret":
                text_entry = Entry(
                    frame1,
                    font = (font1, size-6),
                    show = "*",
                    width = 50)
            else:
                text_entry = Entry(
                    frame1,
                    font = (font1, size-6),
                    width = 50)
            text_entry.grid(
                row = 1, 
                column = 0,
                sticky = W)

            frame2 = Frame(
                window,
                bg = bg,
            )
            frame2.pack()

            Label(
                frame2,
                text = close_label,
                font = (font2, size-6, "bold"),
                padx = 0,
                pady = 10,
                bg = bg).grid(column=0, row=2)

            frame3 = Frame(
                window,
                bg = bg
            )
            frame3.pack()
            b1 = Button(
                frame3,
                command = lambda: [self.get_Text_entry(text_entry), window.destroy()])
            img = PhotoImage(file = ok_button)
            b1.config(image = img)
            b1.pack()

            window.mainloop()

            return info
