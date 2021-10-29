import json
import os
import textwrap

import numpy as np
from matplotlib import pyplot as plt, patches

from project.BackEnd.Display import Display
from project.BackEnd.GoogleEvent import find_google_event
from project.BackEnd.Preset import Presets
from project.BackEnd.Routine import find_routine
from project.BackEnd.Task import find_task

from project.BackEnd.General import CheckWhatDay, XDaysLater, find_day_zero, DateFormat
from project.BackEnd.TimeList import TimeList

dirname = os.path.dirname(__file__)

class Event:
    def __init__(self, type: str, id: int, color: str, times: TimeList,):
        self.type = type
        self.id = id
        self.color=color
        self.times=times

    def return_event(self):
        if self.type == "Task":
            task = find_task(os.path.join(dirname, '../data/save_file.json'), self.id)
            return task
        elif self.type == "GoogleEvent":
            google_event = find_google_event(os.path.join(dirname, '../data/google_events.json'), self.id)
            return google_event
        elif self.type == "Routine":
            routine = find_routine(os.path.join(dirname, '../data/google_events.json'), self.id)
            return routine
        else:
            print("Type does not exist")



class Schedule:
    def __init__(self):
        presets = Presets()
        self.number_of_slots = round(24 * 60 / presets.time_interval)
        self.schedule = np.zeros(shape=(presets.number_of_days, round(self.number_of_slots)), dtype=object) - 1
        self.events_list = []
        self.overlap = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1

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
                "Color": event.color,
                "Times": event.times.times()
            }
            data.append(entry)
        with open(filename, 'w') as file:  # write into file
            json.dump(data, file, indent=6)

    # This bit checks for empty slot in the schedule. It returns a list of the blocks of empty slots.
    def empty_slots(self):
        presets = Presets()
        empty_slots = []
        for day in range(presets.number_of_days):
            for slot in range(self.number_of_slots):
                if isinstance(self.schedule[day][slot], int):
                    empty_slots.append([day, slot])
        empty_blocks = []
        start_slot = empty_slots[0]
        for i in range(1, len(empty_slots)):
            # Check if empty_slots[i] and empty_slots[i+1] are consecutive.
            consecutive = False
            if (not (empty_slots[i][0] == presets.number_of_days - 1 and empty_slots[i][
                1] == self.number_of_slots - 1)
                    and empty_slots[i] != empty_slots[-1]):
                if empty_slots[i][0] == empty_slots[i + 1][0] and empty_slots[i][1] == empty_slots[i + 1][1] - 1:
                    consecutive = True
                if empty_slots[i][1] == self.number_of_slots - 1 and empty_slots[i + 1][1] == 0 \
                        and empty_slots[i][0] == empty_slots[i + 1][0] - 1:
                    consecutive = True
            if not consecutive:
                empty_blocks.append([start_slot, empty_slots[i]])
                if empty_slots[i] != empty_slots[-1]:
                    start_slot = empty_slots[i + 1]
        return empty_blocks

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
                events_list.append(Event(event['Type'], event['ID'], event['Color'], tl))
    except FileNotFoundError:
        print('File does not exist')
    schedule = Schedule()
    for event in events_list:
        schedule.add_event(event)
    return schedule

def SaveImage(filename):
    presets = Presets()
    display = Display()
    day_zero = presets.day_zero
    schedule = import_schedule(filename)
    number_of_days = presets.number_of_days
    number_of_slots = schedule.number_of_slots
    xticks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    yticks = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
              '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    fig, ax = plt.subplots(figsize=(display.width, display.height), facecolor=display.background_color)

    ax.spines[:].set_color(display.face_color)
    ax.tick_params(colors=display.background_color)

    axes = plt.gca()
    axes.set_facecolor(display.face_color)
    axes.set_xlim([0, number_of_days])
    axes.set_ylim([0, number_of_slots])
    axes.invert_yaxis()
    plt.xticks(np.arange(number_of_days), xticks, ha="left", color=display.text_color)
    plt.yticks(np.arange(0, number_of_slots, step=number_of_slots / 24), yticks, color=display.text_color)
    plt.title(f'Schedule for {DateFormat(day_zero)} till {DateFormat(XDaysLater(day_zero, number_of_days - 1))}',
              color=display.text_color)

    for j in range(number_of_days):
        for k in range(number_of_slots):
            event = schedule.schedule[j][k]
            whitespace = j + 0.05
            if not isinstance(schedule.schedule[j][k], int):
                rect = patches.Rectangle((whitespace, k), 0.91, 1, facecolor=event.color)
                plt.gca().add_patch(rect)

    legend_elements = []
    for event in schedule.events_list:
        event_type = event.return_event()
        legend_elements.append(patches.Patch(facecolor=event.color, label=event_type.name))
    legend = axes.legend(handles=legend_elements, bbox_to_anchor=(1.01, 1.0), loc='upper left', frameon=False)
    plt.setp(legend.get_texts(), color=display.text_color)
    plt.grid(axis='x', color=display.text_color, linewidth=0.5, alpha=0.25, linestyle='dotted')
    plt.grid(axis='y', color=display.text_color, linewidth=0.5, alpha=0.25, linestyle='dotted')
    plt.tight_layout()

    plt.savefig(os.path.join(dirname, '../data/schedule.jpg'))

