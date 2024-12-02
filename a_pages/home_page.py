import streamlit as st
from b_utils.d_game_initialize import initialize_player_lists, generate_player_list, club_list_test

st.title("Welcome to Who am I?")
st.write("Start the game by navigating to the game page.")

initialize_player_lists()

if not st.session_state["original_player_list"]:
    st.session_state["original_player_list"] = generate_player_list(club_list_test)
    st.write("Player list generated!")
else:
    st.write("Player list already initialized.")
