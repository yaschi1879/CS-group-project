import streamlit as st
from c_coding.a_api_functions import get_club_name_user_input, get_league_name_user_input

def handle_question_selection(question_template, col2):
    selected = None
    
    # je nachdem, welche frage im who_am_i ausgwählt wurde, wird der user jetzt zu input aufgefordert
    
    if question_template == "Are you currently playing for ...":
        current_club = col2.text_input("Enter my club name:")
        selected = get_club_name_user_input(current_club)
        # gibt club id zurück
        
    elif question_template == "Are you currently playing in ...":
        league = col2.text_input("Enter the name of the league")
        league_choices = get_league_name_user_input(league)
        if league_choices == False:
            st.error("League not found, try again.")
        else:
            country = col2.selectbox("Select the country corresponding to your desired league", list(league_choices.keys()), index=0)
            # die api gibt für einen liga namen mehrere länder zurück, z.B. für SuperLeague -> Schweiz, Türkei, etc
            # hier kann dann das korrekte land in einer selectbox ausgewählt werden
        selected = league_choices[country]

    elif question_template == "Do you come from ...":
        nationality = col2.text_input("Enter the name of the country")
        selected = nationality

    elif question_template == "Did you use to play for ...":
        past_club = col2.text_input("Enter the name of a former club")
        club = get_club_name_user_input(past_club)
        selected = club

    elif question_template == "Are you a ... winner":
        achievements = col2.selectbox(
            "Choose a titel:",
            ["Top 5 League", "Champions League", "World Cup", "European Championship"]
        )
        selected = achievements

    elif question_template == "Are you older than ...":
        age = col2.slider("Age (Years):", min_value=15, max_value=45, value=30, step=1)
        selected = f"older than {age}"

    elif question_template == "Are you younger than ...":
        age = col2.slider("Age (Years):", min_value=15, max_value=45, value=30, step=1)
        selected = f"younger than {age}"

    elif question_template == "Do you play as a ...":
        # Schritt 1: Hauptposition auswählen
        main_position = col2.selectbox(
        "Choose a main position:",
        ["GK", "Defender", "Midfielder", "Striker"]
        )

        # Schritt 2: Spezialisierung basierend auf der Hauptposition
        if main_position == "Defender":
            specific_position = col2.selectbox(
                "Optional: Choose a specific position for Defender:",
                ["", "Left Back", "Center Back", "Right Back"]
            )
            selected = specific_position if specific_position else main_position

        elif main_position == "Midfielder":
            specific_position = col2.selectbox(
                "Optional: Choose a specific position for Midfielder:",
                ["", "Defensive Midfielder", "Offensive Midfielder", "Right Midfielder", "Left Midfielder"]
            )
            selected = specific_position if specific_position else main_position

        elif main_position == "Striker":
            specific_position = col2.selectbox(
                "Optional: Choose a specific position for Striker:",
                ["", "Left Wing", "Right Wing", "Center Forward"]
            )
            selected = specific_position if specific_position else main_position

        # !!!!!!! muss noch mit API abgestimmt werden !!!!!!!!

        else:
            # Für Goalkeeper keine weitere Auswahl
            selected = main_position

    elif question_template == "Do you currently wear the shirt number ... ":
        shirt_number = col2.selectbox(
            "Choose a shirt number range:",
            ["Under 20", "20-30", "Over 30"]
        )
        selected = shirt_number

    elif question_template == "Are you taller than ...":
        height = col2.slider("Height (cm):", min_value=150, max_value=220, value=185, step=1)
        selected = f"taller than {height} cm"

    elif question_template == "Are you shorter than ...":
        height = col2.slider("Height (cm):", min_value=150, max_value=220, value=185, step=1)
        selected = f"shorter than {height} cm"

    return selected
    # user input wird zurückgegeben in der variable selected