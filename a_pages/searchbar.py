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

            st.json(player)

            if isinstance(player, dict): 
                # If the `player` dictionary itself represents the result
                if player_id in player.get("id", ""):  # Safely check if the ID matches
                    # Spielerinfo als Überschrift und Bild
                    st.title(f"{player['name']} - {player['classified_position']}")
                    st.image(player["image"], caption=f"{player['name']} ({player['country']})", width=250)

                    # Informationen in zwei Spalten aufteilen
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Persönliche Details")
                        st.markdown(f"""
                        - *Alter:* {player['age']}
                        - *Größe:* {player['height']} cm
                        - *Fuß:* {player['foot']}
                        - *Trikotnummer:* {player['shirt_number']}
                        - *Beigetreten:* {player['joined_date']}
                        """)

                    with col2:
                        st.subheader("Verein und Liga")
                        st.markdown(f"""
                        - *Verein:* {player['club_name']}
                        - *Liga:* {player['league_name']}
                        - *Ehemalige Vereine:* {', '.join(player['old_clubs_ids'])}
                        - *Früheres Stadion:* {player['old_stadium']}
                        """)

                    # Positionen und Erfolge als separate Abschnitte
                    st.subheader("Spielpositionen")
                    st.markdown(", ".join(player["position"]))

                    st.subheader("Erfolge")
                    st.markdown(", ".join(player["titels"]))
                    #st.write(f"Name: {player.get('name')}, Position: {player.get('position')}, Team: {player.get('club_name')}")
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

