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
        self.assertEqual(event.summary, event2.summary)
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






if __name__ == '__main__':
    unittest.main()
