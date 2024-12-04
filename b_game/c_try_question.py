import streamlit as st
def handle_question_selection(question_template, col1, col2):
    click = None
    
    if question_template == "Are you currently playing for ...?":
        st.session_state.user_input = col1.text_input("Enter my club name:")
    
    click = st.button("Confirm")
        
    if click:
        if st.session_state.user_input:  # Prüfen, ob Eingabe existiert
            st.session_state.question_procedure = False
        else:
            st.warning("Please enter an input before confirming.")
        
    
    
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        