from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout


class CustomDialog(QDialog):
    def __init__(self, prompt, prefs, parent = None):
        super().__init__(parent)
        # Window
        icon = QIcon(prefs.images['icon_warning'])
        self.setWindowIcon(icon)
        self.setFixedWidth(200)
        self.setMinimumHeight(125)

        # Title
        self.setWindowTitle('Warning')

        # Message
        message = QLabel(prompt)
        message.setWordWrap(True)
        message.setStyleSheet(prefs.style_sheets['text'])

        # Custom Buttons
        sublayout = QHBoxLayout()

        self.accept_button = QPushButton('Sure')
        self.accept_button.setStyleSheet(prefs.style_sheets['button_priority_rect'])
        self.accept_button.clicked.connect(self.accept)  # Set Return Action

        sublayout.addWidget(self.accept_button)

        self.reject_button = QPushButton('Nevermind')
        self.reject_button.setStyleSheet(prefs.style_sheets['button_exit_rect'])
        self.reject_button.clicked.connect(self.reject)  # Set Return Action

        sublayout.addWidget(self.reject_button)

        # Layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(message)
        self.layout.addLayout(sublayout)
        self.setLayout(self.layout)
