import unittest
from project.BackEnd.Category import Category, import_category, edit_category, delete_category
from project.BackEnd.Category import random_color, find_category, get_color, delete_all_categories
import os
import filecmp
from shutil import copyfile
from unittest.mock import patch
from project.BackEnd.Preset import Presets



class MyTestCase(unittest.TestCase):

    def test_string(self):
        presets = Presets()
        presets.category_path = 'nofile'
        presets.Store()
        color = random_color()
        category = Category(1, "Name", color)
        self.assertEqual(f"Category: \"Name\" (1): {color}.\n", str(category))
        presets.update()

    def test_export(self):
        presets = Presets()
        presets.category_path = 'jsonfiles/FileForExportTestingCategories.json'
        presets.Store()
        category = Category(1, 'Example', "#87edca")
        if os.path.exists('jsonfiles/FileForExportTestingCategories.json'):
            os.remove('jsonfiles/FileForExportTestingCategories.json')
        category.export_category()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingCategories.json',
                                    'jsonfiles/FileForTestingCategories.json'))
        presets.update()

    def test_import(self):
        presets = Presets()
        presets.category_path = 'jsonfiles/FileForTestingCategories.json'
        presets.Store()
        category = Category(1, 'Example', "#87edca")
        self.assertEqual(category.title, import_category()[0].title)
        self.assertEqual(category.color, import_category()[0].color)
        self.assertEqual(category.category_id, import_category()[0].category_id)
        presets.update()

    def test_delete_and_export(self):
        presets = Presets()
        presets.category_path = 'jsonfiles/FileForTestingCategories.json'
        presets.task_path = 'nofile'
        presets.Store()
        delete_category(1)
        with open('jsonfiles/FileForTestingCategories.json') as file:
            self.assertEqual('[]', file.read())
        category = Category(1, 'Example', "#87edca")
        category.export_category()
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingCategories.json',
                                    'jsonfiles/FileForTestingCategories.json'))
        presets.update()

    def test_empty_file(self):
        presets = Presets()
        presets.category_path = "jsonfiles/empty.json"
        presets.Store()
        file = open("jsonfiles/empty.json", "w")
        file.close()
        category = Category(1, 'Example', "#87edca")
        category.export_category()
        self.assertTrue(filecmp.cmp("jsonfiles/empty.json",
                                    'jsonfiles/FileForTestingCategories.json'))
        presets.update()

    def test_ID(self):
        presets = Presets()
        presets.category_path = 'jsonfiles/TestingCategoriesID.json'
        presets.Store()
        category = Category(-1, 'Example', "#87edca")
        self.assertEqual(5, category.category_id)
        presets.category_path = 'jsonfiles/TestIDempty.json'
        presets.Store()
        category1 = Category(-1, 'Example', "#87edca")
        self.assertEqual(1, category1.category_id)
        presets.category_path = 'jsonfiles/nofile.json'
        presets.Store()
        category2 = Category(-1, 'Example', "#87edca")
        self.assertEqual(2, category2.category_id)
        presets.update()

    def test_find_category(self):
        presets = Presets()
        presets.category_path = 'jsonfiles/TestingCategoriesID.json'
        presets.Store()
        found = find_category(4)
        category = Category(4, 'Example', "#87edca")
        self.assertEqual(category.category_id, found.category_id)
        self.assertEqual(category.title, found.title)
        self.assertEqual("color", found.color)
        self.assertEqual(find_category(5), None)
        presets.update()

    def test_get_color(self):
        presets = Presets()
        presets.category_path = 'jsonfiles/TestingCategoriesID.json'
        presets.Store()
        color = get_color(4)
        self.assertEqual(color, "color")
        color = get_color(3)
        self.assertEqual(color, "#87edca")
        color = get_color(5)
        self.assertEqual(color, None)
        presets.update()

    def test_delete_all_categories(self):
        presets = Presets()
        presets.task_path = 'jsonfiles/FileForTestingOne.json'
        presets.category_path = 'jsonfiles/copy_file_3.json'
        presets.Store()
        copyfile('jsonfiles/TestingCategoriesID.json', 'jsonfiles/copy_file_3.json')
        delete_all_categories()
        self.assertTrue(filecmp.cmp('jsonfiles/copy_file_3.json', 'jsonfiles/TestIDempty.json'))
        presets.update()

    def test_edit_category(self):
        presets = Presets()
        presets.category_path = 'jsonfiles/TestingCategoriesIDCopyForEditing.json'
        presets.Store()
        edit_category(4, "Example", "color")
        self.assertTrue(filecmp.cmp("jsonfiles/TestingCategoriesID.json", 'jsonfiles/TestingCategoriesIDCopyForEditing.json'))
        edit_category(4, "new name", "new color")
        presets.update()

@patch('builtins.print')
def test_no_file_found(mock_print):
    presets = Presets()
    presets.category_path = "jsonfriesID.json"
    presets.Store()
    import_category()
    mock_print.assert_called_with('File does not exist')
    delete_category(3)
    mock_print.assert_called_with('File does not exist')
    edit_category(3, 'hi', 'bye')
    mock_print.assert_called_with('File does not exist')
    presets.update()

if __name__ == '__main__':
    unittest.main()
