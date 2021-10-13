# DEPRECATED IMPORTS
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QFormLayout, QLabel
from project.gui import palette

# IMPORTS
from project.gui import general_window_gui


class TaskInfo(general_window_gui.GeneralWindow):
    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):
        # WINDOW
        placeholder_title = 'Doing Homework'
        placeholder_desc = "Lorem ipsum dolor sit amet, consectetur adipiscing " \
                           "elit, sed do eiusmod tempor incididunt ut labore " \
                           "et dolore magna aliqua. Ut enim ad minim veniam, " \
                           "quis nostrud exercitation ullamco laboris nisi " \
                           "ut aliquip ex ea commodo consequat."

        self.setWindowTitle(f'Task | {placeholder_title}')
        self.setFixedWidth(300)
        self.setStyleSheet(self.prefs.style_sheets['general_window'])

        icon = QIcon(self.prefs.images['icon_task_info'])
        self.setWindowIcon(icon)

        # Layout
        main_layout = QVBoxLayout()
        sub_layout = QFormLayout()
        sub_layout.setSpacing(20)

        # Main Layout Elements
            # Title
        task_title = QLabel(placeholder_title)
        task_title.setContentsMargins(10,0,0,5)
        task_title.setStyleSheet(self.prefs.style_sheets['text_title'])
        main_layout.addWidget(task_title)
            # Description
        task_desc = QLabel(placeholder_desc)
        task_desc.setWordWrap(True)
        task_desc.setStyleSheet(self.prefs.style_sheets['text_bubble'])
        main_layout.addWidget(task_desc)

        # Sub Layout Elements
        category_prompt = QLabel('Category')
        category_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        category = QLabel('a')
        category.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(category_prompt, category)

        duration_prompt = QLabel('Duration')
        duration_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        duration = QLabel('2h')
        duration.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(duration_prompt, duration)

        priority_prompt = QLabel('Priority')
        priority_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        priority = QLabel('1')
        priority.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(priority_prompt, priority)

        deadline_prompt = QLabel('Deadline')
        deadline_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        deadline = QLabel('Tomorrow')
        deadline.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(deadline_prompt, deadline)

        sub_layout.setContentsMargins(10,10,0,10)

        main_layout.addLayout(sub_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.show()

# FOR TESTING
# def window():
#     app = QApplication(sys.argv)
#     win = TaskInfo([], palette.Prefs)
#
#     sys.exit(app.exec())
#
# window()