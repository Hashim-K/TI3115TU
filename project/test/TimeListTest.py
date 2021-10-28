import unittest
from project.BackEnd.TimeList import TimeList


class MyTestCase(unittest.TestCase):

    def test_add_time(self):
        time_list = TimeList()
        time_list.add_time(2, 5, 2, 10)
        self.assertEqual([[[2, 5], [2, 10]]], time_list.timelist)
        time_list.add_time(3, 8, 4, 2)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 8], [4, 2]]], time_list.timelist)

    def test_add_duration(self):
        time_list = TimeList()
        time_list.add_duration(2, 5, 6)
        self.assertEqual([[[2, 5], [2, 10]]], time_list.timelist)
        time_list.add_duration(3, 90, 10)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 90], [4, 3]]], time_list.timelist)
        time_list.add_duration(3, 90, 1)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 90], [4, 3]], [[3, 90], [3, 90]]], time_list.timelist)
        time_list.add_duration(3, 90, 6)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 90], [4, 3]], [[3, 90], [3, 90]], [[3, 90], [3, 95]]], time_list.timelist)
        time_list = TimeList()
        time_list.add_duration(3, 90, 7)
        self.assertEqual([[[3, 90], [4, 0]]], time_list.timelist)


    def test_delete_time(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]], [[3, 90], [4, 3]], [[3, 90], [3, 90]], [[3, 90], [3, 95]]]
        time_list.delete_time(3, 90, 4, 3)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 90], [3, 90]], [[3, 90], [3, 95]]], time_list.times())
        time_list.delete_time(3, 90, 3, 90)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 90], [3, 95]]], time_list.times())
        time_list.delete_time(2, 5, 2, 10)
        time_list.delete_time(3, 90, 3, 96)
        self.assertEqual([[[3, 90], [3, 95]]], time_list.times())
        time_list.delete_time(3, 90, 3, 95)
        self.assertEqual([], time_list.times())


    def test_delete_duration(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]], [[3, 90], [4, 3]], [[3, 90], [3, 90]], [[3, 90], [3, 95]]]
        time_list.delete_duration(3, 90, 1)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 90], [4, 3]], [[3, 90], [3, 95]]], time_list.timelist)
        time_list.delete_duration(3, 90, 6)
        self.assertEqual([[[2, 5], [2, 10]], [[3, 90], [4, 3]]], time_list.timelist)
        time_list.delete_duration(3, 90, 10)
        self.assertEqual([[[2, 5], [2, 10]]], time_list.timelist)

    def test_str(self):
        time_list = TimeList()
        time_list.timelist = [[[2, 5], [2, 10]], [[3, 90], [4, 3]]]
        answer = '[[2, 5], [2, 10]]\n[[3, 90], [4, 3]]\n'
        self.assertEqual(answer, str(time_list))
        time_list.timelist = [[[2, 5], [2, 10]]]
        self.assertEqual('[[2, 5], [2, 10]]\n', str(time_list))

if __name__ == '__main__':
    unittest.main()
