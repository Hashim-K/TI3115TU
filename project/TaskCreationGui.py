import sys

from Task import Task
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator


class TaskCreationWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create new task")
        self.setStyleSheet("color: 'white';" +
                        "font-size: 13px;" +
                        "background-color: #303136;")

        self.initUI()
        self.show()

    def initUI(self):
        layout = QFormLayout()
        layout.setSpacing(15)

        # Title
        self.title_field = QLineEdit(self)
        layout.addRow("Title", self.title_field)

        # Deadline
        self.duedate_field = QLineEdit(self)
        layout.addRow("Due date", self.duedate_field)
        # self.datepicker = QCalendarWidget(self)
        # layout.addRow(self.datepicker)

        # Sessions
        self.numsessions_field = QLineEdit(self)
        self.numsessions_field.setText("1")
        self.numsessions_field.setValidator(QRegExpValidator(QRegExp(r'[0-9]+')))
        layout.addRow("Number of sessions", self.numsessions_field)

        self.duration_label = QLabel("5 minutes", self)

        self.sessionduration_slider = QSlider(Qt.Horizontal, self)
        self.sessionduration_slider.setMinimum(5)
        self.sessionduration_slider.setMaximum(240)
        self.sessionduration_slider.setSingleStep(5)
        self.sessionduration_slider.valueChanged.connect(self.update_duration)

        layout.addRow(QLabel("Session duration"), self.duration_label)
        layout.addRow(self.sessionduration_slider)

        # Description
        self.description_field = QLineEdit(self)
        layout.addRow(QLabel("Description"))
        layout.addRow(self.description_field)

        # Priority
        self.priority_dropdown = QComboBox(self)
        self.priority_dropdown.addItems([
            "None", "1 (highest)", "2", "3", "4", "5 (lowest)"])
        layout.addRow("Priority", self.priority_dropdown)

        # Category
        self.category_dropbox = QComboBox(self)
        categories = ["category 1", "category 2"]
        self.category_dropbox.addItems(categories)
        layout.addRow("Category", self.category_dropbox)

        # Preference
        self.preference_dropbox = QComboBox(self)
        pref_times = ["Morning (8:00-12:00)",
                      "Afternoon (12:00-16:00)", "Evening (16:00-20:00)",
                      "Night (20:00-23:59)", "Ungodly hours (0:00-8:00)"]
        self.preference_dropbox.addItems(pref_times)
        layout.addRow("Preferred time", self.preference_dropbox)

        # Plan on same day
        self.sameday_check = QCheckBox(self)
        layout.addRow("Allow multiple sessions on the same day?", self.sameday_check)

        # Repeat weekly
        self.repeat_check = QCheckBox(self)
        layout.addRow("Repeat this task weekly?", self.repeat_check)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(Stylesheet.grey_button)
        layout.addRow(self.cancel_button)
        self.cancel_button.clicked.connect(self.close)

        # Create button
        self.create_button = QPushButton("Create task")
        self.create_button.setStyleSheet(Stylesheet.blue_button)
        self.create_button.clicked.connect(self.create_task)
        layout.addRow(self.create_button)

        self.setLayout(layout)

    def create_task(self):
        name = self.title_field.text()
        description = self.description_field.text()
        deadline = self.duedate_field.text()
        num_sessions = self.numsessions_field.text()
        num_sessions = int(num_sessions)
        session_duration = self.sessionduration_slider.value()
        priority = self.priority_dropdown.currentIndex()
        category = self.category_dropbox.currentText()
        onsameday = self.sameday_check.isChecked()
        repeat = self.repeat_check.isChecked()
        preferredtime = self.preference_dropbox.currentText()
        print("test")

        new_task = Task(name, description, session_duration, priority, deadline,
                        repeat, category, preferredtime, onsameday, num_sessions)
        print(new_task)

    def update_duration(self, val):
        self.duration_label.setText(str(val) + " minutes")


# will maybe move stylesheet to other file
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
def window():
    app = QApplication(sys.argv)
    win = TaskCreationWindow()

    sys.exit(app.exec())

window()
