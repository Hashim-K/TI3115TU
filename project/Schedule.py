import random
import GoogleImport
from General import *


def Add2Schedule(event, time_interval):
    blocks = []
    for Occurrence in event.Occurences:
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
            Schedule[block[0][0]][slot] = event.ID


def Display(Schedule,xticks,yticks,number_of_days,number_of_slots):
    axes = plt.gca()
    axes.set_xlim([0, number_of_days])
    axes.set_ylim([0, number_of_slots])
    axes.invert_yaxis()
    plt.xticks(np.arange(number_of_days), xticks, rotation=30)
    plt.yticks(np.arange(0, number_of_slots, step=number_of_slots / 24), yticks)
    plt.title('Schedule for '+DateReformat(day_zero)+' till '+DateReformat(XDaysLater(day_zero,number_of_days)))

    for j in range(len(Schedule)):
        for k in range(len(Schedule[j])):
            id = int(Schedule[j][k])
            if id >= 0:
                rect = mpatches.Rectangle((j, k), 1, 1, facecolor=Colors[id])
                plt.gca().add_patch(rect)

    legend_elements = []
    for id in range(len(Events)):
        legend_elements.append(mpatches.Patch(facecolor=Colors[id], label=Labels[id]))
    axes.legend(handles=legend_elements, bbox_to_anchor=(1.01, 1.0), loc='upper left')
    plt.grid(axis='x', color='black')
    plt.grid(axis='y', color='black', linewidth=0.5, alpha=0.25)
    plt.tight_layout()

    plt.show()


# Event Class
Events = []
Colors = []
Labels = []


class Event:
    def __init__(self, Label, Color, Occurrences):
        self.Label = Label
        self.Occurences = Occurrences
        Events.append(self)
        Labels.append(Label)
        Colors.append(Color)
        self.ID = Events.index(self)


# Preset Events
'''
Sleep = Event('Sleep', '#546fa8', [])
MorningRoutine = Event('Morning Routine', '#8399c9', [])
Dinner = Event('Dinner', '#86c452', [[[0, 222], [0, 230]],
                                     [[1, 217], [1, 226]],
                                     [[2, 221], [2, 233]],
                                     [[3, 219], [3, 226]],
                                     [[4, 222], [4, 229]],
                                     [[5, 223], [5, 231]],
                                     [[6, 222], [6, 230]]])
FreeTime = Event('Free Time', '#e6f0e9', [])
'''



day_zero = '2021-09-13'
number_of_days = 10
time_interval = 1
number_of_slots = round(24*60/time_interval)

Schedule = CreateSchedule(time_interval,number_of_days,number_of_slots)

google_events = GoogleImport.Import(day_zero,number_of_days)

colors = GetColors()
color_id = 0
for event in google_events:
    label = str(event[0])
    time1 = DayAndSlot(event[1],day_zero,time_interval)
    time2 = DayAndSlot(event[2],day_zero,time_interval)
    Event(label, colors[color_id], [[time1,time2]])
    color_id = color_id + 1




# This bit creates random times for sleeping and adds it to the schedule along with the morning routine.
# This bit is to be replaced by user input.

'''
for day in days:
    i = days.index(day)
    hour1, min1 = random.randint(22, 23), random.randint(0, 59)
    hour2, min2 = random.randint(7, 8), random.randint(0, 59)
    timemr = 30
    if i == 0:
        Sleep.Occurences.append([[i, 0, 0], [i, hour2, min2]])
        Sleep.Occurences.append([[i, hour1, min1], [i + 1, hour2, min2]])
        MorningRoutine.Occurences.append([[i, hour2, min2], [i, hour2, min2 + timemr]])
        MorningRoutine.Occurences.append([[i + 1, hour2, min2], [i + 1, hour2, min2 + timemr]])
    elif i == 6:
        Sleep.Occurences.append([[i, hour1, min1], [i, 24, 0]])
    else:
        Sleep.Occurences.append([[i, hour1, min1], [i + 1, hour2, min2]])
        MorningRoutine.Occurences.append([[i + 1, hour2, min2], [i + 1, hour2, min2 + timemr]])
'''

# Adding Activities to Schedule.
for Event in Events:
    Add2Schedule(Event,time_interval)

# Identifying free blocks in the schedule.
FreeBlocks = EmptySlots(Schedule,number_of_slots)

# This Part is for demonstrating that the program can identify the empty slots.
'''
for FreeBlock in FreeBlocks:
    FreeTime.Occurences.append(FreeBlock)
Add2Schedule(FreeTime,time_interval)
'''


# Display Schedule
xticks = CreateXTicks(day_zero,number_of_days)
yticks = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
         '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
Display(Schedule,xticks,yticks,number_of_days,number_of_slots)
