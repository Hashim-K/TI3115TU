import Task
import json
from datetime import date

# duration is in number of timeslots

class PossibleTime:
    def __init__(self, taskID, timeslots, score):
        self.taskID = taskID
        self.timeslots = timeslots
        self.score = score

    def __str__(self):
        text_description = f"TaskID: {self.taskID} | {self.timeslots} | score:{self.score}"
        return text_description


def main(filename):
    timetable = create_timetable(filename)
    while len(timetable)>0:
        stc = single_task_check(timetable)
        if stc != -99:
            task = timetable[stc]
            print(task)
            print("Reason: one timeslot remaining")
            Task.delete_task(filename, task.taskID)
            # ADD TASK TO SCHEDULE @TEUS
        else:
            task = best_score_check(timetable)
            print(task)
            print("Reason: best score")
            Task.delete_task(filename, task.taskID)
            # ADD TASK TO SCHEDULE @TEUS
        timetable = create_timetable(filename)
        print(len(timetable))


def create_timetable(filename):
    timetable = []
    tasks_list = Task.import_task(filename)
    schedule_slots = [[[1, 15], [1, 30]], [[1, 57], [1, 75]], [[1, 99], [1, 120]]] #THIS SHOULD BE IMPORTING THE EMPTY SCHEDULE SPOTS @TEUS
    for task in tasks_list:
        for timeslot in schedule_slots:
            start_day = timeslot[0][0]
            start_time = timeslot[0][1]
            end_day = timeslot[1][0]
            end_time = timeslot[1][1]
            while (start_day * 288) + (start_time + task.duration) <= (end_day * 288) + end_time:
                if start_time + task.duration >= 288:
                    temp_end_day = start_day + 1
                    temp_end_time = start_time + task.duration - 288
                else:
                    temp_end_day = start_day
                    temp_end_time = start_time + task.duration

                entry = PossibleTime(task.taskID, [[start_day, start_time], [temp_end_day, temp_end_time]],
                                     calc_score(task, start_time))
                timetable.append(entry)
                start_time += 1
                if start_time >= 288:
                    start_time -= 288
                    start_day += 1
    # print("helloworld")
    # for entry in timetable:
    #   print(entry)
    return timetable


def single_task_check(timetable):
    pos = -99
    for i in range(timetable[-1].taskID+1):
        if sum(t.taskID == i for t in timetable) == 1:
            for pos in range(len(timetable)):
                if timetable[pos].taskID == i + 1:
                    return pos
    return pos


def best_score_check(timetable):
    timetable = sorted(timetable, key=lambda a: (a.score))
    return timetable[0]


def calc_score(task, timeslot):
    # A lower score means that a certain timeslot and task do fit together well according to all the task details
    if task.priority == 0:
        priority = 7
    else:
        priority = task.priority
    score = priority * timeslot_pref(task, timeslot) * (calculate_days_till_deadline(task) - task.session)
    return score


def timeslot_pref(task, timeslot):
    t_avg = timeslot + task.duration / 2
    preferenceRating = 2
    if task.preferred == "Ungodly hours (0:00-8:00)":
        if 0 <= t_avg <= 95:
            preferenceRating = 1
        else:
            preferenceRating = 3
    if task.preferred == "Morning (8:00-12:00)":
        if 96 <= t_avg <= 143:
            preferenceRating = 1
        else:
            preferenceRating = 3
    if task.preferred == "Afternoon (12:00-16:00)":
        if 144 <= t_avg <= 191:
            preferenceRating = 1
        else:
            preferenceRating = 3
    if task.preferred == "Evening (16:00-20:00)":
        if 192 <= t_avg <= 239:
            preferenceRating = 1
        else:
            preferenceRating = 3
    if task.preferred == "Night (20:00-23:59)":
        if 240 <= t_avg <= 287:
            preferenceRating = 1
        else:
            preferenceRating = 3
    # if task.preferred == "No Preference":
    #     preferenceRating = 2
    return preferenceRating


def calculate_days_till_deadline(task):
    with open('presets.json') as file:
        preset_dict = json.load(file)
    day_zero = preset_dict['day_zero'].split('-') # get the date of day_zero so first date of the planner
    deadline_day = task.deadline.split('-')
    # turnss dates into date objects
    date_zero = date(int(day_zero[0]), int(day_zero[1]), int(day_zero[2]))
    deadline_date = date(int(deadline_day[0]), int(deadline_day[1]), int(deadline_day[2]))
    return int(str((deadline_date - date_zero)).split(' ')[0]) # gets the difference of the two dates from the datetime module

#testing if it runs
main('../save_file.json')
