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
            player_id = get_player_name_user_input(user_input)
            player = player_dictionary(player_id)
            st.write(f"Suchergebnisse für: {user_input}")

            st.write(player)

            if isinstance(player, dict): 
                # If the `player` dictionary itself represents the result
                if player_id in player.get("id", ""):  # Safely check if the ID matches
                    st.write(f"Name: {player.get('name')}\n, Position: {player.get('position')}\n, Team: {player.get('club_name')}")
                else:
                    st.write("No results found")

            else:
                st.write("No results found")
    # Calling results from a players llist // Attention on what should be displayed and how (in line 22): Name, ...!!!
            #if results:
                #for result in results:
                    #st.write(f"Name: {result['name']}, Position: {result['position']}, Team: {result['club_name']}")
            #else:
                #st.write("No results found")
# Hier muss der Output dann noch schön dargestellt werden
# Und evtl. Grafik mit Marktwert Entwicklung

