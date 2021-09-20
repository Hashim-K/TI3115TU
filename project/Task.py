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

    @property
    def TaskID(self):
        return self.__TaskID

    @property
    def Name(self):
        return self.__Name

    @property
    def Description(self):
        return self.__Description

    @property
    def Total_Duration(self):
        return self.__Total_Duration

    @property
    def Priority(self):
        return self.__Priority

    @property
    def Deadline(self):
        return self.__Deadline

    @property
    def Repeatable(self):
        return self.__Repeatable

    @property
    def Category(self):
        return self.__Category

    @property
    def Preferred(self):
        return self.__Preferred

    @property
    def Plan_on_same(self):
        return self.__Plan_on_same

    @property
    def Session(self):
        return self.__Session


