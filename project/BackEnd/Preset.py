import json
import os
from project.BackEnd.General import find_day_zero
dirname = os.path.dirname(__file__)

class Presets:
    def __init__(self):
        with open(os.path.join(dirname, '../data/presets.json'), 'r') as openfile:
            preset_dictionary = json.load(openfile)
            self.day_zero = find_day_zero(0)
            self.number_of_days = preset_dictionary['number_of_days']
            self.time_interval = preset_dictionary['time_interval']
            self.length_morning_routine = preset_dictionary['length_morning_routine']
            self.calendar_id = -1
            if preset_dictionary['calendar_id'] != -1:
                self.calendar_id = preset_dictionary['calendar_id']
            self.data_path = os.path.join(dirname, '../data/')
            self.category_path = preset_dictionary['category_path']
            self.google_path = preset_dictionary['google_path']
            self.routine_path = preset_dictionary['routine_path']
            self.task_path = preset_dictionary['task_path']
            self.schedule_path = preset_dictionary['schedule_path']
            self.schedule_image = preset_dictionary['schedule_image']
            if not os.path.exists(self.data_path + "/" + self.day_zero):
                os.makedirs(self.data_path + "/" + self.day_zero)

    def __str__(self):
        return (f"day_zero = '{self.day_zero}'\n"
                f"number_of_days = {self.number_of_days}\n"
                f"time_interval = {self.time_interval}\n"
                f"length_morning_routine = '{self.length_morning_routine}'\n"
                f"calendar_id = '{self.calendar_id}'\n"
                f"data_path = '{self.data_path}'\n"
                f"category_path = '{self.category_path}'\n"
                f"google_path = '{self.google_path}'\n"
                f"routine_path = '{self.routine_path}'\n"
                f"task_path = '{self.task_path}'\n"
                f"schedule_path = '{self.schedule_path}'\n"
                f"schedule_image = '{self.schedule_image}'\n")

    def Store(self):
        presets_json = {'day_zero': self.day_zero,
                        'number_of_days': self.number_of_days,
                        'time_interval': self.time_interval,
                        'length_morning_routine': self.length_morning_routine,
                        'calendar_id': self.calendar_id,
                        'data_path': self.data_path,
                        'category_path': self.category_path,
                        'google_path': self.google_path,
                        'routine_path': self.routine_path,
                        'task_path': self.task_path,
                        'schedule_path': self.schedule_path,
                        'schedule_image': self.schedule_image}
        with open(os.path.join(dirname, '../data/presets.json'), 'w') as out_file:
            json.dump(presets_json, out_file, indent=6)

    def update(self):
        self.category_path = os.path.join(dirname, '../data/' + self.day_zero + '/categories.json')
        self.google_path = os.path.join(dirname, '../data/' + self.day_zero + '/google_events.json')
        self.routine_path = os.path.join(dirname, '../data/' + self.day_zero + '/routines.json')
        self.task_path = os.path.join(dirname, '../data/' + self.day_zero + '/tasks.json')
        self.schedule_path = os.path.join(dirname, '../data/' + self.day_zero + '/schedule.json')
        self.schedule_image = os.path.join(dirname, '../data/' + self.day_zero + '/schedule.jpg')
        self.Store()