import streamlit as st
#from c_coding.d_game_initialize import initialize_player_lists, generate_player_list
#from c_coding.f_game_logic import play_game
#from b_support_pages.sp_who_am_i import handle_question_selection

# Code Lars hier eingefügt!!!
def who_am_i():
    initialize_player_lists()
    if "original_player_list" not in st.session_state:
        st.write("generating player list...")
        st.session_state.original_player_list = generate_player_list()
    st.session_state.current_player_list = st.session_state.original_player_list.copy()

    if "current_player_list" not in st.session_state:
        st.session_state.current_player_list = st.session_state.original_player_list.copy()
    if "selected_player" not in st.session_state:
        st.session_state.selected_player = None
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "lives" not in st.session_state:
        st.session_state.lives = 3
    if "points" not in st.session_state:
        st.session_state.points = 50
    if "guessed_players" not in st.session_state:
        st.session_state.guessed_players = []
    
    # Create a centered layout
    col1, col2, col3, col4, col5 = st.columns([3, 2, 3, 2, 3])  # The middle column takes up the majority of the space

    with col3:
        # Display the logo at the top of the page
        st.image("logo.png", width=200)
    
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

# -------------------------------------------------------------------------------------------
# ab hier beginnt das eigentliche spiel

    if st.button("Start Game"):
        player = play_game(st.session_state.current_player_list, difficulty)
        st.session_state.selected_player = player
        st.success(f"Game started!")
 

    # Erste Selectbox mit Fragen
    col1, col2, col3 = st.columns([2,2,1], vertical_alignment="bottom")

    with col1:
        
        question_template = st.selectbox(
            "Choose a question:",
            ["", 
            "Are you currently playing for ...", 
            "Are you currently playing in ...", 
            "Do you come from ...", 
            "Did you use to play for ...", 
            "Are you a ... winner", 
            "Are you older than ...", 
            "Are you younger than ...", 
            "Do you play as a ...", 
            "Do you currently wear the shirt number ... ", 
            "Are you taller than ...", 
            "Are you shorter than ..."]
        )

    # Weiterführende Auswahl von Kriterien durch if Funktion
    with col2:
        selected = handle_question_selection(question_template, col2)
        # hier wird auf das separate file sp_who_am_i verweisen

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

who_am_i()