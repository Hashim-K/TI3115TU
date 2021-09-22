import sys

from Task import Task
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


class TaskCreationWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create new task")
        self.setStyleSheet("color: 'white';" +
                        "font-size: 16px;" +
                        "background-color: #303136;")

        self.initUI()
        self.show()

    def initUI(self):
        layout = QFormLayout()

        # Title
        self.title_field = QLineEdit(self)
        layout.addRow("Title", self.title_field)

        # Deadline
        self.duedate_field = QLineEdit(self)
        layout.addRow("Due date", self.duedate_field)

        # Sessions
        self.numsessions_field = QLineEdit(self)
        self.numsessions_field.setValidator(QRegExpValidator(QRegExp(r'[0-9]+')))
        layout.addRow("Number of sessions", self.numsessions_field)

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
        deadline = self.duedate_field.text()
        num_sessions = int(self.numsessions_field.text())
        description = self.description_field.text()
        priority = self.priority_dropdown.currentIndex()
        category = self.category_dropbox.currentText()
        onsameday = self.sameday_check.isChecked()
        preferredtime = self.preference_dropbox.currentText()

        new_task = Task("TaskID", name, description, "total_duration", priority, deadline,
                        "repeatable", category, "preferred", onsameday, "sessions")
        print(new_task)


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
