from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5 import QtCore

from project.BackEnd import Task, Category
from project.BackEnd.Schedule import import_schedule

from project.gui.task_info_gui import TaskInfo
from project.gui.general_window_gui import GeneralWindow


class TaskList(QListWidget):
    def __init__(self, window_list, prefs):
        super().__init__()
        # Store windows and prefs
        self.prefs = prefs
        self.ls_w = window_list     # For reloading windows

        # Initial settings
        self.setSpacing(5)
        self.setStyleSheet("border: 2px")
        self.setSortingEnabled(True)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    
    def load_task_list(self, tasks):
        '''Generates list items from tasks.'''
        for task in tasks:
            task_list_item = TaskListItem(task, self.ls_w, self.prefs)
            task_list_item_widget = task_list_item.generate_widget()

            self.addItem(task_list_item)
            self.setItemWidget(task_list_item, task_list_item_widget)

class TaskListItem(QListWidgetItem):
    def __init__(self, task, window_list, prefs):
        super().__init__()
        self.task = task
        self.prefs = prefs
        self.ls_w = window_list

        # UI
        self.setSizeHint(QtCore.QSize(200,75))  # Size hint for Items

    def generate_widget(self):
        # Get relevant values
        task_ID = self.task.taskID
        task_name = self.task.name
        task_desc = self.task.description
        task_deadline = self.task.deadline
        task_duration = self.task.duration
        task_sessions = self.task.session
        category_obj = Category.find_category(self.task.category)
        # Category check
        if category_obj is None:    # No category
            task_category = 'No Category'
            colour_hex = '#FFFFFF'
        else:   # Category
            task_category = category_obj.title
            colour_hex = category_obj.color
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
        tb_name.setFixedWidth(125)
        tb_name.setToolTip(task_desc)

        tb_taskID = QLabel(f'Deadline: <b>{str(task_deadline)}</b>')
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
        button_view = QPushButton('View')
        button_view.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        button_view.clicked.connect(self.view_task)
        button_view.setFixedWidth(100)

        # Colour Piece
        colour_piece = QPushButton(colour_hex)
        colour_piece_sheet = (
                "*{border: 2px solid '"+colour_hex+"';" +
                "border-radius: 5px;" +
                "background-color: '"+colour_hex+"';" +
                "font-size: 13px;"
                "color : rgba(0,0,0,0);" +
                "padding: 5px 0px;" +
                "margin: 0px 0px;}" +
                "*:hover{color: 'black';}"
        )

        colour_piece.setStyleSheet(colour_piece_sheet)
        colour_piece.setFixedWidth(75)

        button_edit = QPushButton('Edit')
        button_edit.setStyleSheet(self.prefs.style_sheets['button_low_priority_rect'])
        button_edit.setFixedWidth(100)

        button_delete = QPushButton('Delete')
        button_delete.setStyleSheet(self.prefs.style_sheets['button_exit_rect'])
        button_delete.clicked.connect(self.delete_task)
        button_delete.setFixedWidth(100)

        # layout_sub.addStretch(1)
        layout_sub.addWidget(button_view)
        layout_sub.addWidget(colour_piece)
        layout_sub.addStretch(1)
        layout_sub.addWidget(button_edit)
        layout_sub.addWidget(button_delete)

        return widget

    # Task Buttons
    def view_task(self):
        window = GeneralWindow.pre_init(self.ls_w, self.prefs, TaskInfo)
        window.get_task(self.task.taskID)   # Fetches task using its class

    def delete_task(self):
        schedule = import_schedule()
        Task.delete_task(self.task.taskID)
        schedule.delete_event("Task", self.task.taskID)
        GeneralWindow.raise_event(self.ls_w, 'reload_tasks')