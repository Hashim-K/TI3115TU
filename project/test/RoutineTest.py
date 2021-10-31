import unittest
from project.BackEnd.Routine import Routine, import_routine, find_routine, delete_routine
from project.BackEnd.Routine import delete_times, delete_all_routines
from project.BackEnd.TimeList import TimeList
import os
import filecmp
from shutil import copyfile
from unittest.mock import patch
from project.BackEnd.Preset import Presets


class MyTestCase(unittest.TestCase):

    def test_string(self):
        presets = Presets()
        presets.routine_path = 'nofile'
        presets.Store()
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        routine = Routine(1, 'Name', time_list)
        answer = "routine \"Name\" (1):\n[[2, 5], [2, 10]]\n"
        self.assertEqual(answer, str(routine))
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, 'Name', time_list)
        answer = "routine \"Name\" (1):\n[[2, 5], [2, 10]]\n[[3, 10], [4, 28]]\n"
        self.assertEqual(answer, str(routine))
        presets.update()

    def test_export_routine(self):
        presets = Presets()
        presets.routine_path = 'jsonfiles/FileForTestingExportRoutines.json'
        presets.Store()
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list)
        if os.path.exists('jsonfiles/FileForTestingExportRoutines.json'):
            os.remove('jsonfiles/FileForTestingExportRoutines.json')
        routine.export_routine()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/FileForTestingExportRoutines.json'))
        presets.update()

    def test_import(self):
        presets = Presets()
        presets.routine_path = 'jsonfiles/FileForTestingRoutines.json'
        presets.Store()
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list)
        self.assertEqual(routine.routine_id, import_routine()[0].routine_id)
        self.assertEqual(routine.timeslots.times(), import_routine()[0].timeslots.times())
        self.assertEqual(routine.name, import_routine()[0].name)
        presets.update()

    def test_delete_and_export(self):
        presets = Presets()
        presets.routine_path = 'jsonfiles/FileForTestingRoutines.json'
        presets.Store()
        delete_routine(1)
        with open('jsonfiles/FileForTestingRoutines.json') as file:
            self.assertEqual('[]', file.read())
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list)
        routine.export_routine()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/FileForTestingExportRoutines.json'))
        presets.update()

    def test_empty_file(self):
        presets = Presets()
        presets.routine_path = "jsonfiles/empty.json"
        presets.Store()
        file = open("jsonfiles/empty.json", "w")
        file.close()
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list)
        routine.export_routine()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/empty.json'))
        presets.update()

    def test_ID(self):
        presets = Presets()
        presets.routine_path = 'jsonfiles/FileForTestingRoutinesID.json'
        presets.Store()
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(-1, "Example", time_list)
        self.assertEqual(5, routine.routine_id)
        presets.routine_path = 'jsonfiles/TestIDempty.json'
        presets.Store()
        routine = Routine(-1, "Example", time_list, )
        self.assertEqual(0, routine.routine_id)
        presets.routine_path = 'nofile'
        presets.Store()
        routine = Routine(-1, "Example", time_list)
        self.assertEqual(1, routine.routine_id)
        presets.update()

    def test_find_routine(self):
        presets = Presets()
        presets.routine_path = 'jsonfiles/FileForTestingRoutinesID.json'
        presets.Store()
        found = find_routine(4)
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(4, "Example2", time_list)
        self.assertEqual(routine.routine_id, found.routine_id)
        self.assertEqual(routine.name, found.name)
        self.assertEqual(found.timeslots.times(), routine.timeslots.times())
        found = find_routine(6)
        self.assertEqual(None, found)
        presets.update()


    def test_delete_all_routines(self):
        copyfile('jsonfiles/FileForTestingRoutinesID.json', 'jsonfiles/copy_file_4.json')
        presets = Presets()
        presets.routine_path = 'jsonfiles/copy_file_4.json'
        presets.Store()
        delete_all_routines()
        self.assertTrue(filecmp.cmp('jsonfiles/copy_file_4.json', 'jsonfiles/TestIDempty.json'))
        presets.update()

    def test_delete_times(self):
        presets = Presets()
        presets.routine_path = 'jsonfiles/FileForTestingRoutines.json'
        presets.Store()
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        delete_times(1, time_list.times())
        self.assertTrue(filecmp.cmp('jsonfiles/FileForTestingRoutines.json',
                                    'jsonfiles/FileForTestingRoutinesDeleteTimes.json'))
        os.remove('jsonfiles/FileForTestingRoutines.json')
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]]]
        time_list.add_time(3, 10, 4, 28)
        routine = Routine(1, "Example", time_list)
        routine.export_routine()
        presets.update()

@patch('builtins.print')
def test_no_file_found(mock_print):
    presets = Presets()
    presets.routine_path = 'nofile'
    presets.Store()
    import_routine()
    mock_print.assert_called_with('File does not exist')
    delete_routine(3)
    mock_print.assert_called_with('File does not exist')
    presets.update()



if __name__ == '__main__':
    unittest.main()
