import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Include the parent directory in the system path to access project modules
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder

# Initialize dictionaries for points, history, and games played
# Ensures session state contains necessary structures for user data
def initialize_game_data():
    if "users" in st.session_state:
        if "points" not in st.session_state:
            st.session_state.points = {user_id: 0 for user_id in st.session_state.users}
        if "points_history" not in st.session_state:
            st.session_state.points_history = {user_id: [] for user_id in st.session_state.users}
        if "rounds" not in st.session_state:
            st.session_state.rounds = {user_id: 0 for user_id in st.session_state.users}



# Display users and their points in an interactive table with ranks
def display_leaderboard():
    st.subheader("Ranking Based on AVG Points")
    if "users" in st.session_state and "points_total" in st.session_state and "rounds" in st.session_state:
        # Create a DataFrame with usernames, points, and average points
        data = {
            "Username": list(st.session_state.users.values()),
            "Points": [st.session_state.points_total[user_id] for user_id in st.session_state.users.keys()],
            "Games Played": [st.session_state.rounds[user_id] for user_id in st.session_state.users.keys()],
            "AVG Points": [
                st.session_state.points_total[user_id] / st.session_state.rounds[user_id]
                if st.session_state.rounds[user_id] > 0 else 0
                for user_id in st.session_state.users.keys()
            ],
        }
        leaderboard_df = pd.DataFrame(data)

        # Sort by AVG Points in descending order and add a Rank column
        leaderboard_df.sort_values(by="AVG Points", ascending=False, inplace=True)
        leaderboard_df.reset_index(drop=True, inplace=True)
        ranks = []
        for idx in leaderboard_df.index:
            if idx == 0:
                ranks.append("🥇")  # Gold medal
            elif idx == 1:
                ranks.append("🥈")  # Silver medal
            elif idx == 2:
                ranks.append("🥉")  # Bronze medal
            else:
                ranks.append(str(idx + 1))  # Numeric rank from 4th place onwards

        leaderboard_df.insert(0, "Rank", ranks)  # Insert Rank column at the beginning

        # Display with AgGrid
        gb = GridOptionsBuilder.from_dataframe(leaderboard_df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(wrapText=True, autoHeight=True)
        grid_options = gb.build()
        AgGrid(leaderboard_df, gridOptions=grid_options, height=400, fit_columns_on_grid_load=True)
    else:
        st.info("No users found. Please register users on the Home page.")


# Display the evolution of player points over time
def plot_points_evolution():
    st.subheader("Points Evolution Over Time")
    if "points_history" in st.session_state and "users" in st.session_state:
        user_options = ["Select All"] + list(st.session_state.users.values())
        selected_user = st.selectbox("Select a User to View Points Evolution", user_options)

        plt.figure(figsize=(10, 6))

        if selected_user == "Select All":
            # Display points evolution for all players
            for user_id, history in st.session_state.points_history.items():
                if history:  # Only plot if history exists
                    plt.plot(range(1, len(history) + 1), history, marker="o", label=st.session_state.users[user_id])
            plt.title("Points Evolution for All Players")
        else:
            # Find the selected user's ID
            user_id = next((uid for uid, uname in st.session_state.users.items() if uname == selected_user), None)
            if user_id and st.session_state.points_history[user_id]:
                plt.plot(
                    range(1, len(st.session_state.points_history[user_id]) + 1),
                    st.session_state.points_history[user_id],
                    marker="o",
                    label=selected_user,
                )
                plt.title(f"Points Evolution for {selected_user}")
            else:
                st.warning(f"No data available for {selected_user}.")

        # Adjust axes excluding empty histories
        non_empty_histories = [hist for hist in st.session_state.points_history.values() if hist]
        if non_empty_histories:
            plt.ylim(0, max(max(hist) for hist in non_empty_histories) + 10)
        else:
            plt.ylim(0, 10)  # Default limit if no history

        plt.xlabel("Game Number")
        plt.ylabel("Total Points")
        if non_empty_histories:
            plt.xticks(range(1, max(len(hist) for hist in non_empty_histories) + 1))
        plt.legend()
        st.pyplot(plt)
    else:
        st.warning("No points history available. Please update points to generate data.")



# Main function for the Leaderboard page
def leaderboard():
    st.title("Leaderboard")

    # Initialize game data to ensure dictionaries are synced with users
    #initialize_game_data()

    # Display the leaderboard
    display_leaderboard()
    
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Display points evolution
    plot_points_evolution()


# Run the Leaderboard page
if __name__ == "__main__":
    leaderboard()
