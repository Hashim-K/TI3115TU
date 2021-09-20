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



