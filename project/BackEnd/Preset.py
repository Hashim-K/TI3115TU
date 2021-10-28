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

    def __str__(self):
        return (f"day_zero = '{self.day_zero}'\n"
                f"number_of_days = {self.number_of_days}\n"
                f"time_interval = {self.time_interval}\n"
                f"length_morning_routine = '{self.length_morning_routine}'\n")

    def Store(self):
        presets_json = {'day_zero': self.day_zero,
                        'number_of_days': self.number_of_days,
                        'time_interval': self.time_interval,
                        'length_morning_routine': self.length_morning_routine}
        with open(os.path.join(dirname, '../data/presets.json'), 'w') as out_file:
            json.dump(presets_json, out_file, indent=6)