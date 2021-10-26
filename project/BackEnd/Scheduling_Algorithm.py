from project.BackEnd import Task, Schedule
import json
from datetime import date, datetime, timedelta
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


def obtain_day_zero(filename):
    with open(filename) as file:
        preset_dict = json.load(file)
    day_zero = preset_dict['day_zero'].split('-')  # get the date of day_zero so first date of the planner
    date_zero = date(int(day_zero[0]), int(day_zero[1]), int(day_zero[2]))  # turns date into date objects
    return date_zero

def obtain_time_interval(filename):
    with open(filename) as file:
        preset_dict = json.load(file)
    return preset_dict['time_interval']


def main(filename):
    """ Deciding which task to schedule next,
    and turning that task into an event an placing it in the schedule.
    """
    copyfile(filename, '../copy_file.json')
    filename = '../copy_file.json'
    forbidden_slots = []
    timetable = create_timetable(filename, obtain_day_zero(os.path.join(dirname, '../data/presets.json')), forbidden_slots)
    print(len(timetable))
    while len(timetable) > 0:
        stc = single_task_check(timetable)
        if stc != -99:
            entry = timetable[stc]
            print(entry)
            print("Reason: one timeslot remaining")
            task = Task.find_task(filename, entry.taskID)
            if task.name not in Schedule.id_dict:
                Schedule.Event(task.name, '#FFFFFF', [])
            Schedule.events[Schedule.id_dict[task.name]].Occurrences.append(entry.timeslots)
            Schedule.StoreEvents()
            Task.delete_session(filename, entry.taskID)
        else:
            entry = best_score_check(timetable)
            #print(entry)
            if (overlap_check(Task.import_task(filename), Schedule.EmptySlots(), entry,
                    obtain_day_zero(os.path.join(dirname, '../data/presets.json')),
                    obtain_time_interval(os.path.join(dirname, '../data/presets.json')))):
                print("Reason: best score")
                task = Task.find_task(filename, entry.taskID)
                #print(task)
                if task.name not in Schedule.id_dict:
                    Schedule.Event(task.name, '#FFFFFF', [])
                Schedule.events[Schedule.id_dict[task.name]].Occurrences.append(entry.timeslots)
                Schedule.StoreEvents()
                Task.delete_session(filename, entry.taskID)
            else:
                forbidden_slots.append(entry)
                print("Not planned: Overlap detected")
        timetable = create_timetable(filename, obtain_day_zero(os.path.join(dirname, '../data/presets.json')), forbidden_slots)
        print(len(timetable))

    Schedule.schedule.Update()
    Schedule.SaveImage()


def create_timetable(filename, date_zero, forbidden_slots):
    """ Creates a list of all PossibleTime objects by making a PossibleTime object
    of every task/timeslot combination and its corresponding score.
    """
    timetable = []
    timeslot_duration = obtain_time_interval(os.path.join(dirname, '../data/presets.json'))
    total_slots = 1440/timeslot_duration
    tasks_list = Task.import_task(filename)
    Schedule.schedule.Update()
    schedule_slots = Schedule.EmptySlots()
    for task in tasks_list:
        saved_end_day = 0
        current_day = date_zero
        deadline_date = datetime.date(task.deadline)
        for timeslot in schedule_slots:
            start_day = timeslot[0][0]
            start_time = timeslot[0][1]
            end_day = timeslot[1][0]
            end_time = timeslot[1][1]
            current_day += timedelta(days=(end_day - saved_end_day))
            while ((start_day * total_slots) + (start_time + task.duration) <= (end_day * total_slots) + end_time
                    and current_day <= deadline_date):
                if start_time + task.duration >= total_slots:
                    temp_end_day = start_day + 1
                    temp_end_time = start_time + task.duration - total_slots
                else:
                    temp_end_day = start_day
                    temp_end_time = start_time + task.duration
                entry = PossibleTime(task.taskID, [[start_day, start_time], [temp_end_day, temp_end_time]],
                                     calc_score(task, start_time))
                forbidden = False
                for forbidden_task in forbidden_slots:
                    if forbidden_task == entry:
                        forbidden = True
                if not forbidden:
                    timetable.append(entry)
                start_time += 1
                if start_time >= total_slots:
                    start_time -= total_slots
                    start_day += 1
                saved_end_day = temp_end_day
    return timetable


def single_task_check(timetable):
    """" Checking if there is a task with only one possible timeslot left. """
    pos = -99
    for i in range(timetable[-1].taskID+1):
        if sum(t.taskID == i for t in timetable) == 1:
            for pos in range(len(timetable)):
                if timetable[pos].taskID == i:
                    return pos
    return pos


def overlap_check(tasks_list, empty_slots, event, date_zero, time_interval):
    """ Checks if the allocated timeslot of event eliminates all the timeslots of another task. """
    print('emptyslots', empty_slots)
    tasks_list.sort(reverse=True)
    not_overlap = []
    taken_slots = [(event.timeslots[0][0], event.timeslots[0][1], event.timeslots[1][1])]
    count = 0
    slot_in_one_day = 1440 / time_interval - 1
    passed_deadline = False
    for task in tasks_list:
        sessions = task.session
        times = []
        count += 1
        days_between = calculate_days_till_deadline(task, date_zero)
        for empty in empty_slots:
            if passed_deadline:
                break
            timeslot = empty[0].copy()
            while True:
                if timeslot[0] > days_between:
                    passed_deadline = True
                    break
                if timeslot[0] != empty[1][0] or timeslot[1] + task.duration <= empty[1][1]:
                    times.append([[timeslot[0], timeslot[1]], [timeslot[0], timeslot[1] + task.duration]])
                else:
                    break
                if timeslot[1] == slot_in_one_day:
                    timeslot[0] += 1
                    timeslot[1] = 0
                else:
                    timeslot[1] += 1
        print(times)
        slot = 0
        while slot < len(times):
            available = True
            for taken_slot in taken_slots:
                if not((times[slot][0][0] != taken_slot[0] or
                        not(taken_slot[1] <= times[slot][0][1] <= taken_slot[2]
                            or taken_slot[1] <= times[slot][1][1] <= taken_slot[2]))):
                    available = False
            if available:
                taken_slots.append((times[slot][0][0], times[slot][0][1], times[slot][1][1]))
                if sessions == 1:
                    not_overlap.append(True)
                    break
                else:
                    sessions -= 1
                    slot += task.duration
            slot += 1
        if len(not_overlap) != count:
            not_overlap.append(False)
    print(taken_slots)
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
    score = (priority * timeslot_pref(task, timeslot, obtain_time_interval(os.path.join(dirname, '../data/presets.json')))
            + (calculate_days_till_deadline(task, obtain_day_zero(os.path.join(dirname, '../data/presets.json'))) - task.session))
    return score


def timeslot_pref(task, timeslot, time_interval):
    """ Comparing if a timeslot fits well with the preference of a task,
    if it corresponds the score is 1 and if it doesn't the score is 3.
    """

    # if timeslot length changes, this code needs to change as well !!!!
    t_avg = timeslot + task.duration / 2  # to know in which timeslot a task/timeslot combination falls we take the average time
    if not task.preferred:
        return 2
    else:
        if time2slot(task.preferred[0], time_interval) <= t_avg <= time2slot(task.preferred[1], time_interval):
            return 1
        else:
            return 3


def time2slot(timestr, time_interval):
    time = datetime.strptime(timestr, '%H:%M:%S')
    total = time.minute
    total += time.hour * 60
    return total / time_interval


def calculate_days_till_deadline(task, date_zero):
    """" Calculating the days between two dates using datetime module,
    Needed to calculate the score of task/timeslot combination.
    """
    deadline_date = datetime.date(task.deadline)  # turns datetime object into date object
    if str(deadline_date - date_zero).split(' ') == ['0:00:00']:
        return 0
    return int(str(deadline_date - date_zero).split(' ')[0])  # gets the difference of the two dates from the datetime module

# #testing if it runs
#main('../save_file.json')