import unittest
from project.BackEnd.Scheduling_Algorithm import calculate_days_till_deadline, overlap_check, PossibleTime, timeslot_pref
from project.BackEnd.Scheduling_Algorithm import calc_score, single_task_check, best_score_check, main, obtain_day_zero
from project.BackEnd.Task import Task, import_task
from project.BackEnd.Schedule import schedule, presets, ClearEvents, events
import os
from datetime import datetime
import numpy as np
dirname = os.path.dirname(__file__)

class MyTestCase(unittest.TestCase):

    def test_calculate_days_till_deadline(self):
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, 1, ["08:00:00", "12:00:00"], True,
                    1, 'nofile')
        self.assertEqual(1, calculate_days_till_deadline(task, obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2023, 1, 17, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True, 1, 'nofile')
        self.assertEqual(455, calculate_days_till_deadline(task,
                            obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 19, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True,
                    1, 'nofile')
        self.assertEqual(0, calculate_days_till_deadline(task,
                            obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))))

    def test_overlap_check(self):
        tasks_list = [Task(1, "Title", "Description", 5, 0, datetime(2021, 11, 8, 0, 0), False, 1, ["08:00:00", "12:00:00"], True, 1, 'no_file')]
        empty = [[[0, 5], [0, 25]]]
        event = PossibleTime(3, [[0, 6], [0, 24]], 1)
        date_zero = obtain_day_zero(os.path.join(dirname, 'jsonfiles/TestDatesTillDeadline.json'))
        self.assertFalse(overlap_check(tasks_list, empty, event, date_zero))
        event = PossibleTime(3, [[0, 5], [0, 10]], 1)
        self.assertTrue(overlap_check(tasks_list, empty, event, date_zero))
        tasks_list.append(Task(-1, "Title", "Description", 15, 0, datetime(2021, 11, 10, 0, 0), False, 1,
                               ["08:00:00", "12:00:00"], True, 1, 'nofile'))
        self.assertFalse(overlap_check(tasks_list, empty, event, date_zero))
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 11, 20, 0, 0), False, 1,
                               ["08:00:00", "12:00:00"], True, 4, 'nofile')
        self.assertFalse(overlap_check([task], empty, event, date_zero))
        task = Task(-1, "Title", "Description", 3, 0, datetime(2021, 11, 21, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True, 2, 'nofile')
        self.assertTrue(overlap_check([task], empty, event, date_zero))
        empty = [[[0, 5], [0, 25]], [[0, 40], [0, 45]], [[3, 30], [3, 35]]]
        event = PossibleTime(3, [[0, 5], [0, 14]], 1)
        task1 = Task(1, "Title", "Description", 10, 0, datetime(2021, 11, 21, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True, 1, 'nofile')
        task2 = Task(2, "Title", "Description", 5, 0, datetime(2021, 11, 23, 0, 0), False, 1,
                            ["08:00:00", "12:00:00"], True, 1, 'nofile')
        task3 = Task(3, "Title", "Description", 5, 0, datetime(2021, 11, 24, 0, 0), False, 1,
                            ["08:00:00", "12:00:00"], True, 1, 'nofile')
        task4 = Task(4, "Title", "Description", 5, 0, datetime(2021, 11, 25, 0, 0), False, 1,
                            ["08:00:00", "12:00:00"], True, 2, 'nofile')
        self.assertTrue(overlap_check([task1, task2, task3], empty, event, date_zero))
        self.assertFalse(overlap_check([task1, task2, task3, task4], empty, event, date_zero))
        self.assertFalse(overlap_check([task1, task2, task4], empty, event, date_zero))
        self.assertTrue(overlap_check([task3, task2, task1], empty, event, date_zero))
        event = PossibleTime(3, [[0, 5], [0, 22]], 1)
        empty = [[[0, 5], [0, 25]], [[0, 40], [0, 45]], [[3, 30], [3, 35]], [[4, 20], [4, 60]]]
        task5 = Task('pay att', "Title", "Description", 6, 0, datetime(2021, 10, 19, 0, 0), False, 1,
                     ["08:00:00", "12:00:00"], True, 1, 'nofile')
        self.assertFalse(overlap_check([task5], empty, event, date_zero))


    def test_timeslot_pref(self):

        task = Task(-1, "Title", "Description", 2, 0, datetime(2021, 10, 20, 0, 0), False, 1,
                    ["00:00:00", "08:00:00"], True, 1, 'nofile')
        timeslot = 4
        self.assertEqual(1, timeslot_pref(task, timeslot, 60))
        timeslot = 20
        self.assertEqual(3, timeslot_pref(task, timeslot, 60))
        task = Task(-1, "Title", "Description", 2, 0, datetime(2021, 10, 20, 0, 0), False, 1,
                    False, True, 1, 'nofile')
        self.assertEqual(2, timeslot_pref(task, timeslot, 60))

    def test_eq(self):
        time1 = PossibleTime(3, [[2, 56], [2, 80]], 2)
        time2 = PossibleTime(3, [[2, 56], [2, 80]], 3)
        time3 = PossibleTime(4, [[2, 56], [2, 80]], 2)
        self.assertTrue(time1 == time2)
        self.assertFalse(time1 == time3)

    def test_string(self):
        time = PossibleTime(3, [[2, 56], [2, 80]], 2)
        self.assertEqual("TaskID: 3 | [[2, 56], [2, 80]] | score: 2", str(time))

    def test_calculate_score(self):
        task_list = import_task(os.path.join(dirname, 'jsonfiles/TaskListForTestingAlgo2.json'))
        day_zero = presets.day_zero
        time_interval = presets.time_interval
        presets.time_interval = 60
        presets.day_zero = "2021-10-19"
        presets.Store()
        timeslot = 22
        self.assertEqual(12, calc_score(task_list[0], timeslot))
        self.assertEqual(21, calc_score(task_list[1], timeslot))
        self.assertEqual(8, calc_score(task_list[2], timeslot))
        timeslot = 15
        self.assertEqual(7, calc_score(task_list[1], timeslot))
        self.assertEqual(6, calc_score(task_list[2], timeslot))
        presets.day_zero = day_zero
        presets.time_interval = time_interval
        presets.Store()


    def test_best_score_and_single_task(self):
        time0 = PossibleTime(0, [[0, 5], [0, 15]], 50)
        time1 = PossibleTime(1, [[0, 5], [0, 15]], 15)
        time2 = PossibleTime(1, [[1, 5], [1, 15]], 20)
        time3 = PossibleTime(2, [[2, 5], [2, 15]], 5)
        time4 = PossibleTime(2, [[3, 5], [3, 15]], 7)
        time5 = PossibleTime(2, [[4, 5], [4, 15]], 5)
        times = [time0, time1, time2, time3, time4]
        self.assertEqual(0, single_task_check(times))
        self.assertEqual(time3, best_score_check(times))
        times.append(time5)
        self.assertEqual(time3, best_score_check(times))
        times = [time1, time2, time3, time4]
        self.assertEqual(-99, single_task_check(times))
        time6 = PossibleTime(5, [[4, 5], [4, 15]], 7)
        times.append(time6)
        self.assertEqual(4, single_task_check(times))


    def test_algorithm_with_deadlines(self):
        ClearEvents()
        time_interval = presets.time_interval
        number_of_days = presets.number_of_days
        day_zero = presets.day_zero
        presets.time_interval = 60
        presets.number_of_days = 2
        presets.day_zero = "2021-10-19"
        presets.Store()
        presets.PrintPresets()
        schedule.number_of_slots = round(24 * 60 / presets.time_interval)
        schedule.Update()
        # setup for test complete
        filename = (os.path.join(dirname, 'jsonfiles/TaskListForTestingAlgo.json'))
        main(filename)
        for event in events:
            if event.Label == "Deadline1Test":
                number1 = event.ID
            if event.Label == "Deadline2":
                number2 = event.ID
            if event.Label == "Long Task":
                number3 = event.ID
        self.assertTrue(number1 in schedule.schedule[0])
        self.assertTrue(number2 in schedule.schedule[0])
        self.assertTrue(number3 in schedule.schedule[1])
        # reverse presets to old values
        presets.time_interval = time_interval
        presets.number_of_days = number_of_days
        presets.day_zero = day_zero
        presets.Store()




if __name__ == '__main__':
    unittest.main()
