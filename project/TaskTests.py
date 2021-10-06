import unittest
from Task import Task

class MyTestCase(unittest.TestCase):
    def test_initialising(self):
        task = Task('Netflix', 'Watching a series', 60, 3, "2021-10-05",
                    False, 'Free Time', "Morning (8:00-12:00)", True, 3)
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


if __name__ == '__main__':
    unittest.main()

Task "Title" (7): Description.
Deadline: 2021-10-08, number of sessions: 1, session duration: 5