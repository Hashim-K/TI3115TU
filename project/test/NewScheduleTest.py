import unittest
from project.BackEnd.NewSchedule import Schedule
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

if __name__ == '__main__':
    unittest.main()
