import streamlit as st
from c_coding.b_player_data import player_dictionary
from c_coding.a_api_functions import get_player_name_user_input

def searchbar():
    st.header("Search Engine")

    col1, col2 = st.columns([3,1])

    with col1:
        user_input = st.text_input ("Geben Sie ein, wonach Sie suchen möchten:", label_visibility="collapsed", placeholder="Type something...")
    with col2:
        search_button = st.button("Search")
        
    if search_button:
            id = get_player_name_user_input(user_input)
            player = player_dictionary(id)
            st.write(f"Suchergebnisse für: {user_input}")

            print(player)

            #results = [item for item in player if user_input.lower() in item["Name"].lower()]

    # Calling results from a players llist // Attention on what should be displayed and how (in line 22): Name, ...!!!
            #if results:
                #for result in results:
                    #st.write(f"Name: {result['name']}, Position: {result['position']}, Team: {result['club_name']}")
            #else:
                #st.write("No results found")
# Hier muss der Output dann noch schön dargestellt werden
# Und evtl. Grafik mit Marktwert Entwicklung

