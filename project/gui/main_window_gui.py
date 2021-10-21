import sys
from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QScrollArea, QAction, QMainWindow, QPushButton, QStackedLayout, QStackedWidget, QToolBar, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit, QFrame
from PyQt5.QtGui import QColor, QIcon, QPixmap, QCursor, QFont
from PyQt5 import QtGui, QtCore
import os
dirname = os.path.dirname(__file__)

# TO DELETE
import string, random

from project.BackEnd import Task, Schedule, GoogleAPI
from project.gui import general_window_gui, task_list, task_creation_gui, routines_list, add_routine_gui


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
        self.stack_routines = QWidget()
        self.stack_preferences = QWidget()

            # Init widgets in stack
        self.stack_tasks_ui()
        self.stack_schedule_ui()
        self.stack_routines_ui()
        self.stack_preferences_ui()
            # Put widgets ins tack
        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack_events)
        self.stack.addWidget(self.stack_schedule)
        self.stack.addWidget(self.stack_routines)
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

        ## Top Block
        top_block_widget = QWidget()
        top_block_widget.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        ## Title
        title = QLabel('Task View')
        title.setMargin(5)
        title.setStyleSheet(self.prefs.style_sheets['text_title'])

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setStyleSheet("color: 'white'")

        ## Counter for tasks
        self.task_view_counter = QLabel('No Tasks')
        self.task_view_counter.setMargin(5)
        self.task_view_counter.setStyleSheet(self.prefs.style_sheets['text_title_mute'])

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
        # tbw_layout.addWidget(line)
        tbw_layout.addWidget(self.task_view_counter)
        tbw_layout.addStretch(1)
        tbw_layout.addWidget(clear_button)
        tbw_layout.addWidget(new_task_button)

        top_block_widget.setLayout(tbw_layout)

        # List
        self.list_widget = task_list.TaskList(self.ls_w ,self.prefs)

        ## Populate List
        self.populate_tasklist()

        # Add Layouts
        layout.addWidget(top_block_widget)
        layout.addWidget(self.list_widget)
        self.stack_events.setLayout(layout)

    ## Schedule View
    def stack_schedule_ui(self):
        # Main Layout
        layout = QVBoxLayout()

        # Top Block
        top_block_widget = QWidget()
        top_block_widget.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        ## Title
        title = QLabel()
        title.setMargin(5)
        title.setText('Schedule View')
        title.setStyleSheet(self.prefs.style_sheets['text_title'])

        ## Export Schedule Button
        export_schedule_button = QPushButton("Export to Calendar")
        export_schedule_button.setToolTip('Export currently unavailable')   # TO DELETE
        export_schedule_button.setStyleSheet(self.prefs.style_sheets['button_disabled_rect'])
        export_schedule_button.setFixedWidth(150)

        # Top Block Layout
        tbw_layout = QHBoxLayout()
        tbw_layout.addWidget(title)
        tbw_layout.addStretch(1)
        tbw_layout.addWidget(export_schedule_button)
        top_block_widget.setLayout(tbw_layout)

        self.schedule_label = QLabel()
        self.update_schedule_image()

        # Main Layout
        layout.addWidget(top_block_widget, alignment=QtCore.Qt.AlignTop)
        layout.addWidget(self.schedule_label)
        self.stack_schedule.setLayout(layout)

    # Routines view
    def stack_routines_ui(self):
        layout = QVBoxLayout()

        ## Top Block
        top_block_widget = QWidget()
        top_block_widget.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        ## Title
        title = QLabel('Routines')
        title.setMargin(5)
        title.setStyleSheet(self.prefs.style_sheets['text_title'])

        ## Add Routine Button
        add_routine_button = QPushButton("Add routine")
        add_routine_button.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        add_routine_button.clicked.connect(self.new_routine)
        add_routine_button.setFixedWidth(100)

        # Clear all button
        clear_all = QPushButton("Clear all")
        clear_all.setStyleSheet(self.prefs.style_sheets['button_exit_rect'])
        clear_all.clicked.connect(self.clear_routines)
        clear_all.setFixedWidth(100)

        # Layout in Box
        tbw_layout = QHBoxLayout()
        tbw_layout.addWidget(title)
        tbw_layout.addStretch(1)
        tbw_layout.addWidget(clear_all)
        tbw_layout.addWidget(add_routine_button)

        top_block_widget.setLayout(tbw_layout)

        # Divider
        line_div = QFrame()
        line_div.setFrameShape(QFrame.HLine)
        line_div.setStyleSheet("color: '#42464E'")

        # Header
        head_text = QLabel("Set at which times you are unavailable.\n" +
                           "Task sessions will not be planned during these times.")
        head_text.setStyleSheet(self.prefs.style_sheets['text_bubble_clear'])

        # List of routines
        self.routine_list = routines_list.RoutinesList(self.ls_w, self.prefs)

        # Main Layout
        layout.addWidget(top_block_widget, alignment=QtCore.Qt.AlignTop)
        layout.addWidget(head_text)
        layout.addWidget(line_div)
        layout.addWidget(self.routine_list)

        self.stack_routines.setLayout(layout)

        # prep schedule
        Schedule.PrepEvents()

        # Update schedule
        self.populate_routine_list()

    ## Preferences View
    def stack_preferences_ui(self):
        layout = QVBoxLayout()
        
        ## Top Block
        top_block_widget = QWidget()
        top_block_widget.setStyleSheet(self.prefs.style_sheets['text_bubble_title'])

        ## Title
        title = QLabel('Preferences')
        title.setMargin(5)
        title.setStyleSheet(self.prefs.style_sheets['text_title'])

        # Layout in Box
        tbw_layout = QHBoxLayout()
        tbw_layout.addWidget(title)
        tbw_layout.addStretch(1)

        top_block_widget.setLayout(tbw_layout)

        ## Body
        body_layout = QGridLayout()
        body_layout.setColumnStretch(0, 1)
        body_layout.setColumnStretch(1, 1)

        # Google Box
        google_box = QGroupBox('Import Calendar')
        google_box.setStyleSheet(self.prefs.style_sheets['std_gbox'])

        ## Google Box Layout
        gb_layout = QVBoxLayout()

        ### Prompt
        prompt_text = "Connecting your Google account will allow 25/8 to " \
                      "import events from your calendar and also export " \
                      "a generated schedule to it."
        prompt = QLabel(prompt_text)
        prompt.setWordWrap(True)
        prompt.setStyleSheet(self.prefs.style_sheets['text'])

        gb_layout.addWidget(prompt)

        ### Prompt Connect
        prompt_connect_text = "1) Connect your Google Account"
        prompt_connect = QLabel(prompt_connect_text)
        prompt_connect.setWordWrap(True)
        prompt_connect.setStyleSheet(self.prefs.style_sheets['text_bubble_slim'])

        gb_layout.addWidget(prompt_connect)

        ### Prompt Connect Subscript
        prompt_text = "This will allow 25/8 to read from and write to your Google " \
                      "Calendar. If a Google a"
        prompt = QLabel(prompt_text)
        prompt.setWordWrap(True)
        prompt.setStyleSheet(self.prefs.style_sheets['text_bubble_clear_slim'])

        gb_layout.addWidget(prompt)

        ### Button
        button = QPushButton(' Connect Google Account')
        icon = QIcon(self.prefs.images['placeholder'])
        button.setIcon(icon)
        button.setFixedWidth(200)
        button.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        button.clicked.connect(GoogleAPI.authenticate)

        gb_layout.addWidget(button, alignment=QtCore.Qt.AlignCenter)

        ### Prompt Import
        prompt_import_text = "2) Import Events"
        prompt_import = QLabel(prompt_import_text)
        prompt_import.setWordWrap(True)
        prompt_import.setStyleSheet(self.prefs.style_sheets['text_bubble_slim'])

        gb_layout.addWidget(prompt_import)

        ### Prompt Connect Subscript
        prompt_text = "Importing the events will enable the scheduler to consider " \
                      "already scheduled events."
        prompt = QLabel(prompt_text)
        prompt.setWordWrap(True)
        prompt.setStyleSheet(self.prefs.style_sheets['text_bubble_clear_slim'])

        gb_layout.addWidget(prompt)

        google_box.setLayout(gb_layout)

        body_layout.addWidget(google_box, 0, 0, 1, 1)

        # Settings Box
        settings_box = QGroupBox('Settings')
        settings_box.setStyleSheet(self.prefs.style_sheets['std_gbox'])

        body_layout.addWidget(settings_box, 0, 1, 1, 1)

        # Main Layout
        layout.addWidget(top_block_widget, alignment=QtCore.Qt.AlignTop)    # Stick to top
        layout.addLayout(body_layout)
        layout.addStretch(1)

        self.stack_preferences.setLayout(layout)

    ## Sidebar
    def text_ui(self):
        layout = QVBoxLayout()

        # HLine
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: '#42464E'")

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color: '#42464E'")

        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setStyleSheet("color: '#42464E'")

        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setStyleSheet("color: '#42464E'")
        
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

        # Set Routines Button
        self.routines_button = QPushButton('Routines')
        self.routines_button.setStyleSheet(self.prefs.style_sheets['button_prio_burger'])
        self.routines_button.clicked.connect(lambda:self.display(2))
        self.routines_button.setFixedWidth(100)

        # Preferences (Google etc.)
        self.preferences_button = QPushButton('Preferences')
        self.preferences_button.setStyleSheet(self.prefs.style_sheets['button_prio_burger'])
        self.preferences_button.clicked.connect(lambda:self.display(3))
        self.preferences_button.setFixedWidth(100)

        # Generate schedule button
        self.generate_button = QPushButton('Generate\nschedule')
        self.generate_button.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        self.generate_button.clicked.connect(self.add_schedule)
        self.generate_button.setFixedWidth(100)

        layout.addWidget(self.event_button)
        layout.addWidget(line)
        layout.addWidget(self.schedule_button)
        layout.addWidget(line2)
        layout.addWidget(self.routines_button)
        layout.addWidget(line3)
        layout.addWidget(self.preferences_button)
        layout.addWidget(line4)
        layout.addStretch()
        layout.addWidget(self.generate_button)

        self.context.setLayout(layout)

    def add_schedule(self):
        service = GoogleAPI.authenticate()
        GoogleAPI.create_calendar(service, 'anything')  # Anything is placeholder

    # Task List Populator
    def populate_tasklist(self):
        """
        Populates the UI list of tasks and edits the 'task view' list using
        a window event.
        """
        # Flush list
        self.list_widget.clear()
        # Repopulate
        try:
            tasks = Task.import_task(self.prefs.directory['tasks'])
            self.list_widget.load_task_list(tasks)

            # Changing number of tasks
            num_tasks = len(tasks)
            if num_tasks == 0:
                self.task_view_counter.setText(f'No Tasks')
            elif num_tasks == 1:
                self.task_view_counter.setText(f'1 Task')
            else:
                self.task_view_counter.setText(f'{int(len(tasks))} Tasks')

        except FileNotFoundError:
            print("json doesn't exist.")

    def populate_routine_list(self):
        self.routine_list.clear()
        self.routine_list.load_routinelist()

    def new_task(self):
        general_window_gui.GeneralWindow.pre_init(self.ls_w, self.prefs, task_creation_gui.TaskCreationWindow)

    def new_routine(self):
        general_window_gui.GeneralWindow.pre_init(self.ls_w, self.prefs, add_routine_gui.AddRoutineWindow)

    def clear_routines(self):
        Schedule.ClearEvents()
        general_window_gui.GeneralWindow.raise_event(self.ls_w, 'reload_routines')

    def update_schedule_image(self):
        self.schedule_image = QPixmap(os.path.join(dirname, '../schedule.jpg'))
        self.schedule_label.setPixmap(self.schedule_image)
    
    # Stack Changer
    def display(self, i):
        self.stack.setCurrentIndex(i)
    
    # EVENTS
    def catch_event(self, event_name):
        if event_name == 'reload_tasks':
            self.populate_tasklist()
        if event_name == 'reload_routines':
            self.populate_routine_list()
            self.update_schedule_image()


class TopBlockWidget(QWidget):  # COULD be TESTED [not done]
    """
    Responsible for generation of topblockwidgets. These widgets are the headers
    of the various views within the main window.
    """
    def __init__(self, title, button_count, button_titles, button_functions, prefs):
        super().__init__()
        # Warnings
        if button_count > 2:
            print('Button count larger than 2, clamped to 2.')
        if not (button_count == len(button_titles) == len(button_functions)):
            print('Not enough button relatives.')

        # Layout
        block_layout = QHBoxLayout()
        self.setStyleSheet(prefs.style_sheets['text_bubble_title'])

        # Title
        block_title = QLabel(title)
        block_title.setMargin(5)
        block_title.setStyleSheet(prefs.style_sheets['text_title'])
        block_layout.addWidget(block_title)

        block_layout.addStretch(1)  # Stretch before buttons

        # Button-Count sensitive action
        if button_count == 0:
            pass
        if button_count >= 1:
            # Button 1
            button_one = QPushButton(button_titles[0])
            button_one.setStyleSheet(prefs.style_sheets['button_priority_rect'])
            button_one.setFixedWidth(75)

            # button_one.clicked.connect(lambda:button_functions[0])

            block_layout.addWidget(button_one)
        if button_count >= 2:
            # Button 2:
            button_two = QPushButton(button_titles[1])
            button_two.setStyleSheet(prefs.style_sheets['button_low_priority_rect'])
            button_two.setFixedWidth(75)

            # button_two.clicked.connect(lambda:button_functions[1])

            block_layout.addWidget(button_two)

        self.setLayout(block_layout)    # Set layout to layout

