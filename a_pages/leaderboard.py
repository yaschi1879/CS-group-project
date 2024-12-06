import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder


# Initialisation des dictionnaires pour les points, l'historique et les parties jouées
def initialize_game_data():
    if "users" in st.session_state:
        if "points" not in st.session_state:
            st.session_state.points = {user_id: 0 for user_id in st.session_state.users}
        if "points_history" not in st.session_state:
            st.session_state.points_history = {user_id: [] for user_id in st.session_state.users}
        if "rounds" not in st.session_state:
            st.session_state.rounds = {user_id: 0 for user_id in st.session_state.users}



# Afficher les utilisateurs et leurs points dans un tableau interactif avec Rank
def display_leaderboard():
    st.subheader("Ranking based on AVG Points")
    if "users" in st.session_state and "points" in st.session_state and "rounds" in st.session_state:
        # Créer un DataFrame des utilisateurs, points et AVG Points
        data = {
            "Username": list(st.session_state.users.values()),
            "Points": [st.session_state.points[user_id] for user_id in st.session_state.users.keys()],
            "Games Played": [st.session_state.rounds[user_id] for user_id in st.session_state.users.keys()],
            "AVG Points": [
                st.session_state.points[user_id] / st.session_state.rounds[user_id]
                if st.session_state.rounds[user_id] > 0 else 0
                for user_id in st.session_state.users.keys()
            ],
        }
        leaderboard_df = pd.DataFrame(data)

        # Trier par AVG Points décroissants et ajouter la colonne Rank
        leaderboard_df.sort_values(by="AVG Points", ascending=False, inplace=True)
        leaderboard_df.reset_index(drop=True, inplace=True)
        ranks = []
        for idx in leaderboard_df.index:
            if idx == 0:
                ranks.append("🥇")  # Médaille d'or
            elif idx == 1:
                ranks.append("🥈")  # Médaille d'argent
            elif idx == 2:
                ranks.append("🥉")  # Médaille de bronze
            else:
                ranks.append(str(idx + 1))  # Rang numérique à partir de la 4ème place

        leaderboard_df.insert(0, "Rank", ranks)  # Insérer la colonne Rank au début

        # Affichage avec AgGrid
        gb = GridOptionsBuilder.from_dataframe(leaderboard_df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(wrapText=True, autoHeight=True)
        grid_options = gb.build()
        AgGrid(leaderboard_df, gridOptions=grid_options, height=400, fit_columns_on_grid_load=True)
    else:
        st.info("No users found. Please register users on the Home page.")


# Mettre à jour les points et les parties jouées pour un utilisateur
def update_user_points():
    st.subheader("Update Points and Games Played")
    if "users" in st.session_state and "points" in st.session_state and "points_history" in st.session_state and "rounds" in st.session_state:
        # Liste des noms d'utilisateurs pour le sélecteur
        user_names = list(st.session_state.users.values())
        selected_user_name = st.selectbox("Select User to Update", options=user_names)

        # Récupérer l'ID correspondant à l'utilisateur sélectionné
        user_id = next(uid for uid, uname in st.session_state.users.items() if uname == selected_user_name)

        points_to_add = st.number_input("Points to Add", min_value=0, value=0, step=1)
        games_to_add = st.number_input("Games to Add", min_value=0, value=0, step=1)

        if st.button("Update"):
            # Ajouter des points
            st.session_state.points[user_id] += points_to_add
            # Ajouter à l'historique des points
            st.session_state.points_history[user_id].append(st.session_state.points[user_id])
            # Mettre à jour le nombre de parties jouées
            st.session_state.rounds[user_id] += games_to_add
            st.success(
                f"Updated! {selected_user_name} now has {st.session_state.points[user_id]} points "
                f"over {st.session_state.rounds[user_id]} games."
            )
    else:
        st.error("No users found! Please register users on the Home page.")



# Afficher l'évolution des points des joueurs
def plot_points_evolution():
    st.subheader("Points Evolution Over Time")
    if "points_history" in st.session_state and "users" in st.session_state:
        user_options = ["Select All"] + list(st.session_state.users.values())
        selected_user = st.selectbox("Select a User to View Points Evolution", user_options)

        plt.figure(figsize=(10, 6))

        if selected_user == "Select All":
            # Afficher l'évolution des points pour tous les joueurs
            for user_id, history in st.session_state.points_history.items():
                if history:  # Ne tracer que si l'historique existe
                    plt.plot(range(1, len(history) + 1), history, marker="o", label=st.session_state.users[user_id])
            plt.title("Points Evolution for All Players")
        else:
            # Trouver l'ID de l'utilisateur sélectionné
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

        # Ajuster les axes en excluant les historiques vides
        non_empty_histories = [hist for hist in st.session_state.points_history.values() if hist]
        if non_empty_histories:
            plt.ylim(0, max(max(hist) for hist in non_empty_histories) + 10)
        else:
            plt.ylim(0, 10)  # Limite par défaut si aucun historique

        plt.xlabel("Game Number")
        plt.ylabel("Total Points")
        if non_empty_histories:
            plt.xticks(range(1, max(len(hist) for hist in non_empty_histories) + 1))
        plt.legend()
        st.pyplot(plt)
    else:
        st.warning("No points history available. Please update points to generate data.")



# Fonction principale pour la page Leaderboard
def leaderboard():
    st.title("Leaderboard")

    # Initialiser les données de jeu
    initialize_game_data()  # Assure que tous les dictionnaires sont synchronisés avec les utilisateurs

    # Afficher le leaderboard
    display_leaderboard()

    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Permettre la mise à jour des points et des parties jouées
    update_user_points()

    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Afficher l'évolution des points
    plot_points_evolution()


# Exécuter la page Leaderboard
if __name__ == "__main__":
    leaderboard()
