import streamlit as st
import a_pages.searchbar
#import a_pages.leaderboard
import a_pages.who_am_i
import a_pages.home_page



# Page title
st.set_page_config(page_title="Who Am I? Game", page_icon="⚽")

# Sidebar for page navigation
st.sidebar.title("Navigation")
pages = {
    "Home": "home_page",
    "Game": "who_am_i",
    "Leaderboard": "leaderboard",
    "Search": "searchbar"
}

# Page selection in sidebar
page = st.sidebar.radio("Select a page", options=list(pages.keys()))

# Call the appropriate function based on the selected page
if page == "Home":
    a_pages.home_page.home_page()
elif page == "Game":
    a_pages.who_am_i.who_am_i()
elif page == "Leaderboard":
    a_pages.leaderboard.stats()
elif page == "Search":
    a_pages.searchbar.searchbar()