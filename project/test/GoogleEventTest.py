import unittest
import os
import filecmp
from shutil import copyfile
from unittest.mock import patch
from project.BackEnd.GoogleEvent import GoogleEvent, import_google_event, find_google_event, delete_google_event, delete_all_google_events
from project.BackEnd.TimeObject import TimeObject


class MyTestCase(unittest.TestCase):

    def test_string(self):
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end, 'nofile')
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

    def test_export(self):
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end, 'nofile')
        if os.path.exists('jsonfiles/FileForExportTestingGoogleEvent.json'):
            os.remove('jsonfiles/FileForExportTestingGoogleEvent.json')
        event.export_google_event('jsonfiles/FileForExportTestingGoogleEvent.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingGoogleEvent.json',
                                    'jsonfiles/FileForTestingGoogleEvents.json'))

    def test_import(self):
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end, 'nofile')
        event2 = import_google_event('jsonfiles/FileForTestingGoogleEvents.json')[0]
        self.assertEqual(event.google_event_id, event2.google_event_id)
        self.assertEqual(event.name, event2.name)
        self.assertEqual(event.description, event2.description)
        self.assertEqual(str(event.start.dateTime), str(event2.start.dateTime))

    def test_delete_and_export(self):
        delete_google_event('jsonfiles/FileForTestingGoogleEvents.json', 1)
        with open('jsonfiles/FileForTestingGoogleEvents.json') as file:
            self.assertEqual('[]', file.read())
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end, 'nofile')
        event.export_google_event('jsonfiles/FileForTestingGoogleEvents.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingGoogleEvent.json',
                                    'jsonfiles/FileForTestingGoogleEvents.json'))

    def test_empty_file(self):
        file = open("jsonfiles/empty.json", "w")
        file.close()
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(1, "Summary", "Description", start, end, 'nofile')
        event.export_google_event('jsonfiles/empty.json')
        self.assertTrue(filecmp.cmp('jsonfiles/empty.json',
                                    'jsonfiles/FileForTestingGoogleEvents.json'))

    def test_ID(self):
        start = TimeObject("2021-11-01", 1, 35)
        end = TimeObject("2021-11-01", 1, 39)
        event = GoogleEvent(-1, "Summary", "Description", start, end, 'jsonfiles/FileForTestingGoogleID.json')
        self.assertEqual(5, event.google_event_id)
        event = GoogleEvent(-1, "Summary", "Description", start, end, 'jsonfiles/TestIDempty.json')
        self.assertEqual(1, event.google_event_id)
        event = GoogleEvent(-1, "Summary", "Description", start, end, 'nofile')
        self.assertEqual(2, event.google_event_id)

    def test_find_event(self):
        found = find_google_event('jsonfiles/FileForTestingGoogleID.json', 3)
        self.assertEqual("Summary", found.name)
        self.assertEqual("Description", found.description)
        self.assertEqual(3, found.google_event_id)
        self.assertEqual("2021-11-02T08:45", found.start.dateTime)
        found = find_google_event('jsonfiles/FileForTestingGoogleID.json', 2)
        self.assertEqual(None, found)

    def test_delete_all(self):
        copyfile('jsonfiles/FileForTestingGoogleID.json', 'jsonfiles/copy_file_5.json')
        delete_all_google_events('jsonfiles/copy_file_5.json')
        self.assertTrue(filecmp.cmp('jsonfiles/copy_file_5.json', 'jsonfiles/TestIDempty.json'))

@patch('builtins.print')
def test_no_file_found(mock_print):
    import_google_event('nofile')
    mock_print.assert_called_with('File does not exist')
    delete_google_event('nofile', 1)
    mock_print.assert_called_with('File does not exist')











if __name__ == '__main__':
    unittest.main()
