import sys

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QDateEdit, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QSlider, QComboBox, QCheckBox, QTimeEdit
from PyQt5.QtWidgets import QPushButton, QApplication, QStyleFactory
from PyQt5.QtCore import QRegExp, Qt, QDate
from PyQt5.QtGui import QRegExpValidator

from project.BackEnd import Task
from project.gui.general_window_gui import GeneralWindow
from project.gui import palette


class AddRoutineWindow(GeneralWindow):

    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):
        # Window Styling
        self.setWindowTitle("Add routine")
        self.setStyleSheet("color: 'white';" +
                        "font-size: 13px;" +
                        "background-color: #303136;"
                        )

        # Layout
        layout = QFormLayout()

        # category
        self.category = QComboBox(self)
        categories = ["Sleep", "Lunch", "Dinner", "Other"]
        self.category.addItems(categories)

        # start time
        self.start_time = QTimeEdit(self)
        # self.start_time.valueChanged.connect(self.update_endtime)
        self.start_time.timeChanged.connect(self.update_endtime)

        # duration
        self.end_time = QLabel("End time", self)

        self.duration = QSlider(Qt.Horizontal, self)
        self.duration.setMinimum(1)
        self.duration.setMaximum(288)  # 24 hours
        self.duration.valueChanged.connect(self.update_endtime)

        # recurrence
        self.recurrence = QComboBox(self)
        recurrences = ["Every day", 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',\
                       "Weekdays", "Weekend"]
        self.recurrence.addItems(recurrences)

        # add button
        self.add_button = QPushButton("Add")

        # add widgets to layout
        layout.addRow("Category", self.category)
        layout.addRow("Start time", self.start_time)
        layout.addRow("Duration", self.duration)
        layout.addRow(self.end_time)
        layout.addRow("Recurrence", self.recurrence)
        layout.addRow(self.add_button)
        self.setLayout(layout)

    def update_endtime(self):
        start = self.start_time.time()
        dur = self.duration.value()
        end = start.addSecs(int(dur*5*60))
        self.end_time.setText("End time: " + end.toString())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AddRoutineWindow([], palette.Prefs())

    sys.exit(app.exec())
