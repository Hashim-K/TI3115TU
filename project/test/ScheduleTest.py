import unittest
from project.BackEnd.Schedule import ImportGoogleEvents, StartAndEnd, AppendEvents, BlockIndex, ResolveOverlap, DeleteEvent
from project.BackEnd.Schedule import Display_, EmptySlots, AddOccurrence, Event, Display, Routines, Presets, Main

class MyTestCase(unittest.TestCase):

    def test_DarkMode(self):
        display = Display()
        display.DarkMode()
        self.assertEqual('white', display.text_color)
        self.assertEqual('#303136', display.background_color)
        self.assertEqual('#363940', display.face_color)


if __name__ == '__main__':
    unittest.main()
