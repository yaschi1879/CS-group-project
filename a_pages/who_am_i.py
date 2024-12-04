import streamlit as st
import os
from b_game.d_game_initialize import initialize_original_player_list, initialize_game_variables, initialize_question_variables
from b_game.a_game_logic import play_game

def who_am_i():
 
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        
    if st.session_state.game_started == False:
        # Startseite
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Anzeige des Logos
            image_path = os.path.join("a_pages", "pictures", "logo.png")
            st.image(image_path, width=200)
            
        with col2:
            st.title("Welcome to the game!")
        
        # Spiel Initialisierung
        if "original_player_list" not in st.session_state or not st.session_state.original_player_list:
            with st.spinner("Generating player list... ⚽"):
                initialize_original_player_list()
            st.success("🎉 Player list successfully generated!")
            
        if "current_player_list" not in st.session_state:
            st.session_state.current_player_list = st.session_state.original_player_list.copy()
        
        if "points_achieved" not in st.session_state:
            st.session_state.points_achieved = 0
        
        # Schwierigkeitsauswahl
        difficulty = st.selectbox(
            "Select Difficulty:",
            ("Select Difficulty...", "None", "Easy", "Medium", "Hard"),
            index=0,
            placeholder="Select a difficulty level...",
        )

        if difficulty == "Select Difficulty...":
            st.warning("Please select a difficulty level to proceed.")
        else:
            st.success(f"Click on the button below to start the game with difficulty: {difficulty}")
            st.session_state.difficulty = difficulty
        
        # Überprüfe, ob der Button gedrückt wurde
        if st.button("Lets play the game?"):
            # Setze den Zustand, dass das Spiel gestartet wurde
            initialize_game_variables()
            initialize_question_variables()
            st.session_state.game_started = True
            # aktualisieren der seite
            st.rerun()
    
    if st.session_state.game_started == True:
        # Spielseite
        st.title("Game in progress")
        play_game()