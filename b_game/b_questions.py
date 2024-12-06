from c_support.a_api_functions import get_club_name_user_input
import streamlit as st

def handle_question_selection(question_template, col1, col2):
    
    league_codes = {
    "Premier League": "GB1",
    "Bundesliga": "L1", 
    "Serie A": "IT1", 
    "La Liga": "ES1", 
    "Ligue 1": "FR1", 
    "Scottish Premiership": "SC1",
    "Liga Portugal": "PO1",
    "Eredivisie": "NL1", 
    "Jupiler Pro League": "BE1", # Belgische Liga
    "Chance Liga": "TS1", # Tschechische Liga
    "SuperSport HNL": "KR1", # Kroatische Liga
    }
    
    
    # je nachdem, welche frage im who_am_i ausgwählt wurde, wird der user jetzt zu input aufgefordert
    
    if question_template == "Are you currently playing for ...?":
        st.session_state.user_input = col1.text_input("Enter my club name:")
        st.session_state.question_state["current_club"] = current_club
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if current_club:
            st.write("if passt")
            st.session_state.question_state["current_club"] = current_club
        
        if st.session_state.confirmed and current_club:
            st.write("2. if psst")
        # !!!!!!!!!!!!!!! das muss zwischen drin jetzt für jede frage gemacht werden mit anderem Confirm ... !!!!
            # gibt club id als liste zurück
            st.session_state.selected = list(get_club_name_user_input(current_club)[0])
            # gibt club namen zurück
            st.session_state.exact_input = get_club_name_user_input(current_club)[1]
            st.session_state.index = "club_id"
            st.write(f"hier: {st.session_state.exact_input}")
        
        
    elif question_template == "Are you currently playing in ...?":
        league = col1.selectbox(
            "Choose a league:",
            ["Premier League", "Bundesliga", "Seria A", "La Liga", "Ligue 1"]
        )
        # !!!!!!!!!!!!!!!!!!!!!! hier alle Ligen der Top 40 Clubs !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if league:
            selected = [league_codes[league]]
            exact_input = league
            index = "league_id"
            

    elif question_template == "Do you come from ...?":
        nationality = col1.text_input("Enter the name of the country")
        if nationality:
            selected = [nationality]
            exact_input = nationality
            index = "country"

    elif question_template == "Did you use to play for ...?":
        past_club = col1.text_input("Enter the name of a former club")
        if past_club:
            # gibt alte club id als liste zurück
            selected = list(get_club_name_user_input(past_club)[0])
            # gibt alten club namen zurück
            exact_input = get_club_name_user_input(past_club)[1]
            index = "old_clubs_ids"

    elif question_template == "Are you a ... winner?":
        achievements = col1.selectbox(
            "Choose a titel:",
            ["Top 5 League", "Champions League", "World Cup", "European Championship"]
        )
        if achievements:
            selected = achievements
            exact_input = achievements
            index = "titels"

    elif question_template == "Are you ... years old?":
        age_range = col1.slider("Age (Years):", min_value=15, max_value=45, value=(20, 25), step=1)
        age_list = list(range(age_range[0], age_range[1] + 1))
        if age_list:
            selected = age_list
            exact_input = f"between {age_range[0]} and {age_range[1]}"
            index = "age"

    elif question_template == "Do you play as a ...?":
        
        # Schritt 1: Hauptposition auswählen
        main_position = col1.selectbox(
        "Choose a main position:",
        ["Goalkeeper", "Defender", "Midfielder", "Striker"]
        )
        index = "classified_position"
        selected = [main_position]
        exact_input = main_position
        
        # Schritt 2: Spezialisierung basierend auf der Hauptposition
        if main_position == "Defender":
            specific_position = col2.selectbox(
                "Optional: Choose a specific position for Defender:",
                ["", "Left Back", "Center Back", "Right Back"]
            )
            if specific_position:
                index = "position"
                selected = [specific_position]
                exact_input = specific_position

        elif main_position == "Midfielder":
            specific_position = col2.selectbox(
                "Optional: Choose a specific position for Midfielder:",
                ["", "Defensive Midfielder", "Offensive Midfielder", "Right Midfielder", "Left Midfielder"]
            )
            if specific_position:
                index = "position"
                selected = [specific_position]
                exact_input = specific_position

        elif main_position == "Striker":
            specific_position = col2.selectbox(
                "Optional: Choose a specific position for Striker:",
                ["", "Left Wing", "Right Wing", "Center Forward"]
            )
            if specific_position:
                index = "position"
                selected = [specific_position]
                exact_input = specific_position
        # !!!!!!! muss noch mit API abgestimmt werden !!!!!!!!

    elif question_template == "Do you currently wear the shirt number ...?":
        shirt_number = col1.text_input("Enter the shirt number")
        selected = [shirt_number]
        index = "shirt_number"
        exact_input = shirt_number
        
    elif question_template == "Are you ...cm tall?":
        height_range = col1.slider("Height (Centimeters):", min_value=150, max_value=220, value=(180, 185), step=1)
        height_list = list(range(height_range[0], age_range[1] + 1))
        selected = height_list
        index = "height"
        exact_input = f"between {height_range[0]} and {height_range[1]}"
    
    