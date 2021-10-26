import os
dirname = os.path.dirname(__file__)

class Prefs():
    # VERSION INFO
    ver_nr = 'v0.97'

    # IMAGES

    images = {
        'img_logo': os.path.join(dirname, '../media/logo.png'),
        'img_logo_min': os.path.join(dirname, '../media/logo_min.png'),
        'img_g_logo': os.path.join(dirname, '../media/google_logo.png'),
        'icon_task_info': os.path.join(dirname, '../media/icon_task_info.png'),
        'icon_add': os.path.join(dirname, '../media/add.png'),
        'icon_info': os.path.join(dirname, '../media/info.png'),
        'icon_warning': os.path.join(dirname, '../media/warning.png'),
        'bar_close': os.path.join(dirname, '../media/bar_close.png'),
        'home_image': os.path.join(dirname, '../media/home_image.png'),
        'arrow_down': os.path.join(dirname, '../media/arrow_down.png'),
        'placeholder': os.path.join(dirname, '../media/slice4.png'),
        # FROM flaticon
        'algo_icon': os.path.join(dirname, '../media/algo_icon.png')   # @ Linector
    }

    # SAVING DIRECTORIES

    directory = {
        'tasks' : os.path.join(dirname, '../data/save_file.json'),
        'categories' : os.path.join(dirname, '../data/categories.json')
    }

    # STYLE SHEET
    style_sheets = {
        'general_window' : ("background: #303136;"),
        # Text
        'text' : ("font-size: 13px; color: 'white';" +
                    "border-radius: 10px;" +
                    " padding: 10px 10px;"),
        'text_tight' : ("font-size: 13px; color: 'white';" +
                    "border-radius: 10px;" +
                    " padding: 0px 0px;"),
        'text_title' : ("font-size: 16px; color: 'white';" +
                    "border-radius: 10px;" +
                    " padding: 0px 0px;"),
        'text_title_large': ("font-size: 24px; color: '#A5AAB9';" +
                       "border-radius: 10px;" +
                       " padding: 0px 10px;"),
        'text_title_mute': ("font-size: 16px; color: '#5b606b';" +
                       "border-radius: 10px;" +
                       " padding: 0px 0px;"),
        'text_mute' : ("font-size: 13px; color: '#A0A0A0';" +
                    "border-radius: 10px;" +
                    " padding: 10px 10px;"),
        'text_mute_tight': ("font-size: 13px; color: '#A0A0A0';" +
                      "border-radius: 10px;" +
                      " padding: 0px 0px;"),
        'text_bubble' : ("font-size: 13px; color: 'white';" +
                    "background-color: '#363940'; border-radius: 10px;" +
                    " padding: 15px 15px;"),
        'text_bubble_slim': ("font-size: 13px; color: 'white';" +
                        "background-color: '#363940'; border-radius: 10px;" +
                        " padding: 10px 15px;"),
        'text_bubble_clear' : ("font-size: 13px; color: '#B9BBBE';" +
                    "border-radius: 10px;" +
                    " padding: 15px 5px;"),
        'text_bubble_clear_slim': ("font-size: 13px; color: '#B9BBBE';" +
                              "border-radius: 10px;" +
                              " padding: 5px 5px;"),
        'text_bubble_title' : ("font-size: 16px; color: 'white';" +
                    "background-color: '#27282C'; border-radius: 10px;" +
                    " padding: 10px 10px;"),
        'text_bubble_alert' : ("font-size: 13px; color: 'white';" +
                    "background-color: '#ff3643'; border-radius: 10px;" +
                    " padding: 10px 10px;"),
        'text_bubble_dark' : ("font-size: 13px; color: 'white';" +
                    "background-color: '#27282C'; border-radius: 10px;" +
                    " padding: 10px 10px;"),
        # LineEdit
        'fill_line' : ("*{font-size: 13px; color: 'white';" +
                    "background-color: '#363940'; border-radius: 10px;" +
                    "border: 2px solid '#222429';" + 
                    " padding: 5px 10px;}" + 
                    "*:focus{border: 2px solid '#404EED';}"),       
        # Buttons
        'button_priority' : (
                    "*{border: 2px solid '#404EED';" + 
                    "border-radius: 15px;" +
                    "background-color: '#404EED';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED';}"
                    ),
        'button_disabled_rect': (
                "*{border: 2px solid '#18191B';" +
                "border-radius: 5px;" +
                "background-color: '#18191B';" +
                "font-size: 13px;"
                "color : '#575C6B';" +
                "padding: 5px 0px;" +
                "margin: 0px 0px;}" +
                "*:hover{background: '#30333D';}"
        ),
        'button_priority_rect' : (
                    "*{border: 2px solid '#404EED';" + 
                    "border-radius: 5px;" +
                    "background-color: '#404EED';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED';}"
                    ),
        'button_low_priority_rect' : (
                    "*{border: 2px solid '#42464E';" +
                    "border-radius: 5px;" +
                    "background-color: '#42464E';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED'; color: 'white';}"
                    ),
        'button_low_priority' : (
                    "*{border: 2px solid '#42464E';" + 
                    "border-radius: 15px;" +
                    "background-color: '#42464E';" + 
                    "font-size: 13px;"
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED'; color: 'white';}"
                    ),
        'button_exit' : (
                    "*{border: 2px solid '#42464E';" + 
                    "border-radius: 15px;" +
                    "background-color: '#42464E';" + 
                    "font-size: 13px;" +
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#db0000'; color: 'white';}"
                    ),
        'button_exit_rect' : (
                    "*{border: 2px solid '#42464E';" + 
                    "border-radius: 5px;" +
                    "background-color: '#42464E';" + 
                    "font-size: 13px;" +
                    "color : 'white';" +
                    "padding: 5px 0px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#db0000'; color: 'white';}"
                    ),
        # Burger menu buttons
        'button_prio_burger' : (
                    "*{border-radius: 2px;" +
                    "font-size: 14px;"
                    "color : 'white';" +
                    "padding: 10px 5px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#363940';" +
                    "border-radius: 5px;" +
                    "border: 2px solid '#42464E';}" 
                    ),
        'button_low_prio_burger' : (
                    "*{border: 2px solid '#42464E';" + 
                    "border-radius: 15px;" +
                    "background-color: '#42464E';" + 
                    "font-size: 16px;"
                    "color : 'white';" +
                    "padding: 5px 25px;" +
                    "margin: 0px 0px;}" +
                    "*:hover{background: '#4069ED';}"
                    ),
        # Special Home Buttons
        'home_special': (
                "*{border-radius: 2px;" +
                "font-size: 14px;"
                "color : 'white';" +
                "padding: 10px 5px;" +
                "margin: 0px 0px;}" +
                "*:hover{background: '#363940';" +
                "border-radius: 5px;" +
                "border: 2px solid '#42464E';}"
        ),
        # GroupBoxes
        'std_gbox' : (
            "*:title{color : 'white';}"
            # "*{border : 2px solid 'black';}"
        )
    }

