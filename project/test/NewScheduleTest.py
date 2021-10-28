import unittest
from project.BackEnd.NewSchedule import Schedule, import_schedule
from project.BackEnd.Preset import Presets
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
        presets.Store()
        schedule = Schedule()
        answer = "Day 1: [GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3),\n" \
                    "GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), GoogleEvent: (3), -1, -1,\n"\
                    "-1, -1, -1, -1, -1, -1, -1, -1, Routine: (2), Routine: (2), Routine: (2), Routine: (2)]\n"\
                    "Day 2: [Routine: (2), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1),\n"\
                    "Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1), Task: (1),\n"\
                    "Task: (1), Task: (1), Task: (1), Task: (1), -1, -1, -1]\n"
        trial = import_schedule('jsonfiles/TestSchedule.json')
        self.assertEqual(answer, str(trial))
        presets.time_interval = 15
        presets.number_of_days = 7
        presets.Store()

if __name__ == '__main__':
    unittest.main()
