import json

class Task:

    def __init__(self, TaskID, Name, Description, Total_Duration, Priority, Deadline,
                 Repeatable, Category, Preferred, Plan_on_same, Session):
        self.TaskID = TaskID
        self.Name = Name
        self.Description = Description
        self.Total_Duration = Total_Duration
        self.Priority = Priority
        self.Deadline = Deadline
        self.Repeatable = Repeatable
        self.Category = Category
        self.Preferred = Preferred
        self.Plan_on_same = Plan_on_same
        self.Session = Session

    def export_task(self, filename):
        entry = {
            "TaskID": self.TaskID,
            "Name": self.Name,
            "Description": self.Description,
            "Total_Duration": self.Total_Duration,
            "Priority": self.Priority,
            "Deadline": self.Deadline,
            "Repeatable": self.Repeatable,
            "Category": self.Category,
            "Preferred": self.Preferred,
            "Plan_on_same": self.Plan_on_same,
            "Session": self.Session
        }
        with open(filename, 'r') as file:
            data = json.load(file)
        data.append(entry)
        with open(filename, 'w') as file:
            json.dump(data, file)


def import_task(filename):
    tasks_list = []
    with open(filename, 'r') as file:
        task_dict = json.load(file)
        for tasks in task_dict:
            tasks_list.append(Task(tasks['TaskID'], tasks['Name'], tasks['Description'], tasks['Total_Duration'],
                    tasks['Priority'], tasks['Deadline'], tasks['Repeatable'],
                    tasks['Category'], tasks['Preferred'], tasks['Plan_on_same'], tasks['Session']))
    print(len(tasks_list))

task1 = Task('0002', 'Anime', 'Best show ever', 4, 0, 'Now', 'Yes', 'Free Time', 'No preference', 'No', 'test')

task1.export_task('TestTask1.json')

import_task('TestTask1.json')
