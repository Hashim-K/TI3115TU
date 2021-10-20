import unittest
from project.BackEnd.Scheduling_Algorithm import calculate_days_till_deadline, overlap_check, PossibleTime
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
        empty = [[[5, 25]]]
        event = PossibleTime(3, [[0, 6], [0, 24]], 1)
        self.assertFalse(overlap_check(tasks_list, empty, event))
        event = PossibleTime(3, [[0, 5], [0, 10]], 1)
        self.assertTrue(overlap_check(tasks_list, empty, event))

if __name__ == '__main__':
    unittest.main()
