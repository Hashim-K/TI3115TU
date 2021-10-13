import json
import os.path
from datetime import datetime
from project.BackEnd import Schedule


class Task:

    highest_id = Schedule.events[-1].ID

    def __init__(self, name: str, description: str, duration: int, priority: int, deadline: str,
                 repeatable: bool, category: str, preferred: str, plan_on_same: bool, session: int, filename: str):
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
        if not os.path.exists(filename) or os.stat(filename).st_size < 4:
            Task.highest_id += 1
            self.taskID = Task.highest_id
        else:
            with open(filename) as file:
                task_dict = json.load(file)
                self.taskID = task_dict[-1]['TaskID'] + 1


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
    try:
        with open(filename, 'r') as file:
            task_dict = json.load(file)
            for tasks in task_dict:
                tasks_list.append(Task(tasks['Name'], tasks['Description'], tasks['Duration'],
                        tasks['Priority'], datetime.fromisoformat(tasks['Deadline']), tasks['Repeatable'],
                        tasks['Category'], tasks['Preferred'], tasks['Plan_on_same'], tasks['Session'], filename))
    except FileNotFoundError:
        print('File does not exist')
    return tasks_list


def delete_task(filename, taskID):
    try:
        with open(filename, 'r') as file:
            task_dict = json.load(file)
        for i in range(len(task_dict)):
            if task_dict[i]['TaskID'] == taskID:
                del task_dict[i]
                break
        with open(filename, 'w') as file:
            json.dump(task_dict, file, indent = 6)
    except FileNotFoundError:
        print('File does not exist')

