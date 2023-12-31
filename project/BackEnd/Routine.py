import json
import os.path

from project.BackEnd.Preset import Presets
from project.BackEnd.TimeList import TimeList


class Routine:
    """ The routine class is used to create, store and edit routines used by the software in a JSON format. """
    highest_id = -1

    def __init__(self, routine_id: int, name: str, timeslots: TimeList):
        presets = Presets()
        if routine_id != -1:  # routine_id is given in the initializer
            self.routine_id = routine_id
        else:
            if not os.path.exists(presets.routine_path) or os.stat(presets.routine_path).st_size < 4: # calculating routine_id from the already exisiting events
                Routine.highest_id += 1
                self.routine_id = Routine.highest_id
            else:
                with open(presets.routine_path) as file:  # calculating routine_id from an already existing JSON file with routines
                    routine_dict = json.load(file)
                    self.routine_id = routine_dict[-1]['routine_id'] + 1
        self.name = name
        self.timeslots = timeslots

    def __str__(self):
        text_description = f"routine \"{self.name}\" ({self.routine_id}):\n{self.timeslots}"
        return text_description


    def export_routine(self):
        """ Storing routines in a JSON file. """
        presets = Presets()
        entry = {
            "routine_id": self.routine_id,
            "Name": self.name,
            "Times": self.timeslots.times()
        }
        if not os.path.exists(presets.routine_path):  # if filename does not exist create a list to fill
            data = []
        else:
            if os.stat(presets.routine_path).st_size == 0:  # if filename is empty make new one
                os.remove(presets.routine_path)
                data = []
            else:
                with open(presets.routine_path, 'r') as file:  # if filename exists load the data
                    data = json.load(file)
        data.append(entry)
        with open(presets.routine_path, 'w') as file:  # write into file
            json.dump(data, file, indent=6)

    def create_event(self):
        color = "#CAA0DA"
        if self.name == "Sleep":
            color = "#546fa8"
        if self.name == "Morning Routine":
            color = "#7b9adb"
        if self.name == "Lunch":
            color = "#e8b048"
        if self.name == "Dinner":
            color = "#ba8420"
        return ["Routine", self.routine_id, color, self.timeslots]


def import_routine():
    """ Creates a list of all the routines in a JSON file. """
    presets = Presets()
    routines_list = []
    try:
        with open(presets.routine_path, 'r') as file:
            routine_dict = json.load(file)
            for routines in routine_dict:
                tl = TimeList()
                for time in routines['Times']:
                    tl.add_time(time[0][0], time[0][1], time[1][0], time[1][1])
                routines_list.append(Routine(routines['routine_id'], routines['Name'], tl))
    except FileNotFoundError:
        print('File does not exist')
    return routines_list


def find_routine(routine_ID):
    """ Seeks for a routine by its routine_id. """
    routines_list = import_routine()
    for routine in routines_list:
        if routine.routine_id == routine_ID:
            return routine
    print('routine: routine not Found')


def delete_all_routines():
    """Deletes all routines from a JSON file."""
    routines_list = import_routine()
    for routine in routines_list:
        delete_routine(routine.routine_id)


def delete_routine(routine_id):
    """ Delete a routine from a JSON file. """
    presets = Presets()
    try:
        with open(presets.routine_path, 'r') as file:
            routine_dict = json.load(file)
        for i in range(len(routine_dict)):
            if routine_dict[i]['routine_id'] == routine_id:
                del routine_dict[i]
                break
        with open(presets.routine_path, 'w') as file:
            json.dump(routine_dict, file, indent = 6)
    except FileNotFoundError:
        print('File does not exist')


def delete_times(routine_id, times):
    """ Delete a session from a JSON file. """
    rl = import_routine()
    delete_all_routines()
    for routine in rl:
        if routine.routine_id == routine_id:
            for i in range(len(times)):
                t = times[i]
                routine.timeslots.delete_time(t[0][0], t[0][1], t[1][0], t[1][1])
        routine.export_routine()

