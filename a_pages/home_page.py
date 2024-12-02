import streamlit as st
from b_utils.d_game_initialize import initialize_player_lists, generate_player_list, club_list_test

st.title("Welcome to Who am I?")
st.write("Start the game by navigating to the game page.")



# alles (von anfang an, bis hier) vor dem strich kann verändert werden
# ---------------------------------------------------------------------------------------
# ab hier nicht rauslöschen, ist wichtig fürs spiel, muss ganz am ende der seite sein
initialize_player_lists()
if not st.session_state["original_player_list"]:
    st.warning("The player list has not been generated yet. Generating now...")
    st.session_state["original_player_list"] = generate_player_list(club_list_test)
    st.success("The player list was successfully generated!")
original_player_list = st.session_state["original_player_list"]