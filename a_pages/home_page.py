import streamlit as st
import os
from b_game.d_game_initialize import initialize_original_player_list
import time

def home_page():
    # Titre et logo
    col1, col2, col3 = st.columns([2, 1, 1])  # Trois colonnes : titre, logo, bouton
    with col1:
        st.title("Who am I ?")
        st.subheader("Guess. Compete. Celebrate!")
    with col2:
        image_path = os.path.join("a_pages", "pictures", "logo.png")
        st.image(image_path, width=200)
       
    with col3:
        st.write("")

    # Séparation visuelle
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Sous-titre "Concept" et description
    col1, col2, col3 = st.columns([2, 0.5, 1])
    with col1: 
        st.title("Game Concept")
        st.write("""
                Welcome to Who Am I? – Football Edition ⚽🔥

                Think you know football? Prove it in the ultimate online guessing game for fans who live and breathe the beautiful game!  
                From legendary icons to rising stars across all leagues, eras, and nations, every clue brings you closer to uncovering the mystery player.  

                **Can you guess who it is with fewer questions and rack up the most points?**  
                Challenge yourself, take on your friends, and rise to the top of the leaderboard.  

                It's time to flex your football IQ and claim your title as the ultimate football mastermind.  

                **Ready to play? The pitch is yours!** 🎮⚡
                """)
    
    with col2:
        image_path = os.path.join("a_pages", "pictures", "ampoule.png")
        st.image(image_path, width=200)
    with col3:
        st.write("")

    # Séparation visuelle
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Sous-titre "Rules" et description
    col1, col2, col3 = st.columns([2, 0.5, 1])
    with col1: 
        st.title("Game Rules")

        st.subheader("1. Create Your Username 🎮")
        st.write("Pick a cool username and get ready to shine!")

        st.subheader("2. Choose Your Level ⚽")
        st.write("Feeling bold? Choose **Easy**, **Medium**, or **Hard** – your call, your challenge!")

        st.subheader("3. Guess the Football Star 🕵️")
        st.write("Use the hints to figure out the mystery player. Think fast and guess smart! 🕶️")

        st.subheader("4. Fewer Questions, More Points 🔥")
        st.write("The fewer questions you ask, the higher your score. Keep it sharp! ")

        st.subheader("5. Check the Leaderboard 📊")
        st.write("See how your score compares with your friends. Who’s the real football whiz? ")

        st.subheader("6. Crown the Champ 🏆")
        st.write("The player with the highest average points takes home the bragging rights! 🏅")

        st.write("Let the games begin – show off your football knowledge and crush it! ⚡⚽")
    with col2:
        image_path = os.path.join("a_pages", "pictures", "sifflet.webp")
        st.image(image_path, width=200)
    with col3:
        st.write("")

    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)
    
    col1, col2, = st.columns([3, 1])
    
    if "original_player_list" not in st.session_state or not st.session_state.original_player_list:
        with st.spinner("Add players once the game set up has been completed... ⚽"):
            initialize_original_player_list()
        st.success("🎉 Game Set up completed")
        time.sleep(3)
        st.rerun()


    # Initialize session_state to store users and their game data
    if "users" not in st.session_state:
        st.session_state.users = {}
    if "points_total" not in st.session_state:
        st.session_state.points_total = {}
    if "points_history" not in st.session_state:
        st.session_state.points_history = {}
    if "rounds" not in st.session_state:
        st.session_state.rounds = {}
    if "player_turn" not in st.session_state:
        st.session_state.player_turn = None
    if "current_turn_index" not in st.session_state:
        st.session_state.current_turn_index = 0
    if "turn_order" not in st.session_state:
        st.session_state.turn_order = []

    st.title("Log In to start the game !")
    st.subheader("Choose your username and show your skills !")

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
    st.subheader("List of registered users:")
    if st.session_state["users"]:
        for user_id, name in st.session_state["users"].items():
            st.write(f"User {user_id}: {name}")
    else:
        st.write("No users registered yet")
    
    st.write("")    
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Formulaire de contact
    st.subheader("Contact")
    col1, col2, col3 = st.columns([0.5, 1, 1])
    with col1:
        st.write("CS Goup 8.6")
        st.write("Dufourstrasse 50")
        st.write("9000, St.Gallen")
        st.write("Switzerland")

    with col2:
        st.write("""
                 For any question or recomandations, feel free to contact us
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
    with col3:
        st.write("")
    
    
# Appeler la fonction




