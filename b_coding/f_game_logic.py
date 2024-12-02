import streamlit as st
import random
from b_coding.e_game_functions import ask_user_for_question, process_question, guess_player
from b_coding.c_filter_criteria import check_player_criteria

def play_game(original_player_list, difficulty):
    # Game variables
    points = 50
    lives = 3
    points_deduction_wrong = 2
    points_deduction_correct = 1
    current_player_list = original_player_list
    selected_player = False
    
    while not selected_player:
        player = random.choice(current_player_list)
        if check_player_criteria(player, difficulty):
            selected_player = player
        else:
            current_player_list.remove(player)
    
    st.session_state["current_player"] = selected_player
    
    while points > 0 and lives > 0:
        question_index, user_input = ask_user_for_question()
        is_correct = process_question(current_player_list, question_index, user_input)

        if not is_correct:
            points -= points_deduction_wrong
            st.write(f"\nNo!")
        elif is_correct:
            points -= points_deduction_correct
            st.write("\nCorrect!")

        st.write(f"\nPoints remaining: {points}, Lives remaining: {lives}")

        # Überprüfe, ob der Spieler raten will
        lives, game_won, game_lost = guess_player(selected_player, lives)

        if game_won:
            st.session_state["points"] = points
            st.session_state["lives"] = lives
            return True  # Spieler erraten, Spiel gewonnen

        if game_lost:
            st.session_state["points"] = points
            st.session_state["lives"] = lives
            return False  # Spiel verloren