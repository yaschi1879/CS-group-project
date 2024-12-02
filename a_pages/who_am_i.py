import streamlit as st
from b_utils.d_game_initialize import initialize_player_lists

st.title("Who Am I?")
st.write("This is the game page where you will guess the player.")

initialize_player_lists()
if not st.session_state["current_player_list"]:
    st.session_state["current_player_list"] = st.session_state["original_player_list"].copy()

difficulty = st.selectbox("Select Difficulty", options=["none", "easy", "medium", "difficult"])

if st.button("Start Game"):
    players = get_player_list(difficulty)
    selected_player = start_game(players, difficulty)
    st.session_state.selected_player = selected_player
    st.write("Game has started with player:", selected_player['name'])