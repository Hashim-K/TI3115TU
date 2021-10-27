import unittest
from project.BackEnd.Category import Category, import_category, edit_category, delete_category
from project.BackEnd.Category import random_colour, find_category, get_colour, delete_all_categories
import os
import filecmp


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
        delete_category('jsonfiles/FileForTestingCategories.json', 1)
        with open('jsonfiles/FileForTestingCategories.json') as file:
            self.assertEqual('[]', file.read())
        category = Category(1, 'Example', "#87edca", 'nofile')
        category.export_category('jsonfiles/FileForExportTestingCategories.json')
        self.assertTrue(filecmp.cmp('jsonfiles/FileForExportTestingCategories.json',
                                    'jsonfiles/FileForTestingCategories.json'))

if __name__ == '__main__':
    unittest.main()
