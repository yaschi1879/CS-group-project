# We hereby declare that the vast majority of the code for this project has been written by us independently. 
# We have utilized ChatGPT as a tool for conceptual purposes and for assistance with small, 
# specific parts of the code, such as generating comments or clarifying implementation ideas.
# However, all critical design decisions, core functionality, 
# and the implementation of the primary codebase were developed through our own efforts and understanding.

# This is Link for the Game application: https://cs-group-project-8c9afmnnkpup2ze7c3yxvo.streamlit.app/ 

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Include the parent directory in the system path to access project modules
import streamlit as st
from b_game.d_game_initialize import initialize_original_player_list
import time

def home_page():
    st.write("")
    st.write("")
    st.write("")
    # Title and logo
    col1, col2, col3 = st.columns([2, 1, 1])  # Three columns: title, logo, button
    with col1:
        st.title("Who am I ?")
        st.subheader("Guess. Compete. Celebrate!")
    with col2:
        image_path = os.path.join("a_pages", "pictures", "logo.png")
        st.image(image_path, width=200)  
    with col3:
        st.write("")

    # Visual separation
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Subtitle "Concept" and description
    col1, col2 = st.columns([2, 1])
    with col1: 
        st.title("Game Concept")
        st.write("""
                Welcome to Who Am I? – Football Edition ⚽🔥

                Think you know football? Prove it in the ultimate online guessing game for fans who live and breathe the beautiful game!  
                From legendary icons to rising stars across all leagues, eras, and nations, every clue brings you closer to uncovering the mystery player.  
                Here's a hint: all players come from the 40 best clubs across the top leagues in europe – only the elite make the cut!
                
                But that’s not all – we’ve implemented a Machine Learning system that predicts the market value of each player 
                for the next 2 years.
                 
                **Can you guess who it is with fewer questions and rack up the most points?**  
                Challenge yourself, take on your friends, and rise to the top of the leaderboard. 

                And if you're unsure about something, look it up in the searchbar! 

                It's time to flex your football IQ and claim your title as the ultimate football mastermind.  

                **Ready to play? The pitch is yours!** 🏟️⚡
                """)
    
    with col2:
        st.write("")

    # Visual separation
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Subtitle "Rules" and description
    col1, col2 = st.columns([2, 1])
    with col1: 
        st.markdown("""
            <style>
                .block-container {
                    padding: 1rem 3rem;
                }
                .stMarkdown {
                    line-height: 1.5;
                }
                h2 {
                    margin-bottom: 0.5rem;
                }
                p {
                    margin-bottom: 1rem;
                }
            </style>
        """, unsafe_allow_html=True)

        st.title("Game Rules")

        st.subheader("1. Create Your Username 🎮")
        st.markdown("Pick a cool username and get ready to shine!")

        st.subheader("2. Choose Your Level ⚽")
        st.markdown("Feeling bold? Choose **Easy**, **Medium**, **Hard** or **Random** – your call, your challenge!")

        st.subheader("3. Guess the Football Star 🕵️")
        st.markdown("Use the hints to figure out the mystery player. Think fast and guess smart! 🕶️")

        st.subheader("4. Fewer Questions, More Points 🔥")
        st.markdown("The fewer questions you ask, the higher your score. Keep it sharp!")

        st.subheader("5. Watch Out for Penalties! ⚠️")
        st.markdown("""
                    - You start with **50 points** and you **lose 1 or 2 points** for every question you ask, depending on whether the answer is true or false.  
                    - You have **3 lives**. Each time you guess a player and it's wrong, you lose **1 life**.  
                    - Use your guesses wisely to stay in the game!
                    """)

        st.subheader("6. Check the Leaderboard 📊")
        st.markdown("See how your score compares with your friends. Who’s the real football whiz?")

        st.subheader("7. Crown the Champ 🏆")
        st.markdown("The player with the highest average points takes home the bragging rights! 🏅")

        st.markdown("**Let the games begin – show off your football knowledge and crush it!** ⚡⚽")
    with col2:
        st.write("")

    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)
    
    col1, col2, = st.columns([3, 1])
    
    if "original_player_list" not in st.session_state or not st.session_state.original_player_list:
        # Display a spinner while the original player list is being initialized
        with st.spinner("Add players once the game set up has been completed... ⚽"):
            # this function is saved on b_game.d_game_initialize
            initialize_original_player_list()
        st.success("🎉 Game Set up completed")
        time.sleep(3)
        st.rerun()


    # Initialize session_state to store users and their game data
    # all the dictionaries below have the same keys: its the user id (1, 2, 3, ...) depending on how many users want to play
    
    # later on the values will be the users names
    if "users" not in st.session_state:
        st.session_state.users = {} 
    # later on the values will be total points achieved, which are displayed on the leaderboard
    if "points_total" not in st.session_state:
        st.session_state.points_total = {} 
    # this dictionary will contain a list for each key with the developement of the points achieved in the game
    if "points_history" not in st.session_state:
        st.session_state.points_history = {} 
    # later on the values will be the completed rounds per user
    if "rounds" not in st.session_state:
        st.session_state.rounds = {} 
    # the variables below are used to determine who is next in the game, see game_initialize for further details
    if "player_turn" not in st.session_state:
        st.session_state.player_turn = None
    if "current_turn_index" not in st.session_state:
        st.session_state.current_turn_index = 0
    if "turn_order" not in st.session_state:
        st.session_state.turn_order = []

    st.title("Log In to Start the Game!")
    st.subheader("Type Your Username and Show Your Skills!")

    # Input field for username
    username = st.text_input("Enter your username:")

    # Button to save the username
    if st.button("Add user"):
        if username:  # Check if the input field is not empty
            # Generate a new ID for the user
            new_id = len(st.session_state["users"]) + 1
            if new_id not in st.session_state["users"]:
                # Add the new user to the dictionary
                st.session_state["users"][new_id] = username
                # Initialize their points, points history, and rounds
                st.session_state["points_total"][new_id] = 0
                st.session_state["points_history"][new_id] = []
                st.session_state["rounds"][new_id] = 0
                st.session_state.turn_order = list(st.session_state.users.keys())
                st.success(f"User {username} added successfully!")
            else:
                st.error("User ID already exists!")
        else:
            st.error("Please enter a username")

    # Display the list of registered users
    st.subheader("List of Registered Users:")
    if st.session_state["users"]:
        for user_id, name in st.session_state["users"].items():
            st.write(f"User {user_id}: {name}")
    else:
        st.write("No users registered yet")
    
    st.write("")    
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Contact form
    st.subheader("Contact")
    col1, col2, col3 = st.columns([0.5, 1, 1])
    with col1:
        st.write("CS Goup 8.6")
        st.write("Dufourstrasse 50")
        st.write("9000, St.Gallen")
        st.write("Switzerland")

    with col2:
        st.write("""
                 For any question or recommendation, feel free to contact us
                 via our contact form""")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email Address")
            message = st.text_area("Your Message")
            submit_button = st.form_submit_button("Send")

            if submit_button:
                if name and email and message:
                    st.success("Thank you for your message! We'll get back to you soon.")
                else:
                    st.error("Please fill out all the fields before sending.")