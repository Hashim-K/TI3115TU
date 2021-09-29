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
            block = [time1, [time1[0], round(24 * 60 / time_interval)]]
            blocks.append(block)
            block = [[time2[0], 0], time2]
            blocks.append(block)


    for block in blocks:
        for slot in range(block[0][1], block[1][1]):
            slot_id = int(schedule_array[block[0][0]][slot])
            if slot_id == -1:
                schedule_array[block[0][0]][slot] = event.ID
            else:
                overlap_array[block[0][0]][slot] = event.ID


def ImportGoogleEvents():
    google_events = GoogleImport.Import(day_zero, number_of_days)
    colors = GetColors()
    color_id = 0
    for event in google_events:
        label = str(event[0])
        time1 = DayAndSlot(event[1], day_zero, time_interval)
        time2 = DayAndSlot(event[2], day_zero, time_interval)
        Event(label, colors[color_id], [[time1, time2]])
        color_id = color_id + 1


def SleepEvent():
    for day in range(len(schedule_array)):
        end_day = day
        end_slot = Slot(alarm_time, time_interval)
        start_day = day
        start_slot = Slot(alarm_time, time_interval) - Slot(length_sleep, time_interval)
        if start_slot < 0:
            if day == 0:
                start_slot = 0
            else:
                start_day = day - 1
                start_slot = start_slot + number_of_slots
        Sleep.Occurrences.append([[start_day, start_slot], [end_day, end_slot]])
        MorningRoutine.Occurrences.append(
            [[end_day, end_slot], [end_day, end_slot + Slot(length_morning_routine, time_interval)]])


def AppendEvents():
    for event in Events:
        Add2Schedule(event)


def Display():
    xticks = CreateXTicks(day_zero, number_of_days)
    yticks = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
              '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
    axes = plt.gca()
    axes.set_xlim([0, number_of_days])
    axes.set_ylim([0, number_of_slots])
    axes.invert_yaxis()
    plt.xticks(np.arange(number_of_days), xticks, rotation=30)
    plt.yticks(np.arange(0, number_of_slots, step=number_of_slots / 24), yticks)
    plt.title('Schedule for ' + DateFormat(day_zero) + ' till ' + DateFormat(XDaysLater(day_zero, number_of_days - 1)))

    for j in range(len(schedule_array)):
        for k in range(len(schedule_array[j])):
            id = int(schedule_array[j][k])
            if id >= 0:
                rect = mpatches.Rectangle((j, k), 1, 1, facecolor=Colors[id])
                plt.gca().add_patch(rect)
            overlap_id = int(overlap_array[j][k])
            if overlap_id >= 0:
                rect = mpatches.Rectangle((j, k), 0.5, 1, facecolor=Colors[overlap_id])
                plt.gca().add_patch(rect)

    legend_elements = []
    for id in range(len(Events)):
        legend_elements.append(mpatches.Patch(facecolor=Colors[id], label=Labels[id]))
    axes.legend(handles=legend_elements, bbox_to_anchor=(1.01, 1.0), loc='upper left')
    plt.grid(axis='x', color='black')
    plt.grid(axis='y', color='black', linewidth=0.5, alpha=0.25)
    plt.tight_layout()

    plt.show()


def ResolveOverlap():
    choice = 0
    is_overlap = False
    identified_overlaps = []
    for day in range(number_of_days):
        for slot in range(number_of_slots):
            event1_id = int(overlap_array[day][slot])
            if event1_id >= 0:
                is_overlap = True
                event2_id = int(schedule_array[day][slot])
                print_message = True
                for overlap in identified_overlaps:
                    if event1_id == overlap[0] and event2_id == overlap[1] and (
                            day == overlap[2] or day - 1 == overlap[2]):
                        print_message = False
                        ExecuteChoice(choice, day, slot, event1_id, event2_id)
                if print_message:
                    print('It seems like ' + str(Labels[event1_id])
                          + ' overlaps with ' + str(Labels[event2_id])
                          + ' on ' + DateFormat(XDaysLater(day_zero, day)) + '.')
                    identified_overlaps.append([event1_id, event2_id, day])
                    print('[1] Prioritize ' + str(Labels[event1_id]) + '.')
                    print('[2] Prioritize ' + str(Labels[event2_id]) + '.')
                    print('[3] Alter times for ' + str(Labels[event2_id]) + '.')
                    choice = int(input())
                    ExecuteChoice(choice, day, slot, event1_id, event2_id)
    return is_overlap


def ExecuteChoice(choice, day, slot, event1_id, event2_id):
    if choice == 1:
        schedule_array[day][slot] = event1_id
        overlap_array[day][slot] = -1
    elif choice == 2:
        schedule_array[day][slot] = event2_id
        overlap_array[day][slot] = -1


# Event Class
Events = []
Colors = []
Labels = []


class Event:
    def __init__(self, Label, Color, Occurrences):
        self.Label = Label
        self.Occurrences = Occurrences
        Events.append(self)
        Labels.append(Label)
        Colors.append(Color)
        self.ID = Events.index(self)


Sleep = Event('Sleep', '#546fa8', [])
MorningRoutine = Event('Morning Routine', '#8399c9', [])

# Main
day_zero = '2021-09-17'  # The first day shown in the schedule.
number_of_days = 10  # The amount of days shown in the schedule.
time_interval = 5  # The bin width of the timeslots.
number_of_slots = round(24 * 60 / time_interval)  # The number of timeslots in a day.

alarm_time = '07:00:00'
length_sleep = '08:00:00'
length_morning_routine = '0:40:00'

ImportGoogleEvents()  # Imports the events from the google calendar.
schedule_array = CreateArray(number_of_days, number_of_slots)  # Creates the empty schedule.
overlap_array = CreateArray(number_of_days, number_of_slots)
SleepEvent()  # Adds sleep and morning routine to the calendar
AppendEvents()  # Appends the events to the schedule.
Display()  # Displays the schedule.
while 1 + 1 == 2:
    overlapping = ResolveOverlap()
    if not overlapping:
        break
Display()


# Stuff that might be useful later.
'''
Dinner = Event('Dinner', '#86c452', [[[0, 222], [0, 230]],
                                     [[1, 217], [1, 226]],
                                     [[2, 221], [2, 233]],
                                     [[3, 219], [3, 226]],
                                     [[4, 222], [4, 229]],
                                     [[5, 223], [5, 231]],
                                     [[6, 222], [6, 230]]])
FreeTime = Event('Free Time', '#e6f0e9', [])

FreeBlocks = EmptySlots(Schedule,number_of_slots)

for FreeBlock in FreeBlocks:
    FreeTime.Occurences.append(FreeBlock)
Add2Schedule(FreeTime,time_interval)
'''
