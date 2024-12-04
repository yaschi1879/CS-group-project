import streamlit as st
def handle_question_selection(question_template, col1, col2):
    
    league_codes = {
    "Premier League": "GB1"
    # !!!!!!!!!!!!! hier noch vervollständigen !!!!!!!!!!!!!!!!!!!!!!!!!
    }
    
    
    # je nachdem, welche frage im who_am_i ausgwählt wurde, wird der user jetzt zu input aufgefordert
    
    if question_template == "Are you currently playing for ...?":
        st.session_state.user_input = col1.text_input("Enter my club name:")
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        