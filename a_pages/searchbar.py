import streamlit as st
import pandas as pd
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
        with st.spinner("Generating player list... ⚽"):
            player_id = get_player_name_user_input(user_input)[0]
        if player_id == "n.a.":
            st.warning(f"no player found for: {user_input}")
        else:
            player = player_dictionary(player_id)
            st.write(f"search result for: {user_input}")

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
                        - *Joined the club:* {player['joined_date']}
                        """)

                with col2:
                        st.subheader("Club and League:")
                        st.markdown(f"""
                        - *Club:* {player['club_name']}
                        - *League:* {player['league_name']}
                        - *Past Clubs:* {', '.join(player['old_clubs_name'])}
                        - *Old Stadium:* {player['old_stadium']}
                        """)

                    # Positionen und Erfolge als separate Abschnitte
                st.subheader("Position:")
                st.markdown(", ".join(player["position"]))

                st.subheader("Achievements:")
                st.markdown(", ".join(player["titels"]))
        else:
            st.write("No results found")
        try:
                market_value = get_marketvalue_history(player_id)
                # Daten in ein DataFrame umwandeln
                df = pd.DataFrame(market_value)

                def clean_value(value):
                    value = value.replace('€', '').replace(',', '')
                    if 'm' in value:
                        return float(value.replace('m', '')) 
                    elif 'k' in value:
                        return float(value.replace('k', '')) /1000  

                df["value"] = df["value"].apply(clean_value)
                
                # Datum konvertieren
                df['date'] = pd.to_datetime(df['date'])

                # Daten sortieren (falls nötig)
                df = df.sort_values(by='date')

                # Line Chart darstellen
                st.subheader("Market Value Development (in Mio. EUR)")
                st.line_chart(df[['date', 'value']].set_index('date'))

        except:
                st.warning("Line Chart not available.")

