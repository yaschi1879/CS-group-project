import streamlit as st
from c_support.a_api_functions import get_club_name_user_input

def handle_question_selection(question_template):
    
    col1, col2 = st.columns([4, 1])
    
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
    
    if question_template == "Are you currently playing for ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter my club name:")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:  # Prüfen, ob Eingabe existiert
                # gibt club id als liste zurück
                st.session_state.selected = [get_club_name_user_input(st.session_state.user_input)[0]]
                # gibt club namen zurück
                st.session_state.exact_input = get_club_name_user_input(st.session_state.user_input)[1]
                st.session_state.index = "club_id"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
                          
    elif question_template == "Are you currently playing in ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.selectbox(
            "Choose a league:",
            ["", "Premier League", "Bundesliga", "Serie A", 
             "La Liga", "Ligue 1", "Scottish Premiership", 
             "Liga Portugal", "Eredivisie (Netherlands)", "Jupiler Pro League (Belgium)",
             "Chance Liga (Czech Rupublic)", "SuperSport HNL (Croatia)"])
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [league_codes[st.session_state.user_input]]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "league_id"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
                
    elif question_template == "Do you come from ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter the name of the country")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "country"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
            
    elif question_template == "Did you use to play for ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter the name of a former club")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                # gibt alte club id als liste zurück
                st.session_state.selected = [get_club_name_user_input(st.session_state.user_input)[0]]
                # gibt alten club namen zurück
                st.session_state.exact_input = get_club_name_user_input(st.session_state.user_input)[1]
                st.session_state.index = "old_clubs_ids"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
    
    elif question_template == "Are you a ... winner?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.selectbox(
            "Choose a titel:",
            ["", "Top 5 League", "Champions League", "World Cup", "European Championship"]
        )
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "titels"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
            
    elif question_template == "Are you ... years old?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.slider("Age (Years):", min_value=15, max_value=45, value=(20, 25), step=1)
        age_list = list(range(st.session_state.user_input[0], st.session_state.user_input[1] + 1))
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = age_list
                if st.session_state.user_input[0] == st.session_state.user_input[1]:
                    st.session_state.exact_input = str(st.session_state.user_input[0])
                else:
                    st.session_state.exact_input = f"between {st.session_state.user_input[0]} and {st.session_state.user_input[1]}"
                st.session_state.index = "age"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
                
    elif question_template == "Is your position...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.selectbox(
            "Choose a main position:",
            ["Goalkeeper", "Defender", "Midfielder", "Striker"]
            )
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "main_position"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
                    
                    
    elif question_template == "Do you currently wear the shirt number ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter the shirt number")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.index = "shirt_number"
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
        
    elif question_template == "Are you ...cm tall?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.slider("Height (Centimeters):", min_value=150, max_value=220, value=(180, 185), step=1)
        height_list = list(range(st.session_state.user_input[0], st.session_state.user_input[1] + 1))
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = height_list
                if st.session_state.user_input[0] == st.session_state.user_input[1]:
                    st.session_state.exact_input = str(st.session_state.user_input[0])
                else:
                    st.session_state.exact_input = f"between {st.session_state.user_input[0]} and {st.session_state.user_input[1]}"
                st.session_state.index = "height"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        