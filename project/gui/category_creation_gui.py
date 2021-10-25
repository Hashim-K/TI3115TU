import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QApplication, QLineEdit, QPushButton, QHBoxLayout, \
    QColorDialog

from project.BackEnd import Category
from project.gui import palette, dialog_window_gui
from project.gui.general_window_gui import GeneralWindow


class CategoryCreationWindow(GeneralWindow):

    def __init__(self, window_list, prefs):
        super().__init__(window_list, prefs)

        self.hex_col_selected = '#FFFFFF'

    def init_ui(self):
        # WINDOW
        self.setWindowTitle(f'Create Category')
        self.setFixedWidth(300)
        self.setStyleSheet(self.prefs.style_sheets['general_window'])

        icon = QIcon(self.prefs.images['icon_add'])
        self.setWindowIcon(icon)

        # Layout
        main_layout = QVBoxLayout()
        sub_layout = QFormLayout()
        sub_layout.setSpacing(20)

        # Main Layout Elements
            # Title
        title = QLabel('Create New Category')
        title.setContentsMargins(10, 0, 0, 5)
        title.setStyleSheet(self.prefs.style_sheets['text_title'])
        main_layout.addWidget(title)

            # Description
        description = "The colour will be used as an identifier for the " \
                      "tasks that get assigned to this category."
        desc = QLabel(description)
        desc.setWordWrap(True)
        desc.setStyleSheet(self.prefs.style_sheets['text_bubble'])
        main_layout.addWidget(desc)

        # Sub Layout Elements
        title = QLabel('Title')
        title.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])
        self.title_edit = QLineEdit(self)
        self.title_edit.setStyleSheet(self.prefs.style_sheets['fill_line'])
        sub_layout.addRow(title, self.title_edit)

        colour = QLabel('Colour')
        colour.setStyleSheet(self.prefs.style_sheets['text_mute_tight'])

        # Colour Row Sublayout
        colour_right_layout = QHBoxLayout()
        colour_button = QPushButton('Pick Colour')
        colour_button.setFixedWidth(125)
        colour_button.setStyleSheet(self.prefs.style_sheets['button_low_priority_rect'])
        colour_button.clicked.connect(self.change_colour)
        colour_right_layout.addWidget(colour_button)

        self.colour_piece = QPushButton('')
        self.colour_piece.setFixedWidth(75)
        colour_right_layout.addWidget(self.colour_piece)
        self.colour_piece.setText('#FFFFFF')
        temp_sheet = (
                "*{border: 2px solid '#FFFFFF';" +
                "border-radius: 5px;" +
                "background-color: '#FFFFFF';" +
                "font-size: 13px;"
                "color : rgba(0,0,0,0);" +
                "padding: 5px 0px;" +
                "margin: 0px 0px;}" +
                "*:hover{color: 'black';}"
        )
        self.colour_piece.setStyleSheet(temp_sheet)

        sub_layout.addRow(colour, colour_right_layout)

        sub_layout.setContentsMargins(10, 10, 0, 10)    # Rows margins

        # Add Button
        add_button = QPushButton('Add')
        add_button.setStyleSheet(self.prefs.style_sheets['button_priority_rect'])
        add_button.clicked.connect(self.make_category)

        main_layout.addLayout(sub_layout)
        main_layout.addWidget(add_button)
        self.setLayout(main_layout)

    def make_category(self):
        # Get Categories for Comparison
        existing_categories = Category.import_category(self.prefs.directory['categories'])
        # Check for existence
        current_name = self.title_edit.text()
        id_of_found = None    # For overwriting old one

        for category in existing_categories:
            if category.title == current_name:
                id_of_found = category.category_id
                break

        # CHANGE: To Edit Old
        if id_of_found is not None:     # If Already exists
            dialog = dialog_window_gui.CustomDialog('Task with name already exists, override?', self.prefs, self)
            if dialog.exec():
                # Delete category
                Category.delete_category(self.prefs.directory['categories'], id_of_found)
            else:
                return  # Stop making category
        # Create
        category = Category.Category(
            -1, self.title_edit.text(), self.hex_col_selected, self.prefs.directory['categories'])
        # Export
        category.export_category(self.prefs.directory['categories'])

    def change_colour(self):
        # Get Colour & Store
        color = QColorDialog.getColor()
        self.hex_col_selected = color.name()
        # Change Preview
        self.colour_piece.setText(color.name())
        new_sheet = (
                "*{border: 2px solid '"+color.name()+"';" +
                "border-radius: 5px;" +
                "background-color: '"+color.name()+"';" +
                "font-size: 13px;"
                "color : rgba(0,0,0,0);" +
                "padding: 5px 0px;" +
                "margin: 0px 0px;}" +
                "*:hover{color: 'black';}"
        )
        self.colour_piece.setStyleSheet(new_sheet)

# FOR TESTING
def window():
    app = QApplication(sys.argv)
    win = CategoryCreationWindow([], palette.Prefs)

    sys.exit(app.exec())

window()