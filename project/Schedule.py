import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

# Creating Schedule
TI = 5  # Time interval in minutes [1,5,10,15,20,30,40,45,60]
Nslots = round(24 * 60 / TI)
Schedule = np.zeros(shape=(7, Nslots)) - 1


# Function for Converting time to Slot
def Time2Slot(time, TimeInterval):
    minute = time[1] * 60 + time[2]
    return [time[0], round(minute / TimeInterval)]


# Function for Adding Activity to Schedule
def Add2Schedule(task):
    blocks = []
    for Occurrence in task.Occurences:
        time1, time2 = Occurrence[0], Occurrence[1]
        if len(time1) == 3:
            time1 = Time2Slot(time1,TI)
        if len(time2) == 3:
            time2 = Time2Slot(time2,TI)
        if time1[0] == time2[0]:
            block = [time1, time2]
            blocks.append(block)
        else:
            block = [time1, [time1[0], round(24 * 60 / TI)]]
            blocks.append(block)
            block = [[time2[0], 0], time2]
            blocks.append(block)

    for block in blocks:
        for slot in range(block[0][1], block[1][1]):
            Schedule[block[0][0]][slot] = task.ID


# x and y ticks
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hours = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00',
         '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']


# Function for Displaying Graph
def Display():
    axes = plt.gca()
    axes.set_xlim([0, 7])
    axes.set_ylim([0, Nslots])
    axes.invert_yaxis()
    plt.xticks(np.arange(7), days, rotation=20)
    plt.yticks(np.arange(0, Nslots, step=Nslots / 24), hours)

    for j in range(len(Schedule)):
        for k in range(len(Schedule[j])):
            id = int(Schedule[j][k])
            if id >= 0:
                rect = mpatches.Rectangle((j, k), 1, 1, facecolor=Colors[id])
                plt.gca().add_patch(rect)

    legend_elements = []
    for id in range(len(Routines)):
        legend_elements.append(mpatches.Patch(facecolor=Colors[id], label=Labels[id]))
    axes.legend(handles=legend_elements, bbox_to_anchor=(1.01, 1.0), loc='upper left')
    plt.grid(axis='x', color='black')
    plt.grid(axis='y', color='black', linewidth=0.5, alpha=0.25)
    plt.tight_layout()

    plt.show()


# Function for Identifying Empty Slots
def EmptySlots():
    FreeBlocks = []
    FreeBlock = []
    for day in range(len(Schedule)):
        for slot in range(len(Schedule[day])):
            if Schedule[day][slot] == -1:
                FreeBlock.append([day,slot])
            else:
                if len(FreeBlock) > 0 or (len(FreeBlock) > 0 and slot == Nslots-1):
                    FreeBlock.append([day,slot])
                    FreeBlocks.append(FreeBlock)
                    FreeBlock = []
    for FreeBlock in FreeBlocks:
        while len(FreeBlock) > 2:
            FreeBlock.pop(1)
    return FreeBlocks




# Routines Class
Routines = []
Colors = []
Labels = []

class Routine:
    def __init__(self, Label, Color, Occurrences):
        self.Label = Label
        self.Occurences = Occurrences
        Routines.append(self)
        Labels.append(Label)
        Colors.append(Color)
        self.ID = Routines.index(self)


# Routines
Sleep = Routine('Sleep', '#546fa8', [])
MorningRoutine = Routine('Morning Routine', '#8399c9', [])
Swimming = Routine('Swimming', '#eddb64', [[[1, 19, 0], [1, 20, 30]], [[3, 19, 0], [3, 20, 30]]])
Dinner = Routine('Dinner', '#86c452', [[[0, 18, 30], [0, 19, 5]],
                                       [[1, 18, 00], [1, 18, 40]],
                                       [[2, 18, 30], [2, 19, 10]],
                                       [[3, 18, 00], [3, 18, 40]],
                                       [[4, 18, 30], [4, 19, 00]],
                                       [[5, 19, 00], [5, 19, 40]],
                                       [[6, 18, 45], [6, 19, 20]]])
FreeTime = Routine('Free Time', '#e6f0e9', [])


#To-be-planned Tasks



# This bit creates random times for sleeping and adds it to the schedule along with the morning routine.
# This bit is to be replaced by user input.
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


# Adding Activity to Schedule
for Routine in Routines:
    Add2Schedule(Routine)

FreeBlocks = EmptySlots()


# This Part is for demonstrating that the program can identify the empty slots.

for FreeBlock in FreeBlocks:
    FreeTime.Occurences.append(FreeBlock)
Add2Schedule(FreeTime)

Display()
