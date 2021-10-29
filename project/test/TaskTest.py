import unittest
from project.BackEnd.Task import Task, import_task, delete_task, find_task, delete_session, delete_all_tasks, edit_task
import filecmp
from datetime import date, datetime
import os
#from project.BackEnd import Schedule
from unittest.mock import patch
from shutil import copyfile
from project.BackEnd.Preset import Presets

class MyTestCase(unittest.TestCase):
    def test_initialising(self):
        presets = Presets()
        presets.task_path = 'nofile'
        presets.Store()
        task = Task(-1, 'Netflix', 'Watching a series', 60, 3, "2021-10-05",
                    False, 'Free Time', ["08:00:00", "12:00:00"], True, 3)
        self.assertEqual('Netflix', task.name)
        self.assertEqual('Watching a series', task.description)
        self.assertEqual(60, task.duration)
        self.assertEqual(3, task.priority)
        self.assertEqual("2021-10-05", task.deadline)
        self.assertEqual(False, task.repeatable)
        self.assertEqual('Free Time', task.category)
        self.assertEqual(["08:00:00", "12:00:00"], task.preferred)
        self.assertEqual(True, task.plan_on_same)
        self.assertEqual(3, task.session)
        presets.update()

    def test_string(self):
        presets = Presets()
        presets.task_path = 'nofile'
        presets.Store()
        task = Task(-1, "Title", "Description", 5, 0, "2021-10-08", False, 1, ["08:00:00", "12:00:00"], True, 1)
        self.assertEqual(
            f"Task \"Title\" ({task.taskID}): Description.\nDeadline: 2021-10-08, number of sessions: 1, session duration: 5",
            str(task))
        presets.update()

    def test_export(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/FileForExportTesting.json'
        presets.Store()
        task = Task(-1, "Title", "Description", 5, 0, date(2021, 10, 8), False, 1, ["08:00:00", "12:00:00"], True,
                    1)
        task.taskID = 1
        if os.path.exists('jsonfiles/FileForExportTesting.json'):
            os.remove('jsonfiles/FileForExportTesting.json')
        task.export_task()
        self.assertTrue(
            filecmp.cmp('jsonfiles/FileForTestingOne.json', 'jsonfiles/FileForExportTesting.json', shallow=False))
        presets.update()

    def test_import(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/FileForTestingOne.json'
        presets.Store()
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True, 1)
        self.assertEqual(task.name, import_task()[0].name)
        self.assertEqual(task.description, import_task()[0].description)
        self.assertEqual(task.duration, import_task()[0].duration)
        self.assertEqual(task.priority, import_task()[0].priority)
        self.assertEqual(task.plan_on_same, import_task()[0].plan_on_same)
        self.assertEqual(task.preferred, import_task()[0].preferred)
        self.assertEqual(task.category, import_task()[0].category)
        self.assertEqual(task.session, import_task()[0].session)
        self.assertEqual(task.deadline, import_task()[0].deadline)
        self.assertEqual(task.repeatable, import_task()[0].repeatable)
        presets.update()

    def test_delete_and_export(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/FileForTestingOne.json'
        presets.Store()
        delete_task(1)
        with open('jsonfiles/FileForTestingOne.json') as file:
            self.assertEqual('[]', file.read())
        task = Task(-1, "Title", "Description", 5, 0, date(2021, 10, 8), False, 1, ["08:00:00", "12:00:00"], True,
                    1)
        task.taskID = 1
        task.export_task()
        self.assertTrue(
            filecmp.cmp('jsonfiles/FileForTestingOne.json', 'jsonfiles/FileForExportTesting.json', shallow=False))
        presets.update()

    def test_empty_file(self):
        presets = Presets()
        presets.task_path = "jsonfiles/empty.json"
        presets.Store()
        file = open("jsonfiles/empty.json", "w")
        file.close()
        task = Task(-1, "Title", "Description", 5, 0, date(2021, 10, 8), False, 1, ["08:00:00", "12:00:00"], True,
                    1)
        task.taskID = 1
        task.export_task()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingOne.json', "jsonfiles/empty.json", shallow=False))
        presets.update()

    def test_correct_taskID(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/TestID.json'
        presets.Store()
        highest_id = 0
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True, 1)
        self.assertEqual(9, task.taskID)
        presets.task_path = 'jsonfiles/testIDempty.json'
        presets.Store()
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True, 1)
        self.assertEqual(task.taskID, highest_id + 1)
        presets.task_path = 'nofile'
        presets.Store()
        task = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, 1,
                    ["08:00:00", "12:00:00"], True, 1)
        self.assertEqual(task.taskID, highest_id + 2)
        presets.update()

    def test_find_task(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/save_file_test.json'
        presets.Store()
        task_found = find_task(3)
        task = Task(3, "Title", "Description", 5, 0, datetime(2021, 10, 8, 0, 0), False, 1, ["08:00:00", "12:00:00"], True,
                    1)
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
        self.assertEqual(find_task(5), None)
        presets.update()

    def test_delete_session(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/FileForTestingDeleteSession.json'
        presets.Store()
        task = Task(1, "Title", "Description", 5, 0, date(2021, 10, 8), False, 1,
                    ["08:00:00", "12:00:00"], True, 2)
        task.export_task()
        delete_session(1)
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingDeleteSession.json', 'jsonfiles/FileForTestingOne.json', shallow=False))
        delete_session(1)
        with open('jsonfiles/FileForTestingDeleteSession.json') as file:
            self.assertEqual('[]', file.read())
        presets.update()

    def test_lt(self):
        presets = Presets()
        presets.task_path = 'nofile'
        presets.Store()
        task1 = Task(-1, "Title", "Description", 10, 0, datetime(2021, 10, 20, 0, 0), False, 1,
                     ["08:00:00", "12:00:00"], True, 1)
        task2 = Task(-1, "Title", "Description", 5, 0, datetime(2021, 10, 20, 0, 0), False, 1,
                     ["08:00:00", "12:00:00"], True, 1)
        task3 = Task(-1, "Title", "Description", 15, 0, datetime(2021, 10, 20, 0, 0), False, 1,
             ["08:00:00", "12:00:00"], True, 1)
        self.assertTrue(task2 < task1)
        self.assertTrue(task1 < task3)
        self.assertFalse(task3 < task2)
        presets.update()

    def test_delete_all(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/copy_file_2.json'
        presets.Store()
        copyfile('jsonfiles/FileForTestingOne.json', 'jsonfiles/copy_file_2.json')
        delete_all_tasks()
        self.assertTrue(filecmp.cmp('jsonfiles/copy_file_2.json', "jsonfiles/TestIDempty.json", shallow=False))
        presets.update()

    def test_edit_task(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/TaskListForTestingAlgo2.json'
        presets.Store()
        edit_task(2, "Edited Title", "Other task for testing", 3, 0,
                    "2021-10-20", True, 1, ["12:00:00", "16:00:00"], False, 1)
        self.assertTrue(filecmp.cmp('jsonfiles/TaskListForTestingAlgo2.json', 'jsonfiles/TestEditedFile.json'))
        edit_task(2, "Deadline2", "Other task for testing", 1, 0,
                  "2021-10-20", False, 1, ["12:00:00", "16:00:00"], False, 1)
        presets.update()

@patch('builtins.print')
def test_no_file_to_import(mock_print):
    presets = Presets()
    presets.task_path = 'nofile'
    presets.Store()
    import_task()
    mock_print.assert_called_with('File does not exist')
    delete_task(1)
    mock_print.assert_called_with('File does not exist')
    delete_session(1)
    mock_print.assert_called_with('File does not exist')
    edit_task(1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 1)
    mock_print.assert_called_with('File does not exist')
    presets.update()

@patch('builtins.print')
def test_no_found_task(mock_print):
    presets = Presets()
    presets.task_path = 'jsonfiles/save_file_test.json'
    presets.Store()
    find_task(5)
    mock_print.assert_called_with('Task: Task not Found')
    presets.update()


if __name__ == '__main__':
    unittest.main()
