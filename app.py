import streamlit as st
import home_page
import searchbar
import who_am_i


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