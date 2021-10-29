import unittest
from project.BackEnd.Display import Display

class MyTestCase(unittest.TestCase):

    def test_display(self):
        display = Display()
        self.assertEqual(10, display.width)
        self.assertEqual(6, display.height)
        self.assertEqual('white', display.text_color)
        self.assertEqual('#303136', display.background_color)
        self.assertEqual('#363940', display.face_color)


if __name__ == '__main__':
    unittest.main()
