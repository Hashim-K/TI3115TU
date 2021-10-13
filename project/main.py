# MAIN modules
from gui.general_window_gui import GeneralWindow
import sys, gui.palette
from PyQt5.QtWidgets import QApplication

# GUI modules
import gui.landing_window_gui

# ADDITIONAL Exception Tracebacks (keeps GUI from crashing)
import cgitb
cgitb.enable(format = 'text')

# MAIN attributes
window_list = list()
prefs = gui.palette.Prefs()

google_credentials = None       # Lookup token

# STARTUP functions
def on_startup():
    # Obtain Google account IF it is there

    # Init landing GUI
    GeneralWindow.pre_init(window_list, prefs, gui.landing_window_gui.LandingView)

# BODY
app = QApplication(sys.argv)
on_startup()                    # Do startup-things
print('keepo')
sys.exit(app.exec())    

'''The event loop of the GUI is in the exit argument as that will make close
wait until ALL UI is closed.'''



