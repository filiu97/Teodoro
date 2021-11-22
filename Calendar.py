from Engine import Engine

from time import time
from dateutil.relativedelta import relativedelta
import datefinder
from datetime import datetime, timedelta
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import iso8601


class Calendar(SpeechEngine):
    
    def __init__(self, calendarsid_file, numbers_file, Months):

        self.CalendarsID = {}
        file = open(calendarsid_file)
        for line in file:
            key, value = line.rstrip("\n").replace(" ", "").split(":")
            self.CalendarsID[key] = value

        self.Numbers = {}
        file = open(numbers_file)
        for line in file:
            key, value = line.rstrip("\n").replace(" ", "").split(":")
            self.Numbers[key] = value

        self.Months = Months
        
        scopes = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
        try:
            self.__credentials = pickle.load(open("token.pkl", "rb")) 
        except:
            # Para hacerlo por primera vez, las credenciales
            self.__credentials = flow.run_console()
            pickle.dump(self.__credentials, open("token.pkl", "wb")) 
        self.service = build("calendar", "v3", credentials=self.__credentials)

        Engine.__init__(self, self.Names, pause_thr = 0.8)
        


    def get_date_hours(self, date_input, time_format = "date"):

        date_obj = iso8601.parse_date(date_input)
        if time_format == "date":
            return date_obj.strftime('%H:%M del %d-%m-%Y ')
        elif time_format == "hours":
            return date_obj.strftime('%H:%M')
        elif time_format == "day_complete":
            return date_obj.strftime('%d-%m-%Y ')

    def get_relative_events(self, calendarID, duration, offset = 0, maxResults = 50):
        today = datetime.today()
        today = datetime.combine(today, datetime.min.time())
        today = today + relativedelta(days=offset)
        diff = today + relativedelta(days=duration)
        tmin = today.isoformat('T') + "Z"
        tmax = diff.isoformat('T') + "Z"
        eventsResult = self.service.events().list(
            calendarId=calendarID,
            timeMin=tmin,
            timeMax=tmax,
            maxResults=maxResults,
            singleEvents=True,
            orderBy='startTime',
        ).execute()
        return eventsResult

    def get_absolute_events(self, calendarID, day_str, maxResults = 50):
        matches = list(datefinder.find_dates(day_str))
        day = matches[0]
        diff = day + relativedelta(days=1)
        tmin = day.isoformat('T') + "Z"
        tmax = diff.isoformat('T') + "Z"
        eventsResult = self.service.events().list(
            calendarId=calendarID,
            timeMin=tmin,
            timeMax=tmax,
            maxResults=maxResults,
            singleEvents=True,
            orderBy='startTime',
        ).execute()
        return eventsResult

    def create_event(self, start_time_str, summary, duration=1, description=None, location=None):
        matches = list(datefinder.find_dates(start_time_str))
        if len(matches):
            start_time = matches[0]
            end_time = start_time + timedelta(hours = duration)
                    
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Europe/Madrid',
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Europe/Madrid',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
            
        return self.service.events().insert(calendarId = self.CalendarsID['personal'], body = event, sendNotifications = True).execute()


    def getCalendar(self, query):

        list_of_words = query.split()
        if ("eventos" in query) or ("calendario" in query):
            calendarID = self.CalendarsID['personal']
            event_type = "eventos"
        else:
            calendarID = self.CalendarsID['trello']
            event_type = "tareas"
        
        if "semanas" in query:
            number = list_of_words[list_of_words.index("semanas") - 1]
            time_str = "las próximas " + number + " semanas"
            time_format = "date"
            key_list = list(self.Numbers.keys())
            val_list = list(self.Numbers.values())
            position = val_list.index(number)
            number = int(key_list[position])
            duration = 7*number
            eventsResult = self.get_relative_events(calendarID, duration)

        elif "semana" in query:
            time_unit = list_of_words[list_of_words.index("semana") - 1]
            if time_unit == "esta":
                time_str = "esta semana"
                time_format = "date"
                duration = 7
                eventsResult = self.get_relative_events(calendarID, duration)
            elif time_unit == "próxima" or time_unit == "siguiente":
                time_str = "la próxima semana"
                time_format = "date"
                duration = 7
                offset = 7
                eventsResult = self.get_relative_events(calendarID, duration, offset)
        
        elif "meses" in query:
            number = list_of_words[list_of_words.index("meses") - 1]
            time_str = "los próximos " + number + " meses"
            time_format = "date"
            key_list = list(self.Numbers.keys())
            val_list = list(self.Numbers.values())
            print(key_list)
            print(val_list)
            position = val_list.index(number)
            number = int(key_list[position])
            print(number)
            print(type(number))
            duration = 30*number
            eventsResult = self.get_relative_events(calendarID, duration)

        elif "mes" in query:
            time_unit = list_of_words[list_of_words.index("mes") - 1]
            if time_unit == "este":
                time_str = "este mes"
                time_format = "date"
                duration = 30
                eventsResult = self.get_relative_events(calendarID, duration)
            elif time_unit == "próximo" or time_unit == "siguiente":
                time_str = "la próximo mes"
                time_format = "date"
                duration = 30
                offset = 30
                eventsResult = self.get_relative_events(calendarID, duration, offset)

        else:
            if "para" in query:
                time_unit = "para"
            elif "de" in query:
                time_unit = "de"
            if list_of_words[list_of_words.index(time_unit) + 1] == "hoy":
                time_str = "hoy"
                time_format = "hours"
                today = datetime.today()
                day_str = today.strftime("%m-%d-%Y")
                eventsResult = self.get_absolute_events(calendarID, day_str)
            elif list_of_words[list_of_words.index(time_unit) + 1] == "mañana":
                time_str = "mañana"
                time_format = "hours"
                today = datetime.today()
                day_str = today + timedelta(days=1)
                day_str = day_str.strftime("%m-%d-%Y")
                eventsResult = self.get_absolute_events(calendarID, day_str)
            elif list_of_words[list_of_words.index(time_unit) + 1] == "pasado":
                time_str = "pasado mañana"
                time_format = "hours"
                today = datetime.today()
                day_str = today + timedelta(days=2)
                day_str = day_str.strftime("%m-%d-%Y")
                eventsResult = self.get_absolute_events(calendarID, day_str)
            else:
                try:
                    day = list_of_words[list_of_words.index(time_unit) + 2]
                    key_list = list(self.Numbers.keys())
                    val_list = list(self.Numbers.values())
                    position = val_list.index(day)
                    day = key_list[position]
                except:
                    day = list_of_words[list_of_words.index(time_unit) + 2]
                try:
                    month = list_of_words[list_of_words.index(time_unit) + 4]
                    key_list = list(self.Months.keys())
                    val_list = list(self.Months.values())
                    position = val_list.index(month)
                    month = key_list[position]
                except:
                    today = datetime.today()
                    month = today.month
                try:
                    year = int(list_of_words[list_of_words.index(time_unit) + 6])
                except:
                    today = datetime.today()
                    year = today.year
                time_str = "el día " + str(day) + " de " +  str(month) + " de " + str(year)
                time_format = "hours"
                day_str = str(month) + "/" + str(day) + "/" + str(year)
                eventsResult = self.get_absolute_events(calendarID, day_str)

        if eventsResult['items']:
            speech = "Tus " + event_type + "  para " + time_str + " son:"
            text = str()
            for event in eventsResult['items']:
                if 'dateTime' in event['start'].keys():
                    text += "   -" + event['summary'] + " a las " + self.get_date_hours(event['start']['dateTime'], time_format) + "\n"
                else:
                    text += "   -" + event['summary'] + " el día " + self.get_date_hours(event['start']['date'], 'day_complete') + "\n"
        else:
            speech = "No tienes nada para " + time_str
            text = "No tienes nada para " + time_str
        
        return speech, text

    def setCalendar(self, query, window):
        calendarID = self.CalendarsID['personal']
        list_of_words = query.split()
        time_unit = "para"
        if list_of_words[list_of_words.index(time_unit) + 1] == "hoy":
            time_str = "hoy"
            today = datetime.today()
            day_str = today.strftime("%m-%d-%Y")
        elif list_of_words[list_of_words.index(time_unit) + 1] == "mañana":
            time_str = "mañana"
            today = datetime.today()
            day_str = today + timedelta(days=1)
            day_str = day_str.strftime("%m-%d-%Y")
        elif list_of_words[list_of_words.index(time_unit) + 1] == "pasado":
            time_str = "pasado mañana"
            today = datetime.today()
            day_str = today + timedelta(days=2)
            day_str = day_str.strftime("%m-%d-%Y")
        else:
            try:
                day = list_of_words[list_of_words.index(time_unit) + 2]
                key_list = list(self.Numbers.keys())
                val_list = list(self.Numbers.values())
                position = val_list.index(day)
                day = key_list[position]
            except:
                day = list_of_words[list_of_words.index(time_unit) + 2]
            try:
                month = list_of_words[list_of_words.index(time_unit) + 4]
                key_list = list(self.Months.keys())
                val_list = list(self.Months.values())
                position = val_list.index(month)
                month = key_list[position]
            except:
                today = datetime.today()
                month = today.month
            try:
                year = int(list_of_words[list_of_words.index(time_unit) + 6])
            except:
                today = datetime.today()
                year = today.year
            time_str = "el día " + str(day) + " de " +  str(month) + " de " + str(year)
            time_format = "hours"

            day_str = str(month) + "/" + str(day) + "/" + str(year)
        
        hours_str = list_of_words[list_of_words.index("a") + 2]

        # if list_of_words[list_of_words.index("a") + 3] == "de":
        #     day_moment = list_of_words[list_of_words.index("de") + 2]
        #     if day_moment == "tarde" or day_moment == "noche":
        #         hour_format = "pm"
        #     else:
        #         hour_format = "am"

        time_str = hours_str #+ " " + hour_format
        summary = list_of_words[-1]
        print(time_str)

        description, location = self.GUI("SetCalendar", prev_window=window)

        print(description)
        print(location)

        self.create_event(time_str,summary.title(), description=description, location=location)
