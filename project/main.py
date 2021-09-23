# MAIN modules
import sys, s_p
from PyQt5.QtWidgets import QApplication

# GUI modules
import landing_gui

# MAIN attributes
window_list = list()
prefs = s_p.Prefs()

google_credentials = None       # Lookup token

# STARTUP functions
def on_startup():
    # Obtain Google account IF it is there

    # Init landing GUI
    gui_landing = landing_gui.LandingView(window_list, prefs)

# BODY
app = QApplication(sys.argv)
on_startup()                    # Do startup-things
print('keepo')
sys.exit(app.exec())    

'''The event loop of the GUI is in the exit argument as that will make close
wait until ALL UI is closed.'''



