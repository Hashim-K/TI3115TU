import json
import os.path
import random

from project.BackEnd.Preset import Presets


class Category:
    """ The category class is used to create, store and edit categories used by the software in a JSON format. """
    highest_id = 0

    def __init__(self, category_id: int, title: str, color: str):
        presets = Presets()
        if category_id != -1:  # category_id is given in the initializer
            self.category_id = category_id
        else:
            # calculating category_id from the already existing categories
            if not os.path.exists(presets.category_path) or os.stat(presets.category_path).st_size < 4:
                Category.highest_id += 1
                self.category_id = Category.highest_id
            else:
                with open(presets.category_path) as file:  # calculating category_id from an already existing JSON file with categories
                    cat_dict = json.load(file)
                    self.category_id = cat_dict[-1]['category_id'] + 1
        self.title = title
        self.color = color

    def __str__(self):
        text_description = f"Category: \"{self.title}\" ({self.category_id}): {self.color}.\n"
        return text_description

    def export_category(self):
        """ Storing category in a JSON file. """
        presets = Presets()
        entry = {
            "category_id": self.category_id,
            "title": self.title,
            "color": self.color
        }
        if not os.path.exists(presets.category_path):   # if filename does not exist create a list to fill
            data = []
        else:
            if os.stat(presets.category_path).st_size == 0:  # if filename is empty make new one
                os.remove(presets.category_path)
                data = []
            else:
                with open(presets.category_path, 'r') as file:  # if filename exists load the data
                    data = json.load(file)
        data.append(entry)
        with open(presets.category_path, 'w') as file:  # write into file
            json.dump(data, file, indent=6)


def import_category():
    """ Creates a list of all the categories in a JSON file. """
    presets = Presets()
    category_list = []
    try:
        with open(presets.category_path, 'r') as file:
            cat_dict = json.load(file)
            for category in cat_dict:
                category_list.append(Category(category['category_id'], category['title'], category['color']))
    except FileNotFoundError:
        print('File does not exist')
    return category_list


def find_category(category_id):
    """ Seeks for a task by its taskID. """
    category_list = import_category()
    for category in category_list:
        if category.category_id == category_id:
            return category
    print('Category(' + str(category_id) + ') not Found')


def get_color(category_id):
    """ Seeks for a task by its taskID. """
    category_list = import_category()
    for category in category_list:
        if category.category_id == category_id:
            return category.color
    print('Category(' + str(category_id) + ') not Found')


def delete_all_categories():
    """Deletes all tasks from a JSON file."""
    category_list = import_category()
    for category in category_list:
        delete_category(category.category_id)


def delete_category(category_id):
    """ Delete a category from a JSON file. """
    presets = Presets()
    try:
        with open(presets.category_path, 'r') as file:
            cat_dict = json.load(file)
        for i in range(len(cat_dict)):
            if cat_dict[i]['category_id'] == category_id:
                del cat_dict[i]
                break
        with open(presets.category_path, 'w') as file:
            json.dump(cat_dict, file, indent=6)
        reset_task_categories(category_id)
    except FileNotFoundError:
        print('File does not exist')


def reset_task_categories(category_id):
    presets = Presets()
    try:
        with open(presets.task_path, 'r') as file:
            task_dict = json.load(file)
        for i in range(len(task_dict)):
            if task_dict[i]['Category'] == category_id:
                task_dict[i]['Category'] = 0
        with open(presets.task_path, 'w') as file:
            json.dump(task_dict, file, indent=6)
    except FileNotFoundError:
        print('File does not exist')


def edit_category(category_id: int, title: str, color: str):
    presets = Presets()
    try:
        with open(presets.category_path, 'r') as file:
            task_dict = json.load(file)
        for i in range(len(task_dict)):
            if task_dict[i]['category_id'] == category_id:
                task_dict[i]['title'] = title
                task_dict[i]['color'] = color
        with open(presets.category_path, 'w') as file:
            json.dump(task_dict, file, indent=6)
    except FileNotFoundError:
        print('File does not exist')


def random_color():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#' + hex_number[2:]
    return hex_number
