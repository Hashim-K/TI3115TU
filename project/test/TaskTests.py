import unittest
from project.BackEnd.Task import Task, import_task, delete_task, find_task, delete_session
import filecmp
from datetime import date, datetime
import os
from project.BackEnd import Schedule
from unittest.mock import patch

class MyTestCase(unittest.TestCase):
    def test_initialising(self):
        task = Task(-1, 'Netflix', 'Watching a series', 60, 3, "2021-10-05",
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
        task = Task(-1, "Title", "Description", 5, 0, "2021-10-08", False, "category 1", "Morning (8:00-12:00)", True, 1,
                    'nofile')
        self.assertEqual(
            f"Task \"Title\" ({task.taskID}): Description.\nDeadline: 2021-10-08, number of sessions: 1, session duration: 5",
            str(task))

    def test_export(self):
        task = Task(-1, "Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        task.taskID = 1
        if os.path.exists('jsonfiles/FileForExportTesting.json'):
            os.remove('jsonfiles/FileForExportTesting.json')
        task.export_task('jsonfiles/FileForExportTesting.json')
        self.assertTrue(
            filecmp.cmp('jsonfiles/FileForTestingOne.json', 'jsonfiles/FileForExportTesting.json', shallow=False))

    def test_import(self):
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
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
        task = Task(-1, "Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        task.taskID = 1
        task.export_task('jsonfiles/FileForTestingOne.json')
        self.assertTrue(
            filecmp.cmp('jsonfiles/FileForTestingOne.json', 'jsonfiles/FileForExportTesting.json', shallow=False))

    def test_empty_file(self):
        file = open("jsonfiles/empty.json", "w")
        file.close()
        task = Task(-1, "Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        task.taskID = 1
        task.export_task("jsonfiles/empty.json")
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingOne.json', "jsonfiles/empty.json", shallow=False))

    def test_correct_taskID(self):
        try:
            highest_id = Schedule.events[-1].ID
        except IndexError:
            highest_id = 0
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'jsonfiles/TestID.json')
        self.assertEqual(9, task.taskID)
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'jsonfiles/testIDempty.json')
        self.assertEqual(task.taskID, highest_id + 1)
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1",
                    "Morning (8:00-12:00)", True, 1, 'nofile')
        self.assertEqual(task.taskID, highest_id + 2)

    def test_find_task(self):
        task_found = find_task('jsonfiles/save_file_test.json', 3)
        task = Task(3, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, "category 1", "Morning (8:00-12:00)", True,
                    1, 'nofile')
        self.assertEqual(task_found.taskID, task.taskID)
        self.assertEqual(task_found.name, task.name)
        self.assertEqual(task_found.description, task.description)
        self.assertEqual(task_found.priority, task.priority)
        self.assertEqual(task_found.duration, task.duration)
        self.assertEqual(task_found.deadline, task.deadline)
        self.assertEqual(task_found.plan_on_same, task.plan_on_same)
        self.assertEqual(task_found.category, task.category)
        self.assertEqual(task_found.preferred, task.preferred)
        self.assertEqual(task_found.session, task.session)
        self.assertEqual(task_found.repeatable, task.repeatable)
        self.assertEqual(find_task('jsonfiles/save_file_test.json', 5), None)

    def test_delete_session(self):
        task = Task(1, "Title", "Description", 5, 0, date(2021, 10, 8), False, "category 1",
                    "Morning (8:00-12:00)", True, 2, 'nofile')
        task.export_task('jsonfiles/FileForTestingDeleteSession.json')
        delete_session('jsonfiles/FileForTestingDeleteSession.json', 1)
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingDeleteSession.json', 'jsonfiles/FileForTestingOne.json', shallow=False))
        delete_session('jsonfiles/FileForTestingDeleteSession.json', 1)
        with open('jsonfiles/FileForTestingDeleteSession.json') as file:
            self.assertEqual('[]', file.read())



@patch('builtins.print')
def test_no_file_to_import(mock_print):
    import_task('NotExistingFile.json')
    mock_print.assert_called_with('File does not exist')
    delete_task('NotExistingFile.json', 1)
    mock_print.assert_called_with('File does not exist')
    delete_session('NotExistingFile.json', 1)
    mock_print.assert_called_with('File does not exist')

@patch('builtins.print')
def test_no_found_task(mock_print):
    find_task('jsonfiles/save_file_test.json', 5)
    mock_print.assert_called_with('Task: Task not Found')


if __name__ == '__main__':
    unittest.main()
