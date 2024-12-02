import streamlit as st
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

# Define functions for each page
def load_home_page():
    from a_pages import home_page

def load_game_page():
    import a_pages.who_am_i

def load_leaderboard_page():
    import a_pages.leaderboard

def load_search_page():
    import a_pages.searchbar

# Call the appropriate function based on the selected page
if page == "Home":
    load_home_page()
elif page == "Game":
    load_game_page()
elif page == "Leaderboard":
    load_leaderboard_page()
elif page == "Search":
    load_search_page()