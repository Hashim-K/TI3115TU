# %% OAuth2 Setup
from googleapiclient.discovery import build                 # Allowing for doing API calls
from google_auth_oauthlib.flow import InstalledAppFlow      # Flow to setup OAuthLib (permission screen)

import pickle                                               # For Credentials Saving

# %% CONNECT WITH GOOGLE ACCOUNT
our_scopes = ['https://www.googleapis.com/auth/calendar']       # Defined what we can access in user's acc
flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=our_scopes)
try:
    credentials = flow.run_local_server()
except Exception:
    print('Failed')
else:
    print('\nSuccessfully Authenticated')

pickle.dump(credentials, open('token.pkl', 'wb'))       # SAVE with pickle

# %% SYNC
credentials = pickle.load(open('token.pkl', 'rb'))      # LOAD with pickle

service = build('calendar', 'v3', credentials = credentials)    # Build API

result = service.calendarList().list().execute()        # Get all calendars
# print(result['items'][0])

cal_id = result['items'][0]['id']
result = service.events().list(calendarId = cal_id, timeMin = '2021-09-05T06:38:20.976447+00:00'
, timeMax = '2021-09-13T06:38:20.976447+00:00').execute()                                                  # Import google cal. events
num_ments = len(result['items'])
print(result['items'])
print(f'The amount of appointments is: {num_ments}')

# %%
import datetime
t = datetime.datetime(2021, 9, 6)
#t = datetime.datetime.now(datetime.timezone.utc)
t_R = t.isoformat()
print(t_R)
# %%
event_names = dict()

for event in result['items']:
    event_name = event['summary']               # Pull Name
    start_time = datetime.datetime.fromisoformat(event['start']['dateTime'])     # Pull Start
    end_time = datetime.datetime.fromisoformat(event['end']['dateTime'])         # Pull Stop
    '''We have pulled simple strings, so we will have to convert them to the
    datetime objects'''

    event_names[event_name] = (start_time, end_time)

#print(event_names)

def pretty_events(events):
    '''Prints all events imported in a human readable format.'''
    di_events = events.items()
    for event, inner in di_events:
        print(f'Event Name: {event}')
        print(inner[0].strftime('Date: %d-%m-%Y, Time: %H:%M'))
        print(inner[1].strftime('Date: %d-%m-%Y, Time: %H:%M'))
        print('\n')
pretty_events(event_names)
