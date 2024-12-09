import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import random
import os
import time
from b_game.c_question import handle_question_selection
from b_game.d_game_initialize import initialize_game_variables, determine_next_turn
from c_support.a_api_functions import get_player_name_user_input
from c_support.b_player_data import player_dictionary
from c_support.c_filter_criteria import check_player_criteria
from d_machine_learning.ml_d_forecast import forecast



def play_game():
    with st.spinner("Searching for a player... ⚽"):
        while not st.session_state.selected_player:
            player = random.choice(st.session_state.current_player_list)
            if check_player_criteria(player):
                st.session_state.selected_player = player
                #st.session_state.current_player_list.remove(player)
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!¨!!!!!!!!!!!!!!!!!!!!!!
            else:
                st.session_state.current_player_list.remove(player)
    
    if not st.session_state.player_data:
        try:
            with st.spinner("Gathering data for the selected player... ⚽"):
                st.session_state.player_data = player_dictionary(st.session_state.selected_player)
        except:
            st.session_state.selected_player = []
            st.rerun()
    
    # hier funktion die den user bestimmt
    # speichern von user in st.session_state.player turn
    st.title((f"{st.session_state.users[st.session_state.player_turn]}, it's your turn!"))
    st.write("")
    
    col1, col2 = st.columns([1, 3])
    if st.session_state.show_solution == False and st.session_state.solution_true == False:
        with col1:
            image_path = os.path.join("b_game", "Fragezeichen.png")
            st.image(image_path, caption="Who am I?", width=150)
            
    if st.session_state.show_solution == True:
        with col1:
            st.image(st.session_state.player_data["image"], caption=f"I am {st.session_state.player_data['name']}", width=150)
    
    if st.session_state.solution_true == True:
        with col1:
            st.image(st.session_state.player_data["image"], caption=f"I am {st.session_state.player_data['name']}", width=150)
    
    with col2:
        with st.container():
            st.subheader("Hints:")
            st.markdown(f"""
                        - I am {st.session_state.player_data["foot"]} footed
                        - I joined my current club on {st.session_state.player_data["joined_date"]}
                        - I have played in this stadium: {st.session_state.player_data["old_stadium"]}
                        """)
    
    col1, col2, col3 = st.columns([1, 1, 0.5])
    
    with st.container():
        with col1:
            lives_display = "⚽" * st.session_state.lives + "❌ " * (3 - st.session_state.lives)
            st.subheader(f"Lives: {lives_display}")
        with col2:
            st.subheader(f"Points left: {st.session_state.points}")
        st.write("")
        st.write("")

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
        "Is your position ...?", 
        "Do you currently wear the shirt number ...?", 
        "Are you ...cm tall?"]
        )
    st.session_state.question_chosen = question_template
    
    if st.session_state.question_chosen:
        st.session_state.question_procedure = True
    
    if st.session_state.question_procedure == True:
        # wechsel auf b_questions file
        handle_question_selection(st.session_state.question_chosen)
        
    if st.session_state.check == True:
        index = st.session_state.index
        selected = st.session_state.selected
        exact_input = st.session_state.exact_input
        match_found = False
        
        if isinstance(st.session_state.player_data[index], list):
            for answer in selected:
                if answer in st.session_state.player_data[index]:
                    match_found = True
                    break
        else:
            for answer in selected:
                if answer == st.session_state.player_data[index]:
                    match_found = True   
                    break
        
        if st.session_state.points > 0 and st.session_state.lives > 0:
            if match_found == True:
                st.session_state.points -= 1
                answer_text = f"<span style='color:green;'>Yes</span>"
            elif match_found == False:
                st.session_state.points -= 2
                answer_text = f"<span style='color:red;'>No</span>"
        
        if st.session_state.points == 0 or st.session_state.lives == 0:
            st.session_state.show_solution = True
            
        formatted_question = st.session_state.question_chosen.replace("...", str(exact_input))
     
        st.session_state.questions.append(f"{formatted_question} \xa0 {answer_text}")
        st.session_state.check = False
        st.rerun()

    st.write("")
    st.write("")
    st.write("")
    st.subheader("Questions asked so far:")  # Subheader verwenden
    if st.session_state.questions:
        questions_list = "\n".join(
        [f"{i}. {question}" for i, question in enumerate(reversed(st.session_state.questions), start=1)]
        )
        st.markdown(questions_list, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Guess the Player")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Enter Player Name", placeholder="Type Player here...", label_visibility="collapsed")
    
    with col2:
        guess_button = st.button("Enter Guess")
        
    if guess_button:
        with st.spinner("Checking your answer... ⚽"):
            guessed_player_id = get_player_name_user_input(user_input)[0]
        if guessed_player_id is None:
            st.warning("Player not found, Please try again.")
        elif st.session_state.lives > 0:
            if guessed_player_id == st.session_state.player_data["id"]:
                # Spieler korrekt erraten
                st.balloons()
                time.sleep(2)
                st.session_state.solution_true = True
                st.rerun()
            
            else:
                # Spieler nicht korrekt erraten
                st.session_state.lives -= 1
                if st.session_state.lives > 0:
                    col1, col2 = st.columns([4,1])
                    with col1:
                        if st.session_state.lives > 1:
                            st.error(f"❌ Wrong guess! {st.session_state.lives} lives left")
                        if st.session_state.lives == 1:
                            st.error(f"❌ Wrong guess! {st.session_state.lives} live left")
                        time.sleep(3)
                        st.rerun()
                else:
                   st.session_state.show_solution = True
                   st.rerun()
        
        elif st.session_state.lives == 0:
            st.session_state.show_solution = True
            st.rerun()
    
    if st.session_state.solution_true == True:
        st.success(f"🎉 Congratulations, I am {st.session_state.player_data["name"]}! Continue with guessing my future market value")
        st.write("")
        st.write("")
        st.write("")
        st.subheader("Guess the market value")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.session_state.ml_question = col1.text_input("Guess my estimated market value (+/- 25%) for Dec 1, 2027 (in € and millions)", placeholder="80")
        with col2:
            st.write("")
            st.write("")
            st.session_state.ml_clicked = st.button("Guess")
            
    if st.session_state.show_solution == True:
        st.error("❌ Game over! Continue with guessing the future market value")
        if st.session_state.points > 0:
            st.session_state.points = 0
            st.rerun()
        st.write("")
        st.write("")
        st.write("")
        st.subheader("Guess the market value")
        col1, col2 = st.columns([4, 1]) 
        with col1:
            st.session_state.ml_question = col1.text_input("Guess my estimated market value for Dec 1, 2027 (in € and millions):")
        with col2:
            st.session_state.ml_clicked = st.button("Guess")
        
    if st.session_state.ml_clicked:
        if st.session_state.ml_question:
            solution = forecast(st.session_state.selected_player)[3]["value"]
            tolerance = 0.25 * solution
            lower_bound = solution - tolerance
            upper_bound = solution + tolerance
            percent_off = abs(int(st.session_state.ml_question) - solution) / solution * 100
            if lower_bound <= int(st.session_state.ml_question) <= upper_bound:
                points_total = st.session_state.points + 10
                st.success(f"🎉 Congratulations! My estimated market value for December 2027 is €{solution}m, you were {percent_off}% off")
            else:
                points_total = st.session_state.points
                st.error(f"❌ Wrong! My estimated market value for December 2027 is €{solution}m, you were {percent_off}% off")
            st.info(f"{st.session_state.users[st.session_state.player_turn]}, you earned {points_total} points this round. Choose one of the options below to continue")
            st.session_state.points_total[st.session_state.player_turn] += points_total
            st.session_state.rounds[st.session_state.player_turn] += 1
            st.session_state.points_history[st.session_state.player_turn].append(points_total)
        else:
            with col1:
                    st.warning("Please enter an input before guessing.")
    
    st.write("")
    st.write("")
    st.write("")
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1.1, 1, 0.75])     
        with col1:
            # Button zum Verlassen des Spiels
            if st.button("Reset the Game"):
                st.session_state.game_started = False
                st.rerun()

        with col2:
            # Button zum Wechseln der Schwierigkeit
            if st.button("Change Difficulty"):
                st.session_state.change_difficulty = True
                st.rerun()
        
        with col3:
            if st.button("Show Solution"):
                st.session_state.lives = 0
                st.session_state.points = 0
                st.session_state.show_solution = True
                st.rerun()

        with col4:
            # Button für die nächste Runde
            if st.button("Next Round"):
                initialize_game_variables()
                determine_next_turn()
                st.rerun()
            
    if st.session_state.change_difficulty == True:
        difficulty = st.selectbox(
        "Select Difficulty:",
        ("Select Difficulty...", "None", "Easy", "Medium", "Hard"),
        index=0,
        placeholder="Select a difficulty level for the next round...",
        )

        if difficulty == "Select Difficulty...":
            st.warning("Please select a difficulty level to proceed.")
        else:
            st.session_state.difficulty = difficulty
            st.success(f"Difficulty level adjusted to: {difficulty}")