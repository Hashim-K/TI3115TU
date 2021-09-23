import sys, general_window_gui
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QAction, QMainWindow, QPushButton, QStackedLayout, QStackedWidget, QToolBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QColor, QIcon, QPixmap, QCursor
from PyQt5 import QtGui, QtCore

class MainWindow(general_window_gui.GeneralWindow):
    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):
        # WINDOW
        self.setFixedSize(1000, 750)

        # Window Style
        icon = QIcon(self.prefs.images['img_logo_min'])
        self.setWindowIcon(icon)
        self.setWindowTitle("25/8")
        self.setStyleSheet(self.prefs.style_sheets['general_window'])

        # Layout
        layout = QHBoxLayout()    # Make grid
        self.setLayout(layout)

        # text = QLabel()
        # text.setText("v. 0.0.1 \n258 \n\nThis")
        # text.setWordWrap(True)
        # text.setStyleSheet("font-size: 13px; color: 'white'; background-color: '#363940'; border-radius: 10px; padding: 10px 10px;")

        self.text = QWidget()
        self.text_ui()

        # Stack
        self.stack_events = QWidget()
        self.stack_schedule = QWidget()

        self.stack_events_ui()
        self.stack_schedule_ui()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack_events)
        self.stack.addWidget(self.stack_schedule)

        layout.addWidget(self.text)
        layout.addWidget(self.stack)
        
        self.setLayout(layout)

    # Stack View UI generators
    def stack_events_ui(self):
        layout = QVBoxLayout()
        
        text = QLabel()
        text.setText('Event View')
        text.setStyleSheet(self.prefs.style_sheets['text_bubble_dark'])

        layout.addWidget(text)
        self.stack_events.setLayout(layout)
    
    def stack_schedule_ui(self):
        layout = QVBoxLayout()
        
        text = QLabel()
        text.setText('Schedule View')
        text.setStyleSheet(self.prefs.style_sheets['text_bubble_dark'])

        layout.addWidget(text)
        self.stack_schedule.setLayout(layout)
    
    def text_ui(self):
        layout = QVBoxLayout()
        
        button1 = QPushButton('Event')
        button1.setStyleSheet(
                    "*{border: 2px solid '#404EED';" + 
                    "border-radius: 15px;" +
                    "background-color: '#404EED';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 25px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED';}"
                    )
        button1.clicked.connect(lambda:self.display(0))

        button2 = QPushButton('Schedule')
        button2.setStyleSheet(
                    "*{border: 2px solid '#404EED';" + 
                    "border-radius: 15px;" +
                    "background-color: '#404EED';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 25px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED';}"
                    )
        button2.clicked.connect(lambda:self.display(1))

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addStretch()

        self.text.setLayout(layout)
    
    # Stack Changer
    def display(self, i):
        self.stack.setCurrentIndex(i)

    # def __init__(self, window_list, prefs):
    #     super().__init__()

    #     self.ls_w = window_list     # Store window list for ADD/REMOVE
    #     self.ls_w.append(self)

    #     self.prefs = prefs      # Load in prefs

    #     self.init_ui()       # Initializes UI elements
    #     self.show()         # Show Window

    # def init_ui(self):
    #     # WINDOW
    #     self.setFixedSize(1000, 750)

    #     # Window Style
    #     icon = QIcon(self.prefs.images['img_logo_min'])
    #     self.setWindowIcon(icon)
    #     self.setWindowTitle("25/8")
    #     self.setStyleSheet(self.prefs.style_sheets['general_window'])

    #     # Toolbar
    #     exit = QAction(QIcon(self.prefs.images['bar_close']), 'Exit', self)     # Make button
    #     exit.triggered.connect(self.close)

    #     self.toolbar = self.addToolBar('Toolbar')  # Generate Toolbar
    #     self.toolbar.addAction(exit)
    #     self.toolbar.setStyleSheet('background : #27282C')

    #     # Stack
    #     stack = QStackedWidget()
    #     self.setCentralWidget(stack)
    
    # def closeEvent(self, a0: QtGui.QCloseEvent) -> None:    # Upon closure
    #     self.ls_w.remove(self)
    

