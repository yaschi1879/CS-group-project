import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from c_support.a_api_functions import get_club_players

club_list = [281, 418, 27, 31, 12, 583, 16, 631, 46, 1050, 15, 985, 131, 294, 720, 
            13, 23826, 379, 800, 11, 506, 5, 610, 6195, 2282, 398, 24, 368, 124, 
            234, 681, 383, 336, 62, 244, 1082, 419, 430, 1090, 148]

club_list_test = [281, 418, 27, 31, 12]


def generate_player_list(list):
    player_list = []
    for club in list:
        players = get_club_players(club)
        player_list.extend(players)
    return player_list
    

def initialize_original_player_list():
    #st.session_state.original_player_list = generate_player_list(club_list_test)
    [581678, 42205]
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
def initialize_game_variables():
    st.session_state.show_solution = False
    st.session_state.change_difficulty = False
    st.session_state.check = False
    st.session_state.question_procedure = False
    st.session_state.solution_true = False
    st.session_state.ml_question = False
    st.session_state.ml_clicked = False
    st.session_state.lives = 3
    st.session_state.points = 50
    st.session_state.selected_player = []
    st.session_state.player_data = {}
    st.session_state.questions = []
    st.session_state.selected = []
    st.session_state.index = []
    st.session_state.exact_input = []
    st.session_state.user_input = []
  
    
def determine_next_turn():
    st.session_state.turn_order = list(st.session_state.users.keys())
    # Setze den nächsten Spieler basierend auf dem aktuellen Index
    next_index = st.session_state.current_turn_index % len(st.session_state.turn_order)
    st.session_state.player_turn = st.session_state.turn_order[next_index]
    
    # Aktualisiere den Index für die nächste Runde
    st.session_state.current_turn_index += 1
