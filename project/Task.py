import json
from Schedule import Events
import os.path
from datetime import datetime

class Task:

    highest_id = Events[-1].ID

    def __init__(self, name, description, duration, priority, deadline,
                 repeatable, category, preferred, plan_on_same, session):
        self.name = name #string
        self.description = description #string
        self.duration = duration #int / datetime object
        self.priority = priority #int
        self.deadline = deadline #date (datetime object)
        self.repeatable = repeatable #boolean
        self.category = category #integer
        self.preferred = preferred #string ??
        self.plan_on_same = plan_on_same # boolean
        self.session = session #int
        Task.highest_id += 1
        self.taskID = Task.highest_id #calculated by programme

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
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
        else:
            data = []
        data.append(entry)
        with open(filename, 'w') as file:
            json.dump(data, file, indent = 6)


def import_task(filename):
    tasks_list = []
    with open(filename, 'r') as file:
        task_dict = json.load(file)
        for tasks in task_dict:
            tasks_list.append(Task(tasks['Name'], tasks['Description'], tasks['Duration'],
                    tasks['Priority'], datetime.fromisoformat(tasks['Deadline']), tasks['Repeatable'],
                    tasks['Category'], tasks['Preferred'], tasks['Plan_on_same'], tasks['Session']))
    return tasks_list

print(import_task('save_file.json')[0])
