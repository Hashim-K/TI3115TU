import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QGridLayout, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

app = QApplication(sys.argv)      # Q Application generation
window = QWidget()                  # Generating First Window
window.setFixedSize(250, 500)

# WINDOWLIST
ls_window = list()              # Required for addition to WHILE cycle

# Style Window
window_icon = QIcon('wrench.png')
window.setWindowIcon(window_icon)
window.setWindowTitle("258")
window.setStyleSheet("background: #303136;")

grid = QGridLayout()

# METHODS
def buttonClick():
    sys.exit()

def catchCommand(text_command):
    if text_command == '/close' or text_command == '/exit':
        sys.ext()
    elif text_command == '/help':
        helpWindowInit()

class helpWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        ls_window.remove(self)
    
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.setWindowTitle('Help')
        self.setWindowIcon(window_icon)
        self.setStyleSheet('background: #303136;')

        self.setFixedSize(275, 225)

        # Text
        text = QLabel()
        text.setText("v. 0.0.1 \n258 \n\nThis software does not guarantee correct functioning. Loss of data at the user's end is not our responsibility.")
        text.setWordWrap(True)
        text.setStyleSheet("font-size: 13px; color: 'white'; background-color: '#363940'; border-radius: 10px; padding: 10px 10px;")

        grid.addWidget(text, 0, 0, 1 ,3)

        # Label
        self.label = QLabel()
        self.label.setStyleSheet("color: 'white'; font-size: 13px;")

        grid.addWidget(self.label, 2, 0, 1, 3)

        # Text Window
        self.input = QLineEdit()
        self.input.setStyleSheet(
            "*{color: 'white';" +
            "border: 2px solid '#404EED';" +
            "border-radius: 15px;" + 
            "background-color: '#404EED';" +
            "padding: 5px 5px;" +
            "font-size: 13px;}" +
            #"*:hover{background: '#4069ED'; color: 'white';}" +
            "*:focus{background: '#4069ED'; color: 'white';}"
            )
        self.input.textChanged.connect(self.label.setText)
        print(self.input.text())
        #self.input.returnPressed.connect(catchCommand(self.label.text))
        self.input.returnPressed.connect(self.quickSand)

        grid.addWidget(self.input, 3, 0, 1, 2)

        self.button = QPushButton('Close')
        self.button.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) # Set cursor to hand on mouseover
        self.button.setStyleSheet(
        "*{border: 2px solid '#42464E';" + 
        "border-radius: 15px;" +
        "background-color: '#42464E';" + 
        "font-size: 13px;" +
        "color : 'white';" +
        "padding: 5px 0px;" +
        "margin: 0px 0px;}" +
        "*:hover{background: '#db0000'; color: 'white';}"
        )

        self.button.clicked.connect(lambda:self.close())
        grid.addWidget(self.button, 3, 2, 1, 1)  # 1 row, 2 cols
    
    def quickSand(self):
        catchCommand(self.input.text())
        self.input.clear()

def helpWindowInit():
    isOpened = False
    for item in ls_window:
        if isinstance(item, helpWindow):
            isOpened = True
    if not isOpened:
        hh = helpWindow()
        ls_window.append(hh)    # THIS list APPEND needs to happen, otherwise the window
        # will not sit in the EXECUTION ORDER
        hh.show()

def windowInit(klass):
    isOpened = False
    for item in ls_window:
        if isinstance(item, klass):
            isOpened = True
    if not isOpened:
        window = klass()
        ls_window.append(window)
        window.show()

def helper():
    windowInit(helpWindow)

# IMAGE
image = QPixmap('slice1.png')
print(image.height)

scale = 0.27

image = image.scaled(scale * image.width(), scale * image.height(), transformMode=QtCore.Qt.SmoothTransformation)
logo = QLabel()
logo.setPixmap(image)
logo.setAlignment(QtCore.Qt.AlignCenter)
logo.setStyleSheet('margin-top: 10px;')
grid.addWidget(logo, 0, 0, 1, 2)

# BUTTON
button = QPushButton('Sign in to Google Account')
button.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) # Set cursor to hand on mouseover
button.setStyleSheet(
    "*{border: 2px solid '#404EED';" + 
    "border-radius: 15px;" +
    "background-color: '#404EED';" + 
    "font-size: 13px;"
    "color : 'white';" +
    "padding: 5px 0px;" +
    "margin: 0px 0px;}" +
    "*:hover{background: '#4069ED';}"
    )

grid.addWidget(button, 1, 0, 1, 2)  # 1 row, 2 cols

# BUTTON 2
button2 = QPushButton('Exit')
button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) # Set cursor to hand on mouseover
button2.setStyleSheet(
    "*{border: 2px solid '#42464E';" + 
    "border-radius: 15px;" +
    "background-color: '#42464E';" + 
    "font-size: 13px;" +
    "color : 'white';" +
    "padding: 5px 0px;" +
    "margin: 0px 0px;}" +
    "*:hover{background: '#db0000'; color: 'white';}"
    )
button2.clicked.connect(buttonClick)

grid.addWidget(button2, 2, 0)

# BUTTON 3
button3 = QPushButton('Help')
button3.setCursor(QCursor(QtCore.Qt.PointingHandCursor)) # Set cursor to hand on mouseover
button3.setStyleSheet(
    "*{border: 2px solid '#42464E';" + 
    "border-radius: 15px;" +
    "background-color: '#42464E';" + 
    "font-size: 13px;"
    "color : 'white';" +
    "padding: 5px 0px;" +
    "margin: 0px 0px;}" +
    "*:hover{background: '#4069ED'; color: 'white';}"
    )
    
button3.clicked.connect(lambda:windowInit(helpWindow))

grid.addWidget(button3, 2, 1)



#frame1()
window.setLayout(grid)  # Connect grid
window.show()
sys.exit(app.exec())
