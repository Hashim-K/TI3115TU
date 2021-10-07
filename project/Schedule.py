import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import GoogleImport
from General import *


def Add2Schedule(event):
    blocks = []
    for Occurrence in event.Occurrences:
        time1, time2 = Occurrence[0], Occurrence[1]
        if time1[0] == time2[0]:
            block = [time1, time2]
            blocks.append(block)
        else:
            block = [time1, [time1[0], round(24 * 60 / presets.time_interval)]]
            blocks.append(block)
            block = [[time2[0], 0], time2]
            blocks.append(block)

    for block in blocks:
        for slot in range(block[0][1], block[1][1]):
            slot_id = int(Schedule.schedule[block[0][0]][slot])
            if slot_id == -1:
                Schedule.schedule[block[0][0]][slot] = event.ID
            else:
                Schedule.overlap[block[0][0]][slot] = event.ID


def ImportGoogleEvents():
    day_zero = presets.day_zero
    time_interval = presets.time_interval
    google_events = GoogleImport.Import(day_zero, presets.number_of_days)
    colors = ['#DAF0C2', '#B0DC7A', '#7FBD32', '#649528', '#477114', '#CBBA01', '#B6A702', '#A39600', '#8A7C00']
    color_id = 0
    for event in google_events:
        label = str(event[0])
        time1 = DayAndSlot(event[1], day_zero, time_interval)
        time2 = DayAndSlot(event[2], day_zero, time_interval)
        Event(label, colors[color_id], [[time1, time2]])
        color_id = color_id + 1


def DeleteEvent(index):
    events.pop(index)
    for event in events[index:]:
        event.ID = event.ID - 1


def RoutineEvents():
    time_interval = presets.time_interval
    number_of_slots = len(Schedule.schedule[0])
    for day in range(len(Schedule.schedule)):
        end_day = day
        end_slot = Slot(presets.alarm_time, time_interval)
        start_day = day
        start_slot = Slot(presets.alarm_time, time_interval) - Slot(presets.length_sleep, time_interval)
        if start_slot < 0:
            if day == 0:
                start_slot = 0
            else:
                start_day = day - 1
                start_slot = start_slot + number_of_slots
        Sleep.Occurrences.append([[start_day, start_slot], [end_day, end_slot]])
        MorningRoutine.Occurrences.append(
            [[end_day, end_slot], [end_day, end_slot + Slot(presets.length_morning_routine, time_interval)]])
        start_lunch = Slot(presets.lunch_time, time_interval)
        end_lunch = Slot(presets.lunch_time, time_interval) + Slot(presets.length_lunch, time_interval)
        Lunch.Occurrences.append([[end_day, start_lunch], [end_day, end_lunch]])
        start_dinner = Slot(presets.dinner_time, time_interval)
        end_dinner = Slot(presets.dinner_time, time_interval) + Slot(presets.length_dinner, time_interval)
        Dinner.Occurrences.append([[end_day, start_dinner], [end_day, end_dinner]])


def AppendEvents():
    for event in events:
        Add2Schedule(event)


def Display():
    day_zero = presets.day_zero
    number_of_days = len(Schedule.schedule)
    xticks = CreateXTicks(day_zero, number_of_days)
    yticks = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
              '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    number_of_days = len(Schedule.schedule)
    number_of_slots = len(Schedule.schedule[0])
    axes = plt.gca()
    axes.set_xlim([0, number_of_days])
    axes.set_ylim([0, number_of_slots])
    axes.invert_yaxis()
    plt.xticks(np.arange(number_of_days), xticks, rotation=30)
    plt.yticks(np.arange(0, number_of_slots, step=number_of_slots / 24), yticks)
    plt.title('Schedule for ' + DateFormat(day_zero) + ' till ' + DateFormat(XDaysLater(day_zero, number_of_days - 1)))

    for j in range(len(Schedule.schedule)):
        for k in range(len(Schedule.schedule[j])):
            id = int(Schedule.schedule[j][k])
            if id >= 0:
                rect = mpatches.Rectangle((j, k), 1, 1, facecolor=events[id].Colour)
                plt.gca().add_patch(rect)
            overlap_id = int(Schedule.overlap[j][k])
            if overlap_id >= 0:
                rect = mpatches.Rectangle((j, k), 0.5, 1, facecolor=events[overlap_id].Colour)
                plt.gca().add_patch(rect)

    legend_elements = []
    for id in range(len(events)):
        legend_elements.append(mpatches.Patch(facecolor=events[id].Colour, label=events[id].Label))
    axes.legend(handles=legend_elements, bbox_to_anchor=(1.01, 1.0), loc='upper left')
    plt.grid(axis='x', color='black')
    plt.grid(axis='y', color='black', linewidth=0.5, alpha=0.25)
    plt.tight_layout()

    plt.show()


def ResolveOverlap():
    number_of_days = len(Schedule.schedule)
    number_of_slots = len(Schedule.schedule[0])
    is_overlap = False
    identified_overlaps = []
    for day in range(number_of_days):
        for slot in range(number_of_slots):
            event1_id = int(Schedule.overlap[day][slot])
            if event1_id >= 0:
                is_overlap = True
                event2_id = int(Schedule.schedule[day][slot])
                print_message = True
                for overlap in identified_overlaps:
                    if event1_id == overlap[0] and event2_id == overlap[1] and day == overlap[2]:
                        print_message = False
                if print_message:
                    print('It seems like ' + str(events[event1_id].Label)
                          + ' overlaps with ' + str(events[event2_id].Label)
                          + ' on ' + DateFormat(XDaysLater(presets.day_zero, day)) + '.')
                    identified_overlaps.append([event1_id, event2_id, day])
    return is_overlap


# Event Class
events = []


class Event:
    def __init__(self, Label, Color, Occurrences):
        self.Label = Label
        self.Occurrences = Occurrences
        self.Colour = Color
        events.append(self)
        self.ID = events.index(self)


class PreSets:
    def __init__(self, day_zero, number_of_days, time_interval, alarm_time, length_sleep, length_morning_routine,
                 lunch_time, length_lunch, dinner_time, length_dinner):
        self.day_zero = day_zero
        self.number_of_days = number_of_days
        self.time_interval = time_interval
        self.alarm_time = alarm_time
        self.length_sleep = length_sleep
        self.length_morning_routine = length_morning_routine
        self.lunch_time = lunch_time
        self.length_lunch = length_lunch
        self.dinner_time = dinner_time
        self.length_dinner = length_dinner


class GetArrays:
    def __init__(self):
        self.schedule = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1
        self.overlap = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1


# Objects


Sleep = Event('Sleep', '#546fa8', [])
MorningRoutine = Event('Morning Routine', '#8399c9', [])
Lunch = Event('Lunch', '#e8b048', [])
Dinner = Event('Dinner', '#ba8420', [])

presets = PreSets('2021-09-17', 7, 5, '07:30:00', '08:00:00', '00:40:00',
                  '12:30:00', '00:45:00', '18:30:00', '01:15:00')


def SetSchedule():
    global Schedule
    Schedule = GetArrays()


def SetUp():
    SetSchedule()
    #ImportGoogleEvents()  # Blocked for till the google import works again.
    RoutineEvents()
    AppendEvents()
    Display()
    ResolveOverlap()


def Adjust():
    SetSchedule()
    AppendEvents()
    Display()
    ResolveOverlap()


SetUp()
DeleteEvent(0)
Adjust()

EmptySlots(Schedule.schedule)


