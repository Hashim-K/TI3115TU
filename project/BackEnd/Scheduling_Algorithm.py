import numpy as np

import Task
#duration is in number of timeslots

class PossibleTime:
    def __init__(self, taskID, timeslots, score):
        self.taskID = taskID
        self.timeslots = timeslots
        self.score = score
    def __str__(self):
        text_description = f"TaskID \"{self.taskID}\" (\"{self.timeslots}\"): {self.score}. \n"
        return text_description

def stage1(filename):
    timetable=np.ndarray(dtype=np.object)
    tasks_list = Task.import_task(filename)
    schedule_slots = [[[1, 15], [1, 30]], [[1, 57], [1, 78]], [[1, 99], [1, 120]]]
    for task in tasks_list:
        for timeslot in schedule_slots:
            start_day = timeslot[0][0]
            start_time = timeslot[0][1]
            end_day = timeslot[1][0]
            end_time = timeslot[1][1]
            while (start_day * 288)+(start_time + task.duration) <= (end_day * 288)+end_time:
                if start_time+task.duration >= 288:
                    temp_end_day = start_day + 1
                    temp_end_time = start_time + task.duration - 288
                else:
                    temp_end_day = start_day
                    temp_end_time = start_time + task.duration
                timetable= np.append(PossibleTime(task.taskID, [[start_day, start_time], [temp_end_day, temp_end_time]],
                                              calc_score(task, start_time)))
                start_time=+1
                if start_time >= 288:
                    start_time =- 288
                    start_day =+ 1
    print(timetable[0])
def calc_score(task, timeslot):
    #sessionR is number of sessions remaining
    score = task.priority * timeslot_pref(task, timeslot) #multiplied by Daystilldeadline-sessionR
    return score

def timeslot_pref(task,timeslot):
    Tavg=timeslot+task.duration/2
    if task.preferred == "Ungodly hours (0:00-8:00)":
        if 0<=Tavg<=95:
            return 1
        else:
            return 3
    if task.preferred == "Morning (8:00-12:00)":
        if 96 <= Tavg <= 143:
            return 1
        else:
            return 3
    if task.preferred == "Afternoon (12:00-16:00)":
        if 144 <= Tavg <= 191:
            return 1
        else:
            return 3
    if task.preferred == "Evening (16:00-20:00)":
        if 192 <= Tavg <= 239:
            return 1
        else:
            return 3
    if task.preferred == "Night (20:00-23:59)":
        if 240 <= Tavg <= 287:
            return 1
        else:
            return 3
    if task.preferred == "No Preference":
            return 2

    stage1('../save_file.json')