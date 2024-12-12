import sys
import os

# Add the parent directory to the system path so Python can find other modules in the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from c_support.a_api_functions import get_club_players

# List of club IDs used to generate player lists
club_list = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]


def generate_player_list(list):
    # Generates a list of players by retrieving all players playing for the club for each club in the provided list
    player_list = []
    for club in list:
        # function below is defined on c_support.a_api_functions
        players = get_club_players(club) 
        # Add players to the cumulative list
        player_list.extend(players) 
    return player_list
    

def initialize_original_player_list():
    # Initializes the original player list in the session state
    st.session_state.original_player_list = generate_player_list(club_list)
    
def initialize_game_variables():
    # Sets initial values for game-related variables in the session state
    # all variables with value False are used for game control
    st.session_state.show_solution = False
    st.session_state.change_difficulty = False
    st.session_state.check = False
    st.session_state.question_procedure = False
    st.session_state.solution_true = False
    st.session_state.ml_question = False
    st.session_state.ml_clicked = False
    
    st.session_state.lives = 3 # Number of lives the player starts with
    st.session_state.points = 50 # Starting points for the player
    st.session_state.selected_player = [] # Selected player during the game
    st.session_state.player_data = {} # Stores data of selected players
    st.session_state.questions = [] # List of questions for the game
    st.session_state.selected = [] # Tracks selected items in the game
    st.session_state.index = [] # Tracks indices of selections
    st.session_state.exact_input = [] # Tracks exact user inputs
    st.session_state.user_input = [] # Tracks user inputs
  
    
def determine_next_turn():
    # Determines the next player's turn in the game
    st.session_state.turn_order = list(st.session_state.users.keys())
    # Set the next player based on the current turn index
    next_index = st.session_state.current_turn_index % len(st.session_state.turn_order)
    st.session_state.player_turn = st.session_state.turn_order[next_index]
    
   # Update the index for the next round
    st.session_state.current_turn_index += 1
