import json
import os.path

from project.BackEnd.Preset import Presets
from project.BackEnd.TimeList import TimeList
from project.BackEnd.TimeObject import TimeObject, str_init
dirname = os.path.dirname(__file__)



class GoogleEvent:
    """ The google_event class is used to create, store and edit google_events used by the software in a JSON format. """

    highest_id = 0

    def __init__(self, google_event_id: int, name: str, description: str, start: TimeObject, end: TimeObject):
        preset = Presets()
        if google_event_id != -1: # google_event_id is given in the initializer
            self.google_event_id = google_event_id
        else:
            if not os.path.exists(preset.google_path) or os.stat(preset.google_path).st_size < 4: # calculating google_event_id from the already exisiting events
                GoogleEvent.highest_id += 1
                self.google_event_id = GoogleEvent.highest_id
            else:
                with open(preset.google_path) as file: # calculating google_event_id from an already existing JSON file with google_events
                    google_event_dict = json.load(file)
                    self.google_event_id = google_event_dict[-1]['google_event_id'] + 1
        self.name = name
        self.description = description
        self.start = start
        self.end = end

    def __str__(self):
        text_description = f"google_event: \"{self.name}\" ({self.google_event_id})\n"\
                            + f"description: {self.description}.\n"\
                            + f"'start': {{\n"\
                            + f"    'dateTime': {self.start.dateTime}\n"\
                            + f"    'timeZone': {self.start.timeZone}\n"\
                            + f"}},\n"\
                            + f"'end\': {{\n"\
                            + f"    'dateTime': {self.end.dateTime}\n"\
                            + f"    'timeZone': {self.end.timeZone}\n"\
                            + f"}}\n"
        return text_description

    def export_google_event(self):
        """ Storing google_events in a JSON file. """
        preset = Presets()
        entry = {
            "google_event_id": self.google_event_id,
            "Name": self.name,
            "Description": self.description,
            "Start":{
                "dateTime": self.start.dateTime,
                "timeZone": self.start.timeZone
            },
            "End":{
                "dateTime": self.end.dateTime,
                "timeZone": self.end.timeZone
            }
        }
        if not os.path.exists(preset.google_path):  # if filename does not exist create a list to fill
            data = []
        else:
            if os.stat(preset.google_path).st_size == 0:  # if filename is empty make new one
                os.remove(preset.google_path)
                data = []
            else:
                with open(preset.google_path, 'r') as file:  # if filename exists load the data
                    data = json.load(file)
        data.append(entry)
        with open(preset.google_path, 'w') as file:  # write into file
            json.dump(data, file, indent=6)

    def create_event(self):
        [start_day, start_slot] = self.start.dateTime_to_timeslot()
        [end_day, end_slot] = self.end.dateTime_to_timeslot()
        timelist = TimeList()
        timelist.add_time(start_day, start_slot, end_day, end_slot)
        return ["GoogleEvent", self.google_event_id, "#027CB7", timelist]

def import_google_event():
    """ Creates a list of all the google_events in a JSON file. """
    presets = Presets()
    google_events_list = []
    try:
        with open(presets.google_path, 'r') as file:
            google_event_dict = json.load(file)
            for google_events in google_event_dict:
                google_events_list.append(GoogleEvent(google_events['google_event_id'], google_events['Name'], google_events['Description']
                                                      , str_init(google_events['Start']['dateTime'],google_events['Start']['timeZone'])
                                                      , str_init(google_events['End']['dateTime'],google_events['End']['timeZone'])))
    except FileNotFoundError:
        print('File does not exist')
    return google_events_list


def find_google_event(google_event_ID):
    """ Seeks for a google_event by its google_event_id. """
    google_events_list = import_google_event()
    for google_event in google_events_list:
        if google_event.google_event_id == google_event_ID:
            return google_event
    print('google_event: google_event not Found')


def delete_all_google_events():
    """Deletes all google_events from a JSON file."""
    google_events_list = import_google_event()
    for google_event in google_events_list:
        delete_google_event(google_event.google_event_id)


def delete_google_event(google_event_id):
    """ Delete a google_event from a JSON file. """
    presets = Presets()
    try:
        with open(presets.google_path, 'r') as file:
            google_event_dict = json.load(file)
        for i in range(len(google_event_dict)):
            if google_event_dict[i]['google_event_id'] == google_event_id:
                del google_event_dict[i]
                break
        with open(presets.google_path, 'w') as file:
            json.dump(google_event_dict, file, indent = 6)
    except FileNotFoundError:
        print('File does not exist')
