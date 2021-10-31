from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame

from project.gui import general_window_gui


class AboutWindow(general_window_gui.GeneralWindow):
    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def init_ui(self):
        # WINDOW
        self.setFixedSize(300, 250)

        # Window Style
        self.setWindowIcon(QIcon(self.prefs.images['icon_info']))
        self.setWindowTitle("About 25/8")
        self.setStyleSheet(self.prefs.style_sheets['general_window'])

        # Main layout
        layout = QVBoxLayout()

        ## Body

        ### Title
        title_text = QLabel(f'About 25/8 | {self.prefs.ver_nr}')
        title_text.setContentsMargins(10,10,0,0)
        title_text.setStyleSheet(self.prefs.style_sheets['text_title'])

        layout.addWidget(title_text)

        ### Text Upper
        prompt = "The user of this software carries full liability for " \
                 "all effects that come forth of its use. Employ " \
                 "functionalities that pose potential security risks at " \
                 "your own discretion."
        upper_text = QLabel(prompt)
        upper_text.setWordWrap(True)
        upper_text.setStyleSheet(self.prefs.style_sheets['text'])

        layout.addWidget(upper_text)

        ### Line
        line_div = QFrame()
        line_div.setFrameShape(QFrame.HLine)
        line_div.setStyleSheet("color: '#42464E'")

        layout.addWidget(line_div)

        ### Text Lower
        prompt = "© Group 25 | All Rights Reserved"
        lower_text = QLabel(prompt)
        lower_text.setWordWrap(True)
        lower_text.setStyleSheet(self.prefs.style_sheets['text_mute'])

        layout.addWidget(lower_text)


        # SubLayout
        sublayout = QHBoxLayout()

        ## Close Button
        close_button = QPushButton('Close')
        close_button.setStyleSheet(self.prefs.style_sheets['button_exit_rect'])
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.close)

        sublayout.addStretch()
        sublayout.addWidget(close_button)

        # Layout
        layout.addLayout(sublayout)
        self.setLayout(layout)

    def catch_event(self, event_name):
        if event_name == 'close_landing_deriv':     # Closing when landing closes
            self.close()