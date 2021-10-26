import sys
import datetime

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QDateEdit, QVBoxLayout, QHBoxLayout, QTimeEdit
from PyQt5.QtWidgets import QLabel, QSlider, QComboBox, QCheckBox, QPushButton
from PyQt5.QtCore import QRegExp, Qt, QDate, QTime
from PyQt5.QtGui import QRegExpValidator, QIcon

from project.BackEnd import Task, Category
from project.gui.general_window_gui import GeneralWindow
import os
dirname = os.path.dirname(__file__)

class TaskCreationWindow(GeneralWindow):

    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):
        # Window Styling
        self.setWindowTitle("Create new task")
        self.setStyleSheet("color: 'white';" +
                        "font-size: 13px;" +
                        "background-color: #303136;"
                        )
        icon = QIcon(self.prefs.images['icon_add'])
        self.setWindowIcon(icon)

        # Layout
        main_layout = QVBoxLayout()

        top_layout = QFormLayout()
        top_layout.setSpacing(15)

        bottom_layout = QHBoxLayout()

        # Title
        self.title_field = QLineEdit(self)
        self.title_field.setStyleSheet(self.prefs.style_sheets['fill_line'])
        top_layout.addRow("Title", self.title_field)
        self.title_field.setMaxLength(30)

        # Deadline
        self.datepicker = QDateEdit(calendarPopup=True)
        # self.datepicker.setStyleSheet("padding: 5px 10px;") > Breaks UI
        self.datepicker.setMinimumDate(QDate.currentDate())
        self.datepicker.setMaximumDate(QDate.currentDate().addDays(7))
        top_layout.addRow("Deadline", self.datepicker)

        # Sessions
        self.numsessions_field = QLineEdit(self)
        self.numsessions_field.setStyleSheet(self.prefs.style_sheets['fill_line'])
        self.numsessions_field.setText("1")
        self.numsessions_field.setValidator(QRegExpValidator(QRegExp(r'[1-9]')))
        top_layout.addRow("Number of sessions", self.numsessions_field)

        # Duration
        self.duration_label = QLabel("15 minutes", self)

        self.sessionduration_slider = QSlider(Qt.Horizontal, self)
        self.sessionduration_slider.setMinimum(1)
        self.sessionduration_slider.setMaximum(16)
        self.sessionduration_slider.valueChanged.connect(self.update_duration)

        top_layout.addRow(QLabel("Session duration"), self.duration_label)
        top_layout.addRow(self.sessionduration_slider)

        # Description
        self.description_field = QLineEdit(self)
        self.description_field.setStyleSheet(self.prefs.style_sheets['fill_line'])
        self.description_field.setMaxLength(200)
        top_layout.addRow(QLabel("Description"))
        top_layout.addRow(self.description_field)
        # self.description_field = QTextEdit(self)
        # layout.addRow(QLabel("Description"))
        # layout.addRow(self.description_field)

        # Priority
        self.priority_dropdown = QComboBox(self)
        self.priority_dropdown.setStyleSheet("padding: 5px 10px;")
        self.priority_dropdown.addItems([
            "None", "1 (highest)", "2", "3", "4", "5 (lowest)"])
        top_layout.addRow("Priority", self.priority_dropdown)

        # Category
        self.category_dropbox = QComboBox(self)
        self.category_dropbox.setStyleSheet("padding: 5px 10px;")
        self.category_dropbox.addItem("No category", 0)
        self.update_categories_dropdown()
        # categories = ["category 1", "category 2"]
        # self.category_dropbox.addItems(categories)
        top_layout.addRow("Category", self.category_dropbox)

        # Preference
        self.preference_check = QCheckBox(self)
        self.preference_check.setChecked(True)
        top_layout.addRow("Preferred time", self.preference_check)

        # self.preference_start = QTimeEdit()
        # self.preference_end = QTimeEdit()
        # top_layout.addRow("Start time", self.preference_start)
        # top_layout.addRow("End time", self.preference_end)

        preference_start = QHBoxLayout()
        preference_start.addWidget(QLabel("Start time"))
        preference_start.addStretch(1)

        self.start_hour = QComboBox(self)
        self.start_hour.addItems([f'{x}' for x in range(24)])
        preference_start.addWidget(self.start_hour)
        preference_start.addWidget(QLabel('h'))
        self.start_min = QComboBox(self)
        self.start_min.addItems(['0', '15', '30', '45'])
        preference_start.addWidget(self.start_min)
        preference_start.addWidget(QLabel('m'))

        preference_end = QHBoxLayout()
        preference_end.addWidget(QLabel("End time"))
        preference_end.addStretch(1)

        self.end_hour = QComboBox(self)
        self.end_hour.addItems([f'{x}' for x in range(24)])
        preference_end.addWidget(self.end_hour)
        preference_end.addWidget(QLabel('h'))
        self.end_min = QComboBox(self)
        self.end_min.addItems(['0', '15', '30', '45'])
        preference_end.addWidget(self.end_min)
        preference_end.addWidget(QLabel('m'))

        top_layout.addRow(preference_start)
        top_layout.addRow(preference_end)

        # Plan on same day
        self.sameday_check = QCheckBox(self)
        top_layout.addRow("Allow multiple sessions on the same day?", self.sameday_check)

        # Repeat weekly
        self.repeat_check = QCheckBox(self)
        top_layout.addRow("Repeat this task weekly?", self.repeat_check)

        # Create button
        self.create_button = QPushButton("Create task")
        self.create_button.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        self.create_button.clicked.connect(self.create_task)
        # top_layout.addRow(self.create_button)
        bottom_layout.addWidget(self.create_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(self.prefs.style_sheets['button_low_priority_rect'])
        # top_layout.addRow(self.cancel_button)
        self.cancel_button.clicked.connect(self.close)
        bottom_layout.addWidget(self.cancel_button)

        # Layout and Size
        top_layout.setContentsMargins(0, 5, 0, 15)  # Bottom padding
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)

        self.setFixedWidth(480)

    def update_duration(self, val):
        self.duration_label.setText(str(15*val) + " minutes")

    def update_categories_dropdown(self):
        """Updates the categories dropdown under 'Preferences'"""
        categories = Category.import_category(self.prefs.directory['categories'])
        # print('clear')
        for category in categories:
            # Add To Dropdown
            self.category_dropbox.addItem(category.title, category.category_id)

    def create_task(self):
        # Creat Task
        name = self.title_field.text()
        description = self.description_field.text()
        deadline = self.datepicker.date()
        deadline = deadline.toPyDate()
        num_sessions = self.numsessions_field.text()
        num_sessions = int(num_sessions)
        session_duration = self.sessionduration_slider.value()
        session_duration = int(session_duration)
        priority = self.priority_dropdown.currentIndex()
        category = self.category_dropbox.currentData()
        onsameday = self.sameday_check.isChecked()
        repeat = self.repeat_check.isChecked()
        preferred_time = self.preference_check.isChecked()
        if preferred_time:
            pref_start = str(datetime.time(int(self.start_hour.currentText()), int(self.start_min.currentText())))
            pref_end = str(datetime.time(int(self.end_hour.currentText()), int(self.end_min.currentText())))
            preferred_time = (pref_start, pref_end)

        new_task = Task.Task(-1, name, description, session_duration, priority, deadline,
                        repeat, category, preferred_time, onsameday, num_sessions, self.prefs.directory['tasks'])
        print(new_task)

        # Export Task to Save File
        Task.Task.export_task(new_task, self.prefs.directory['tasks'])
        GeneralWindow.raise_event(self.ls_w, 'reload_tasks')

        # then close task creation GUI
        self.close()


# DEPRECATED STYLESHEET [now uses palette]
class Stylesheet():
    grey_button = ("*{border: 2px solid '#42464E';" +
                            "border-radius:  15px;" +
                            "background-color: '#42464E';" +
                            "font-size: 16px;" +
                            "color: 'white';" +
                            "padding: 5px 0px;" +
                            "margin: 0px 0px;}" +
                            "*:hover{background: 'db0000'; color: 'white';}")
    blue_button = ("*{border: 2px solid '#404EED';" +
                            "border-radius:  15px;" +
                            "background-color: '#404EED';" +
                            "font-size: 16px;" +
                            "color: 'white';" +
                            "padding: 5px 0px;" +
                            "margin: 0px 0px;}" +
                            "*:hover{background: 'db0000'; color: 'white';}")

# Below code is just for testing
# def window():
#     app = QApplication(sys.argv)
#     win = TaskCreationWindow([], '')

#     sys.exit(app.exec())

# window()
