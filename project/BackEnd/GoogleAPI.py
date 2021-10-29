import datetime

from project.BackEnd.Google import Create_Service
from project.BackEnd.GoogleEvent import GoogleEvent, find_google_event
from project.BackEnd.NewSchedule import import_schedule
from project.BackEnd.Preset import Presets
from project.BackEnd.Routine import find_routine
from project.BackEnd.Task import Task, find_task
from pprint import pprint
import os
import time

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


def return_event(event):
    if event.type == "Task":
        task = find_task(os.path.join(dirname, '../data/save_file.json'), event.id)
        return task
    elif event.type == "GoogleEvent":
        google_event = find_google_event(os.path.join(dirname, '../data/google_events.json'), event.id)
        return google_event
    elif event.type == "Routine":
        routine = find_routine(os.path.join(dirname, '../data/routines.json'), event.id)
        return routine
    else:
        print("Type does not exist")


def get_event(service, event_id):
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    print(event['summary'])


def delete_event(service, event_id):
    service.events().delete(calendarId='primary', eventId=event_id).execute()


def insert_event(service, event):
    presets = Presets()
    dayzero=presets.day_zero
    ev = return_event(event)
    desc = ""
    if event.type == "Task":
        desc = ev.description
    for times in event.times.times():
        [[start_day, start_slot], [end_day, end_slot]]=times
        start=TimeObject(dayzero, start_day, start_slot)
        end=TimeObject(dayzero, end_day, end_slot)
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
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))



def import_events(service, eventfile, schedulefile):
    schedule = import_schedule(schedulefile)
    for event in list_events(service, True):
        if event['status'] == 'confirmed':
            startTime=str_init(event['start']['dateTime'],event['start']['timeZone'])
            endTime=str_init(event['end']['dateTime'],event['end']['timeZone'])
            if 'description' in event:
                desc = event['description']
            else:
                desc = ""
            ge = GoogleEvent(-1, event['summary'], desc, startTime, endTime, eventfile)
            ge.export_google_event(eventfile)
            event = ge.create_event()
            schedule.add_event(event)
    schedule.export_schedule(schedulefile)

def export_events(service, schedule):
    presets = Presets()
    if presets.calendar_id == -1:
        calid = create_calendar(service, 'TwentyFive-Eight')
        presets.calendar_id = calid
        presets.Store()
    else:
        cal = get_calendar(service, presets.calendar_id)
        print(cal)

def main():
    service = authenticate()
    create_calendar(service, 'I hate people')
    # delete_calendar(service, '3eosiknkb75tu3cta6140ke5dg@group.calendar.google.com')
    # list_calendars(service)
    # insert_event(service, Task.find_task())
    # colorprofiles = service.colors().get().execute()
    # pprint(colorprofiles)

if __name__ == "__main__":
    main()
