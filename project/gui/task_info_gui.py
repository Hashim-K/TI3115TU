from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QPushButton


# IMPORTS
from project.gui import general_window_gui
from project.BackEnd import Task, Category


class TaskInfo(general_window_gui.GeneralWindow):
    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def get_task(self, task_ID):
        """Fetch the task for data"""
        self.task = Task.find_task(self.prefs.directory['tasks'], task_ID)
        self.init_ui_late()

    def init_ui_late(self):
        # WINDOW
        placeholder_title = self.task.name
        placeholder_desc = self.task.description

        self.setWindowTitle(f'Task | {placeholder_title}')
        self.setFixedWidth(300)
        self.setStyleSheet(self.prefs.style_sheets['general_window'])

        icon = QIcon(self.prefs.images['icon_task_info'])
        self.setWindowIcon(icon)

        # Layout
        main_layout = QVBoxLayout()
        sub_layout = QFormLayout()
        sub_layout.setSpacing(20)

        # Main Layout Elements
            # Title
        task_title = QLabel(placeholder_title)
        task_title.setContentsMargins(10,0,0,5)
        task_title.setStyleSheet(self.prefs.style_sheets['text_title'])
        main_layout.addWidget(task_title)
            # Description
        task_desc = QLabel(placeholder_desc)
        task_desc.setWordWrap(True)
        task_desc.setStyleSheet(self.prefs.style_sheets['text_bubble'])
        main_layout.addWidget(task_desc)

        # Sub Layout Elements
        session_prompt = QLabel('Sessions')
        session_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        session = QLabel(f'{self.task.session}')
        session.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(session_prompt, session)

        duration_prompt = QLabel('Duration')
        duration_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        duration = QLabel(f'{self.task.duration * 15} minutes')
        duration.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(duration_prompt, duration)

        deadline_prompt = QLabel('Deadline')
        deadline_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        deadline = QLabel(f'{self.task.deadline}')
        deadline.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(deadline_prompt, deadline)

        priority_prompt = QLabel('Priority')
        priority_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        priority = QLabel(f'{self.task.priority}')
        priority.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(priority_prompt, priority)

        category_prompt = QLabel('Category')
        category_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        # Category Load
        category = Category.find_category(self.prefs.directory['categories'], self.task.category)
        if category is None:
            cat_name = 'No Category'
        else:
            cat_name = category.title
        category = QLabel(f'{cat_name}')
        category.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(category_prompt, category)

        preferred_prompt = QLabel('Preference')
        preferred_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        preferred = QLabel(f'{self.task.preferred}')
        preferred.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(preferred_prompt, preferred)

        repeatable_prompt = QLabel('Repeatable')
        repeatable_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        repeatable = QLabel(f'{self.task.repeatable}')
        repeatable.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(repeatable_prompt, repeatable)

        plan_on_same_prompt = QLabel('Same Day')
        plan_on_same_prompt.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        plan_on_same = QLabel(f'{self.task.plan_on_same}')
        plan_on_same.setStyleSheet(self.prefs.style_sheets['text_tight'])
        sub_layout.addRow(plan_on_same_prompt, plan_on_same)

        sub_layout.setContentsMargins(10,10,0,10)

        main_layout.addLayout(sub_layout)
        main_layout.addStretch(1)

        # Button
        close_button = QPushButton('Close')
        close_button.setStyleSheet(self.prefs.style_sheets['button_exit_rect'])
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

        self.setLayout(main_layout)

        self.show()

# FOR TESTING
# def window():
#     app = QApplication(sys.argv)
#     win = TaskInfo([], palette.Prefs)
#
#     sys.exit(app.exec())
#
# window()