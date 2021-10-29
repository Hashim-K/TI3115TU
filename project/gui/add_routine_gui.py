import datetime
import sys

from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QDateEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QSlider, QComboBox, QCheckBox, QTimeEdit
from PyQt5.QtWidgets import QPushButton, QApplication, QStyleFactory
from PyQt5.QtCore import QRegExp, Qt, QDate
from PyQt5.QtGui import QRegExpValidator, QIcon

from project.BackEnd import Task, Schedule, NewSchedule
from project.BackEnd.General import DateFormat, XDaysLater
from project.BackEnd.TimeList import TimeList
from project.gui.general_window_gui import GeneralWindow
from project.gui import palette


class AddRoutineWindow(GeneralWindow):

    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):
        # Window Styling
        self.setWindowTitle("Add Routine")
        self.setStyleSheet("color: 'white';" +
                        "font-size: 13px;" +
                        "background-color: #303136;"
                        )
        icon = QIcon(self.prefs.images['icon_add'])
        self.setWindowIcon(icon)
        self.setFixedWidth(300)

        # Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setHorizontalSpacing(50)

        # Title
        title = QLabel('Add Routine')
        title.setContentsMargins(0,10,0,10)
        title.setStyleSheet(self.prefs.style_sheets['text_title'])

        # category
        title_category = QLabel('Category')
        title_category.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        self.category = QComboBox(self)
        self.category.setStyleSheet("padding: 5px 10px;")
        categories = ["Sleep", "Lunch", "Dinner", "Other"]
        self.category.addItems(categories)

        # start time
        title_start_time = QLabel('Start Time')

        start_time_layout = QHBoxLayout()
        start_time_layout.addWidget(QLabel("Start time"))
        start_time_layout.addStretch(1)

        self.start_hour = QComboBox(self)
        self.start_hour.addItems([f'{x}' for x in range(24)])
        start_time_layout.addWidget(self.start_hour)
        start_time_layout.addWidget(QLabel('h'))
        self.start_min = QComboBox(self)
        self.start_min.addItems(['0', '15', '30', '45'])
        start_time_layout.addWidget(self.start_min)
        start_time_layout.addWidget(QLabel('m'))

        # End time
        title_end_time = QLabel("End time")
        end_time_layout = QHBoxLayout()
        end_time_layout.addWidget(QLabel("End time"))
        end_time_layout.addStretch(1)

        self.end_hour = QComboBox(self)
        self.end_hour.addItems([f'{x}' for x in range(24)])
        end_time_layout.addWidget(self.end_hour)
        end_time_layout.addWidget(QLabel('h'))
        self.end_min = QComboBox(self)
        self.end_min.addItems(['0', '15', '30', '45'])
        end_time_layout.addWidget(self.end_min)
        end_time_layout.addWidget(QLabel('m'))

        # recurrence
        title_recurrence = QLabel('Recurrence')
        title_recurrence.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        self.recurrence = QComboBox(self)
        self.recurrence.setStyleSheet("padding: 5px 10px;")
        recurrences = ["Every day", 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',\
                       "Weekdays", "Weekend"]
        self.recurrence.addItems(recurrences)

        # add button
        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        self.add_button.clicked.connect(self.add_routine)

        # Overlap text
        self.overlap_text = QLabel()
        self.overlap_text.setWordWrap(True)

        # add widgets to layout
        form_layout.addRow(title)
        form_layout.addRow(title_category, self.category)
        form_layout.addRow(start_time_layout)
        form_layout.addRow(end_time_layout)
        form_layout.addRow(title_recurrence, self.recurrence)
        form_layout.addRow(self.overlap_text)
        form_layout.addRow(self.add_button)
        self.setLayout(form_layout)

    # def update_endtime(self):
    #     start = self.start_time.time()
    #     dur = self.duration.value()
    #     end = start.addSecs(int(dur*5*60))
    #     self.end_time.setText("End time: " + end.toString())

    def add_routine(self):

        # get all values
        # start = self.start_time.time().toString()
        # dur = self.duration.value()  # slots

        start = datetime.time(int(self.start_hour.currentText()), int(self.start_min.currentText()))
        end = datetime.time(int(self.end_hour.currentText()), int(self.end_min.currentText()))
        dummydate = datetime.date(1, 1, 1)
        start_dum = datetime.datetime.combine(dummydate, start)
        end = datetime.datetime.combine(dummydate, end)
        duration = end - start_dum
        slots = divmod(duration.total_seconds(), 900)[0]

        cat = self.category.currentText()
        id = Schedule.id_dict[cat]

        days = self.recurrence.currentText()

        day_dict = {"Monday": [0], "Tuesday": [1], "Wednesday": [2],
                        "Thursday": [3], "Friday": [4], "Saturday": [5],
                        "Sunday": [6], "Weekdays": range(5), "Weekend": [5, 6],
                        "Every day": range(7)}

        # add event to schedule
        tl = TimeList()
        for i in day_dict[days]:
            Schedule.AddOccurrence(id, i, str(start), int(slots))

        # Check overlap
        if Schedule.schedule.Update():
            # display info
            overlap_set = Schedule.schedule.Update()
            self.notify_overlap(overlap_set)
            # clear event
            Schedule.events.clear()
            Schedule.GetEvents()
        else:
            # No overlap, Update schedule
            Schedule.StoreEvents()
            Schedule.SaveImage()
            GeneralWindow.raise_event(self.ls_w, 'reload_routines')
            self.close()

    def notify_overlap(self, info):
        text = ""
        while info:
            overlap = info.pop()
            text += f"{Schedule.events[overlap[0]].Label} overlaps with {Schedule.events[overlap[1]].Label} on " \
                    f"{DateFormat(XDaysLater(Schedule.presets.day_zero, overlap[2]))}.\n"
        print(text)
        self.overlap_text.setText(text)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AddRoutineWindow([], palette.Prefs())

    sys.exit(app.exec())
