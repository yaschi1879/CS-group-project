import streamlit as st
from a_pages import home_page
from a_pages import searchbar
from a_pages import who_am_i


# Sidebar mit Navigationsoptionen
st.set_page_config(page_title="Application", layout="wide")

# Création des onglets
selected_page = st.sidebar.radio("Menu", ["Home Page", "Searchbar", "Who am I"])

# Affichage conditionnel des pages
if selected_page == "Home Page":
    home_page()
elif selected_page == "Searchbar":
    searchbar()
elif selected_page == "Who am I":
    who_am_i()