import unittest
from project.BackEnd.Scheduling_Algorithm import calculate_days_till_deadline, overlap_check, PossibleTime, timeslot_pref
from project.BackEnd.Task import Task, import_task
import os
from datetime import datetime
dirname = os.path.dirname(__file__)

class MyTestCase(unittest.TestCase):

    def test_calculate_days_till_deadline(self):
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        self.assertEqual(1, calculate_days_till_deadline(task, os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json')))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2023, 1, 17, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(455, calculate_days_till_deadline(task,
                                                         os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json')))

    def test_overlap_check(self):
        tasks_list = import_task(os.path.join(dirname, 'jsonfiles/FileForTestingOne.json'))
        empty = [[[5, 25]], [], [], [], [], [], []]
        event = PossibleTime(3, [[0, 6], [0, 24]], 1)
        self.assertFalse(overlap_check(tasks_list, empty, event))
        event = PossibleTime(3, [[0, 5], [0, 10]], 1)
        self.assertTrue(overlap_check(tasks_list, empty, event))
        tasks_list.append(Task(-1, "Title", "Description", 15, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                               "Morning (8:00-12:00)", True, 1, 'nofile'))
        self.assertFalse(overlap_check(tasks_list, empty, event))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                               "Morning (8:00-12:00)", True, 4, 'nofile')
        self.assertFalse(overlap_check([task], empty, event))
        task = Task(-1, "Title", "Description", 3, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 2, 'nofile')
        self.assertTrue(overlap_check([task], empty, event))
        empty = [[[5, 25], [40, 45]], [], [[30, 35]], [], [], [], []]
        event = PossibleTime(3, [[0, 5], [0, 14]], 1)
        task1 = Task(-1, "Title", "Description", 10, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        task2 = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                            "Morning (8:00-12:00)", True, 1, 'nofile')
        task3 = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                            "Morning (8:00-12:00)", True, 1, 'nofile')
        task4 = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, "category 1",
                            "Morning (8:00-12:00)", True, 2, 'nofile')
        self.assertTrue(overlap_check([task1, task2, task3], empty, event))
        self.assertFalse(overlap_check([task1, task2, task3, task4], empty, event))
        self.assertFalse(overlap_check([task1, task2, task4], empty, event))
        self.assertTrue(overlap_check([task3, task2, task1], empty, event))

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
