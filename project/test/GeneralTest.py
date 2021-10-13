import unittest
from project.BackEnd.General import DaysSince2020, LeapYear,  CheckWhatDay, DayAndSlot
from project.BackEnd.General import Slot2Time, XDaysLater, DateFormat, Slot, TimeBetween


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
        self.assertEqual([0, 208], DayAndSlot('04-10-2021,17:21:00', '2021-10-04', 5))
        self.assertEqual([0, 0], DayAndSlot('04-10-2021,00:00:00', '2021-10-04', 5))
        self.assertEqual([0, 0], DayAndSlot('04-10-2021,00:00:00', '2021-10-04', 5))
        self.assertEqual([0, 17], DayAndSlot('04-10-2021,17:00:00', '2021-10-04', 60))
        self.assertEqual([0, 209], DayAndSlot('04-10-2021,17:23:00', '2021-10-04', 5))

    def test_Slot(self):
        self.assertEqual(208, Slot('17:21:00', 5))
        self.assertEqual(0, Slot('00:00:00', 5))
        self.assertEqual(17, Slot('17:00:00', 60))
        self.assertEqual(209, Slot('17:23:00', 5))

    def test_Slot2Time(self):
        self.assertEqual('13:55:00', Slot2Time(167, 5))
        self.assertEqual('07:35:00', Slot2Time(91, 5))
        self.assertEqual('15:05:00', Slot2Time(181, 5))
        self.assertEqual('02:05:00', Slot2Time(125, 1))


    def test_DateFormat(self):
        self.assertEqual('September 23rd', DateFormat('2021-09-23'))
        self.assertEqual('January 1st', DateFormat('2021-01-01'))
        self.assertEqual('July 12th', DateFormat('2021-07-12'))
        self.assertEqual('March 2nd', DateFormat('2021-03-02'))

    # I think the description of XDaysLater is not correct
    def test_XDaysLater(self):
        self.assertEqual('2021-7-12', XDaysLater('2021-07-12', 0))
        self.assertEqual('2020-12-17', XDaysLater('2020-12-12', 5))
        self.assertEqual('2021-12-12', XDaysLater('2020-12-12', 366))
        self.assertEqual('2021-12-6', XDaysLater('2021-10-07', 60))

    # ([[start_day, start_slot], [end_day, end_slot]])
    def test_time_between(self):
        block = [[2, 174], [2, 198]]
        self.assertEqual('2:00:00', TimeBetween(block, 5))
        block = [[2, 174], [2, 200]]
        self.assertEqual('2:10:00', TimeBetween(block, 5))
        block = [[3, 0], [3, 1]]
        self.assertEqual('0:05:00', TimeBetween(block, 5))
        block = [[2, 174], [6, 204]]
        self.assertEqual('98:30:00', TimeBetween(block, 5))




if __name__ == '__main__':
    unittest.main()
