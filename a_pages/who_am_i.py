import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Include the parent directory in the system path to access project modules
import streamlit as st
from b_game.d_game_initialize import initialize_original_player_list, initialize_game_variables, determine_next_turn
from b_game.a_game_logic import play_game

def who_am_i(): # Initialize session state variables if not already set
    if "users" not in st.session_state:
        st.session_state.users = {}
    if "points_total" not in st.session_state:
        st.session_state.points_total = {}
    if "points_history" not in st.session_state:
        st.session_state.points_history = {}
    if "rounds" not in st.session_state:
        st.session_state.rounds = {}
    if "player_turn" not in st.session_state:
        st.session_state.player_turn = None
    if "current_turn_index" not in st.session_state:
        st.session_state.current_turn_index = 0
    if "turn_order" not in st.session_state:
        st.session_state.turn_order = []

    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        
    if st.session_state.game_started == False:
        # Welcome screen before the game starts
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display the game logo
            image_path = os.path.join("a_pages", "pictures", "logo.png")
            st.image(image_path, width=200)
            
        with col2:
            st.title("Welcome to the Game!")
        
        # Initialize the player list
        if "original_player_list" not in st.session_state or not st.session_state.original_player_list:
            with st.spinner("Generating player list... ⚽"):
                initialize_original_player_list()
            st.success("🎉 Player list successfully generated!")
            
        if "current_player_list" not in st.session_state:
            st.session_state.current_player_list = st.session_state.original_player_list.copy()
    
        # Reset game points and rounds for all users
        st.session_state.points_total = {key: 0 for key in st.session_state.points_total}
        st.session_state.points_history = {key: [] for key in st.session_state.points_total}
        st.session_state.rounds = {key: 0 for key in st.session_state.points_total}
        
        
        # Difficulty selection
        difficulty = st.selectbox(
            "Select Difficulty:",
            ("Select difficulty...", "Random", "Easy", "Medium", "Hard"),
            index=0,
            placeholder="Select a difficulty level...",
            )

        if not st.session_state.users:
            st.warning("Please add users on the home page to proceed")
            
        if difficulty == "Select Difficulty...":
            st.warning("Please select a difficulty level to proceed.")
        else:
            st.success(f"Click on the button below to start the game with difficulty: {difficulty}")
            st.session_state.difficulty = difficulty
        
        # Checking if Button was clicked 
        if st.button("Start Game") and difficulty != "Select Difficulty..." and st.session_state.users:
            # Set the game as started
            st.session_state.current_turn_index = 0
            initialize_game_variables()
            determine_next_turn()
            st.session_state.game_started = True
            # Refresh the page
            st.rerun()
    
    
    if st.session_state.game_started == True:
        # Gameplay screen
        play_game()