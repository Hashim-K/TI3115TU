from project.BackEnd.Google import Create_Service
from project.BackEnd.GoogleEvent import GoogleEvent, import_google_event, delete_google_event
from project.BackEnd.Schedule import import_schedule, Event
from project.BackEnd.Preset import Presets
import os

from project.BackEnd.TimeObject import str_init, TimeObject

dirname = os.path.dirname(__file__)


def authenticate():
    CLIENT_SECRET_FILE = os.path.join(dirname, '../data/client_secret.json')
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    return Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_calendar(service, title):
    request_body = {
        'summary': title
    }
    response = service.calendars().insert(body=request_body).execute()
    return response['id']


def get_calendar(service, calendar_id):
    return service.calendars().get(calendarId=calendar_id).execute()


def delete_calendar(service, calendar_id):
    service.calendars().delete(calendarId=calendar_id).execute()


def list_calendars(service):
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print("title: " + calendar_list_entry['summary'])
            print("id: " + calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break


def list_events(service, primary):
    presets = Presets()
    dayzero = TimeObject(presets.day_zero, 0, 0)
    dayseven = TimeObject(presets.day_zero, 6, 1440/presets.time_interval)
    if primary or presets.calendar_id == -1:
        calendar_id = 'primary'
    else:
        calendar_id = presets.calendar_id

    page_token = None
    eventlist=[]
    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token, singleEvents=True,
                                       timeMax=str(dayseven), timeMin=str(dayzero)).execute()
        for event in events['items']:
            print(event)
            eventlist.append(event)
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return eventlist


def get_event(service, event_id):
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    print(event['summary'])


def delete_event(service, event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()


def insert_event(service, event):
    presets = Presets()
    dayzero=presets.day_zero
    ev = event.return_event()
    desc = ""
    if event.type == "Task":
        desc = ev.description
    for times in event.times.times():
        [[start_day, start_slot], [end_day, end_slot]] = times
        start = TimeObject(dayzero, start_day, start_slot)
        end = TimeObject(dayzero, end_day, end_slot+1)
        print(start_slot)
        print(end_slot)
        event = {
            'summary': ev.name,
            'description': desc,
            'start': {
                'dateTime': str(start),
                'timeZone': start.timeZone,
            },
            'end': {
                'dateTime': str(end),
                'timeZone': end.timeZone,
            },
        }
        event = service.events().insert(calendarId=presets.calendar_id, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))



def import_events(service):
    schedule = import_schedule()
    googleevent = import_google_event()
    for ge in googleevent:
        schedule.delete_event("GoogleEvent", ge.google_event_id)
        delete_google_event(ge.google_event_id)
    for event in list_events(service, True):
        if event['status'] == 'confirmed':
            startTime=str_init(event['start']['dateTime'],event['start']['timeZone'])
            endTime=str_init(event['end']['dateTime'],event['end']['timeZone'])
            if 'description' in event:
                desc = event['description']
            else:
                desc = ""
            ge = GoogleEvent(-1, event['summary'], desc, startTime, endTime)
            ge.export_google_event()
            vars = ge.create_event()
            event = Event(vars[0], vars[1], vars[2], vars[3])
            schedule.add_event(event)
    schedule.export_schedule()

def export_events(service):
    presets = Presets()
    if presets.calendar_id != -1:
        delete_calendar(service, presets.calendar_id)
    calid = create_calendar(service, 'TwentyFive-Eight')
    presets.calendar_id = calid
    presets.Store()
    schedule = import_schedule()
    for event in schedule.events_list:
        if event.type == "Task":
            insert_event(service, event)
