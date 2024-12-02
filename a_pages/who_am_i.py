import streamlit as st
from b_utils.d_game_initialize import initialize_player_lists

initialize_player_lists()
if not st.session_state["original_player_list"]:
    st.warning("The player list has not been generated yet. Generating now...")
    st.session_state["original_player_list"] = generate_player_list(club_list_test)
    st.success("The player list was successfully generated!")   
original_player_list = st.session_state["original_player_list"]
# nicht rauslöschen, ist wichtig fürs spiel, muss ganz am anfang der seite sein
# ---------------------------------------------------------------------------------------

difficulty = st.selectbox("Select Difficulty", options=["none", "easy", "medium", "difficult"])

if st.button("Start Game"):
    players = get_player_list(difficulty)
    selected_player = start_game(players, difficulty)
    st.session_state.selected_player = selected_player
    st.write("Game has started with player:", selected_player['name'])


def test():
    # Create a centered layout
    col1, col2, col3, col4, col5 = st.columns([3, 2, 3, 2, 3])  # The middle column takes up the majority of the space

    with col3:
        # Display the logo at the top of the page
        st.image("logo.png", width=200)

    if "questions" not in st.session_state:
        st.session_state.questions = []

    # Initialisiere Session-State für Leben und erratene Spieler
    if "lives" not in st.session_state:
        st.session_state.lives = 3  # Spieler startet mit 3 Leben
    if "guessed_players" not in st.session_state:
        st.session_state.guessed_players = []

    # Obere rechte Ecke: Lebensanzeige
    with col5:
        lives_display = "⚽" * st.session_state.lives + "❌ " * (3 - st.session_state.lives)
        st.write(lives_display)

    difficulty = st.selectbox(
    "Select Difficulty:",
    ("Select Difficulty...", "None", "Easy", "Medium", "Hard"),
    index=0,
    placeholder="Select a difficulty level...",
    )

    if difficulty == "Select Difficulty...":
        st.warning("Please select a difficulty level to proceed.")
    else:
        st.success(f"You selected: {difficulty}")

# Display questions only if a valid difficulty is selected !! 
# Implement the Conditions for the difficulty levels

# Indiz vor der ersten Frage. Wo?
# User muss auf dieser Seite irgendwie vorhanden sein; Spieler 1 ist an der Reihe... 

    # Erste Selectbox mit Fragen
    col1, col2, col3 = st.columns([2,2,1], vertical_alignment="bottom")

    with col1:
        question_template = st.selectbox(
            "Choose a question:",
            ["", 
            "I am currently playing for ...", 
            "I play in ...", "I am from ...", 
            "I used to play for ...", 
            "I am a ... winner", 
            "I am older than ...", 
            "I am younger than ...", 
            "I play as ...", 
            "I wear the shirt number ... at my current club", 
            "I am taller than ...", 
            "I am shorter than ..."]
        )

    # Weiterführende Auswahl von Kriterien durch if Funktion
    with col2:
        selected = None
        if question_template == "I am currently playing for ...":
            current_club = st.selectbox(
                "Choose my club:",
                ["", "Real Madrid", "Arsenal", "Liverpool"] #!!!!!
            )
            selected = current_club
            
        elif question_template == "I play in ...":
            league = st.selectbox(
                "Choose my league:",
                ["Premier League", "Bundesliga", "Eredivise", "LaLiga", "Serie A", "Ligue 1", "Liga Portugal", "Süper Lig", "Jupiler Pro League"]
            )
            selected = league

        elif question_template == "I am from ...":
            nationality = st.selectbox(
                "Choose my country:",
                ["Germany", "Switzerland", "Spain"]
            )
            selected = nationality

        elif question_template == "I used to play for ...":
            past_club = st.selectbox(
                "Choose a club:",
                ["Real Mardid", "Arsenal", "Liverpool"]
            )
            selected = past_club

        elif question_template == "I am a ... winner":
            achievements = st.selectbox(
                "Choose my achievements:",
                ["Top 5 league", "Champions League", "World Cup", "European championship", "Europa League"]
            )
            selected = achievements

        elif question_template == "I am older than ...":
            age = st.slider("",
                min_value=15, max_value=45, value=30, step=1
            )
            selected = f"older than {age}"

        elif question_template == "I am younger than ...":
            age = st.slider("",
                min_value=15, max_value=45, value=30, step=1
            )
            selected = f"younger than {age}"

        elif question_template == "I play as ...":
            position = st.selectbox(
                "Choose a position:",
                ["GK", "Defender", "Midfielder", "Striker"]
            )
            selected = position

        elif question_template == "I wear the shirt number ... at my current club":
            shirt_number = st.selectbox(
                "Write a shirt number:",
                ["Unter 20", "20-30", "Über 30"]
            )
            selected = shirt_number

        elif question_template == "I am taller than ...":
            height = st.slider(
                "",
                min_value=150, max_value=220, value=185, step=1
            )
            selected = f"taller than {height} cm"

        elif question_template == "I am shorter than ...":
            height = st.slider(
                "",
                min_value=150, max_value=220, value=185, step=1
            )
            selected = f"shorter than {height} cm"

    with col3:
        if st.button("Ask Question"):
            # Add the question to the session state list
            if selected:
                full_question = question_template.replace("...", selected)
                st.session_state.questions.append(full_question)
            else:
                st.warning("Please provide an additional input to complete the question.")

    # Display all questions asked so far
    st.subheader("Questions Asked:")
    for i, question in enumerate(st.session_state.questions, start=1):
        st.write(f"{i}. {question}")

    # Input field and button
    col1, col2 = st.columns([3, 2], vertical_alignment="bottom")

    with col1:
        user_input = st.text_input("Enter your guess:", placeholder="Type Player here...", label_visibility="collapsed")

    with col2:
        button_clicked = st.button("Guess")

    # Überprüfung bei Button-Klick
    if button_clicked:
        if st.session_state.lives > 0:
            if user_input in players_data and user_input not in st.session_state.guessed_players:
                # Spieler korrekt erraten
                st.success("🎉 You guessed the player correctly!")
                st.image(players_data[user_input], caption=f"{user_input}", width=200)
                st.session_state.guessed_players.append(user_input)
            elif user_input in st.session_state.guessed_players:
                st.warning("You already guessed this player!")
            else:
                # Spieler nicht korrekt erraten
                st.session_state.lives -= 1
                if st.session_state.lives > 0:
                    st.error(f"❌ Wrong guess! You have {st.session_state.lives} lives left.")
                else:
                    st.error("❌ Game over! You've used up all your lives.")
        else:
            st.error("❌ No lives left! Restart the app to try again.")