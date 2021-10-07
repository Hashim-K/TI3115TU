import sys

import palette
from gui.general_window_gui import GeneralWindow
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QDateEdit, QVBoxLayout,\
    QStackedWidget, QListWidgetItem, QLabel, QSlider, QComboBox, QCheckBox, QPushButton,\
    QApplication, QStyleFactory
from PyQt5.QtCore import QRegExp, Qt, QDate, QSize
from PyQt5.QtGui import QRegExpValidator

class SetUpWindow(GeneralWindow):

    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):

        layout = QVBoxLayout()
        self.setStyleSheet(palette.Prefs.style_sheets["general_window"])

        # create stack items
        self.google_layout = QWidget()
        self.set_times_layout = QWidget()

        # initialize first page of stack
        self.google_ui()

        # create stack and add items
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.google_layout)
        self.Stack.addWidget(self.set_times_layout)

        # add stack to layout
        layout.addWidget(self.Stack)
        self.setLayout(layout)

    def google_ui(self):
        self.setWindowTitle("Generate my schedule (1/3)")
        layout1 = QVBoxLayout()

        question_text = QLabel("Do you want to import your Google calendar?")
        question_text.setStyleSheet(palette.Prefs.style_sheets['text_title'])
        layout1.addWidget(question_text)

        self.login_button = QPushButton("Log in")
        self.login_button.setStyleSheet(palette.Prefs.style_sheets['button_priority'])
        layout1.addWidget(self.login_button)

        self.skip_button = QPushButton("Skip")
        self.skip_button.setStyleSheet(palette.Prefs.style_sheets['button_low_priority'])
        self.skip_button.clicked.connect(self.set_times_ui)
        layout1.addWidget(self.skip_button)

        self.google_layout.setLayout(layout1)

    def set_times_ui(self):
        self.setWindowTitle("Generate my schedule (2/3)")

        layout2 = QVBoxLayout()

        question2_text = QLabel("Which times would you like to set as unavailable?")
        question2_text.setStyleSheet(palette.Prefs.style_sheets['text_title'])
        layout2.addWidget(question2_text)

        self.set_times_layout.setLayout(layout2)
        self.Stack.setCurrentIndex(1)


class TimeItem(QListWidgetItem):
    def __init__(self, task, window_list, prefs):
        super().__init__()
        self.task = task
        self.prefs = prefs
        self.ls_w = window_list

        # UI
        self.setSizeHint(QSize(200,75))  # Size hint for Items
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SetUpWindow([], '')

    sys.exit(app.exec())
