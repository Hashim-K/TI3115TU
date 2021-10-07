import unittest
from project.BackEnd.General import DaysSince2020, LeapYear

class MyTestCase(unittest.TestCase):

    def test_LeapYear(self):
        self.assertTrue(LeapYear(1868))
        self.assertTrue(LeapYear(2348))
        self.assertTrue(LeapYear(2000))
        self.assertFalse(LeapYear(1800))
        self.assertFalse(LeapYear(1933))
        self.assertFalse(LeapYear(2365))
        self.assertFalse(LeapYear(2019))

    def test_DaysSince2020(self):
        self.assertEqual(0, DaysSince2020([1, 1, 2020]))
        self.assertEqual(366, DaysSince2020([1, 1, 2021]))
        self.assertEqual(365, DaysSince2020([31, 12, 2020]))
        self.assertEqual(731, DaysSince2020([1, 1, 2022]))

if __name__ == '__main__':
    unittest.main()
