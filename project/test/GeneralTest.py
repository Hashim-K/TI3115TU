import unittest
from project.BackEnd.General import DaysSince2020, LeapYear,  CheckWhatDay, DayAndSlot, Slot
from project.BackEnd.General import Slot2Time, XDaysLater, CreateXTicks, EmptySlots, DateFormat


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
        self.assertEqual(731, DaysSince2020([1, 1, 2022]))
        self.assertEqual(645, DaysSince2020([7, 10, 2021]))
        self.assertEqual(1520, DaysSince2020([29, 2, 2024]))

    def test_CheckWhatDay(self):
        self.assertEqual(0, CheckWhatDay([12, 7, 2021]))
        self.assertEqual(1, CheckWhatDay([12, 7, 2022]))
        self.assertEqual(2, CheckWhatDay([1, 1, 2020]))
        self.assertEqual(3, CheckWhatDay([29, 2, 2024]))
        self.assertEqual(4, CheckWhatDay([15, 10, 2021]))
        self.assertEqual(5, CheckWhatDay([16, 10, 2021]))
        self.assertEqual(6, CheckWhatDay([17, 10, 2021]))

    def test_DayAndSlot(self):
        self.assertEqual([2, 208], DayAndSlot('06-10-2021,17:21:00', '2021-10-04', 5))


if __name__ == '__main__':
    unittest.main()
