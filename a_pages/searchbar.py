import streamlit as st
import pandas as pd
from c_support.b_player_data import player_dictionary
from c_support.a_api_functions import get_player_name_user_input, get_marketvalue_history
from d_machine_learning.ml_d_forecast import forecast

def searchbar():
    st.header("Search Engine")
    col1, col2 = st.columns([3,1])

    with col1:
        user_input = st.text_input ("Geben Sie ein, wonach Sie suchen möchten:", label_visibility="collapsed", placeholder="Type something...")
    with col2:
        search_button = st.button("Search")

    if search_button:
        with st.spinner ("Searching for player... ⚽"):
            player_id = get_player_name_user_input(user_input)[0]
        if player_id == "n.a.":
            st.warning(f"no active player found for: {user_input}")
        else:
            with st.spinner ("Gathering data... ⚽"):
                player = player_dictionary(player_id)
                st.write(f"search result for: {user_input}")

            if isinstance(player, dict):
                # If the `player` dictionary itself represents the result
                if player_id in player.get("id", ""):  # Safely check if the ID matches
                    # Spielerinfo als Überschrift und Bild
                    st.title(player["name"])
                    st.image(player["image"], caption=f"{player['name']} ({player['classified_position']})", width=250)

                    # Informationen in zwei Spalten aufteilen
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Personal Details:")
                        st.markdown(f"""
                        - *Nationality:* {player['country']}
                        - *Age:* {player['age']}
                        - *Height:* {player['height']} cm
                        - *Foot:* {player['foot']}
                        """)

                    with col2:
                        st.subheader("Club and League:")
                        st.markdown(f"""
                        - *Club:* {player['club_name']}
                        - *Joined the club:* {player['joined_date']}
                        - *Shirt Number:* {player['shirt_number']}
                        - *League:* {player['league_name']}
                        """)

                    # Positionen und Erfolge als separate Abschnitte
                    st.subheader("Position:")
                    st.markdown(", ".join(player["position"]))

                    st.subheader("Titles:")
                    st.markdown(", ".join(player["titles"]))

                    st.subheader("Former Clubs:")
                    old_clubs_name_unique = []
                    for club in player["old_clubs_name"]:
                        if club not in old_clubs_name_unique:
                            old_clubs_name_unique.append(club)
                    st.markdown(", ".join(old_clubs_name_unique))

        try:
            market_value = get_marketvalue_history(player_id)
            forecast_value = forecast(player_id)
            extended_value = market_value + forecast_value
            st.write(extended_value)

            # Prüfe, ob Daten vorhanden sind
            if not extended_value or len(extended_value) == 0:
                st.warning("No market value data available.")
            else:
                # Daten in ein DataFrame umwandeln
                df = pd.DataFrame(extended_value)

                def clean_value(value):
                    value = value.replace('€', '').replace(',', '')
                    if 'm' in value:
                        return float(value.replace('m', ''))
                    elif 'k' in value:
                        return float(value.replace('k', '')) / 1000

                df["value"] = df["value"].apply(lambda x: clean_value(x) if isinstance(x, str) else None)
                df['date'] = pd.to_datetime(df['date'], format="%b %d, %Y", errors='coerce')

                # Prüfe auf ungültige Werte
                if df['date'].isna().any():
                    st.warning("Some dates could not be parsed. Check the data format.")

                df = df.sort_values(by='date')

                if df.empty or df['value'].isna().all():
                    st.warning("No valid data to display.")
                else:
            # Line Chart darstellen
                    st.subheader("Market Value Development (in Mio. EUR)")
                    st.line_chart(df[['date', 'value']].set_index('date'))

        except Exception as e:
            if player_id != "n.a.":
                st.warning(f"Line Chart not available: {e}")

