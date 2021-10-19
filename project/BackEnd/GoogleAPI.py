from project.BackEnd.Google import Create_Service
from pprint import pprint
import os
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

def main():
    service = authenticate()
    # create_calendar(service, 'I hate people')
    # delete_calendar(service, '3eosiknkb75tu3cta6140ke5dg@group.calendar.google.com')
    # list_calendars(service)
    colorprofiles = service.colors().get().execute()
    pprint(colorprofiles)

main()