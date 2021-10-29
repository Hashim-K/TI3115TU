import unittest
import os
import filecmp
from shutil import copyfile
from unittest.mock import patch
from project.BackEnd.GoogleEvent import GoogleEvent, import_google_event, find_google_event, delete_google_event, delete_all_google_events
from project.BackEnd.TimeObject import TimeObject
from project.BackEnd.Preset import Presets


class MyTestCase(unittest.TestCase):

    def test_string(self):
        presets = Presets()
        presets.google_path = 'nofile'
        presets.Store()
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end)
        answer = "google_event: \"Summary\" (1)\n" \
                 "description: Description.\n" \
                 "'start': {\n" \
                 "    'dateTime': 2021-11-02T08:45\n" \
                 "    'timeZone': +0100\n" \
                 "},\n" \
                 "'end': {\n" \
                 "    'dateTime': 2021-11-02T09:45\n" \
                 "    'timeZone': +0100\n" \
                 "}\n"
        self.assertEqual(answer, str(event))
        presets.update()

    def test_export(self):
        presets = Presets()
        presets.google_path = 'jsonfiles/FileForExportTestingGoogleEvent.json'
        presets.Store()
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end)
        if os.path.exists('jsonfiles/FileForExportTestingGoogleEvent.json'):
            os.remove('jsonfiles/FileForExportTestingGoogleEvent.json')
        event.export_google_event()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingGoogleEvent.json',
                                    'jsonfiles/FileForTestingGoogleEvents.json'))
        presets.update()

    def test_import(self):
        presets = Presets()
        presets.google_path = 'jsonfiles/FileForTestingGoogleEvents.json'
        presets.Store()
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end)
        event2 = import_google_event()[0]
        self.assertEqual(event.google_event_id, event2.google_event_id)
        self.assertEqual(event.name, event2.name)
        self.assertEqual(event.description, event2.description)
        self.assertEqual(str(event.start.dateTime), str(event2.start.dateTime))
        presets.update()

    def test_delete_and_export(self):
        presets = Presets()
        presets.google_path = 'jsonfiles/FileForTestingGoogleEvents.json'
        presets.Store()
        delete_google_event(1)
        with open('jsonfiles/FileForTestingGoogleEvents.json') as file:
            self.assertEqual('[]', file.read())
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end)
        event.export_google_event()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingGoogleEvent.json',
                                    'jsonfiles/FileForTestingGoogleEvents.json'))
        presets.update()

    def test_empty_file(self):
        presets = Presets()
        presets.google_path = 'jsonfiles/empty.json'
        presets.Store()
        file = open("jsonfiles/empty.json", "w")
        file.close()
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end)
        event.export_google_event()
        self.assertTrue(filecmp.cmp('jsonfiles/empty.json',
                                    'jsonfiles/FileForTestingGoogleEvents.json'))
        presets.update()

    def test_ID(self):
        presets = Presets()
        presets.google_path = 'jsonfiles/FileForTestingGoogleID.json'
        presets.Store()
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(-1, "Summary", "Description", start, end)
        self.assertEqual(5, event.google_event_id)
        presets.google_path = 'jsonfiles/TestIDempty.json'
        presets.Store()
        event = GoogleEvent(-1, "Summary", "Description", start, end)
        self.assertEqual(1, event.google_event_id)
        presets.google_path = 'nofile'
        presets.Store()
        event = GoogleEvent(-1, "Summary", "Description", start, end)
        self.assertEqual(2, event.google_event_id)
        presets.update()

    def test_find_event(self):
        presets = Presets()
        presets.google_path = 'jsonfiles/FileForTestingGoogleID.json'
        presets.Store()
        found = find_google_event(3)
        self.assertEqual("Summary", found.name)
        self.assertEqual("Description", found.description)
        self.assertEqual(3, found.google_event_id)
        self.assertEqual("2021-11-02T08:45", found.start.dateTime)
        found = find_google_event(2)
        self.assertEqual(None, found)
        presets.update()

    def test_delete_all(self):
        copyfile('jsonfiles/FileForTestingGoogleID.json', 'jsonfiles/copy_file_5.json')
        presets = Presets()
        presets.google_path = 'jsonfiles/copy_file_5.json'
        presets.Store()
        delete_all_google_events()
        self.assertTrue(filecmp.cmp('jsonfiles/copy_file_5.json', 'jsonfiles/TestIDempty.json'))


@patch('builtins.print')
def test_no_file_found(mock_print):
    presets = Presets()
    presets.google_path = 'nofile'
    presets.Store()
    import_google_event()
    mock_print.assert_called_with('File does not exist')
    delete_google_event(1)
    mock_print.assert_called_with('File does not exist')
    presets.update()











if __name__ == '__main__':
    unittest.main()
