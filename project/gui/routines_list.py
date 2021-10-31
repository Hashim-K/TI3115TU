from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5 import QtCore

from project.BackEnd import General, Routine
from project.BackEnd.Routine import import_routine
from project.BackEnd.Schedule import import_schedule
from project.BackEnd.TimeList import TimeList
from project.gui.general_window_gui import GeneralWindow


class RoutinesList(QListWidget):
    def __init__(self, window_list, prefs):
        super().__init__()
        # Store windows and prefs
        self.prefs = prefs
        self.ls_w = window_list     # For reloading windows

        # Initial settings
        self.setSpacing(5)
        self.setStyleSheet("border: 2px")
        self.setSortingEnabled(True)       

    def load_routinelist(self):
        routinelist = import_routine()
        for routine in routinelist:
            # make routine item
            name = routine.name
            for time in routine.timeslots.times():
                [[start_day, start_time], [end_day, end_time]] = time
                tl = TimeList()
                tl.add_time(start_day, start_time, end_day, end_time)
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                start_day = days[start_day]
                start_time = General.Slot2Time(start_time, 15)
                end_time = General.Slot2Time(end_time+1, 15)
                id = routine.routine_id
                item = RoutineItem(name, start_day, start_time, end_time, tl, id, self.ls_w, self.prefs)
                self.addItem(item)
                item_widget = item.generate_widget()
                self.setItemWidget(item, item_widget)

class RoutineItem(QListWidgetItem):
    def __init__(self, name, start_day, start_time, end_time, tl,  id, window_list, prefs):
        super().__init__()
        self.prefs = prefs
        self.ls_w = window_list

        self.name = name
        self.start_day = start_day
        self.start_time = start_time
        self.end_time = end_time
        self.tl = tl
        self.id = id

        # UI
        self.setSizeHint(QtCore.QSize(200, 75))  # Size hint for Items

    # generateWidget
    def generate_widget(self):

        # WIDGET
        widget = QWidget()
        widget.setStyleSheet(self.prefs.style_sheets['text_bubble'])

        ## Layout
        layout = QHBoxLayout()
        widget.setLayout(layout)

        # Layout Elements
        li_name = QLabel(f'<b>{self.name}</b>')
        li_name.setStyleSheet(self.prefs.style_sheets['text_tight'])
        li_day = QLabel(f'{self.start_day}')
        li_day.setStyleSheet(self.prefs.style_sheets['text_tight'])
        li_times = QLabel(f'<b>{self.start_time}</b> - <b>{self.end_time}</b>')
        li_times.setStyleSheet(self.prefs.style_sheets['text_tight'])
        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet(self.prefs.style_sheets['button_exit_rect'])
        delete_button.setFixedWidth(100)
        delete_button.clicked.connect(self.delete_routine_time)

        layout.addWidget(li_name)
        layout.addWidget(li_day)
        layout.addWidget(li_times)
        layout.addWidget(delete_button)

        return widget

    def delete_routine_time(self):
        Routine.delete_times(self.id, self.tl.times())
        schedule = import_schedule()
        schedule.delete_times("Routine", self.id, self.tl.times())
        GeneralWindow.raise_event(self.ls_w, 'reload_routines')
