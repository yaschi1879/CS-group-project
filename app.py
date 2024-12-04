import streamlit as st
import a_pages.searchbar
#import a_pages.leaderboard
import a_pages.who_am_i
#import a_pages.home_page



# Sidebar mit Navigationsoptionen
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page:",  # Titel für die Sidebar
    ("Home", "Search", "Game", "Leaderboard")  # Optionen
)


# Call the appropriate function based on the selected page
if page == "Home":
    a_pages.home_page.home_page()
#elif page == "Game":
   # a_pages.who_am_i.who_am_i()
#elif page == "Leaderboard":
#    a_pages.leaderboard.stats()
elif page == "Search":
    a_pages.searchbar.searchbar()