import Task
import json
from datetime import date, datetime
from shutil import copyfile

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
    copyfile(filename, '../copy_file.json')
    filename = '../copy_file.json'
    timetable = create_timetable(filename)
    while len(timetable) > 0:
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
            Task.delete_session(filename, task.taskID)
            # ADD TASK TO SCHEDULE @TEUS
        timetable = create_timetable(filename)
        print(len(timetable))


def create_timetable(filename):
    timetable = []
    tasks_list = Task.import_task(filename)
    schedule_slots = [[[1, 15], [1, 30]], [[1, 57], [1, 75]], [[1, 99], [1, 120]]] # THIS SHOULD BE IMPORTING THE EMPTY SCHEDULE SPOTS @TEUS
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
    """" Checking if there is a task with only one possible timeslot left. """
    pos = -99
    for i in range(timetable[-1].taskID+1):
        if sum(t.taskID == i for t in timetable) == 1:
            for pos in range(len(timetable)):
                if timetable[pos].taskID == i + 1:
                    return pos
    return pos


def best_score_check(timetable):
    """ Retrieving the lowest score from the timetable. """
    timetable = sorted(timetable, key=lambda a: (a.score))
    return timetable[0]


def calc_score(task, timeslot):
    """" Calculating the score, which is an indication how well a task and timeslot fit together. """
    if task.priority == 0:  # priority of one means no priority
        priority = 7
    else:
        priority = task.priority
    score = priority * timeslot_pref(task, timeslot) + (calculate_days_till_deadline(task) - task.session)
    return score


def timeslot_pref(task, timeslot):
    """ Comparing if a timeslot fits well with the preference of a task,
    if it corresponds the score is 1 and if it doesn't the score is 3.
    """
    t_avg = timeslot + task.duration / 2  # to know in which timeslot a task/timeslot combination falls we take the average time
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
    """" Calculating the days between two dates using datetime module,
    Needed to calculate the score of task/timeslot combination.
    """
    with open('presets.json') as file:
        preset_dict = json.load(file)
    day_zero = preset_dict['day_zero'].split('-')  # get the date of day_zero so first date of the planner
    date_zero = date(int(day_zero[0]), int(day_zero[1]), int(day_zero[2]))  # turns date into date objects
    deadline_date = datetime.date(task.deadline) # turns datetime object into date object
    return int(str((deadline_date - date_zero)).split(' ')[0])  # gets the difference of the two dates from the datetime module

# #testing if it runs
main('../save_file.json')
