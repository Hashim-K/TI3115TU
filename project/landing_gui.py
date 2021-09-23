import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5 import QtGui, QtCore


class general_window(QWidget):
    '''General window skeleton; initializes window UI and adds it to passed window_list'''
    def __init__(self, window_list):
        super().__init__()
        self.ls_w = window_list
        self.ls_w.append(self)
        self.initUI()       # Initializes UI elements

    def initUI(self):
        pass
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.ls_w.remove(self)

class landing_view(general_window):
    def __init__(self, window_list):
        super().__init__(window_list)
    
    def initUI(self):
        # DATA
        msg_not_logged = 'offline mode'
        msg_logged = f'Welcome ##NAME##'
        # WINDOW
        self.setFixedSize(250, 500)
        # Window Style
        self.setWindowTitle("25/8")
        self.setStyleSheet(Stylesheet.general_window)
        # Grid Init
        grid = QGridLayout()

        # Image
        logo = QPixmap('project/logo.png')
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
        self.msg.setStyleSheet(Stylesheet.text_bubble_dark)

        grid.addWidget(self.msg, 0, 1, 1, 1)

        # Version Text
        v_text = QLabel()
        v_text.setText('v0.1')
        v_text.setStyleSheet(Stylesheet.text_mute)
        v_text.setAlignment(QtCore.Qt.AlignRight)

        grid.addWidget(v_text, 0, 0, 1, 1)

        # Sign in Button
        button = QPushButton('Launch')
        button.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) # Set cursor to hand on mouseover
        button.setStyleSheet(Stylesheet.priority_button)

        grid.addWidget(button, 2, 0, 1, 2)

        self.setLayout(grid)

        # Close Button
        close_button = QPushButton('Exit')
        close_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        close_button.setStyleSheet(Stylesheet.exit_button)

        close_button.clicked.connect(lambda:sys.exit())

        grid.addWidget(close_button, 3, 0, 1, 1)

        # Help Button
        help_button = QPushButton('About')
        help_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        help_button.setStyleSheet(Stylesheet.low_priority_button)

        grid.addWidget(help_button, 3, 1, 1, 1)



class Stylesheet():
    general_window = ("background: #303136;")
    text = ("font-size: 13px; color: 'white';" +
                    "border-radius: 10px;" +
                    " padding: 10px 10px;")
    text_mute = ("font-size: 13px; color: '#A0A0A0';" +
                    "border-radius: 10px;" +
                    " padding: 10px 10px;")
    text_bubble = ("font-size: 13px; color: 'white';" +
                    "background-color: '#363940'; border-radius: 10px;" +
                    " padding: 10px 10px;")
    text_bubble_dark = ("font-size: 13px; color: 'white';" +
                    "background-color: '#27282C'; border-radius: 10px;" +
                    " padding: 10px 10px;")
    text_bubble_alert = ("font-size: 13px; color: 'white';" +
                    "background-color: '#ff3643'; border-radius: 10px;" +
                    " padding: 10px 10px;")
    priority_button = (
                    "*{border: 2px solid '#404EED';" + 
                    "border-radius: 15px;" +
                    "background-color: '#404EED';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED';}"
                    )
    low_priority_button = (
                    "*{border: 2px solid '#42464E';" + 
                    "border-radius: 15px;" +
                    "background-color: '#42464E';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED'; color: 'white';}"
                    )
    exit_button = (
                    "*{border: 2px solid '#42464E';" + 
                    "border-radius: 15px;" +
                    "background-color: '#42464E';" + 
                    "font-size: 13px;" +
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#db0000'; color: 'white';}"
                    ) 

app = QApplication(sys.argv)
ls = list()
lv = landing_view(ls)
lv.show()
sys.exit(app.exec())

