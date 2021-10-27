import json
import os
import textwrap

import numpy as np
from project.BackEnd.GoogleEvent import find_google_event
from project.BackEnd.Preset import Presets
from project.BackEnd.Routine import find_routine
from project.BackEnd.Task import find_task

from project.BackEnd.General import CheckWhatDay, XDaysLater, find_day_zero
from project.BackEnd.TimeList import TimeList

dirname = os.path.dirname(__file__)

class Event:
    def __init__(self, type: str, id: int, times: TimeList):
        self.type = type
        self.id = id
        self.times=times

    def return_event(self):
        if type == "Task" :
            task = find_task(os.path.join(dirname, '../data/save_file.json'), self.id)
            return task
        elif type == "GoogleEvent":
            google_event = find_google_event(os.path.join(dirname, '../data/google_events.json'), self.id)
            return google_event
        elif type == "Routine":
            routine = find_routine(os.path.join(dirname, '../data/google_events.json'), self.id)
            return routine
        else:
            print("Type does not exist")



class Schedule:
    def __init__(self):
        presets = Presets()
        self.number_of_slots = round(24 * 60 / presets.time_interval)
        self.schedule = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval)), dtype=object) - 1
        self.events_list = []

    def __str__(self):
        text =""
        for i in range(len(self.schedule)):
            text_description = "Day "+ str(i+1) +": ["
            for j in range(len(self.schedule[i])):
                if isinstance(self.schedule[i][j], int):
                    text_description += str(self.schedule[i][j])
                else:
                    text_description += self.schedule[i][j].type+": (" + str(self.schedule[i][j].id) + ")"
                if j < len(self.schedule[i])-1:
                    text_description += ", "
            text_description += "]\n"
            for line in textwrap.wrap(text_description, 100):
                text += line + "\n"

        return text

    def add_event(self, event):
        self.events_list.append(event)
        presets = Presets()
        ti = presets.time_interval
        number_of_slots = int(1440/ti)
        for time in event.times.times():
            start_day = time[0][0]
            start_time = time[0][1]
            end_day = time[1][0]
            end_time = time[1][1]
            while start_day*number_of_slots+start_time <= end_day*number_of_slots+end_time:
                self.schedule[start_day, start_time] = event
                start_time += 1
                if start_time >= number_of_slots:
                    start_time -= number_of_slots
                    start_day += 1

    def export_schedule(self, filename):
        """ Storing events in a JSON file. """
        if not os.path.exists(filename):  # if filename does not exist create a list to fill
            data = []
        else:
            if os.stat(filename).st_size == 0:  # if filename is empty make new one
                os.remove(filename)
                data = []
            else:
                with open(filename, 'r') as file:  # if filename exists load the data
                    data = json.load(file)
        for event in self.events_list:
            entry = {
                "Type": event.type,
                "ID": event.id,
                "Times": event.times.times()
            }
            data.append(entry)
        with open(filename, 'w') as file:  # write into file
            json.dump(data, file, indent=6)

def import_schedule(filename):
    """ Creates a list of all the routines in a JSON file. """
    events_list = []
    try:
        with open(filename, 'r') as file:
            event_dict = json.load(file)
            for event in event_dict:
                tl = TimeList()
                for time in event['Times']:
                    tl.add_time(time[0][0], time[0][1], time[1][0], time[1][1])
                events_list.append(Event(event['Type'], event['ID'], tl))
    except FileNotFoundError:
        print('File does not exist')
    schedule = Schedule()
    for event in events_list:
        schedule.add_event(event)
    return schedule
