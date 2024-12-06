import streamlit as st
from c_support.a_api_functions import get_club_name_user_input
def handle_question_selection(question_template):
    col1, col2 = st.columns([4, 1])
    
    if question_template == "Are you currently playing for ...?":
        with col1:
            st.session_state.user_input = col1.text_input("Enter my club name:")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:  # Prüfen, ob Eingabe existiert
                # gibt club id als liste zurück
                st.session_state.selected = list(get_club_name_user_input(st.session_state.user_input)[0])
                # gibt club namen zurück
                st.session_state.exact_input = get_club_name_user_input(st.session_state.user_input)[1]
                st.session_state.index = "club_id"
                st.session_state.question_procedure = False
                st.session_state.check = True
                st.rerun()
            else:
                st.warning("Please enter an input before confirming.")
        
    
    
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        