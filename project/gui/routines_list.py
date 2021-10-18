from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5 import QtCore

from project.BackEnd import Schedule, General


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
        for category in Schedule.events:
            for occurrence in category.Occurrences:
                # make routine item
                name = category.Label
                day = occurrence[0][0]
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day = days[day]
                start_time = occurrence[0][1]
                start_time = General.Slot2Time(start_time, 5)
                end_time = occurrence[1][1]
                end_time = General.Slot2Time(end_time, 5)
                item = RoutineItem(name, day, start_time, end_time, self.ls_w, self.prefs)

                self.addItem(item)

                item_widget = item.generate_widget()
                self.setItemWidget(item, item_widget)

    def make_item(self, name, start_time, end_time):
        '''Makes a TimeItem and puts it in the list.'''
        time_list_item = RoutineItem([name, start_time, end_time], self.ls_w, self.prefs)
        time_list_item_widget = time_list_item.generate_widget()

        self.addItem(time_list_item)
        self.setItemWidget(time_list_item, time_list_item_widget)

    def export_time_list(self):
        pass
        

class RoutineItem(QListWidgetItem):
    def __init__(self, name, day, start_time, end_time, window_list, prefs):
        super().__init__()
        self.prefs = prefs
        self.ls_w = window_list

        self.name = name
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

        # UI
        self.setSizeHint(QtCore.QSize(200,75))  # Size hint for Items
        
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
        li_day = QLabel(f'{self.day}')
        li_day.setStyleSheet(self.prefs.style_sheets['text_tight'])
        li_times = QLabel(f'<b>{self.start_time}</b> - <b>{self.end_time}</b>')
        li_times.setStyleSheet(self.prefs.style_sheets['text_tight'])

        layout.addWidget(li_name)
        layout.addWidget(li_day)
        layout.addWidget(li_times)

        return widget
