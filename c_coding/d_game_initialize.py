import streamlit as st
from c_coding.a_api_functions import get_club_players

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
    st.session_state.original_player_list = generate_player_list(club_list_test)
# wichtig: momentan erst die test liste
    
def initialize_game_variables():
    st.session_state.current_player_list = st.session_state.original_player_list.copy()
    st.session_state.selected_player = None
    st.session_state.lives = 3
    st.session_state.points = 50
    st.session_state.guessed_players = []
    


