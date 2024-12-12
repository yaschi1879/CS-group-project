# We hereby declare that the vast majority of the code for this project has been written by us independently. 
# We have utilized ChatGPT as a tool for conceptual purposes and for assistance with small, 
# specific parts of the code, such as generating comments or clarifying implementation ideas.
# However, all critical design decisions, core functionality, 
# and the implementation of the primary codebase were developed through our own efforts and understanding.

# This is Link for the Game application: https://cs-group-project-8c9afmnnkpup2ze7c3yxvo.streamlit.app/
# our GitHub: https://github.com/yaschi1879/CS-group-project

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Include the parent directory in the system path to access project modules

import streamlit as st
from c_support.a_api_functions import get_club_name_user_input

# This function defines the further process of asking questions 
def handle_question_selection(question_template):
    
    col1, col2 = st.columns([4, 1])
    
    league_codes = {
    "Premier League": "GB1",
    "Bundesliga": "L1", 
    "Serie A": "IT1", 
    "La Liga": "ES1", 
    "Ligue 1": "FR1", 
    "Scottish Premiership": "SC1",
    "Liga Portugal": "PO1",
    "Eredivisie": "NL1", 
    "Jupiler Pro League": "BE1", # Belgian league
    "Chance Liga": "TS1", # Czech league
    "SuperSport HNL": "KR1", # Croatian League
    }
    
    # First question is processed
    # the handling is very similar between the question, so its only explained once
    if question_template == "Are you currently playing for ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter my club name:") # User Input
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            # Once enter is pressed and the user gave actual input the following steps are executed
            if st.session_state.user_input:
                # selected contains the value which will be compared to the player_data dictionary, here its the club id
                # selected has always to be a list, it makes the comparison to the player_data a lot easier, see this on a_game_logic
                st.session_state.selected = [get_club_name_user_input(st.session_state.user_input)[0]]
                # exact input contains the correct club name and uses the api function defined on c_support.a_api_functions
                # if the user enters Sporting, selected contains the correct name Sporting CP
                st.session_state.exact_input = get_club_name_user_input(st.session_state.user_input)[1]
                # index contains the key tied to the compared value of the player_data dictionary
                st.session_state.index = "club_id"
                # below the game control variables are adjusted
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                # Since the code will be rerunned, we go back to the a_game_logic file
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.") #if user hasnt given input yet 

    #second question                     
    elif question_template == "Are you currently playing in ...?":
        st.session_state.user_input = False
        with col1: # list of all the leagues for the game
            st.session_state.user_input = col1.selectbox(
            "Choose a league:",
            ["", "Premier League", "Bundesliga", "Serie A", 
             "La Liga", "Ligue 1", "Scottish Premiership", 
             "Liga Portugal", "Eredivisie (Netherlands)", "Jupiler Pro League (Belgium)",
             "Chance Liga (Czech Rupublic)", "SuperSport HNL (Croatia)"])
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [league_codes[st.session_state.user_input]]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "league_id"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
    #third question           
    elif question_template == "Do you come from ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter the name of the country")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "country"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
    
    #fourth question        
    elif question_template == "Did you use to play for ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter the name of a former club")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                # returns former club ID as list
                st.session_state.selected = [get_club_name_user_input(st.session_state.user_input)[0]]
                # returns former club name 
                st.session_state.exact_input = get_club_name_user_input(st.session_state.user_input)[1]
                st.session_state.index = "old_clubs_ids"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
    
    #fifth question
    elif question_template == "Are you a ... winner?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.selectbox(
            "Choose a titel:",
            ["", "Top 5 League", "Champions League", "World Cup", "European Championship"]
        )
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "titles"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
    
    #sixth question       
    elif question_template == "Are you ... years old?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.slider("Age (Years):", min_value=15, max_value=45, value=(20, 25), step=1)
        age_list = list(range(st.session_state.user_input[0], st.session_state.user_input[1] + 1))
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = age_list
                if st.session_state.user_input[0] == st.session_state.user_input[1]:
                    st.session_state.exact_input = str(st.session_state.user_input[0])
                else:
                    st.session_state.exact_input = f"between {st.session_state.user_input[0]} and {st.session_state.user_input[1]}"
                st.session_state.index = "age"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
    
    #seventh question           
    elif question_template == "Is your position ...?":
        st.session_state.user_input = False
        with col1: # List of positions available to chose from
            st.session_state.user_input = col1.selectbox(
            "Choose a main position:",
            ["Goalkeeper", "Defender", "Midfielder", "Striker"]
            )
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.index = "classified_position"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
                    
    #eighth question              
    elif question_template == "Do you currently wear the shirt number ...?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.text_input("Enter the shirt number")
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = [st.session_state.user_input]
                st.session_state.index = "shirt_number"
                st.session_state.exact_input = st.session_state.user_input
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")

    #ninth question    
    elif question_template == "Are you ...cm tall?":
        st.session_state.user_input = False
        with col1:
            st.session_state.user_input = col1.slider("Height (Centimeters):", min_value=150, max_value=220, value=(180, 185), step=1)
        height_list = list(range(st.session_state.user_input[0], st.session_state.user_input[1] + 1))
        with col2:
            st.write("")
            st.write("")
            enter = st.button("Confirm")
        if enter:
            if st.session_state.user_input:
                st.session_state.selected = height_list
                if st.session_state.user_input[0] == st.session_state.user_input[1]:
                    st.session_state.exact_input = str(st.session_state.user_input[0])
                else:
                    st.session_state.exact_input = f"between {st.session_state.user_input[0]} and {st.session_state.user_input[1]}"
                st.session_state.index = "height"
                st.session_state.question_procedure = False
                st.session_state.question_selected = False
                st.session_state.check = True
                st.rerun()
            else:
                with col1:
                    st.warning("Please enter an input before confirming.")
        