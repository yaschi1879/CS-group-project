import streamlit as st
import random
from c_coding.c_filter_criteria import check_player_criteria
from c_coding.b_player_data import player_dictionary
from b_game.c_try_question import handle_question_selection
from c_coding.a_api_functions import get_player_name_user_input
from b_game.d_game_initialize import initialize_game_variables, initialize_question_variables

def play_game():
    while not st.session_state.selected_player:
        with st.spinner("Searching for a player ⚽"):
            player = random.choice(st.session_state.current_player_list)
            if check_player_criteria(player):
                st.session_state.selected_player = player
                st.success(f"🎉 Player has been selected based on difficulty: {st.session_state.difficulty}")
            else:
                st.session_state.current_player_list.remove(player)
    
    if not st.session_state.player_data:
        try:
            with st.spinner("Gathering data for the selected player"):
                st.session_state.player_data = player_dictionary(st.session_state.selected_player)
                st.success("🎉 Set up completed")
        except:
            st.session_state.selected_player = []
            st.rerun()
    
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        st.write("lives:", "⚽" * st.session_state.lives, "❌ " * (3 - st.session_state.lives))
    with col2:
        st.write(f"points: {st.session_state.points}")
    
    col1, col2 = st.columns([4, 1]) 
    with col1:
        question_template = st.selectbox(
        "Choose a question",
        ["",
        "Are you currently playing for ...?", 
        "Are you currently playing in ...?", 
        "Do you come from ...?", 
        "Did you use to play for ...?", 
        "Are you a ... winner?", 
        "Are you ... years old?", 
        "Do you play as a ...?", 
        "Do you currently wear the shirt number ...?", 
        "Are you ...cm tall?"]
        )
    st.session_state.question_template = question_template
    
    with col2:
        st.write("")
        st.write("")
        question_button = st.button("Select Question")
    
    if question_button:
        if st.session_state.question_template:
            st.session_state.question_procedure = True
            
    if st.session_state.user_input and not st.session_state.question_procedure:
        st.write("scheisse man")
    
    if st.session_state.question_procedure == True:
        col, col2 = st.columns([1, 1])
        handle_question_selection(st.session_state.question_template, col1, col2)
        
    
    match_found = None
    if st.session_state.exact_input:
        index = st.session_state.index
        selected = st.session_state.selected
        exact_input = st.session_state.exact_input
        
        st.write("inizialiserung oke")
            
        full_question = question_template.replace("...", str(exact_input))
        st.session_state.questions.append(full_question)
        
        st.write("frage hinzugefügt")
                
        for answer in selected:
            if isinstance(st.session_state.player_data[index], list):
                if answer in st.session_state.player_data[index]:
                    match_found = True
                    break
                    
            elif answer == st.session_state.player_data[index]:
                match_found = True
            else:
                match_found = False
            
            st.write("true oder false")
        else:
            st.warning("Please provide an additional input to complete the question!")
                        
    if st.session_state.points > 0 and st.session_state.lives > 0:
        if match_found == True:
            st.session_state.points -= 1
            st.success(f"Yes, this question is correct. You have lost only 1 Point")
            
        elif match_found == False:
            st.session_state.points -= 2
            st.warning(f"No, this question is incorrect. You have lost 2 Points")

        
        st.subheader("Questions Asked:")
        for i, question in enumerate(st.session_state.questions, start=1):
            st.write(f"{i}. {question}")
    
    if st.session_state.points == 0:
        st.warning("Game over! You have 0 points left. Click on next round to continue")
        

    # Input field and button
    col1, col2 = st.columns([3, 2], vertical_alignment="bottom")

    with col1:
        user_input = st.text_input("Enter Player Name", placeholder="Type Player here...", label_visibility="collapsed")

    #with col2:
        #guess_clicked = st.button("Enter guess")
        
    if user_input:
        guessed_player_id = get_player_name_user_input(user_input)[0]
        guessed_player_name = get_player_name_user_input(user_input)[1]
        if guessed_player_id is None:
            st.warning("Player not found, Please try again.")
        elif st.session_state.lives > 0:
            if guessed_player_id == st.session_state.player_data["id"]:
                # Spieler korrekt erraten
                st.success(f"🎉 Congratulations, I am indeed {guessed_player_name}")
                st.image(st.session_state.player_data["image"], caption=f"{guessed_player_name}", width=200)
            elif guessed_player_id in st.session_state.players_guessed_so_far:
                st.warning("You have already tried this player!")
            else:
                # Spieler nicht korrekt erraten
                st.session_state.lives -= 1
                if st.session_state.lives > 0:
                    col1, col2 = st.columns([4,1])
                    with col1:
                        st.error(f"❌ Wrong guess! You have {st.session_state.lives} lives left. Click on continue")
                    with col2:
                        st.button("Continue")
                else:
                    st.error("❌ Game over! You've used up all your lives. Select one of the options below")
        elif st.session_state.lives == 0:
            st.error("❌ Game over! You've used up all your lives. Select one of the options below")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])     
    with col1:
        # Button zum Verlassen des Spiels
        if st.button("Exit the Game"):
            st.session_state.game_started = False
            st.rerun()

    with col2:
        # Button zum Wechseln der Schwierigkeit
        if st.button("Change Difficulty"):
            # Logik zum Wechseln der Schwierigkeit hier
            st.write("Difficulty change coming soon...")
    
    with col3:
        if st.button("Show Solution"):
            st.write("Show Solution coming soon...")

    with col4:
        # Button für die nächste Runde
        if st.button("Next Round"):
            initialize_game_variables()
            st.rerun()
