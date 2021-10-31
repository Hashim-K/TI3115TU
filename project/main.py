# MAIN modules
import json
import os

from gui.general_window_gui import GeneralWindow
import sys
import gui.palette
from PyQt5.QtWidgets import QApplication

# GUI modules
import gui.landing_window_gui

# ADDITIONAL Exception Tracebacks (keeps GUI from crashing)
import cgitb

from project.BackEnd.General import find_day_zero
from project.BackEnd.Preset import Presets

dirname = os.path.dirname(__file__)

cgitb.enable(format = 'text')

# MAIN attributes
window_list = list()
prefs = gui.palette.Prefs()

google_credentials = None       # Lookup token

# STARTUP functions
def on_startup():
    # Obtain Google account IF it is there
    day_zero = find_day_zero(0)
    print(os.path.isfile(os.path.join(dirname, 'data/presets.json')))
    print(os.path.join(dirname, 'data/presets.json'))
    if not os.path.exists(os.path.join(dirname, 'data/' + day_zero)):
        os.makedirs(os.path.join(dirname, 'data/' + day_zero))
    if not os.path.exists(os.path.join(dirname, 'data/temp/')):
        os.makedirs(os.path.join(dirname, 'data/temp/'))
    if not os.path.isfile(os.path.join(dirname, 'data/presets.json')):
        presets_json = {'day_zero': day_zero,
                        'number_of_days': 7,
                        'time_interval': 15,
                        'length_morning_routine': "00:15:00",
                        'calendar_id': -1,
                        'data_path': os.path.join(dirname, 'data/'),
                        'category_path': os.path.join(dirname, 'data/' + day_zero + '/categories.json'),
                        'google_path': os.path.join(dirname, 'data/' + day_zero + '/google_events.json'),
                        'routine_path': os.path.join(dirname, 'data/' + day_zero + '/routines.json'),
                        'task_path': os.path.join(dirname, 'data/' + day_zero + '/tasks.json'),
                        'schedule_path': os.path.join(dirname, 'data/' + day_zero + '/schedule.json'),
                        'schedule_image': os.path.join(dirname, 'data/' + day_zero + '/schedule.jpg')}
        with open(os.path.join(dirname, 'data/presets.json'), 'w') as out_file:
            json.dump(presets_json, out_file, indent=6)
    presets = Presets()
    presets.update()
    # Init landing GUI
    GeneralWindow.pre_init(window_list, prefs, gui.landing_window_gui.LandingView)

# BODY
app = QApplication(sys.argv)
on_startup()                    # Do startup-things
print('keepo')
sys.exit(app.exec())    

'''The event loop of the GUI is in the exit argument as that will make close
wait until ALL UI is closed.'''



