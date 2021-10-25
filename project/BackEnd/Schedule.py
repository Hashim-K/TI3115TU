import json
from json import JSONDecodeError

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from project.BackEnd import GoogleImport
from project.BackEnd.General import DayAndSlot, DateFormat, XDaysLater, CheckWhatDay, Slot2Time, TimeBetween, Slot
import os
dirname = os.path.dirname(__file__)




# This function initializes the stuff in GoogleImport and gets a list of the google events. Then for each event in
# the list, it assigns a color and creates an event class object.
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


# This function determines the start day and slot and end day and slot in the form used in event.Occurrences
# ([[start_day, start_slot], [end_day, end_slot]]).
def StartAndEnd(day, start_slot, duration):
    start_day = day
    end_day = day
    end_slot = start_slot + duration
    while start_slot < 0:
        start_day = start_day - 1
        start_slot = start_slot + schedule.number_of_slots
    while end_slot >= schedule.number_of_slots:
        end_day = end_day + 1
        end_slot = end_slot - schedule.number_of_slots
    if start_day < 0:
        start_day = 0
        start_slot = 0
    if end_day >= presets.number_of_days:
        end_day = presets.number_of_days - 1
        end_slot = schedule.number_of_slots
    return [[start_day, start_slot], [end_day, end_slot]]


# This function appends all events in the events list to the schedule.
def AppendEvents():
    for event in events:
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
                slot_id = int(schedule.schedule[block[0][0]][slot])
                if slot_id == -1:
                    schedule.schedule[block[0][0]][slot] = event.ID
                else:
                    schedule.overlap[block[0][0]][slot] = event.ID


# Block index
def BlockIndex(blocks, day, slot):
    for block in blocks:
        if block[0][0] == block[1][0]:
            if block[0][0] == day and block[0][1] <= slot <= block[1][1]:
                return blocks.index(block)
        else:
            if block[0][0] == day and block[0][1] <= slot or (block[1][0] == day and block[1][1] >= slot):
                return blocks.index(block)


# This bit goes through all slots in the schedule.overlap array to check whether overlap occurs. It returns
# True or False based on whether there is overlap or not.
def ResolveOverlap():
    number_of_days = presets.number_of_days
    number_of_slots = len(schedule.schedule[0])
    is_overlap = False
    identified_overlaps = []
    for day in range(number_of_days):
        for slot in range(number_of_slots):
            event1_id = int(schedule.overlap[day][slot])
            if event1_id >= 0:
                is_overlap = True
                event2_id = int(schedule.schedule[day][slot])
                print_message = True
                for overlap in identified_overlaps:
                    if event1_id == overlap[0] and event2_id == overlap[1] and day == overlap[2]:
                        print_message = False
                if print_message:
                    index = BlockIndex(events[event2_id].Occurrences, day, slot)
                    print(f"It seems like '{events[event1_id].Label}' overlaps with '{events[event2_id].Label}' on "
                          f"{DateFormat(XDaysLater(presets.day_zero, day))}. "
                          f"[Event={events[event2_id].ID}, Occurrence={index}]\n")
                    identified_overlaps.append([event1_id, event2_id, day])
    return is_overlap


# This function deletes an event based on its id.
def DeleteEvent(index):
    events.pop(index)
    for event in events[index:]:
        event.ID = event.ID - 1


# This function displays the schedule plot. It can be modified to return a .jpg file which could be used by the GUI.
def SaveImage():
    if presets.dark_mode:
        display.DarkMode()
    else:
        display.LightMode()
    day_zero = presets.day_zero
    number_of_days = presets.number_of_days
    number_of_slots = schedule.number_of_slots
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    date = [int(day_zero.split('-')[2]), int(day_zero.split('-')[1]), int(day_zero.split('-')[0])]
    day = CheckWhatDay(date)
    xticks = []
    for i in range(number_of_days):
        if day + i > 6:
            day = day - 7
        xticks.append(days[day + i])
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
            id = int(schedule.schedule[j][k])
            whitespace = j + 0.05
            if id >= 0:
                rect = patches.Rectangle((whitespace, k), 0.91, 1, facecolor=events[id].Color)
                plt.gca().add_patch(rect)
            overlap_id = int(schedule.overlap[j][k])
            if overlap_id >= 0:
                rect = patches.Rectangle((whitespace, k), 0.5, 1, facecolor=events[overlap_id].Color)
                plt.gca().add_patch(rect)

    legend_elements = []
    for id in range(len(events)):
        legend_elements.append(patches.Patch(facecolor=events[id].Color, label=events[id].Label))
    legend = axes.legend(handles=legend_elements, bbox_to_anchor=(1.01, 1.0), loc='upper left', frameon=False)
    plt.setp(legend.get_texts(), color=display.text_color)
    plt.grid(axis='x', color=display.text_color, linewidth=0.5, alpha=0.25, linestyle='dotted')
    plt.grid(axis='y', color=display.text_color, linewidth=0.5, alpha=0.25, linestyle='dotted')
    plt.tight_layout()

    plt.savefig('schedule.jpg')


def PrintBlockInfo(blocks):
    print(f'index   start_date   start_time  end_date     end_time    duration')
    for block in blocks:
        prefix = ''
        if blocks.index(block) < 10:
            prefix = '0'
        print(f' [{prefix}{blocks.index(block)}]'
              f'   {XDaysLater(presets.day_zero, block[0][0])}'
              f'    {Slot2Time(block[0][1], presets.time_interval)} '
              f'   {XDaysLater(presets.day_zero, block[1][0])}'
              f'    {Slot2Time(block[1][1], presets.time_interval)}'
              f'    {TimeBetween(block, presets.time_interval)}')
    print()


def PrintEmpty():
    print('Empty blocks:')
    PrintBlockInfo(EmptySlots())


# This bit checks for empty slot in the schedule. It returns a list of the blocks of empty slots.
def EmptySlots():
    number_of_slots = schedule.number_of_slots
    free_blocks = []
    free_block = []
    for day in range(presets.number_of_days):
        for slot in range(schedule.number_of_slots):
            if slot == number_of_slots -1:
                free_block.append([day, slot])
                free_blocks.append(free_block)
                free_block = []
            elif schedule.schedule[day][slot] == -1:
                free_block.append([day, slot])
            else:
                # if slot == number_of_slots -1:
                #     free_block.append([day, slot])
                #     free_blocks.append(free_block)
                #     free_block = []
                if len(free_block) > 0 or (len(free_block) > 0 and slot == number_of_slots - 1):
                    free_block.append([day, slot])
                    free_blocks.append(free_block)
                    free_block = []
    for free_block in free_blocks:
        while len(free_block) > 2:
            free_block.pop(1)
    for free_block in free_blocks:  # this code is a temporary fix
        if len(free_block) < 2:
            free_blocks.pop(free_blocks.index(free_block))
    return free_blocks


def ClearEvents():
    with open(os.path.join(dirname, 'events.json'), 'w') as file:
        file.write('')
    events.clear()
    PrepEvents()


def PrepEvents():
    try:
        GetEvents()
    except:
        pass
    if not events:
        SetSleep()
        SetLunch()
        SetDinner()
        StoreEvents()

    schedule.Update()
    SaveImage()


def GetEvents():
    with open(os.path.join(dirname, 'events.json'), 'r') as open_file:
        events_dict = json.load(open_file)
        for event in events_dict:
            Event(event['Label'], event['Color'], event['Occurrences'])


def StoreEvents():
    # ClearEvents()
    events_dict = []
    for event in events:
        events_dict.append({'Label': event.Label,
                            'Color': event.Color,
                            'Occurrences': event.Occurrences})
    with open(os.path.join(dirname, 'events.json'), 'w') as out_file:
        out_file.write(json.dumps(events_dict, indent=4))


def AddOccurrence(id, day, start_time, duration):
    events[id].Occurrences.append(StartAndEnd(day, Slot(start_time, presets.time_interval), duration))
    if id == 0:
        SetMorningRoutine()

# Classes
class Event:
    def __init__(self, Label, Color, Occurrences):
        self.Label = Label
        self.Occurrences = Occurrences
        self.Color = Color
        events.append(self)
        self.ID = events.index(self)
        id_dict[Label] = self.ID

    def PrintOccurrences(self):
        print(f'Occurrences for {self.Label}')
        PrintBlockInfo(self.Occurrences)

    def EditOccurrence(self, index, start_time=0, end_time=0, duration=0, add_day=0):
        start_day = self.Occurrences[index][0][0] + add_day
        if duration != 0:
            duration = Slot(duration, presets.time_interval)
        else:
            duration = Slot(end_time, presets.time_interval) - Slot(start_time, presets.time_interval)
            if duration < 0:
                duration = schedule.number_of_slots + duration
        if start_time != 0:
            start_slot = Slot(start_time, presets.time_interval)
        else:
            start_slot = Slot(end_time, presets.time_interval) - duration
            if start_slot < 0:
                start_slot = schedule.number_of_slots + start_slot
        self.Occurrences[index] = StartAndEnd(start_day, start_slot, duration)
        if self.ID == 0 and presets.morning_routine:
            SetMorningRoutine()


class Display:
    def __init__(self):
        self.width = 10
        self.height = 6
        self.text_color = 'black'
        self.background_color = 'white'
        self.face_color = 'white'

    def DarkMode(self):
        self.text_color = 'white'
        self.background_color = '#303136'
        self.face_color = '#363940'

    def LightMode(self):
        self.text_color = 'black'
        self.background_color = 'white'
        self.face_color = '#DDDDDD'


def SetSleep():
    Event('Sleep', '#546fa8', [])
    Event('Morning Routine', '#7b9adb', [])


def SetLunch():
    Event('Lunch', '#e8b048', [])


def SetDinner():
    Event('Dinner', '#ba8420', [])


def SetMorningRoutine():
    morning_routine_id = id_dict['Morning Routine']
    sleep_id = id_dict['Sleep']
    events[morning_routine_id].Occurrences = []
    for Occurrence in events[sleep_id].Occurrences:
        duration = Slot(presets.length_morning_routine, presets.time_interval)
        events[morning_routine_id].Occurrences.append(StartAndEnd(Occurrence[1][0], Occurrence[1][1], duration))


class Presets:
    def __init__(self):
        with open(os.path.join(dirname, 'presets.json'), 'r') as openfile:
            preset_dictionary = json.load(openfile)
            self.day_zero = preset_dictionary['day_zero']
            self.number_of_days = preset_dictionary['number_of_days']
            self.time_interval = preset_dictionary['time_interval']
            self.alarm_time = preset_dictionary['alarm_time']
            self.length_sleep = preset_dictionary['length_sleep']
            self.length_morning_routine = preset_dictionary['length_morning_routine']
            self.lunch_time = preset_dictionary['lunch_time']
            self.length_lunch = preset_dictionary['length_lunch']
            self.dinner_time = preset_dictionary['dinner_time']
            self.length_dinner = preset_dictionary['length_dinner']
            self.sleep = preset_dictionary['sleep']
            self.morning_routine = preset_dictionary['morning_routine']
            self.lunch = preset_dictionary['lunch']
            self.dinner = preset_dictionary['dinner']
            self.import_google = preset_dictionary['import_google']
            self.dark_mode = preset_dictionary['dark_mode']

    def PrintPresets(self):
        print(f"day_zero = '{self.day_zero}'\n"
              f"number_of_days = {self.number_of_days}\n"
              f"time_interval = {self.time_interval}\n"
              f"alarm_time = '{self.alarm_time}'\n"
              f"length_sleep = '{self.length_sleep}'\n"
              f"length_morning_routine = '{self.length_morning_routine}'\n"
              f"lunch_time = '{self.lunch_time}'\n"
              f"length_lunch = '{self.length_lunch}'\n"
              f"dinner_time = '{self.dinner_time}'\n"
              f"length_dinner = '{self.length_dinner}'\n"
              f"sleep = {self.sleep}\n"
              f"morning_routine = {self.morning_routine}\n"
              f"lunch = {self.lunch}\n"
              f"dinner = {self.dinner}\n"
              f"import_google = {self.import_google}\n"
              f"dark_mode = {self.dark_mode}\n")

    def Store(self):
        presets_json = {'day_zero': self.day_zero,
                        'number_of_days': self.number_of_days,
                        'time_interval': self.time_interval,
                        'alarm_time': self.alarm_time,
                        'length_sleep': self.length_sleep,
                        'length_morning_routine': self.length_morning_routine,
                        'lunch_time': self.lunch_time,
                        'length_lunch': self.length_lunch,
                        'dinner_time': self.dinner_time,
                        'length_dinner': self.length_dinner,
                        'sleep': self.sleep,
                        'morning_routine': self.morning_routine,
                        'lunch': self.lunch,
                        'dinner': self.dinner,
                        'import_google': self.import_google,
                        'dark_mode': self.dark_mode}
        with open(os.path.join(dirname, 'presets.json'), 'w') as out_file:
            out_file.write(json.dumps(presets_json))


class Main:
    def __init__(self):
        self.schedule = []
        self.overlap = []
        self.number_of_slots = round(24 * 60 / presets.time_interval)

    def EmptyArrays(self):
        self.schedule = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1
        self.overlap = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1

    def Update(self):
        self.EmptyArrays()
        AppendEvents()
        return ResolveOverlap()


# Events, presets and the schedule instance.
id_dict = {}
events = []
presets = Presets()
display = Display()
schedule = Main()