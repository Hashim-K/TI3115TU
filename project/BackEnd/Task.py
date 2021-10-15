import json

import os.path
from dataclasses import dataclass
from datetime import datetime


# @dataclass
from project.BackEnd import Schedule


class Task:
    try:
        highest_id = Schedule.events[-1].ID
    except IndexError:
        highest_id = 0


    def __init__(self, taskID: int, name: str, description: str, duration: int, priority: int, deadline: str,
                 repeatable: bool, category: str, preferred: str, plan_on_same: bool, session: int, filename: str):
        if taskID != -1:
            self.taskID = taskID
        else:
            if not os.path.exists(filename) or os.stat(filename).st_size < 4:
                Task.highest_id += 1
                self.taskID = Task.highest_id
            else:
                with open(filename) as file:
                    task_dict = json.load(file)
                    self.taskID = task_dict[-1]['TaskID'] + 1
        self.name = name
        self.description = description
        self.duration = duration
        self.priority = priority
        self.deadline = deadline
        self.repeatable = repeatable
        self.category = category
        self.preferred = preferred
        self.plan_on_same = plan_on_same
        self.session = session

    def __str__(self):
        text_description = f"Task \"{self.name}\" ({self.taskID}): {self.description}.\n"\
                            + f"Deadline: {self.deadline}, " \
                            + f"number of sessions: {self.session}, session duration: {self.duration}"
        return text_description

    def export_task(self, filename):
        entry = {
            "TaskID": self.taskID,
            "Name": self.name,
            "Description": self.description,
            "Duration": self.duration,
            "Priority": self.priority,
            "Deadline": self.deadline.isoformat(),
            "Repeatable": self.repeatable,
            "Category": self.category,
            "Preferred": self.preferred,
            "Plan_on_same": self.plan_on_same,
            "Session": self.session
        }
        if not os.path.exists(filename):
            data = []
        else:
            if os.stat(filename).st_size == 0:
                os.remove(filename)
                data = []
            else:
                with open(filename, 'r') as file:
                    data = json.load(file)
        data.append(entry)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=6)


def import_task(filename):
    tasks_list = []
    with open(filename, 'r') as file:
        task_dict = json.load(file)
        for tasks in task_dict:
            tasks_list.append(Task(tasks['TaskID'], tasks['Name'], tasks['Description'], tasks['Duration'],
                    tasks['Priority'], datetime.fromisoformat(tasks['Deadline']), tasks['Repeatable'],
                    tasks['Category'], tasks['Preferred'], tasks['Plan_on_same'], tasks['Session'], filename))
    return tasks_list

def find_task(filename, task_ID):
    """ Seeks for a task by its taskID. """
    tasks_list = import_task(filename)

    for task in tasks_list:
        if task.taskID == task_ID:
            return task
    print('Task: Task not Found')


def delete_task(filename, taskID):
    with open(filename, 'r') as file:
        task_dict = json.load(file)
        # print(task_dict)
    for i in range(len(task_dict)):
        if task_dict[i]['TaskID'] == taskID:
            del task_dict[i]
            break
    with open(filename, 'w') as file:
        # print(task_dict)
        json.dump(task_dict, file, indent = 6)
