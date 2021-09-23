import sys, general_window_gui, main_window_gui
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5 import QtGui, QtCore

class LandingView(general_window_gui.GeneralWindow):
    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)
    
    def launch(self):
        main_window = main_window_gui.MainWindow(self.ls_w, self.prefs)
        self.close()
    
    def init_ui(self):
        # DATA
        msg_not_logged = 'offline mode'
        msg_logged = f'Welcome ##NAME##'
        # WINDOW
        self.setFixedSize(250, 500)
        # Window Style
        icon = QIcon(self.prefs.images['img_logo_min'])
        self.setWindowIcon(icon)
        self.setWindowTitle("25/8")
        self.setStyleSheet(self.prefs.style_sheets['general_window'])
        # Grid Init
        grid = QGridLayout()

        # Image
        logo = QPixmap(self.prefs.images['img_logo'])
        scale = 0.27
        logo = logo.scaled(scale * logo.width(), scale * logo.height(), transformMode=QtCore.Qt.SmoothTransformation)
        l_logo = QLabel()
        l_logo.setPixmap(logo)
        l_logo.setAlignment(QtCore.Qt.AlignCenter)
        l_logo.setStyleSheet('margin-top: 10px')

        grid.addWidget(l_logo, 1, 0, 1, 2)

        # Msg Bubble
        self.msg = QLabel()
        self.msg.setText(msg_not_logged)                # ADD LOGGED CHECK
        self.msg.setAlignment(QtCore.Qt.AlignCenter)
        self.msg.setFixedHeight(30)
        self.msg.setWordWrap(True)
        self.msg.setStyleSheet(self.prefs.style_sheets['text_bubble_dark'])

        grid.addWidget(self.msg, 0, 1, 1, 1)

        # Version Text
        v_text = QLabel()
        v_text.setText('v0.1')
        v_text.setStyleSheet(self.prefs.style_sheets['text_mute'])
        v_text.setAlignment(QtCore.Qt.AlignRight)

        grid.addWidget(v_text, 0, 0, 1, 1)

        # Launch Button
        button = QPushButton('Launch')
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) # Set cursor to hand on mouseover
        button.setStyleSheet(self.prefs.style_sheets['button_priority'])

        button.clicked.connect(self.launch)

        grid.addWidget(button, 2, 0, 1, 2)

        self.setLayout(grid)

        # Close Button
        close_button = QPushButton('Exit')
        close_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        close_button.setStyleSheet(self.prefs.style_sheets['button_exit'])

        close_button.clicked.connect(lambda:sys.exit())

        grid.addWidget(close_button, 3, 0, 1, 1)

        # Help Button
        help_button = QPushButton('About')
        help_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        help_button.setStyleSheet(self.prefs.style_sheets['button_low_priority'])

        grid.addWidget(help_button, 3, 1, 1, 1)

