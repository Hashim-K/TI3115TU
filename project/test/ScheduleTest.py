import unittest
from unittest.mock import patch
from project.BackEnd.Schedule import ImportGoogleEvents, StartAndEnd, AppendEvents, BlockIndex, ResolveOverlap, DeleteEvent
from project.BackEnd.Schedule import Display, EmptySlots, AddOccurrence, Event, Presets, Main, schedule, presets
import os
import json
dirname = os.path.dirname(__file__)
import numpy as np

class MyTestCase(unittest.TestCase):

    with open(os.path.join(dirname, '../BackEnd/presets.json'), 'r') as openfile:
        pre = json.load(openfile)

    def test_empty_slots(self):
        # presets.number_of_days = 7
        # presets.time_interval = 5
        # schedule.number_of_slots = round(24 * 60 / presets.time_interval)
        # schedule.schedule = np.zeros(shape=(presets.number_of_days, round(24 * 60 / presets.time_interval))) - 1
        answer = [[[0, 0], [0, 287]], [[1, 0], [1, 287]], [[2, 0], [2, 287]], [[3, 0], [3, 287]],
                  [[4, 0], [4, 287]], [[5, 0], [5, 287]], [[6, 0], [6, 287]]]
        self.assertEqual(answer, EmptySlots())

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

@patch('builtins.print')
def test_PrintPresets(mock_print):
    with open(os.path.join(dirname, '../BackEnd/presets.json'), 'r') as openfile:
        pre = json.load(openfile)
    answer = (f"day_zero = '{pre['day_zero']}'\n"
              f"number_of_days = {pre['number_of_days']}\n"
              f"time_interval = {pre['time_interval']}\n"
              f"alarm_time = '{pre['alarm_time']}'\n"
              f"length_sleep = '{pre['length_sleep']}'\n"
              f"length_morning_routine = '{pre['length_morning_routine']}'\n"
              f"lunch_time = '{pre['lunch_time']}'\n"
              f"length_lunch = '{pre['length_lunch']}'\n"
              f"dinner_time = '{pre['dinner_time']}'\n"
              f"length_dinner = '{pre['length_dinner']}'\n"
              f"sleep = {pre['sleep']}\n"
              f"morning_routine = {pre['morning_routine']}\n"
              f"lunch = {pre['lunch']}\n"
              f"dinner = {pre['dinner']}\n"
              f"import_google = {pre['import_google']}\n"
              f"dark_mode = {pre['dark_mode']}\n")
    trial = Presets()
    trial.PrintPresets()
    mock_print.assert_called_with(answer)
    trial = Presets()
    trial.length_lunch = 'random text'
    trial.PrintPresets()
    answer = (f"day_zero = '{pre['day_zero']}'\n"
              f"number_of_days = {pre['number_of_days']}\n"
              f"time_interval = {pre['time_interval']}\n"
              f"alarm_time = '{pre['alarm_time']}'\n"
              f"length_sleep = '{pre['length_sleep']}'\n"
              f"length_morning_routine = '{pre['length_morning_routine']}'\n"
              f"lunch_time = '{pre['lunch_time']}'\n"
              f"length_lunch = 'random text'\n"
              f"dinner_time = '{pre['dinner_time']}'\n"
              f"length_dinner = '{pre['length_dinner']}'\n"
              f"sleep = {pre['sleep']}\n"
              f"morning_routine = {pre['morning_routine']}\n"
              f"lunch = {pre['lunch']}\n"
              f"dinner = {pre['dinner']}\n"
              f"import_google = {pre['import_google']}\n"
              f"dark_mode = {pre['dark_mode']}\n")
    mock_print.assert_called_with(answer)


if __name__ == '__main__':
    unittest.main()
