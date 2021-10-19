import sys

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton

from project.gui import palette
from project.gui.general_window_gui import GeneralWindow


class OverlapWindow(GeneralWindow):
    '''Pops up when the user tries to add a routine which overlaps with an existing routine.
    The user can choose one of the following actions:
    1. Cancel adding the new routine and keep the existing.
    2. Delete the existing routine and add the new routine.
    (below may not be implemented)
    3. Shift the new routine such that it does not overlap. (too complicated IMO)
    4. Merge the two routines into one. (not very practical if they are two different categories?)
    5. Crop the new routine. (seems doable)'''

    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

    def get_overlap_info(self, overlap_info):
        self.overlap_info = overlap_info

    def init_ui(self):
        self.setWindowTitle("Resolve overlap")
        self.setStyleSheet(self.prefs.style_sheets['general_window'])

        layout = QVBoxLayout()

        # Text which tells the user there is overlap.
        explanation = QLabel("The new routine overlaps with an existing routine.\n"
                             "What would you like to do?")
        explanation.setStyleSheet(self.prefs.style_sheets['text'])
        layout.addWidget(explanation)

        # Button for action 1: Cancel adding the new routine and keep the existing.
        self.button_1 = QPushButton("Cancel adding the new routine and keep the existing routine.")
        self.button_1.setStyleSheet(self.prefs.style_sheets['button_priority'])
        layout.addWidget(self.button_1)

        #Button for action 2: Delete the existing routine and add the new routine.
        self.button_2 = QPushButton("Delete the existing routine and add the new routine.")
        self.button_2.setStyleSheet(self.prefs.style_sheets['button_priority'])
        layout.addWidget(self.button_2)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = OverlapWindow([], palette.Prefs())

    sys.exit(app.exec())
