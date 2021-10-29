import unittest
from project.BackEnd.Category import Category, import_category, edit_category, delete_category
from project.BackEnd.Category import random_colour, find_category, get_colour, delete_all_categories
import os
import filecmp
from shutil import copyfile
from unittest.mock import patch

from project.BackEnd.Preset import Presets


class MyTestCase(unittest.TestCase):

    def test_string(self):
        colour = random_colour()
        category = Category(1, "Name", colour, 'nofile')
        self.assertEqual(f"Category: \"Name\" (1): {colour}.\n", str(category))

    def test_export(self):
        category = Category(1, 'Example', "#87edca", 'nofile')
        if os.path.exists('jsonfiles/FileForExportTestingCategories.json'):
            os.remove('jsonfiles/FileForExportTestingCategories.json')
        category.export_category('jsonfiles/FileForExportTestingCategories.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingCategories.json',
                                    'jsonfiles/FileForTestingCategories.json'))

    def test_import(self):
        category = Category(1, 'Example', "#87edca", 'nofile')
        self.assertEqual(category.title, import_category('jsonfiles/FileForTestingCategories.json')[0].title)
        self.assertEqual(category.colour, import_category('jsonfiles/FileForTestingCategories.json')[0].colour)
        self.assertEqual(category.category_id, import_category('jsonfiles/FileForTestingCategories.json')[0].category_id)

    def test_delete_and_export(self):
        delete_category('jsonfiles/FileForTestingCategories.json', 'nofile',1)
        with open('jsonfiles/FileForTestingCategories.json') as file:
            self.assertEqual('[]', file.read())
        category = Category(1, 'Example', "#87edca", 'nofile')
        category.export_category('jsonfiles/FileForTestingCategories.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingCategories.json',
                                    'jsonfiles/FileForTestingCategories.json'))

    def test_empty_file(self):
        file = open("jsonfiles/empty.json", "w")
        file.close()
        category = Category(1, 'Example', "#87edca", 'nofile')
        category.export_category('jsonfiles/empty.json')
        self.assertTrue(filecmp.cmp("jsonfiles/empty.json",
                                    'jsonfiles/FileForTestingCategories.json'))

    def test_ID(self):
        presets = Presets()
        presets.task_path='jsonfiles/TestingCategoriesID.json'
        presets.Store()
        category = Category(-1, 'Example', "#87edca", 'jsonfiles/TestingCategoriesID.json')
        self.assertEqual(5, category.category_id)
        presets.task_path='jsonfiles/TestIDempty.json'
        presets.Store()
        category = Category(-1, 'Example', "#87edca", 'jsonfiles/TestIDempty.json')
        self.assertEqual(1, category.category_id)
        presets.task_path='jsonfiles/nofile.json'
        presets.Store()
        category = Category(-1, 'Example', "#87edca", 'nofile.json')
        self.assertEqual(2, category.category_id)
        presets.update()

    def test_find_category(self):
        found = find_category('jsonfiles/TestingCategoriesID.json', 4)
        category = Category(4, 'Example', "#87edca", 'nofile')
        self.assertEqual(category.category_id, found.category_id)
        self.assertEqual(category.title, found.title)
        self.assertEqual("Colour", found.colour)
        self.assertEqual(find_category('jsonfiles/TestingCategoriesID.json', 5), None)

    def test_get_colour(self):
        colour = get_colour('jsonfiles/TestingCategoriesID.json', 4)
        self.assertEqual(colour, "Colour")
        colour = get_colour('jsonfiles/TestingCategoriesID.json', 3)
        self.assertEqual(colour, "#87edca")
        colour = get_colour('jsonfiles/TestingCategoriesID.json', 5)
        self.assertEqual(colour, None)

    def test_delete_all_categories(self):
        copyfile('jsonfiles/TestingCategoriesID.json', 'jsonfiles/copy_file_3.json')
        delete_all_categories('jsonfiles/copy_file_3.json', 'nofile')
        self.assertTrue(filecmp.cmp('jsonfiles/copy_file_3.json', 'jsonfiles/TestIDempty.json'))

    def test_edit_category(self):
        edit_category("jsonfiles/TestingCategoriesID.json", 4, "new name", "new colour")
        self.assertTrue(filecmp.cmp("jsonfiles/TestingCategoriesID.json", 'jsonfiles/TestingCategoriesIDCopyForEditing.json'))
        edit_category("jsonfiles/TestingCategoriesID.json", 4, "Example", "Colour")

@patch('builtins.print')
def test_no_file_found(mock_print):
    import_category('No file')
    mock_print.assert_called_with('File does not exist')
    delete_category('nofile', 'nofile', 3)
    mock_print.assert_called_with('File does not exist')
    edit_category('nofile', 3, 'hi', 'bye')
    mock_print.assert_called_with('File does not exist')

if __name__ == '__main__':
    unittest.main()
