import unittest
from unittest.mock import patch
from project.BackEnd.Task import Task, import_task, delete_task
import filecmp
from datetime import date, datetime
import os
from project.BackEnd import Schedule

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
        if os.path.exists('jsonfiles/FileForExportTesting.json'):
            os.remove('jsonfiles/FileForExportTesting.json')
        task.export_task('jsonfiles/FileForExportTesting.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingOne.json', 'jsonfiles/FileForExportTesting.json', shallow=False))

    def test_import(self):
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1", "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(task.name, import_task('jsonfiles/FileForTestingOne.json')[0].name)
        self.assertEqual(task.description, import_task('jsonfiles/FileForTestingOne.json')[0].description)
        self.assertEqual(task.duration, import_task('jsonfiles/FileForTestingOne.json')[0].duration)
        self.assertEqual(task.priority, import_task('jsonfiles/FileForTestingOne.json')[0].priority)
        self.assertEqual(task.plan_on_same, import_task('jsonfiles/FileForTestingOne.json')[0].plan_on_same)
        self.assertEqual(task.preferred, import_task('jsonfiles/FileForTestingOne.json')[0].preferred)
        self.assertEqual(task.category, import_task('jsonfiles/FileForTestingOne.json')[0].category)
        self.assertEqual(task.session, import_task('jsonfiles/FileForTestingOne.json')[0].session)
        self.assertEqual(task.deadline, import_task('jsonfiles/FileForTestingOne.json')[0].deadline)
        self.assertEqual(task.repeatable, import_task('jsonfiles/FileForTestingOne.json')[0].repeatable)

    def test_delete_and_export(self):
        delete_task('jsonfiles/FileForTestingOne.json', 1)
        with open('jsonfiles/FileForTestingOne.json') as file:
            self.assertEqual('[]', file.read())
        task = Task("Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        task.taskID = 1
        task.export_task('jsonfiles/FileForTestingOne.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingOne.json', 'jsonfiles/FileForExportTesting.json', shallow=False))

    def test_empty_file(self):
        file = open("jsonfiles/empty.json", "w")
        file.close()
        task = Task("Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        task.taskID = 1
        task.export_task("jsonfiles/empty.json")
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingOne.json', "jsonfiles/empty.json", shallow=False))

    def test_correct_taskID(self):
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'jsonfiles/TestID.json')
        self.assertEqual(9, task.taskID)
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'jsonfiles/testIDempty.json')
        self.assertEqual(task.taskID, Schedule.events[-1].ID + 1)
        task = Task("Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(task.taskID, Schedule.events[-1].ID + 2)

@patch('builtins.print')
def test_no_file_to_import(mock_print):
    import_task('NotExistingFile.json')
    mock_print.assert_called_with('File does not exist')
    delete_task('NotExistingFile.json', 1)
    mock_print.assert_called_with('File does not exist')









if __name__ == '__main__':
    unittest.main()
