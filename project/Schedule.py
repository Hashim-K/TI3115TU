import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random



#Creating Schedule
def TimeToSlot(time,TI):
    minute = time[1]*60 + time[2]
    return [time[0],round(minute/TI)]
TI = 5    #Time interval in minutes [1,5,10,15,20,30,40,45,60]
Nslots = round(24*60/TI)
Schedule = np.zeros(shape=(7,Nslots))-1



#Function for Adding Activity to Schedule
def Add2Schedule(Task):
    Blocks = []
    for Occurrence in Task.Occurences:
        time1,time2 = Occurrence[0],Occurrence[1]
        if time1[0] == time2[0]:
            Block = [TimeToSlot(time1,TI),TimeToSlot(time2,TI)]
            Blocks.append(Block)
        else:
            Block = [TimeToSlot(time1,TI),[time1[0],round(24*60/TI)]]
            Blocks.append(Block)
            Block = [[time2[0],0],TimeToSlot(time2,TI)]
            Blocks.append(Block)

    for Block in Blocks:
        for slot in range(Block[0][1],Block[1][1]):
            Schedule[Block[0][0]][slot] = Task.ID



#Function for Displaying Graph
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
hours = ['0:00','1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']
def Display():
    AdjustedSchedule = np.transpose(Schedule)
    yticks = []
    axes = plt.gca()
    axes.set_xlim([0,7])
    axes.set_ylim([0,Nslots])
    axes.invert_yaxis()
    plt.xticks(np.arange(7),days,rotation=20)
    plt.yticks(np.arange(0,Nslots,step=Nslots/24),hours)

    for i in range(len(Schedule)):
        for j in range(len(Schedule[i])):
            ID = int(Schedule[i][j])
            if ID >= 0:
                rect=mpatches.Rectangle((i,j),1,1,facecolor=Colors[ID])
                plt.gca().add_patch(rect)

    legend_elements = []
    for ID in range(len(Tasks)):
        legend_elements.append(mpatches.Patch(facecolor=Colors[ID],label=Tasks[ID]))
    axes.legend(handles=legend_elements,bbox_to_anchor=(1.01, 1.0), loc='upper left')
    plt.grid(axis = 'x',color='black')
    plt.grid(axis = 'y',color='black',linewidth = 0.5,alpha=0.25)
    plt.tight_layout()

    plt.show()



#Tasks Class
Tasks = []
Colors = []
class Task:
    def __init__(self,Label,Color,Occurences):
        self.Label = Label
        self.Occurences = Occurences
        Tasks.append(Label)
        Colors.append(Color)
        self.ID = Tasks.index(Label)

#Tasks
Sleep = Task('Sleep','#546fa8',[])
MorningRoutine = Task('Morning Routine','#8399c9',[])
Swimming = Task('Swimming','#eddb64',[[[1,19,0],[1,20,30]],[[3,19,0],[3,20,30]]])
Dinner = Task('Dinner','#86c452',[[[0,18,30],[0,19,5]],
                                  [[1,18,00],[1,18,40]],
                                  [[2,18,30],[2,19,10]],
                                  [[3,18,00],[3,18,40]],
                                  [[4,18,30],[4,19,00]],
                                  [[5,19,00],[5,19,40]],
                                  [[6,18,45],[6,19,20]]])



#This bit creates random times for sleeping and adds it to the schedule along with the morning routine. This bit is to be replaced by user input.
for day in days:
    i = days.index(day)
    hour1,min1 = random.randint(22,23),random.randint(0,59)
    hour2,min2 = random.randint(7,8),random.randint(0,59)
    timemr = 30
    if i == 0:
        Sleep.Occurences.append([[i,0,0],[i,hour2,min2]])
        Sleep.Occurences.append([[i,hour1,min1],[i+1,hour2,min2]])
        MorningRoutine.Occurences.append([[i,hour2,min2],[i,hour2,min2+timemr]])
        MorningRoutine.Occurences.append([[i+1,hour2,min2],[i+1,hour2,min2+timemr]])
    elif i == 6:
        Sleep.Occurences.append([[i,hour1,min1],[i,24,0]])
    else:
        Sleep.Occurences.append([[i,hour1,min1],[i+1,hour2,min2]])
        MorningRoutine.Occurences.append([[i+1,hour2,min2],[i+1,hour2,min2+timemr]])

#Adding Activity to Schedule
Add2Schedule(Sleep)
Add2Schedule(MorningRoutine)
Add2Schedule(Swimming)
Add2Schedule(Dinner)

Display()
