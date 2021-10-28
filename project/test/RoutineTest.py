import unittest
from project.BackEnd.Routine import Routine, import_routine, find_routine, delete_routine
from project.BackEnd.Routine import delete_times, delete_all_routines
from project.BackEnd.TimeList import TimeList
import os
import filecmp
from shutil import copyfile
from unittest.mock import patch


class MyTestCase(unittest.TestCase):

    def test_string(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        routine = Routine(1, 'Name', time_list, 'nofile')
        answer = "routine \"Name\" (1):\n[[2, 5], [2, 10]]\n"
        self.assertEqual(answer, str(routine))
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, 'Name', time_list, 'nofile')
        answer = "routine \"Name\" (1):\n[[2, 5], [2, 10]]\n[[3, 10], [4, 28]]\n"
        self.assertEqual(answer, str(routine))

    def test_export_routine(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list, 'nofile')
        if os.path.exists('jsonfiles/FileForTestingExportRoutines.json'):
            os.remove('jsonfiles/FileForTestingExportRoutines.json')
        routine.export_routine('jsonfiles/FileForTestingExportRoutines.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/FileForTestingExportRoutines.json'))

    def test_import(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list, 'nofile')
        self.assertEqual(routine.routine_id, import_routine('jsonfiles/FileForTestingRoutines.json')[0].routine_id)
        self.assertEqual(routine.timeslots.times(), import_routine('jsonfiles/FileForTestingRoutines.json')[0].timeslots.times())
        self.assertEqual(routine.name, import_routine('jsonfiles/FileForTestingRoutines.json')[0].name)

    def test_delete_and_export(self):
        delete_routine('jsonfiles/FileForTestingRoutines.json', 1)
        with open('jsonfiles/FileForTestingRoutines.json') as file:
            self.assertEqual('[]', file.read())
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list, 'nofile')
        routine.export_routine('jsonfiles/FileForTestingRoutines.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/FileForTestingExportRoutines.json'))

    def test_empty_file(self):
        file = open("jsonfiles/empty.json", "w")
        file.close()
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list, 'nofile')
        routine.export_routine("jsonfiles/empty.json")
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/empty.json'))

    def test_ID(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(-1, "Example", time_list, 'jsonfiles/FileForTestingRoutinesID.json')
        self.assertEqual(5, routine.routine_id)
        routine = Routine(-1, "Example", time_list, 'jsonfiles/TestIDempty.json')
        self.assertEqual(0, routine.routine_id)
        routine = Routine(-1, "Example", time_list, 'nofile')
        self.assertEqual(1, routine.routine_id)

    def test_find_routine(self):
        found = find_routine('jsonfiles/FileForTestingRoutinesID.json', 4)
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(4, "Example2", time_list, 'nofile')
        self.assertEqual(routine.routine_id, found.routine_id)
        self.assertEqual(routine.name, found.name)
        self.assertEqual(found.timeslots.times(), routine.timeslots.times())
        found = find_routine('jsonfiles/FileForTestingRoutinesID.json', 6)
        self.assertEqual(None, found)


    def test_delete_all_routines(self):
        copyfile('jsonfiles/FileForTestingRoutinesID.json', 'jsonfiles/copy_file_4.json')
        delete_all_routines('jsonfiles/copy_file_4.json')
        self.assertTrue(filecmp.cmp('jsonfiles/copy_file_4.json', 'jsonfiles/TestIDempty.json'))

    def test_delete_times(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        delete_times('jsonfiles/FileForTestingRoutines.json', 1, time_list.times())
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/FileForTestingRoutinesDeleteTimes.json'))
        os.remove('jsonfiles/FileForTestingRoutines.json')
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list, 'nofile')
        routine.export_routine('jsonfiles/FileForTestingRoutines.json')

@patch('builtins.print')
def test_no_file_found(mock_print):
    import_routine('nofile')
    mock_print.assert_called_with('File does not exist')
    delete_routine('no file', 3)
    mock_print.assert_called_with('File does not exist')



if __name__ == '__main__':
    unittest.main()
