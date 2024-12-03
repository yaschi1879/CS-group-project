import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from c_coding.b_player_data import player_dictionary
from c_coding.a_api_functions import get_player_name_user_input, get_marketvalue_history

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

            if isinstance(player, dict): 
                # If the `player` dictionary itself represents the result
                if player_id in player.get("id", ""):  # Safely check if the ID matches
                    # Spielerinfo als Überschrift und Bild
                    st.title(f"{player['name']} - {player['classified_position']}")
                    st.image(player["image"], caption=f"{player['name']} ({player['country']})", width=250)

                    # Informationen in zwei Spalten aufteilen
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Personal Details:")
                        st.markdown(f"""
                        - *Age:* {player['age']}
                        - *Height:* {player['height']} cm
                        - *Foot:* {player['foot']}
                        - *Shirt Number:* {player['shirt_number']}
                        - *Beigetreten:* {player['joined_date']}
                        """)

                    with col2:
                        st.subheader("Club and League:")
                        st.markdown(f"""
                        - *Club:* {player['club_name']}
                        - *League:* {player['league_name']}
                        - *Past Clubs:* {', '.join(player['old_clubs_ids'])}
                        - *Old Stadium:* {player['old_stadium']}
                        """)

                    # Positionen und Erfolge als separate Abschnitte
                    st.subheader("Position:")
                    st.markdown(", ".join(player["position"]))

                    st.subheader("Achievements:")
                    st.markdown(", ".join(player["titels"]))
            else:
                st.write("No results found")

            market_value = get_marketvalue_history(player_id)
            # Daten in DataFrame umwandeln
            df = pd.DataFrame(market_value)

            # Bereinigung des `value`-Werts
            df['value'] = df['value'].str.replace('€', '').str.replace('m', '').astype(float)

            # Datum konvertieren
            df['date'] = pd.to_datetime(df['date'])

            # Plot mit Matplotlib erstellen
            plt.figure(figsize=(10, 6))
            plt.plot(df['date'], df['value'], marker='o', linestyle='-', color='blue')

            # Titel und Achsenbeschriftungen hinzufügen
            plt.title("Market Value Development", fontsize=16)
            plt.xlabel("Date", fontsize=14)
            plt.ylabel("Market Value (€ Million)", fontsize=14)

            # Gitter hinzufügen
            plt.grid(True)

            # Diagramm in Streamlit anzeigen
            st.pyplot(plt)
# Hier muss der Output dann noch schön dargestellt werden
# Und evtl. Grafik mit Marktwert Entwicklung

