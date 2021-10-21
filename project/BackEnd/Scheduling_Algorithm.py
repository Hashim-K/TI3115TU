from project.BackEnd import Task, Schedule
import json
from datetime import date, datetime
from shutil import copyfile
import os

dirname = os.path.dirname(__file__)

# duration is in number of timeslots

class PossibleTime:
    """ Used to store a task/timeslot combination and its corresponding score. """
    def __init__(self, taskID, timeslots, score):
        self.taskID = taskID
        self.timeslots = timeslots
        self.score = score

    def __str__(self):
        text_description = f"TaskID: {self.taskID} | {self.timeslots} | score: {self.score}"
        return text_description

    def __eq__(self, other):
        return self.taskID == other.taskID and self.timeslots == other.timeslots


def main(filename):
    """ Deciding which task to schedule next,
    and turning that task into an event an placing it in the schedule.
    """
    copyfile(filename, '../copy_file.json')
    filename = '../copy_file.json'
    timetable = create_timetable(filename)
    print(len(timetable))
    while len(timetable) > 0:
        stc = single_task_check(timetable)
        if stc != -99:
            entry = timetable[stc]
            print(entry)
            print("Reason: one timeslot remaining")
            # ADD TASK TO SCHEDULE @TEUS
            task = Task.find_task(filename, entry.taskID)
            if task.name not in Schedule.id_dict:
                Schedule.Event(task.name, '#FFFFFF', [])
            Schedule.events[Schedule.id_dict[task.name]].Occurrences.append(entry.timeslots)
            Schedule.StoreEvents()
            Task.delete_session(filename, entry.taskID)
        else:
            entry = best_score_check(timetable)
            print(entry)
            print("Reason: best score")
            # ADD TASK TO SCHEDULE @TEUS
            task = Task.find_task(filename, entry.taskID)
            print(task)
            if task.name not in Schedule.id_dict:
                Schedule.Event(task.name, '#FFFFFF', [])
            Schedule.events[Schedule.id_dict[task.name]].Occurrences.append(entry.timeslots)
            Schedule.StoreEvents()
            Task.delete_session(filename, entry.taskID)
        timetable = create_timetable(filename)
        print(len(timetable))

    Schedule.schedule.Update()
    Schedule.SaveImage()


def create_timetable(filename):
    """ Creates a list of all PossibleTime objects by making a PossibleTime object
    of every task/timeslot combination and its corresponding score.
    """
    timetable = []
    timeslot_duration = 5
    total_slots = 1440/timeslot_duration
    tasks_list = Task.import_task(filename)
    Schedule.schedule.Update()
    schedule_slots = Schedule.EmptySlots()
    print(schedule_slots)
    for task in tasks_list:
        for timeslot in schedule_slots:
            start_day = timeslot[0][0]
            start_time = timeslot[0][1]
            end_day = timeslot[1][0]
            end_time = timeslot[1][1]
            while (start_day * total_slots) + (start_time + task.duration) <= (end_day * total_slots) + end_time:
                if start_time + task.duration >= total_slots:
                    temp_end_day = start_day + 1
                    temp_end_time = start_time + task.duration - total_slots
                else:
                    temp_end_day = start_day
                    temp_end_time = start_time + task.duration

                entry = PossibleTime(task.taskID, [[start_day, start_time], [temp_end_day, temp_end_time]],
                                     calc_score(task, start_time))
                timetable.append(entry)
                start_time += 1
                if start_time >= total_slots:
                    start_time -= total_slots
                    start_day += 1
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


def overlap_check(tasks_list, empty_slots, event):
    """ Checks if the allocated timeslot of event eliminates all the timeslots of another task. """
    tasks_list.sort(reverse=True)
    not_overlap = []
    taken_slots = [(event.timeslots[0][0], event.timeslots[0][1], event.timeslots[1][1])]
    count = 0
    for task in tasks_list:
        sessions = task.session
        times = []
        count += 1
        for i in range(len(empty_slots)):
            for empty_slot in empty_slots[i]:
                for j in range(empty_slot[1] - empty_slot[0]):
                    if empty_slot[0] + j + task.duration <= empty_slot[1]:
                        times.append([i, empty_slot[0] + j, empty_slot[0] + j + task.duration])
                    else:
                        break
        for slot in times:
            available = True
            for taken_slot in taken_slots:
                if not((slot[0] != taken_slot[0] or
                        not(taken_slot[1] <= slot[1] <= taken_slot[2] or taken_slot[1] <= slot[2] <= taken_slot[2]))):
                    available = False
            if available is True:
                taken_slots.append((slot[0], slot[1], slot[2]))
                if sessions == 1:
                    not_overlap.append(True)
                    break
                else:
                    sessions -= 1
        if len(not_overlap) != count:
            not_overlap.append(False)
    if False in not_overlap:
        return False
    return True



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
    score = priority * timeslot_pref(task, timeslot) + (calculate_days_till_deadline(task, os.path.join(dirname, 'presets.json')) - task.session)
    return score


def timeslot_pref(task, timeslot):
    """ Comparing if a timeslot fits well with the preference of a task,
    if it corresponds the score is 1 and if it doesn't the score is 3.
    """
    # if timeslot length changes, this code needs to change as well !!!!
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


def calculate_days_till_deadline(task, filename):
    """" Calculating the days between two dates using datetime module,
    Needed to calculate the score of task/timeslot combination.
    """
    with open(filename) as file:
        preset_dict = json.load(file)
    day_zero = preset_dict['day_zero'].split('-')  # get the date of day_zero so first date of the planner
    date_zero = date(int(day_zero[0]), int(day_zero[1]), int(day_zero[2]))  # turns date into date objects
    deadline_date = datetime.date(task.deadline)  # turns datetime object into date object
    return int(str((deadline_date - date_zero)).split(' ')[0])  # gets the difference of the two dates from the datetime module

# #testing if it runs
# main('../save_file.json')