import sys, general_window_gui
from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea, QAction, QMainWindow, QPushButton, QStackedLayout, QStackedWidget, QToolBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
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

        self.context = QWidget()
        self.text_ui()

        # Stack of Widgets on RIGHT
        self.stack_events = QWidget()
        self.stack_schedule = QWidget()

            # Init widgets in stack
        self.stack_events_ui()
        self.stack_schedule_ui()
            # Put widgets ins tack
        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack_events)
        self.stack.addWidget(self.stack_schedule)
            # Add widgets to layout
        layout.addWidget(self.context)  # Context menu on left
        layout.addWidget(self.stack)    # Right side (current widget in stack)
        
        self.setLayout(layout)

    def getWidget(self, title):
        text = QLabel(title) 
        text.setStyleSheet("color : 'white'")

        button = QPushButton('Delete')
        button.setStyleSheet(self.prefs.style_sheets['button_priority'])

        widgeet = QWidget()
        widgeet.setStyleSheet(self.prefs.style_sheets['text_bubble'])
        layout = QHBoxLayout()
        layout.addWidget(text)
        layout.addWidget(button)
        widgeet.setLayout(layout)

        return widgeet

    # UI GENERATORS
    def stack_events_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Title Text
        text = QLabel()
        text.setText('Event <u>View</u>')
        text.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        # List
        listWidget = QListWidget()
        listWidget.setSpacing(5)    # Spacing between items
        listWidget.setStyleSheet("border: 2 px")
        listWidget.setSortingEnabled(True)
        listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # Disable scroll bar
        
        #
        for i in range(1, 25):
            object = QListWidgetItem(str(i))
            object.setSizeHint(QtCore.QSize(200, 75))
            widgeet = self.getWidget('Sky High' + str(i))


            listWidget.addItem(object)
            listWidget.setItemWidget(object, widgeet)
        #

        # Add Layouts
        layout.addWidget(text)
        layout.addWidget(listWidget)
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
        
        self.event_button = QPushButton('Event')
        self.event_button.setStyleSheet(self.prefs.style_sheets['button_prio_burger'])
        self.event_button.clicked.connect(lambda:self.display(0))

        self.schedule_button = QPushButton('Schedule')
        self.schedule_button.setStyleSheet(self.prefs.style_sheets['button_prio_burger'])
        self.schedule_button.clicked.connect(lambda:self.display(1))

        layout.addWidget(self.event_button)
        layout.addWidget(self.schedule_button)
        layout.addStretch()

        self.context.setLayout(layout)
    
    # Stack Changer
    def display(self, i):
        self.stack.setCurrentIndex(i)
