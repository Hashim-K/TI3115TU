import sys

import palette, times_list
from general_window_gui import GeneralWindow
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QFormLayout, QLineEdit, QDateEdit, QVBoxLayout,\
    QStackedWidget, QListWidgetItem, QLabel, QSlider, QComboBox, QCheckBox, QPushButton,\
    QApplication, QStyleFactory
from PyQt5.QtCore import QRegExp, Qt, QDate, QSize
from PyQt5.QtGui import QRegExpValidator, QPixmap

class SetUpWindow(GeneralWindow):

    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)
        # List of Times
        self.times_list = []

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()
        self.prefs = palette.Prefs()    # To delete
        self.setStyleSheet(self.prefs.style_sheets["general_window"])

        # Window prefs
        self.setWindowTitle('Setup')
        self.setFixedSize(500, 600)

        # create stack items
        self.google_layout = QWidget()
        self.set_times_layout = QWidget()
        self.algo_layout = QWidget()

        # initialize first page of stack
        self.google_ui()
        self.set_times_ui()

        # create stack and add items
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.google_layout)
        self.Stack.addWidget(self.set_times_layout)

        # Bottom Block
        bottom_block = QWidget()
        bottom_block.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        # Skip Button
        self.next_button = QPushButton("Skip")
        self.next_button.setStyleSheet(palette.Prefs.style_sheets['button_low_priority_rect'])
        self.next_button.clicked.connect(lambda: self.change_behaviour('next'))
        self.next_button.setFixedWidth(75)

        # Previous Button
        self.prev_button = QPushButton("Previous")
        self.prev_button.setStyleSheet(palette.Prefs.style_sheets['button_exit_rect'])
        self.prev_button.clicked.connect(lambda: self.change_behaviour('previous'))
        self.prev_button.setFixedWidth(75)
        self.prev_button.hide()

        # Bottom Block Layout
        bb_layout = QHBoxLayout()
        bb_layout.addStretch(1)
        bb_layout.addWidget(self.prev_button)
        bb_layout.addWidget(self.next_button)

        bottom_block.setLayout(bb_layout)

        # add stack to layout
        layout.addWidget(self.Stack)
        layout.addWidget(bottom_block)
        self.setLayout(layout)
    
    # Bottom Block Behaviour
    """
    The bottom block behaviour controls the appearance and functionality of the buttons
    in the bottom block depending on the stack index that we are currently on.
    """
    def change_behaviour(self, BUTTON_TYPE):
        idx = self.Stack.currentIndex()
        if BUTTON_TYPE == 'next':
            if idx == 0:
                self.Stack.setCurrentIndex(1)
                self.next_button.setText('Next')
                self.prev_button.show()
        else:
            if idx == 1:
                self.Stack.setCurrentIndex(0)
                self.next_button.setText('Skip')
                self.prev_button.hide()

    # stack 1
    def google_ui(self):
        layout1 = QVBoxLayout()

        # Prompt
        question_text = QLabel("Do you want to import your Google calendar?")
        question_text.setStyleSheet(palette.Prefs.style_sheets['text_title'])
        layout1.addWidget(question_text, alignment=Qt.AlignCenter)

        # Google Logo
        g_logo = QPixmap(self.prefs.images['img_g_logo'])
        scale = 0.7
        g_logo = g_logo.scaled(scale * g_logo.width(), scale * g_logo.height(), transformMode=Qt.SmoothTransformation)
        logo_label = QLabel()
        logo_label.setPixmap(g_logo)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet('margin-bottom: 30px; margin-top: 30px')

        layout1.addWidget(logo_label)

        # Description
        desc_text = (
            "Importing a Google calendar will allow for the scheduling " +
            "algorithm to take already scheduled events into account " +
            "when scheduling tasks."
        )
        desc = QLabel(desc_text)
        desc.setWordWrap(True)
        desc.setStyleSheet(palette.Prefs.style_sheets['text_bubble'])

        layout1.addWidget(desc)

        # Login Button
        self.login_button = QPushButton("Log in")
        self.login_button.setStyleSheet(palette.Prefs.style_sheets['button_priority_rect'])
        self.login_button.setFixedWidth(125)

        layout1.addWidget(self.login_button, alignment=Qt.AlignCenter)

        # layout1.addStretch(1)
        self.google_layout.setLayout(layout1)

    # stack 2
    def set_times_ui(self):
        layout2 = QVBoxLayout()

        # Prompt
        question2_text = QLabel("Which times would you like to set as unavailable?")
        question2_text.setStyleSheet(palette.Prefs.style_sheets['text_title'] + 'margin-bottom: 10px')
        layout2.addWidget(question2_text)

        # TimeList
        self.t_list = times_list.TimeList(self.ls_w, self.prefs)

        for x in range(0,20):
            self.t_list.make_item(f'Sleeping {x}', '20.00', '24.00')

        layout2.addWidget(self.t_list)

        self.set_times_layout.setLayout(layout2)
        #self.Stack.setCurrentIndex(1)

# For testing [TO DELETE]
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SetUpWindow([], '')

    sys.exit(app.exec())
