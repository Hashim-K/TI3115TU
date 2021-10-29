import unittest
from project.BackEnd.Preset import Presets
from project.BackEnd.General import find_day_zero
import filecmp

class MyTestCase(unittest.TestCase):

    def test_str(self):
        preset = Presets()
        preset.number_of_days = 5
        preset.time_interval = 30
        preset.day_zero = 'a day'
        preset.length_morning_routine = "01:45:00"
        calendar_id = preset.calendar_id
        answer = (f"day_zero = 'a day'\n"
                  f"number_of_days = 5\n"
                  f"time_interval = 30\n"
                  f"length_morning_routine = '01:45:00'\n"
                  f"calendar_id = '{calendar_id}'\n")
        self.assertEqual(answer, str(preset))

    def test_Store(self):
        preset = Presets()
        calendar_id = preset.calendar_id
        preset.number_of_days = 5
        preset.time_interval = 30
        preset.day_zero = 'a day'
        preset.length_morning_routine = "01:45:00"
        preset.calendar_id = 3
        preset.Store()
        self.assertTrue(filecmp.cmp("../data/presets.json",
                                    'jsonfiles/TestPresetsStore.json'))
        preset.number_of_days = 7
        preset.time_interval = 15
        preset.day_zero = find_day_zero(0)
        preset.length_morning_routine = "01:45:00"
        preset.calendar_id = calendar_id
        preset.Store()



if __name__ == '__main__':
    unittest.main()
