import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5 import QtGui, QtCore

class GeneralWindow(QWidget):
    '''General window skeleton; initializes window UI and adds it to passed window_list'''
    def __init__(self, window_list, prefs):
        super().__init__()

        self.ls_w = window_list     # Store window list for ADD/REMOVE
        self.ls_w.append(self)

        self.prefs = prefs      # Load in prefs

        self.init_ui()       # Initializes UI elements
        self.show()         # Show Window

    def init_ui(self):
        pass
    
    def catch_event(self, event_name):
        pass
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:    # Upon closure
        self.ls_w.remove(self)

    '''Pre_init takes care of whether the windowtype already exists on screen.'''
    @staticmethod
    def pre_init(window_list, prefs, window_type):
        for window in window_list:
            if isinstance(window, window_type):
                return None
        new_window = window_type(window_list, prefs)
    
    @staticmethod
    def raise_event(window_list, event_name):
        for window in window_list:
            window.catch_event(event_name)