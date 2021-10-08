import unittest
from project.BackEnd.Task import Task, import_task, delete_task
import filecmp
from datetime import date, datetime
import os
from Schedule import Events

class MyTestCase(unittest.TestCase):
    def test_initialising(self):
        task = Task('Netflix', 'Watching a series', 60, 3, "2021-10-05",
                    False, 'Free Time', "Morning (8:00-12:00)", True, 3, 'nofile')
        self.assertEqual('Netflix', task.name)
        self.assertEqual('Watching a series', task.description)
        self.assertEqual(60, task.duration)
        self.assertEqual(3, task.priority)
        self.assertEqual("2021-10-05", task.deadline)
        self.assertEqual(False, task.repeatable)
        self.assertEqual('Free Time', task.category)
        self.assertEqual("Morning (8:00-12:00)", task.preferred)
        self.assertEqual(True, task.plan_on_same)
        self.assertEqual(3, task.session)

    def test_string(self):
        task = Task("Title", "Description", 5, 0, "2021-10-08", False, "category 1", "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(f"Task \"Title\" ({task.taskID}): Description.\nDeadline: 2021-10-08, number of sessions: 1, session duration: 5", str(task))

    def test_export(self):
        task = Task("Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True, 1, 'nofile')
        task.taskID = 1
        if os.path.exists('test/jsonfiles/FileForExportTesting.json'):
            os.remove('test/jsonfiles/FileForExportTesting.json')
        task.export_task('test/jsonfiles/FileForExportTesting.json')
        self.assertTrue(filecmp.cmp('test/jsonfiles/FileForTestingOne.json', 'test/jsonfiles/FileForExportTesting.json', shallow=False))

    def test_import(self):
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1", "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(task.name, import_task('test/jsonfiles/FileForTestingOne.json')[0].name)
        self.assertEqual(task.description, import_task('test/jsonfiles/FileForTestingOne.json')[0].description)
        self.assertEqual(task.duration, import_task('test/jsonfiles/FileForTestingOne.json')[0].duration)
        self.assertEqual(task.priority, import_task('test/jsonfiles/FileForTestingOne.json')[0].priority)
        self.assertEqual(task.plan_on_same, import_task('test/jsonfiles/FileForTestingOne.json')[0].plan_on_same)
        self.assertEqual(task.preferred, import_task('test/jsonfiles/FileForTestingOne.json')[0].preferred)
        self.assertEqual(task.category, import_task('test/jsonfiles/FileForTestingOne.json')[0].category)
        self.assertEqual(task.session, import_task('test/jsonfiles/FileForTestingOne.json')[0].session)
        self.assertEqual(task.deadline, import_task('test/jsonfiles/FileForTestingOne.json')[0].deadline)
        self.assertEqual(task.repeatable, import_task('test/jsonfiles/FileForTestingOne.json')[0].repeatable)

    def test_delete_and_export(self):
        delete_task('test/jsonfiles/FileForTestingOne.json', 1)
        with open('test/jsonfiles/FileForTestingOne.json') as file:
            self.assertEqual('[]', file.read())
        task = Task("Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        task.taskID = 1
        task.export_task('test/jsonfiles/FileForTestingOne.json')
        self.assertTrue(filecmp.cmp('test/jsonfiles/FileForTestingOne.json', 'test/jsonfiles/FileForExportTesting.json', shallow=False))

    def test_empty_file(self):
        file = open("test/jsonfiles/empty.json", "w")
        file.close()
        task = Task("Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        task.taskID = 1
        task.export_task("test/jsonfiles/empty.json")
        self.assertTrue(filecmp.cmp('test/jsonfiles/FileForTestingOne.json', "test/jsonfiles/empty.json", shallow=False))

    def test_correct_taskID(self):
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'test/jsonfiles/TestID.json')
        self.assertEqual(task.taskID, 9)
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'test/jsonfiles/testIDempty.json')
        self.assertEqual(task.taskID, highest_id = Events[-1].ID + 1)
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(task.taskID, highest_id = Events[-1].ID + 1)






if __name__ == '__main__':
    unittest.main()