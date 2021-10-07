from googleapiclient.discovery import build  # Allowing for doing API calls
from google_auth_oauthlib.flow import InstalledAppFlow  # Flow to setup OAuthLib (permission screen)
import pickle  # For Credentials Saving
import datetime
from project.BackEnd.General import *


# Does stuff needed for importing google events.
def DoStuff(Monday, Sunday):
    # %% CONNECT WITH GOOGLE ACCOUNT
    our_scopes = ['https://www.googleapis.com/auth/calendar']  # Defined what we can access in user's acc
    flow = InstalledAppFlow.from_client_secrets_file('../client_secret.json', scopes=our_scopes)
    try:
        credentials = flow.run_local_server()
    except Exception:
        print('Failed')
    else:
        print('\nSuccessfully Authenticated')

    pickle.dump(credentials, open('../token.pkl', 'wb'))  # SAVE with pickle

    # %% SYNC
    credentials = pickle.load(open('../token.pkl', 'rb'))  # LOAD with pickle

    service = build('calendar', 'v3', credentials=credentials)  # Build API

    result = service.calendarList().list().execute()  # Get all calendars
    # print(result['items'][0])

    cal_id = result['items'][0]['id']
    result = service.events().list(calendarId=cal_id, timeMin=str(Monday)+'T06:59:59.0+00:00',
                                   timeMax=str(Sunday) + 'T06:59:59.0+00:00').execute()  # Import google cal. events

    event_names = dict()

    for event in result['items']:
        event_name = event['summary']  # Pull Name
        start_time = datetime.datetime.fromisoformat(event['start']['dateTime'])  # Pull Start
        end_time = datetime.datetime.fromisoformat(event['end']['dateTime'])  # Pull Stop
        '''We have pulled simple strings, so we will have to convert them to the
        datetime objects'''

        event_names[event_name] = (start_time, end_time)

    return event_names


# Coordinates the stuff above.
def Import(monday, X):
    sunday = str(XDaysLater(monday, X - 1))
    event_lst = []
    events = DoStuff(monday, sunday)
    di_events = events.items()
    for event, inner in di_events:
        event_lst.append([f'{event}', inner[0].strftime('%d-%m-%Y,%H:%M'), inner[1].strftime('%d-%m-%Y,%H:%M')])
    return event_lst
