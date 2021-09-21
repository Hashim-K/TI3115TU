import sys

from PyQt5.QtWidgets import *


class TaskCreationWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create new task")
        self.setStyleSheet("color: 'white';"+
                        "background-color: #303136;")

        self.initUI()
        self.show()

    def initUI(self):

        self.title_field = QLineEdit(self)
        self.duration_field = QLineEdit(self)
        self.duedate_field = QLineEdit(self)

        layout = QFormLayout()
        layout.addRow("Title", self.title_field)
        layout.addRow("Total duration", self.duration_field)
        layout.addRow("Due date", self.duedate_field)
        self.setLayout(layout)

        self.create_button = QPushButton("Create task")
        self.create_button.setStyleSheet(Stylesheet.blue_button)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(Stylesheet.grey_button)
        layout.addRow(self.cancel_button)
        layout.addRow(self.create_button)

        self.create_button.clicked.connect(self.create_task)

    def create_task(self):
        name = self.title_field.text()
        total_duration = self.duration_field.text()
        deadline = self.duedate_field.text()
        print(name, total_duration, deadline)
        # new_task = Task(name, total_duration, deadline)

# will maybe move stylesheet to other file
class Stylesheet():
    grey_button = ("*{border: 2px solid '#42464E';" +
                            "border-radius:  15px;" +
                            "background-color: '#42464E';" +
                            "font-size: 13px;" +
                            "color: 'white';" +
                            "padding: 5px 0px;" +
                            "margin: 0px 0px;}" +
                            "*:hover{background: 'db0000'; color: 'white';}")
    blue_button = ("*{border: 2px solid '#404EED';" +
                            "border-radius:  15px;" +
                            "background-color: '#404EED';" +
                            "font-size: 13px;" +
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
