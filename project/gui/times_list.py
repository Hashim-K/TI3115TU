from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5 import QtCore

class TimeList(QListWidget):
    def __init__(self, window_list, prefs):
        super().__init__()
        # Store windows and prefs
        self.prefs = prefs
        self.ls_w = window_list     # For reloading windows

        # Initial settings
        self.setSpacing(5)
        self.setStyleSheet("border: 2px")
        self.setSortingEnabled(True)       

    def export_time_list(self):
        pass
        

class TimeItem(QListWidgetItem):
    def __init__(self, item_prefs, window_list, prefs):
        super().__init__()
        self.prefs = prefs
        self.ls_w = window_list

        self.item_prefs = item_prefs
        '''
        0) Name, 1) Start Time, 2) End Time (times as datetime)
        '''

        # UI
        self.setSizeHint(QtCore.QSize(200,75))  # Size hint for Items
        
    # generateWidget
    def generate_widget(self):
        # Fields
        name = self.item_prefs[0]
        start_time = self.item_prefs[1]
        end_time = self.item_prefs[2]

        # WIDGET
        widget = QWidget()
        widget.setStyleSheet(self.prefs.style_sheets['text_bubble'])

        ## Layout
        layout = QHBoxLayout()
        widget.setLayout(layout)

        # Layout Elements
        li_name = QLabel(f'Name: <b>{name}</b>')
        li_times = QLabel(f'<b>{start_time}</b> - <b>{end_time}</b>')

        layout.addWidget(li_name)
        layout.addWidget(li_times)

        return widget