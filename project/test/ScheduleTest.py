import unittest
from project.BackEnd.Schedule import Schedule, import_schedule, Event
from project.BackEnd.Preset import Presets
from project.BackEnd.Category import random_colour
from project.BackEnd.TimeList import TimeList
import numpy as np

class MyTestCase(unittest.TestCase):

    def test_empty_slots(self):
        presets = Presets()
        presets.number_of_days = 3
        presets.time_interval = 60
        presets.Store()
        schedule = Schedule()
        schedule.number_of_slots = round(24 * 60 / presets.time_interval)
        schedule.schedule = np.zeros(shape=(presets.number_of_days, round(schedule.number_of_slots)), dtype=object) - 1
        answer = [[[0, 0], [2, 23]]]
        self.assertEqual(answer, schedule.empty_slots())
        for i in range(5):
            schedule.schedule[1][10 + i] = 'Task'
        answer = [[[0, 0], [1, 9]], [[1, 15], [2, 23]]]
        self.assertEqual(answer, schedule.empty_slots())
        schedule.schedule = np.zeros(shape=(presets.number_of_days, round(schedule.number_of_slots)), dtype=object) - 1
        schedule.schedule[2][-1] = 'Task'
        answer = [[[0, 0], [2, 22]]]
        self.assertEqual(answer, schedule.empty_slots())
        presets.number_of_days = 7
        presets.time_interval = 15
        presets.Store()

    def test_create_schedule_from_event_list(self):
        presets = Presets()
        presets.time_interval = 60
        presets.number_of_days = 2
        presets.schedule_path = 'jsonfiles/TestSchedule.json'
        presets.Store()
        answer = "Day 1: [GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3),\n" \
                    "GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), -1, -1,\n"\
                    "-1, -1, -1, -1, -1, -1, -1, -1, Routine: (2), Routine: (2), Routine: (2), Routine: (2)]\n"\
                    "Day 2: [Routine: (2), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1),\n"\
                    "Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1),\n"\
                    "Task: (1), Task: (1), Task: (1), Task: (1), -1, -1, -1]\n"
        trial = import_schedule()
        self.assertEqual(answer, str(trial))
        presets.time_interval = 15
        presets.number_of_days = 7
        presets.update()

    def test_return_event(self):
        preset = Presets()
        preset.task_path = 'jsonfiles/FileForTestingOne.json'
        preset.google_path = 'jsonfiles/FileForTestingGoogleEvents.json'
        preset.routine_path = 'jsonfiles/FileForTestingRoutines.json'
        preset.Store()
        time = TimeList()
        event = Event("Task", 1, random_colour(), time)
        task = event.return_event()
        self.assertFalse(task.repeatable)
        event = Event("GoogleEvent", 1, random_colour(), time)
        google = event.return_event()
        self.assertEqual("Summary", google.name)
        event = Event("Routine", 1, random_colour(), time)
        routine = event.return_event()
        self.assertEqual("Example", routine.name)
        event = Event("Event", 1, random_colour(), time).return_event()
        self.assertEqual(None, event)
        preset.update()



if __name__ == '__main__':
    unittest.main()
