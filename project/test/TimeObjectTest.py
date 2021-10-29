import unittest
from project.BackEnd.TimeObject import TimeObject, str_init
import time
import datetime

class MyTestCase(unittest.TestCase):

    def test_init(self):
        timeobject = TimeObject("2021-11-01", 1, 15)
        self.assertEqual("2021-11-02T03:45", timeobject.dateTime)
        self.assertEqual(time.strftime("%z", time.gmtime()), timeobject.timeZone)
        timeobject = TimeObject("2021-11-01", 10, 75)
        self.assertEqual("2021-11-11T18:45", timeobject.dateTime)

    def test_datetime_to_timeslot(self):
        timeobject = TimeObject("2021-11-01", 1, 15)
        self.assertEqual("2021-11-02T03:45", timeobject.dateTime)
        self.assertEqual([1, 15], timeobject.dateTime_to_timeslot())

    def test_str_init(self):
        t = str_init("2021-11-02T03:45", time.strftime("%z", time.gmtime()))
        timeobject = TimeObject("2021-11-01", 1, 15)
        self.assertEqual(t.timeZone, timeobject.timeZone)
        self.assertEqual(t.dateTime, timeobject.dateTime)


if __name__ == '__main__':
    unittest.main()


