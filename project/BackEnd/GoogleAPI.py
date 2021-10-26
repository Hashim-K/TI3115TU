from project.BackEnd.Google import Create_Service
from project.BackEnd.Task import Task
from pprint import pprint
import os
import time
dirname = os.path.dirname(__file__)


def authenticate():
    CLIENT_SECRET_FILE = os.path.join(dirname, '../new_client_secret.json')
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    return Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_calendar(service, title):
    request_body = {
        'summary': title
    }
    response = service.calendars().insert(body=request_body).execute()
    print(response)


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


def list_events(service):
    page_token = None
    eventlist=[]
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            eventlist.append(event)
            print(event['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def get_event(service, event_id):
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    print(event['summary'])


def delete_event(service, event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()


def insert_event(service, task):
    event = {
        'summary': task.name,
        'description': task.description,
        'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': time.tzname[time.daylight],
        },
        'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': time.tzname[time.daylight],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def import_events(service):
    list_events(service)


def export_events(service):
    print("hi")

def main():
    service = authenticate()
    # create_calendar(service, 'I hate people')
    # delete_calendar(service, '3eosiknkb75tu3cta6140ke5dg@group.calendar.google.com')
    # list_calendars(service)
    insert_event(service, Task.find_task())
    # colorprofiles = service.colors().get().execute()
    # pprint(colorprofiles)

main()