import sys, general_window_gui, Task
from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea, QAction, QMainWindow, QPushButton, QStackedLayout, QStackedWidget, QToolBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QColor, QIcon, QPixmap, QCursor
from PyQt5 import QtGui, QtCore

# TO DELETE
import string, random

class MainWindow(general_window_gui.GeneralWindow):
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

        # Title Text
        text = QLabel()
        text.setText('Event <u>View</u>')
        text.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        # List
        list_widget = TaskList()
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

            tli = TaskListItem(s_task, self.prefs)
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
        layout.addWidget(text)
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

###     TASK LIST AND ITEM      ###
class TaskList(QListWidget):
    def __init__(self):
        super().__init__()

        # Initial settings
        self.setSpacing(5)
        self.setStyleSheet("border: 2px")
        self.setSortingEnabled(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

class TaskListItem(QListWidgetItem):
    def __init__(self, task, prefs):
        super().__init__()
        self.task = task
        self.prefs = prefs

    def generate_widget(self):
        # Get relevant values
        task_ID = self.task.taskID
        task_name = self.task.name
        task_desc = self.task.description
        task_duration = self.task.duration
        task_sessions = self.task.session
        task_category = self.task.category
        task_priority = self.task.priority

        # WIDGET
        widget = QWidget()
        widget.setStyleSheet(self.prefs.style_sheets['text_bubble'])
        ## Layout
        layout_overal = QVBoxLayout()
        layout_top = QHBoxLayout()
        layout_sub = QHBoxLayout()

        layout_overal.addLayout(layout_top)
        layout_overal.addLayout(layout_sub)
        widget.setLayout(layout_overal)

        ## Layout Elements
        ### Top
        tb_name = QLabel(task_name)
        tb_name.setStyleSheet(self.prefs.style_sheets['text_title'])
        tb_name.setFixedWidth(75)
        tb_name.setToolTip(task_desc)

        tb_taskID = QLabel(f'Task ID: <b>{str(task_ID)}</b>')
        tb_taskID.setStyleSheet(self.prefs.style_sheets['text_tight'])

        tb_category = QLabel(f'Category: <b>{task_category}</b>')
        tb_category.setStyleSheet(self.prefs.style_sheets['text_tight'])

        tb_priority = QLabel(f'Priority: <b>{task_priority}</b>')
        tb_priority.setStyleSheet(self.prefs.style_sheets['text_tight'])

        layout_top.addWidget(tb_name)
        layout_top.addWidget(tb_taskID)
        layout_top.addWidget(tb_category)
        layout_top.addWidget(tb_priority)

        ### Lower (buttons)
        button_edit = QPushButton('Edit')
        button_edit.setStyleSheet(self.prefs.style_sheets['button_priority'])
        button_edit.setFixedWidth(100)

        button_delete = QPushButton('Delete')
        button_delete.setStyleSheet(self.prefs.style_sheets['button_exit'])
        button_delete.setFixedWidth(100)

        layout_sub.addStretch(1)
        layout_sub.addWidget(button_edit)
        layout_sub.addWidget(button_delete)

        return widget

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

