# We hereby declare that the vast majority of the code for this project has been written by us independently. 
# We have utilized ChatGPT as a tool for conceptual purposes and for assistance with small, 
# specific parts of the code, such as generating comments or clarifying implementation ideas.
# However, all critical design decisions, core functionality, 
# and the implementation of the primary codebase were developed through our own efforts and understanding.

# This is Link for the Game application: https://cs-group-project-8c9afmnnkpup2ze7c3yxvo.streamlit.app/
# our GitHub: https://github.com/yaschi1879/CS-group-project

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Include the parent directory in the system path to access project modules
import streamlit as st
from b_game.d_game_initialize import initialize_original_player_list, initialize_game_variables, determine_next_turn
from b_game.a_game_logic import play_game

def who_am_i(): 
    # Initialize session state variables if not already set
    # This process ensures that when a users directly opens this page while skipping the home page, no error code appears
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

    # this is an important game control variable
    # if the value is false, the user is on the welcome screen of the game
    # if the value is set to true, the actual game starts
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        
    if st.session_state.game_started == False:
        # Welcome screen before the game starts
        # If the user chooses to reset the game, the user will be guided back to this page
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display the game logo
            image_path = os.path.join("a_pages", "pictures", "logo.png")
            st.image(image_path, width=200)
            
        with col2:
            st.title("Welcome to the Game!")
        
        # Initialize the player list
        # This list contains all players of the top 40 clubs, it should have arleady been initialized on the home page
        if "original_player_list" not in st.session_state or not st.session_state.original_player_list:
            with st.spinner("Generating player list... ⚽"):
                initialize_original_player_list()
            st.success("🎉 Player list successfully generated!")
        
        
        if "current_player_list" not in st.session_state:
            st.session_state.current_player_list = []
        # This is a copy of the original player list
        # Once a player is choosen for the game, the player will be omitted from the list
        # If the player resets the game, the player list will be reseted too
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

        # The two if statements below ensure, that all variables needed for the game are correctly allocated with a value
        if not st.session_state.users:
            st.warning("Please add users on the home page to proceed")
            
        if difficulty == "Select Difficulty...":
            st.warning("Please select a difficulty level to proceed.")
        else:
            st.success(f"Click on the button below to start the game with difficulty: {difficulty}")
            st.session_state.difficulty = difficulty
        
        # Checking if Button was clicked and all the variables are set correctly
        if st.button("Start Game") and difficulty != "Select Difficulty..." and st.session_state.users:
            # Initialize all necessary varialbes, go to c_support.d_game_initalize for further details
            st.session_state.current_turn_index = 0
            initialize_game_variables()
            determine_next_turn()
            st.session_state.game_started = True
            # Refresh the page
            # This time the user will be guided to the if statement below since game_started is now True
            st.rerun()
    
    
    if st.session_state.game_started == True:
        # Gameplay screen
        # Attention, the function below is defined on b_game.a_game_logic -> go there to continue
        play_game()