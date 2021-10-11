import sys

from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea, QAction, QMainWindow, QPushButton, QStackedLayout, QStackedWidget, QToolBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit, QFrame
from PyQt5.QtGui import QColor, QIcon, QPixmap, QCursor, QFont
from PyQt5 import QtGui, QtCore

# TO DELETE
import string, random

from project.BackEnd import Task
from project.gui import general_window_gui, task_list, task_creation_gui


class MainView(general_window_gui.GeneralWindow):
    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):
        # WINDOW
        self.setMinimumSize(900, 600)

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
        self.stack_preferences = QWidget()

            # Init widgets in stack
        self.stack_tasks_ui()
        self.stack_schedule_ui()
        self.stack_preferences_ui()
            # Put widgets ins tack
        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack_events)
        self.stack.addWidget(self.stack_schedule)
        self.stack.addWidget(self.stack_preferences)
            # Add widgets to layout
        layout.addWidget(self.context)  # Context menu on left
        layout.addWidget(self.stack)    # Right side (current widget in stack)
        
        self.setLayout(layout)

    # UI GENERATORS
    ## Task View
    def stack_tasks_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Top Block
        top_block_widget = QWidget()
        top_block_widget.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        ## Title
        title = QLabel('Task View')
        title.setMargin(5)
        title.setStyleSheet(self.prefs.style_sheets['text_title'])

        ## New Task Button
        new_task_button = QPushButton('New')
        new_task_button.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        new_task_button.setFixedWidth(75)

        new_task_button.clicked.connect(self.new_task)

        ## Clear Button
        clear_button = QPushButton('Clear')
        clear_button.setStyleSheet(self.prefs.style_sheets['button_exit_rect'])
        clear_button.setFixedWidth(75) 

        ### Layout
        tbw_layout = QHBoxLayout()
        tbw_layout.addWidget(title)
        tbw_layout.addStretch(1)
        tbw_layout.addWidget(clear_button)
        tbw_layout.addWidget(new_task_button)

        top_block_widget.setLayout(tbw_layout)

        # List
        self.list_widget = task_list.TaskList(self.ls_w ,self.prefs)

        ## Populate List
        self.populate_list()

        # Add Layouts
        layout.addWidget(top_block_widget)
        layout.addWidget(self.list_widget)
        self.stack_events.setLayout(layout)
    
    def stack_schedule_ui(self):
        layout = QVBoxLayout()
        
        text = QLabel()
        text.setText('Schedule View')
        text.setStyleSheet(self.prefs.style_sheets['text_bubble_dark'])

        layout.addWidget(text)
        self.stack_schedule.setLayout(layout)

    def stack_preferences_ui(self):
        layout = QVBoxLayout()
        
        text = QLabel()
        text.setText('Preferences View')
        text.setStyleSheet(self.prefs.style_sheets['text_bubble_dark'])

        layout.addWidget(text)
        self.stack_preferences.setLayout(layout)
    
    def text_ui(self):
        layout = QVBoxLayout()

        # HLine
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: '#42464E'")

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color: '#42464E'")
        
        # Event Button
        self.event_button = QPushButton('Tasks')
        self.event_button.setStyleSheet(self.prefs.style_sheets['button_prio_burger'])
        self.event_button.clicked.connect(lambda:self.display(0))
        self.event_button.setFixedWidth(100)

        # Schedule Button
        self.schedule_button = QPushButton('Schedule')
        self.schedule_button.setStyleSheet(self.prefs.style_sheets['button_prio_burger'])
        self.schedule_button.clicked.connect(lambda:self.display(1))
        self.schedule_button.setFixedWidth(100)

        # Preferences Button
        self.prefs_button = QPushButton('Preferences')
        self.prefs_button.setStyleSheet(self.prefs.style_sheets['button_prio_burger'])
        self.prefs_button.clicked.connect(lambda:self.display(2))
        self.prefs_button.setFixedWidth(100)

        layout.addWidget(self.event_button)
        layout.addWidget(line)
        layout.addWidget(self.schedule_button)
        layout.addWidget(line2)
        layout.addWidget(self.prefs_button)
        layout.addStretch()

        self.context.setLayout(layout)

    # Task List Populator
    def populate_list(self):
        # Flush list
        self.list_widget.clear()
        # Repopulate
        tasks = Task.import_task('save_file.json')
        self.list_widget.load_task_list(tasks)

    # New Task Window
    def new_task(self):
        general_window_gui.GeneralWindow.pre_init(self.ls_w, self.prefs, task_creation_gui.TaskCreationWindow)
    
    # Stack Changer
    def display(self, i):
        self.stack.setCurrentIndex(i)
    
    # EVENTS
    def catch_event(self, event_name):
        if event_name == 'reload_tasks':
            self.populate_list()

