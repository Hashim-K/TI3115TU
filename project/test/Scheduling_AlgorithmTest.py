import unittest
from project.BackEnd.Scheduling_Algorithm import calculate_days_till_deadline, overlap_check, PossibleTime, timeslot_pref, obtain_day_zero
from project.BackEnd.Task import Task, import_task
import os
from datetime import datetime
dirname = os.path.dirname(__file__)

class MyTestCase(unittest.TestCase):

    def test_calculate_days_till_deadline(self):
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        self.assertEqual(1, calculate_days_till_deadline(task, obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2023, 1, 17, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(455, calculate_days_till_deadline(task,
                            obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 19, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True,
                    1, 'nofile')
        self.assertEqual(0, calculate_days_till_deadline(task,
                            obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))))

    def test_overlap_check(self):
        tasks_list = import_task(os.path.join(dirname, 'jsonfiles/FileForTestingOne.json'))
        empty = [[[0, 5], [0, 25]]]
        event = PossibleTime(3, [[0, 6], [0, 24]], 1)
        date_zero = obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))
        self.assertFalse(overlap_check(tasks_list, empty, event, date_zero))
        event = PossibleTime(3, [[0, 5], [0, 10]], 1)
        self.assertTrue(overlap_check(tasks_list, empty, event, date_zero))
        tasks_list.append(Task(-1, "Title", "Description", 15, 0, datetime(2021, 11, 10, 0, 0), False, "category 1",
                               "Morning (8:00-12:00)", True, 1, 'nofile'))
        self.assertFalse(overlap_check(tasks_list, empty, event, date_zero))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 11, 20, 0, 0), False, "category 1",
                               "Morning (8:00-12:00)", True, 4, 'nofile')
        self.assertFalse(overlap_check([task], empty, event, date_zero))
        task = Task(-1, "Title", "Description", 3, 0, datetime(2021, 11, 21, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 2, 'nofile')
        self.assertTrue(overlap_check([task], empty, event, date_zero))
        empty = [[[0, 5], [0, 25]], [[0, 40], [0, 45]], [[3, 30], [3, 35]]]
        event = PossibleTime(3, [[0, 5], [0, 14]], 1)
        task1 = Task(1, "Title", "Description", 10, 0, datetime(2021, 11, 21, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        task2 = Task(2, "Title", "Description", 5, 0, datetime(2021, 11, 23, 0, 0), False, "category 1",
                            "Morning (8:00-12:00)", True, 1, 'nofile')
        task3 = Task(3, "Title", "Description", 5, 0, datetime(2021, 11, 24, 0, 0), False, "category 1",
                            "Morning (8:00-12:00)", True, 1, 'nofile')
        task4 = Task(4, "Title", "Description", 5, 0, datetime(2021, 11, 25, 0, 0), False, "category 1",
                            "Morning (8:00-12:00)", True, 2, 'nofile')
        self.assertTrue(overlap_check([task1, task2, task3], empty, event, date_zero))
        self.assertFalse(overlap_check([task1, task2, task3, task4], empty, event, date_zero))
        self.assertFalse(overlap_check([task1, task2, task4], empty, event, date_zero))
        self.assertTrue(overlap_check([task3, task2, task1], empty, event, date_zero))
        event = PossibleTime(3, [[0, 5], [0, 22]], 1)
        empty = [[[0, 5], [0, 25]], [[0, 40], [0, 45]], [[3, 30], [3, 35]], [[4, 20], [4, 60]]]
        task5 = Task('pay att', "Title", "Description", 6, 0, datetime(2021, 10, 19, 0, 0), False, "category 1",
                     "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertFalse(overlap_check([task5], empty, event, date_zero))


    def test_timeslot_pref(self):
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "Ungodly hours (0:00-8:00)", True, 1, 'nofile')
        timeslot = 80
        self.assertEqual(1, timeslot_pref(task, timeslot))
        timeslot = 95
        self.assertEqual(3, timeslot_pref(task, timeslot))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(1, timeslot_pref(task, timeslot))
        timeslot = 150
        self.assertEqual(3, timeslot_pref(task, timeslot))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "Afternoon (12:00-16:00)", True, 1, 'nofile')
        self.assertEqual(1, timeslot_pref(task, timeslot))
        timeslot = 192
        self.assertEqual(3, timeslot_pref(task, timeslot))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "Evening (16:00-20:00)", True, 1, 'nofile')
        self.assertEqual(1, timeslot_pref(task, timeslot))
        timeslot = 265
        self.assertEqual(3, timeslot_pref(task, timeslot))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "Night (20:00-23:59)", True, 1, 'nofile')
        self.assertEqual(1, timeslot_pref(task, timeslot))
        timeslot = 300
        self.assertEqual(3, timeslot_pref(task, timeslot))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "None", True, 1, 'nofile')
        self.assertEqual(2, timeslot_pref(task, timeslot))

    def test_eq(self):
        time1 = PossibleTime(3, [[2, 56], [2, 80]], 2)
        time2 = PossibleTime(3, [[2, 56], [2, 80]], 3)
        time3 = PossibleTime(4, [[2, 56], [2, 80]], 2)
        self.assertTrue(time1 == time2)
        self.assertFalse(time1 == time3)

    def test_string(self):
        time = PossibleTime(3, [[2, 56], [2, 80]], 2)
        self.assertEqual("TaskID: 3 | [[2, 56], [2, 80]] | score: 2", str(time))


if __name__ == '__main__':
    unittest.main()
