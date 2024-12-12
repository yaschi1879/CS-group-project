import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Include the parent directory in the system path to access project modules
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
    # Randomly selects a player who meets the criteria, removing players that do not
    with st.spinner("Searching for a player... ⚽"):
        while not st.session_state.selected_player:
            player = random.choice(st.session_state.current_player_list)
            # the function below is defined on page c_support.c_filter_criteria
            if check_player_criteria(player):
                st.session_state.selected_player = player
                st.session_state.current_player_list.remove(player)
            else:
                st.session_state.current_player_list.remove(player)
    
    # If player data is not yet fetched, gather it
    # try/excpet because in few cases the data is not complete
    if not st.session_state.player_data:
        try:
            with st.spinner("Gathering data for the selected player... ⚽"):
                # all the necessary data for a player is stored in player_data
                # the function player_dicitonary processes the data coming from the API and is defined on c_support.b_player_data
                st.session_state.player_data = player_dictionary(st.session_state.selected_player)
        except:
            st.session_state.selected_player = []
            st.rerun()
    
    # Display the current player's turn
    # user saved in st.session_state.player turn
    # player_turn is allocated with a value on b_game.d_game_initialize
    st.title((f"{st.session_state.users[st.session_state.player_turn]}, It's Your Turn!"))
    st.write("")
    
    col1, col2 = st.columns([1, 3])
    # Show the questionmark image while the player is yet to be guessed
    if st.session_state.show_solution == False and st.session_state.solution_true == False:
        with col1:
            image_path = os.path.join("b_game", "questionmark.png")
            st.image(image_path, caption="Who am I?", width=150)
    
    # Show the image of the player once the player was guessed correctly or the button show solution was pressed   
    if st.session_state.show_solution == True:
        with col1:
            st.image(st.session_state.player_data["image"], caption=f"I am {st.session_state.player_data['name']}", width=150)
    
    if st.session_state.solution_true == True:
        with col1:
            st.image(st.session_state.player_data["image"], caption=f"I am {st.session_state.player_data['name']}", width=150)
    
    with col2:
        # Display player hints
        with st.container():
            st.subheader("Hints:")
            st.markdown(f"""
                        - I am {st.session_state.player_data["foot"]} footed
                        - I joined my current club on {st.session_state.player_data["joined_date"]}
                        - I have played in this stadium: {st.session_state.player_data["old_stadium"]}
                        """)
            
    # Display player stats (lives and points)
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
    with col1: # selectbox with the questions that are available to choose from
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
    
    # Once a question was chosen the control variable question_procedure is set true
    if st.session_state.question_chosen:
        st.session_state.question_procedure = True
    
    # This part handles the selected question
    if st.session_state.question_procedure == True:
        # change to c_questions file
        handle_question_selection(st.session_state.question_chosen)
    
    # If the user gave input on the selected question, the hand_question_selection allocated the variable check with True
    # The code below compares the user input with the data in the player_dictionary   
    if st.session_state.check == True:
        # Transmitting the input
        index = st.session_state.index
        selected = st.session_state.selected
        exact_input = st.session_state.exact_input
        # preallocating match_found with False
        match_found = False
        
        # if the value in the player_dicitonary is a list, the following code iterates through that list
        # index is used to take the correct key of the dictionary
        if isinstance(st.session_state.player_data[index], list):
            for answer in selected:
                if answer in st.session_state.player_data[index]:
                    # If one of the solutions fits with (one of) the values of selected, match_found is true
                    # e.g. Did you use to play for Liverpool? -> if Liverpool is in the list of old clubs, match_found is true
                    match_found = True
                    break
        # if there is only one value in the dictionary for key = index, (one of) the values of the user input is compared to it
        else:
            for answer in selected:
                if answer == st.session_state.player_data[index]:
                    # e.g. Are you between 180cm and 190cm tall -> selected contains a list with all heights in this range
                    # if one of the hights matches with the hight in the player dictionary, match found is true
                    match_found = True   
                    break
        # if no match is found, match_found keeps its preallocated value = False
        # this part checks if the user has any points or lives remaining and the points for a wrong or wright question are deducted
        if st.session_state.points > 0 and st.session_state.lives > 0:
            if match_found == True:
                st.session_state.points -= 1
                answer_text = f"<span style='color:green;'>Yes</span>"
            elif match_found == False:
                st.session_state.points -= 2
                answer_text = f"<span style='color:red;'>No</span>"
        
        # if the user has no points or lives remaining, the game is over
        if st.session_state.points == 0 or st.session_state.lives == 0:
            st.session_state.show_solution = True
        
        # prepare the questions for displaying them in Questions asked so far
        formatted_question = st.session_state.question_chosen.replace("...", str(exact_input))
        st.session_state.questions.append(f"{formatted_question} \xa0 {answer_text}")
        # game control variable is set to False to end this part
        st.session_state.check = False
        st.rerun()

    st.write("")
    st.write("")
    st.write("")
    st.subheader("Questions asked so far:")  # Display list of asked questions
    if st.session_state.questions:
        questions_list = "\n".join(
        [f"{i}. {question}" for i, question in enumerate(reversed(st.session_state.questions), start=1)]
        )
        st.markdown(questions_list, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Guess the Player") #Handle player guesses
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Enter Player Name", placeholder="Type Player here...", label_visibility="collapsed")
    
    with col2:
        guess_button = st.button("Enter")
    
    # if a player is guessed the part below handles processing the guess 
    if guess_button:
        with st.spinner("Checking your answer... ⚽"):
            # player id is evaluated from the user input, see c_support.a_api_functions for further details
            guessed_player_id = get_player_name_user_input(user_input)[0]
        # Checks if input was given
        if guessed_player_id is None:
            st.warning("No player found, please try again.")
        # Checks if the user has lives remaining
        elif st.session_state.lives > 0:
            if guessed_player_id == st.session_state.player_data["id"]:
                # Player guessed correctly
                st.balloons()
                time.sleep(2)
                # game control variable is set True
                st.session_state.solution_true = True
                st.rerun()
            
            else:
                # Player not guessed correctly, one live is deducted
                st.session_state.lives -= 1
                # If the user has lives remaining, the game continues
                if st.session_state.lives > 0:
                    col1, col2 = st.columns([4,1])
                    with col1:
                        if st.session_state.lives > 1:
                            st.error(f"❌ Wrong guess! {st.session_state.lives} lives left")
                        if st.session_state.lives == 1:
                            st.error(f"❌ Wrong guess! {st.session_state.lives} live left")
                        time.sleep(3)
                        st.rerun()
                # If the user has no lives remaining, game control variable is set true
                else:
                   st.session_state.show_solution = True
                   st.rerun()
        # same here
        elif st.session_state.lives == 0:
            st.session_state.show_solution = True
            st.rerun()
    
    # That will be shown when user guesses player correctly
    if st.session_state.solution_true == True:
        st.success(f"🎉 Congratulations, I am {st.session_state.player_data["name"]}! Continue with guessing my future market value")
        st.write("")
        st.write("")
        st.write("")
        st.subheader("Guess the market value")
        col1, col2 = st.columns([4, 1])
        # game proceeds with guessing the future market value (last part of the game)
        with col1:
            st.session_state.ml_question = col1.text_input("Guess my estimated market value (+/- 25%) for Dec 1, 2025 (in € and millions):", placeholder="e.g. 80")
        with col2:
            st.write("")
            st.write("")
            st.session_state.ml_clicked = st.button("Guess")
    
    # That will be shown when the game is over    
    if st.session_state.show_solution == True:
        st.error("❌ Game over! Continue with guessing the future market value") # This is shown when user does not guess player correctly and has no lives left
        if st.session_state.points > 0:
            st.session_state.points = 0
            st.rerun()
        st.write("")
        st.write("")
        st.write("")
        # game proceeds with guessing the future market value (last part of the game)
        st.subheader("Guess the market value")
        col1, col2 = st.columns([4, 1]) 
        with col1:
            st.session_state.ml_question = col1.text_input("Guess my estimated market value (+/- 25%) for Dec 1, 2025 (in € and millions):", placeholder="e.g. 80")
        with col2:
            st.write("")
            st.write("")
            st.session_state.ml_clicked = st.button("Guess")
    
    # Processing of the future market value input by the user   
    if st.session_state.ml_clicked: 
        if st.session_state.ml_question:
            with st.spinner("Checking your answer... ⚽"):
                # forecast is defined on ml_machine_learning.ml_d_forecast
                solution = round(forecast(str(st.session_state.selected_player))[1]["value"], 2)
                # the user has to be in the range of +/- 25%
                tolerance = 0.25 * solution
                lower_bound = solution - tolerance
                upper_bound = solution + tolerance
                # calculates how far the user is away of the solution
                percent_off = round(abs(int(st.session_state.ml_question) - solution) / solution * 100, 2)
                if lower_bound <= int(st.session_state.ml_question) <= upper_bound:
                    points_total = st.session_state.points + 10
                    # If estimated market value is guessed correctly
                    st.success(f"🎉 Congratulations! My estimated market value for December 2025 is €{solution}m, you were off by {percent_off}%")
                else:
                    points_total = st.session_state.points
                    # If estimated market value is guessed wrong
                    st.error(f"❌ Wrong! My estimated market value for December 2025 is €{solution}m, you were off by {percent_off}%")
                st.info(f"{st.session_state.users[st.session_state.player_turn]}, you earned {points_total} points this round. Choose one of the options below to continue")
                # points_total, rounds and points_history are added, the can now be seen on the leaderboard
                st.session_state.points_total[st.session_state.player_turn] += points_total
                st.session_state.rounds[st.session_state.player_turn] += 1
                st.session_state.points_history[st.session_state.player_turn].append(points_total)
        else:
            with col1:
                    st.warning("Please enter an input before guessing!")
    
    st.write("")
    st.write("")
    st.write("")

    # Buttons below to choose from
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1.1, 1, 0.75])     
        with col1:
            # Button for leaving the game
            if st.button("Reset the Game"):
                st.session_state.game_started = False
                st.rerun()

        with col2:
            # Button for changing the Difficulty level
            if st.button("Change Difficulty"):
                st.session_state.change_difficulty = True
                st.rerun()
        
        with col3:
            # Button to show solution
            if st.button("Show Solution"):
                st.session_state.lives = 0
                st.session_state.points = 0
                st.session_state.show_solution = True
                st.rerun()

        with col4:
            # Button for the next round
            if st.button("Next Round"):
                # important, all the game_varibles will be reset to default value (see d_game_initialize for further details)
                initialize_game_variables()
                determine_next_turn()
                st.rerun()
    
    # Handle difficulty change during game play
    if st.session_state.change_difficulty == True:
        difficulty = st.selectbox(
        "Select Difficulty:",
        ("Select Difficulty...", "Random", "Easy", "Medium", "Hard"),
        index=0,
        placeholder="Select a difficulty level for the next round...",
        )

        if difficulty == "Select Difficulty...":
            st.warning("Please select a difficulty level to proceed.")
        else:
            st.session_state.difficulty = difficulty
            st.success(f"Difficulty level adjusted to: {difficulty}")