import unittest
from unittest.mock import patch
from project.BackEnd.Schedule import StartAndEnd, AppendEvents, ResolveOverlap, DeleteEvent
from project.BackEnd.Schedule import Display, EmptySlots, AddOccurrence, Event, Presets, Main, schedule, presets
import os
import json
dirname = os.path.dirname(__file__)
import numpy as np
import filecmp

class MyTestCase(unittest.TestCase):

    with open(os.path.join(dirname, '../data/presets.json'), 'r') as openfile:
        pre = json.load(openfile)

    def test_Display(self):
        display = Display()
        display.DarkMode()
        self.assertEqual('white', display.text_color)
        self.assertEqual('#303136', display.background_color)
        self.assertEqual('#363940', display.face_color)
        display.LightMode()
        self.assertEqual('black', display.text_color)
        self.assertEqual('white', display.background_color)
        self.assertEqual('#DDDDDD', display.face_color)

    def test_array_initialization(self):
        trial = Main()
        trial.EmptyArrays()
        length1 = MyTestCase.pre['number_of_days']
        length2 = int(24 * 60 / MyTestCase.pre['time_interval'])
        self.assertEqual(length1, len(trial.schedule))
        self.assertEqual(length2, len(trial.schedule[0]))
        self.assertEqual(trial.schedule.all(), trial.overlap.all())

    # def test_preset_store(self):
    #     preset = Presets()
    #     day_zero = preset.day_zero
    #     preset.day_zero = "random text"
    #     preset.Store()
    #     self.assertTrue(filecmp.cmp('../data/presets.json', 'jsonfiles/TestPresetsStore.json'))
    #     preset.day_zero = day_zero
    #     preset.Store()

    def test_empty_slots(self):
        presets.number_of_days = 3
        presets.time_interval = 60
        schedule.number_of_slots = round(24 * 60 / presets.time_interval)
        schedule.schedule = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1
        answer = [[[0, 0], [2, 23]]]
        self.assertEqual(answer, EmptySlots())
        for i in range(5):
            schedule.schedule[1][10+i] = 3
        answer = [[[0, 0], [1, 9]], [[1, 15], [2, 23]]]
        self.assertEqual(answer, EmptySlots())
        schedule.schedule = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1
        schedule.schedule[2][-1] = 2
        answer = [[[0, 0], [2, 22]]]
        self.assertEqual(answer, EmptySlots())


# @patch('builtins.print')
# def test_PrintPresets(mock_print):
#     with open(os.path.join(dirname, '../data/presets.json'), 'r') as openfile:
#         pre = json.load(openfile)
#     answer = (f"day_zero = '{pre['day_zero']}'\n"
#               f"number_of_days = {pre['number_of_days']}\n"
#               f"time_interval = {pre['time_interval']}\n"
#               f"length_morning_routine = '{pre['length_morning_routine']}'\n"
#               f"dark_mode = {pre['dark_mode']}\n")
#     trial = Presets()
#     trial.PrintPresets()
#     mock_print.assert_called_with(answer)
#     trial = Presets()
#     trial.time_interval = 'random text'
#     trial.PrintPresets()
#     answer = (f"day_zero = '{pre['day_zero']}'\n"
#               f"number_of_days = {pre['number_of_days']}\n"
#               f"time_interval = random text\n"
#               f"length_morning_routine = '{pre['length_morning_routine']}'\n"
#               f"dark_mode = {pre['dark_mode']}\n")
#     mock_print.assert_called_with(answer)


if __name__ == '__main__':
    unittest.main()
