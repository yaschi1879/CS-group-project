import streamlit as st
from b_utils.d_game_initialize import initialize_player_lists, generate_player_list, club_list_test

initialize_player_lists()
if not st.session_state["original_player_list"]:
    st.warning("The player list has not been generated yet. Generating now...")
    st.session_state["original_player_list"] = generate_player_list(club_list_test)
    st.success("The player list was successfully generated!")   
original_player_list = st.session_state["original_player_list"]
# nicht rauslöschen, ist wichtig fürs spiel, muss ganz am anfang der seite sein
# ---------------------------------------------------------------------------------------

# ab hier kann alles verändert werden
st.title("Who Am I?")
st.write("This is the game page where you will guess the player.")

# irgendwo brauch es eines selectbox für difficulty, so etwa wie diese
difficulty = st.selectbox("Select Difficulty", options=["none", "easy", "medium", "hard"])

# irgendwo brauch es einen button start playing, so etwa wie diesen
start_button = st.button("Start Playing")

if start_button:
    st.write(f"Starting the game with difficulty: {difficulty}")
    start_game(original_player_list, difficulty)  # Starte das Spiel mit der ausgewählten Schwierigkeit
