import sys

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QDateEdit, QVBoxLayout, QHBoxLayout, QTimeEdit
from PyQt5.QtWidgets import QLabel, QSlider, QComboBox, QCheckBox, QPushButton
from PyQt5.QtCore import QRegExp, Qt, QDate, QTime
from PyQt5.QtGui import QRegExpValidator

from project.BackEnd import Task
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
        top_layout.addRow("Deadline", self.datepicker)

        # Sessions
        self.numsessions_field = QLineEdit(self)
        self.numsessions_field.setStyleSheet(self.prefs.style_sheets['fill_line'])
        self.numsessions_field.setText("1")
        self.numsessions_field.setValidator(QRegExpValidator(QRegExp(r'[0-9]+')))
        top_layout.addRow("Number of sessions", self.numsessions_field)

        # Duration
        self.duration_label = QLabel("5 minutes", self)

        self.sessionduration_slider = QSlider(Qt.Horizontal, self)
        self.sessionduration_slider.setMinimum(1)
        self.sessionduration_slider.setMaximum(48)
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
        categories = ["category 1", "category 2"]
        self.category_dropbox.addItems(categories)
        top_layout.addRow("Category", self.category_dropbox)

        # Preference
        top_layout.addRow(QLabel("Preferred time (0:00 to 0:00 is considered as no preference)"))

        self.preference_start = QTimeEdit()
        self.preference_end = QTimeEdit()
        top_layout.addRow("Start time", self.preference_start)
        top_layout.addRow("End time", self.preference_end)

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
        self.duration_label.setText(str(5*val) + " minutes")

    def create_task(self):
        # Creat Task
        name = self.title_field.text()
        description = self.description_field.text()
        deadline = self.datepicker.date()
        deadline = deadline.toPyDate()
        num_sessions = self.numsessions_field.text()
        num_sessions = int(num_sessions)
        session_duration = self.sessionduration_slider.value()
        session_duration = 5*int(session_duration)
        priority = self.priority_dropdown.currentIndex()
        category = self.category_dropbox.currentText()
        onsameday = self.sameday_check.isChecked()
        repeat = self.repeat_check.isChecked()
        preferredtime = (self.preference_start.time().toString(), self.preference_end.time().toString())

        new_task = Task.Task(-1, name, description, session_duration, priority, deadline,
                        repeat, category, preferredtime, onsameday, num_sessions, self.prefs.directory['tasks'])
        print(new_task)

        # Export Task to Save File
        Task.Task.export_task(new_task, os.path.join(dirname, "../save_file.json"))
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
