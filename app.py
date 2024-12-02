import streamlit as st
from a_pages import home_page
from a_pages import searchbar
from a_pages import who_am_i


# Sidebar mit Navigationsoptionen
st.sidebar.title("Navigation")
option = st.sidebar.radio(
    "Wählen Sie eine Option:",
    ("Homepage", "Searchbar", "Game")
)

# Für jede Option in der Navigation Inhalte widergeben
if option == "Homepage":
    home_page()
elif option == "Searchbar":
    searchbar()
elif option == "Game":
    who_am_i()