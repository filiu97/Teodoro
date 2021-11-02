

from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build
import pickle
import datefinder
import pprint as pp
from datetime import datetime, time, timedelta
import color



scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)

# Para hacerlo por primera vez, las credenciales
# credentials = flow.run_console()
# pickle.dump(credentials, open("token.pkl", "wb")) 

credentials = pickle.load(open("token.pkl", "rb"))  

service = build("calendar", "v3", credentials=credentials)
# result = service.calendarList().list().execute()
# print(result)
# calendar_id = result['items'][0]['id']
# print(calendar_id)
# result = service.events().list(calendarId=calendar_id).execute()
# print(result['items'][0])

def create_event(start_time_str, summary, duration=1, attendees=None, description=None, location=None):
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
        'attendees': [
        {'email':attendees },
    ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    pp.pprint('''*** %r event added: 
    With: %s
    Start: %s
    End:   %s''' % (summary.encode('utf-8'),
        attendees,start_time, end_time))
        
    return service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()

# create_event('24 Jul 12.30pm', "Test Meeting using CreateFunction Method",0.5,"karlosfiliu97@gmail.com","Test Description","En mi culo")


from dateutil.relativedelta import relativedelta

# Get events
today = datetime.today()
d = 7
diff = today + relativedelta(days=d)
tmin = today.isoformat('T') + "Z"
tmax = diff.isoformat('T') + "Z"
maxResults = 50
eventsResult = service.events().list(
    calendarId='primary',
    timeMin=tmin,
    timeMax=tmax,
    maxResults=maxResults,
    singleEvents=True,
    orderBy='startTime',
).execute()


import iso8601

def get_date(date_input):

    date_obj = iso8601.parse_date(date_input)
    return date_obj.strftime('%H:%M del %d-%m-%Y ')


print("Tus eventos de los próximos " + str(d) + " días son:")

for event in eventsResult['items']:
    if 'dateTime' in event['start'].keys():
        print("   -" + event['summary'] + " a las " + get_date(event['start']['dateTime']))
    else:
        print("   -" + event['summary'] + " el día " + get_date(event['start']['date']))



def get_hours(date_input):

    date_obj = iso8601.parse_date(date_input)
    return date_obj.strftime('%H:%M')

day_str = "2021/11/02"
matches = list(datefinder.find_dates(day_str))

day = matches[0]
diff = day + relativedelta(days=1)
tmin = day.isoformat('T') + "Z"
tmax = diff.isoformat('T') + "Z"
eventsResult = service.events().list(
    calendarId='primary',
    timeMin=tmin,
    timeMax=tmax,
    maxResults=maxResults,
    singleEvents=True,
    orderBy='startTime',
).execute()

print("Tus eventos para el día " + str(day.strftime("%d-%m-%Y")) + " son:")

for event in eventsResult['items']:
    if 'dateTime' in event['start'].keys():
        print("   -" + event['summary'] + " a las " + get_hours(event['start']['dateTime']))
    else:
        print("   -" + event['summary'] + " el día " + event['start']['date'])