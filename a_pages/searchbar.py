import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Include the parent directory in the system path to access project modules
from c_support.b_player_data import player_dictionary
from c_support.a_api_functions import get_player_name_user_input, get_marketvalue_history
from d_machine_learning.ml_d_forecast import forecast

def searchbar():
    # Header for the search engine page
    st.header("Search Engine")
    col1, col2 = st.columns([3,1]) # Columns for search input and button

    with col1:
        user_input = st.text_input ("Enter what you want to search for:", label_visibility="collapsed", placeholder="Type something...")
    with col2:
        search_button = st.button("Search")

    if search_button:
        with st.spinner ("Searching for player... ⚽"):
            player_id = get_player_name_user_input(user_input)[0] # Retrieve player ID based on user input
        if player_id == "n.a.":
            st.warning(f"no active player found for: {user_input}")
        else:
            with st.spinner ("Gathering data... ⚽"):
                player = player_dictionary(player_id) # Fetch player data
                st.write(f"search result for: {user_input}")

            if isinstance(player, dict):
                # If the `player` dictionary itself represents the result
                if player_id in player.get("id", ""):  # Validate the player ID
                    # Display player info as title and image
                    st.title(player["name"])
                    st.image(player["image"], caption=f"{player['name']} ({player['classified_position']})", width=250)

                     # Split information into two columns
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

                    # Display positions and titles
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
        st.write("")
        st.write("")
        st.write("")
        st.subheader("Market Value:")
        try:
            with st.spinner ("Loading market value ... ⚽"):
                market_value = get_marketvalue_history(player_id) # Retrieve market value history
                last_market_value = market_value[len(market_value)-1]["value"]
                market_value.append({"date": "Dec 12, 2024", "value": last_market_value})

                # Checking if Data is available or exists
                if market_value == "n.a.":
                    st.warning("No market value data available.")
                else:
                    # Transform Data into a DataFrame
                    df = pd.DataFrame(market_value)

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
                        # preparing Forecast-Data
                        forecast_value = forecast(player_id) # Forecast future market values
                        forecast_df = pd.DataFrame(forecast_value)
                        forecast_df['date'] = pd.to_datetime(forecast_df['date'], format="%b %d, %Y", errors='coerce')

                        # Create a Plotly chart
                        fig = go.Figure()

                        # Add historical Data
                        fig.add_trace(go.Scatter(
                            x=df['date'],
                            y=df['value'],
                            mode='lines',
                            name='Market Value History',
                            line=dict(color='blue', width=2)
                        ))

                        # Add forecast data
                        fig.add_trace(go.Scatter(
                            x=forecast_df['date'],
                            y=forecast_df['value'],
                            mode='lines',
                            name='Forecast',
                            line=dict(color='red', width=2, dash='dot')  # Punktierte Linie für Prognosen
                        ))

                        # adjust layout
                        fig.update_layout(
                            title="Market Value Development (in Mio. EUR)",
                            xaxis_title="Date",
                            yaxis_title="Value (in Mio. EUR)",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )

                        # show diagramm
                        st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            if player_id != "n.a.":
                st.warning(f"Line Chart not available: {e}")