# We hereby declare that the vast majority of the code for this project has been written by us independently. 
# We have utilized ChatGPT as a tool for conceptual purposes and for assistance with small, 
# specific parts of the code, such as generating comments or clarifying implementation ideas.
# However, all critical design decisions, core functionality, 
# and the implementation of the primary codebase were developed through our own efforts and understanding.

# This is Link for the Game application: https://cs-group-project-8c9afmnnkpup2ze7c3yxvo.streamlit.app/ 

import streamlit as st
import a_pages.searchbar
import a_pages.leaderboard 
import a_pages.who_am_i
import a_pages.home_page



# Sidebar mit Navigationsoptionen
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page:",  # Titel für die Sidebar
    ("Home", "Search", "Game", "Leaderboard")  # Optionen
)


# Call the appropriate function based on the selected page
if page == "Home":
    a_pages.home_page.home_page()
elif page == "Game":
    a_pages.who_am_i.who_am_i()
elif page == "Leaderboard":
    a_pages.leaderboard.leaderboard()
elif page == "Search":
    a_pages.searchbar.searchbar()