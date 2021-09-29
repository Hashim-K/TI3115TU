import sys, Task
from gui import general_window_gui, task_list
from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea, QAction, QMainWindow, QPushButton, QStackedLayout, QStackedWidget, QToolBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QColor, QIcon, QPixmap, QCursor, QFont
from PyQt5 import QtGui, QtCore

# TO DELETE
import string, random

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

    # UI GENERATORS
    def stack_events_ui(self):
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
        list_widget = task_list.TaskList()
        # SAMPLES TO DELETE
        sample_task = Task.Task('Meeting',
         'Long Meeting', 25, 2, 27, False, 'Work', 'No', False, 2)

        for i in range(25):
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            desc = ''.join(random.choices(string.ascii_uppercase + string.digits, k=25))
            dur = random.randint(2, 24)
            prio = random.randint(0, 7)
            deadline = random.randint(0, 5)
            repeat = False
            cat_len = random.randint(5,9)
            category = ''.join(random.choices(string.ascii_uppercase + string.digits, k=cat_len))
            pref = ''
            plan_same = False
            sess = random.randint(0, 5)

            s_task = Task.Task(name, desc, dur, prio, deadline, repeat, category, pref
            , plan_same, sess)

            tli = task_list.TaskListItem(s_task, self.prefs)
            tli.setSizeHint(QtCore.QSize(200, 75))

            tliw = tli.generate_widget()
            list_widget.addItem(tli)
            list_widget.setItemWidget(tli, tliw)

        # task_task_list_item = TaskListItem(sample_task, self.prefs)
        # task_task_list_item.setSizeHint(QtCore.QSize(200,75))

        # ttli_widget = task_task_list_item.generate_widget()

        # list_widget.addItem(task_task_list_item)
        # list_widget.setItemWidget(task_task_list_item, ttli_widget)

        # callcards = ['Echo', 'Beta', 'Alpha', 'Delta', 'Gamma']

        # for i in range(len(callcards)):
        #     object = QListWidgetItem(callcards[i])
        #     object.setSizeHint(QtCore.QSize(200, 75))
        #     widgeet = self.getWidget(callcards[i])


        #     list_widget.addItem(object)
        #     list_widget.setItemWidget(object, widgeet)
        #

        # Add Layouts
        layout.addWidget(top_block_widget)
        layout.addWidget(list_widget)
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
        
        self.event_button = QPushButton('Tasks')
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

