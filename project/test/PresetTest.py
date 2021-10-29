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
        category_path = preset.category_path
        google_path = preset.google_path
        routine_path = preset.routine_path
        task_path = preset.task_path
        schedule_path = preset.schedule_path
        schedule_image = preset.schedule_image
        data_path = preset.data_path
        answer = (f"day_zero = 'a day'\n"
                  f"number_of_days = 5\n"
                  f"time_interval = 30\n"
                  f"length_morning_routine = '01:45:00'\n"
                  f"calendar_id = '{calendar_id}'\n"
                  f"data_path = '{data_path}'\n"
                  f"category_path = '{category_path}'\n"
                  f"google_path = '{google_path}'\n"
                  f"routine_path = '{routine_path}'\n"
                  f"task_path = '{task_path}'\n"
                  f"schedule_path = '{schedule_path}'\n"
                  f"schedule_image = '{schedule_image}'\n")
        self.assertEqual(answer, str(preset))

    def test_Store_and_Update(self):
        preset = Presets()
        calendar_id = preset.calendar_id
        preset.number_of_days = 5
        preset.time_interval = 30
        preset.day_zero = 'a day'
        preset.length_morning_routine = "01:45:00"
        preset.calendar_id = 3
        preset.google_path = 'substitute'
        preset.category_path = 'substitute'
        preset.google_path = 'substitute'
        preset.routine_path = 'substitute'
        preset.task_path = 'substitute'
        preset.schedule_path = 'substitute'
        preset.schedule_image = 'substitute'
        preset.data_path = 'substitute'
        preset.Store()
        self.assertTrue(filecmp.cmp("../data/presets.json",
                                    'jsonfiles/TestPresetsStore.json'))
        preset.number_of_days = 7
        preset.time_interval = 15
        preset.day_zero = find_day_zero(0)
        preset.length_morning_routine = "01:45:00"
        preset.calendar_id = calendar_id
        preset.update()
        self.assertFalse(filecmp.cmp("../data/presets.json",
                                    'jsonfiles/TestPresetsStore.json'))



if __name__ == '__main__':
    unittest.main()
