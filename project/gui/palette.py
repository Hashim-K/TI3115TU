class Prefs():
    # IMAGES

    images = {
        'img_logo' : 'gui/media/logo.png',
        'img_logo_min' : 'gui/media/logo_min.png',
        'img_g_logo' : 'media/google_logo.png',
        'bar_close' : 'media/bar_close.png',
        # FROM flaticon
        'algo_icon' : 'media/algo_icon.png'   # @ Linector
    }

    # SAVING DIRECTORIES

    directory = {
        'tasks' : ''
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
        'text_mute' : ("font-size: 13px; color: '#A0A0A0';" +
                    "border-radius: 10px;" +
                    " padding: 10px 10px;"),
        'text_bubble' : ("font-size: 13px; color: 'white';" +
                    "background-color: '#363940'; border-radius: 10px;" +
                    " padding: 15px 15px;"),
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
        # GroupBoxes
        'std_gbox' : (
            "*:title{color : 'white';}"
            # "*{border : 2px solid 'black';}"
        )
    }

