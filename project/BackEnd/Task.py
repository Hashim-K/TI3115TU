import json
import os.path
from datetime import datetime
from project.BackEnd import Schedule


class Task:
    """ The task class is used to create, store and edit tasks used by the software in a JSON format. """
    try:
        highest_id = Schedule.events[-1].ID
    except IndexError:
        highest_id = 0


    def __init__(self, taskID: int, name: str, description: str, duration: int, priority: int, deadline: str,
                 repeatable: bool, category: int, preferred, plan_on_same: bool, session: int, filename: str):
        if taskID != -1:  # taskID is given in the initializer
            self.taskID = taskID
        else:
            if not os.path.exists(filename) or os.stat(filename).st_size < 4:  # calculating taskID from the already exisiting events
                Task.highest_id += 1
                self.taskID = Task.highest_id
            else:
                with open(filename) as file: # calculating taskID from an already existing JSON file with tasks
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

    def __lt__(self, other):
        return self.duration < other.duration

    def export_task(self, filename):
        """ Storing tasks in a JSON file. """
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
        if not os.path.exists(filename):  # if filename does not exist create a list to fill
            data = []
        else:
            if os.stat(filename).st_size == 0: # if filename is empty make new one
                os.remove(filename)
                data = []
            else:
                with open(filename, 'r') as file: # if filename exists load the data
                    data = json.load(file)
        data.append(entry)
        with open(filename, 'w') as file: # write into file
            json.dump(data, file, indent=6)


def import_task(filename):
    """ Creates a list of all the tasks in a JSON file. """
    tasks_list = []
    try:
        with open(filename, 'r') as file:
            task_dict = json.load(file)
            for tasks in task_dict:
                tasks_list.append(Task(tasks['TaskID'], tasks['Name'], tasks['Description'], tasks['Duration'],
                        tasks['Priority'], datetime.fromisoformat(tasks['Deadline']), tasks['Repeatable'],
                        tasks['Category'], tasks['Preferred'], tasks['Plan_on_same'], tasks['Session'], filename))
    except FileNotFoundError:
        print('File does not exist')
    return tasks_list


def find_task(filename, task_ID):
    """ Seeks for a task by its taskID. """
    tasks_list = import_task(filename)
    for task in tasks_list:
        if task.taskID == task_ID:
            return task
    print('Task: Task not Found')


def delete_all_tasks(filename):
    """Deletes all tasks from a JSON file."""
    tasks_list = import_task(filename)
    for task in tasks_list:
        delete_task(filename, task.taskID)


def delete_task(filename, taskID):
    """ Delete a task from a JSON file. """
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


def delete_session(filename, taskID):
    """ Delete a session from a JSON file. """
    try:
        with open(filename, 'r') as file:
            task_dict = json.load(file)
        for i in range(len(task_dict)):
            if task_dict[i]['TaskID'] == taskID:
                if task_dict[i]['Session'] == 1:  # delete task if only one session left
                    del task_dict[i]
                else:
                    task_dict[i]['Session'] -= 1
                break
        with open(filename, 'w') as file:
            json.dump(task_dict, file, indent = 6)
    except FileNotFoundError:
        print('File does not exist')


def edit_task(filename, taskID: int, name: str, description: str, duration: int, priority: int, deadline: str,
                 repeatable: bool, category: str, preferred, plan_on_same: bool, session: int):
    try:
        with open(filename, 'r') as file:
            task_dict = json.load(file)
        for i in range(len(task_dict)):
            if task_dict[i]['TaskID'] == taskID:
                task_dict[i]['Name'] = name
                task_dict[i]['Description'] = description
                task_dict[i]['Duration'] = duration
                task_dict[i]['Priority'] = priority
                task_dict[i]['Deadline'] = deadline
                task_dict[i]['Repeatable'] = repeatable
                task_dict[i]['Category'] = category
                task_dict[i]['Preferred'] = preferred
                task_dict[i]['Plan_on_same'] = plan_on_same
                task_dict[i]['Session'] = session
                break
        with open(filename, 'w') as file:
            json.dump(task_dict, file, indent=6)
    except FileNotFoundError:
        print('File does not exist')

