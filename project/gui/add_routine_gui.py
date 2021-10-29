import datetime
import sys

from PyQt5.QtWidgets import QFormLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QComboBox
from PyQt5.QtWidgets import QPushButton, QApplication
from PyQt5.QtGui import QIcon

from project.BackEnd.Preset import Presets
from project.BackEnd.Routine import Routine
from project.BackEnd.Schedule import import_schedule, generate_image, Event
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
        presets = Presets()
        start = datetime.time(int(self.start_hour.currentText()), int(self.start_min.currentText()))
        end = datetime.time(int(self.end_hour.currentText()), int(self.end_min.currentText()))
        # dummydate = datetime.date(1, 1, 1)
        # start_dum = datetime.datetime.combine(dummydate, start)
        # end = datetime.datetime.combine(dummydate, end)
        # duration = end - start_dum
        # slots = divmod(duration.total_seconds(), 900)[0]

        name = self.category.currentText()


        days = self.recurrence.currentText()

        day_dict = {"Monday": [0], "Tuesday": [1], "Wednesday": [2],
                        "Thursday": [3], "Friday": [4], "Saturday": [5],
                        "Sunday": [6], "Weekdays": range(5), "Weekend": [5, 6],
                        "Every day": range(7)}

        # add event to schedule
        tl = TimeList()
        for start_day in day_dict[days]:
            start_time = int((start.hour*60+start.minute)/presets.time_interval)
            end_time = int((end.hour*60+end.minute)/presets.time_interval)
            end_day = start_day
            if end_time < start_time:
                end_day = start_day+1
            tl.add_time(start_day, start_time, end_day, end_time)
        routine = Routine(-1, name, tl)
        vars = routine.create_event()
        event = Event(vars[0], vars[1], vars[2], vars[3])
        if routine.name == "Sleep":
            tl1 = TimeList()
            tl1.add_duration()
            routine1 = Routine(-1, "Morning Routine", )
            vars1 = routine.create_event()
            event1 = Event(vars[0], vars[1], vars[2], vars[3])

        schedule = import_schedule()

        # Check overlap
        if schedule.check_overlap(event):
            # display info
            self.notify_overlap()
        else:
            routine.export_routine()
            schedule.add_event(event)
            schedule.export_schedule()
            generate_image()
            GeneralWindow.raise_event(self.ls_w, 'reload_routines')
            self.close()

    def notify_overlap(self):
        text = "The new routine overlaps with an existing routine."
        self.overlap_text.setText(text)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AddRoutineWindow([], palette.Prefs())

    sys.exit(app.exec())
