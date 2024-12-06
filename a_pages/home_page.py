import streamlit as st
import os
from b_game.d_game_initialize import initialize_original_player_list
import time

def home_page():
    # Initialisation de l'état pour gérer la connexion
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    # Titre et logo
    col1, col2, col3 = st.columns([2, 1, 1])  # Trois colonnes : titre, logo, bouton
    with col1:
        st.title("Name der App")
        st.subheader("Guess. Compete. Celebrate! (find a better slogan)")
    with col2:
        image_path = os.path.join("a_pages", "pictures", "logo.png")
        st.image(image_path, width=200)
       
    with col3:
        # Bouton Log In stylisé
        if st.button("Log In"):
            st.session_state.show_login = True

    # Affichage des champs pour la connexion si le bouton "Log In" est cliqué
    if st.session_state.show_login and not st.session_state.logged_in:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

        # Ajouter les deux boutons côte à côte
            col1, col2 = st.columns([0.1, 1])
            with col1:
                confirm_button = st.form_submit_button("Confirm")
            with col2:
                close_button = st.form_submit_button("Close")

        # Validation des identifiants
            if confirm_button:
                if username == "mathieu" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome {username}!")
                else:
                    st.error("Invalid username or password!")

        # Si l'utilisateur clique sur "Close"
            if close_button:
                st.session_state.show_login = False

    # Séparation visuelle
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Sous-titre "Concept" et description
    col1, col2, col3 = st.columns([2, 0.5, 1])
    with col1: 
        st.title("Game Concept")
        st.write("""
        Welcome to Who Am I? – Football Edition, the ultimate online guessing game for true football fans! 
        Test your knowledge of players from all leagues, eras, and nations. With every clue, the mystery deepens – will you crack the code before time runs out? 
        Compete with friends or challenge yourself to climb the leaderboard. Are you ready to show the world you're the ultimate football expert? Let’s play!""")
    
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
        st.title("Rules")
        st.write("""
        1. Rule 1 : Description...
        2. Rule 2 : Description...
        3. Rule 3 : Description...
        """)
    with col2:
        image_path = os.path.join("a_pages", "pictures", "sifflet.webp")
        st.image(image_path, width=200)
    with col3:
        st.write("")

    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)
    
    col1, col2, = st.columns([3, 1]) 
    
    with col1:    
        st.title("Players")
    
    if "original_player_list" not in st.session_state or not st.session_state.original_player_list:
        with st.spinner("Add players once the game set up has been completed... ⚽"):
            initialize_original_player_list()
        st.success("🎉 Game Set up completed")
        time.sleep(3)
        st.rerun()


    # Initialize session_state to store users and their game data
    if "users" not in st.session_state:
        st.session_state["users"] = {}
    if "points" not in st.session_state:
        st.session_state["points"] = {}
    if "points_history" not in st.session_state:
        st.session_state["points_history"] = {}
    if "rounds" not in st.session_state:
        st.session_state["rounds"] = {}
    
    if st.session_state.original_player_list:

        st.title("Log In to start the game !")
        st.subheaders("Choose your username and show your skills !")

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
                st.session_state["points"][new_id] = 0
                st.session_state["points_history"][new_id] = []
                st.session_state["rounds"][new_id] = 0
                st.success(f"User {username} added successfully!")
            else:
                st.error("User ID already exists!")
        else:
            st.error("Please enter a username.")

    # Display the list of registered users
    st.subheader("List of registered users:")
    if st.session_state["users"]:
        for user_id, name in st.session_state["users"].items():
            st.write(f"User {user_id}: {name}")
    else:
        st.write("No users registered yet.")

    # !!!!!!!!!!!!!!!!!!!! Mathieu, hier bitte irgend ein Feld, wo man die Spieler eingeben kann !!!!!!!!!!!!!!!!!!!!!!!
    # Spieler sollen als Dictionary in st.session_state.users abgespeichert werden
    # key = Zahlen, je nach dem wie viele users -> ist für alle dictionarys (users, points, rounds der selbe)
    # value = Namen von Usern
    # zusätzlich funktion die checked ob alle user im dictionary users einen points value im dictionary points haben, falls nicht, diesen auf 0 setzen
    # zusätzlich funktion die checked ob aller user im dictionary users einen rounds value im dictionary rounds haben, falls nicht, diesen auf 0 setzen
        st.write("...")
    
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




