import unittest
from unittest.mock import patch
from project.BackEnd.Schedule import ImportGoogleEvents, StartAndEnd, AppendEvents, BlockIndex, ResolveOverlap, DeleteEvent
from project.BackEnd.Schedule import Display_, EmptySlots, AddOccurrence, Event, Display, Routines, Presets, Main

class MyTestCase(unittest.TestCase):

    def test_DarkMode(self):
        display = Display()
        display.DarkMode()
        self.assertEqual('white', display.text_color)
        self.assertEqual('#303136', display.background_color)
        self.assertEqual('#363940', display.face_color)

@patch('builtins.print')
def test_PrintPresets(mock_print):
    answer = ("day_zero = '2021-09-12'\n"
          "number_of_days = 7\n"
          "time_interval = 5\n"
          "alarm_time = '07:30:00'\n"
          "length_sleep = '08:00:00'\n"
          "length_morning_routine = '00:40:00'\n"
          "lunch_time = '12:30:00'\n"
          "length_lunch = '00:45:00'\n"
          "dinner_time = '18:30:00'\n"
          "length_dinner = '01:15:00'\n"
          "sleep = True\n"
          "morning_routine = True\n"
          "lunch = True\n"
          "dinner = True\n"
          "import_google = True\n")
    trial = Presets()
    trial.PrintPresets()
    mock_print.assert_called_with(answer)
    trial = Presets()
    trial.length_lunch = 'random text'
    trial.PrintPresets()
    answer = ("day_zero = '2021-09-12'\n"
              "number_of_days = 7\n"
              "time_interval = 5\n"
              "alarm_time = '07:30:00'\n"
              "length_sleep = '08:00:00'\n"
              "length_morning_routine = '00:40:00'\n"
              "lunch_time = '12:30:00'\n"
              "length_lunch = 'random text'\n"
              "dinner_time = '18:30:00'\n"
              "length_dinner = '01:15:00'\n"
              "sleep = True\n"
              "morning_routine = True\n"
              "lunch = True\n"
              "dinner = True\n"
              "import_google = True\n")
    mock_print.assert_called_with(answer)


if __name__ == '__main__':
    unittest.main()
