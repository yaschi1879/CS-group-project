import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import AgGrid, GridOptionsBuilder


def generate_fake_scores():
    data = {
        "Player": ["Lars", "Yannick", "Roy", "Enya", "Mathieu"],
        "Points": [150, 200, 180, 170, 160],
        "Games Played": [3, 4, 2, 3, 5],
        "Points History": [
            [50, 50, 50],      # Points de Lars par partie
            [70, 50, 40, 40],  # Points de Yannick
            [90, 90],          # Points de Roy
            [60, 60, 50],      # Points de Enya
            [30, 40, 30, 30, 30]  # Points de Mathieu
        ],
    }
    scores = pd.DataFrame(data)
    scores["AVG Points"] = scores["Points"] / scores["Games Played"]
    return scores


def compute_leaderboard(scores):
    scores = scores.sort_values(by="AVG Points", ascending=False).reset_index(drop=True)
    scores.index += 1  # Rang commence à 1

    # Ajouter la colonne "Rank"
    scores.insert(0, "Rank", scores.index)

    # Ajouter les médailles aux 3 premiers dans la colonne "AVG Points"
    medals = ["🥇", "🥈", "🥉"]
    for i in range(min(3, len(scores))):
        scores.iloc[i, scores.columns.get_loc("AVG Points")] = f"{scores.iloc[i, scores.columns.get_loc('AVG Points')]:.2f} {medals[i]}"

    return scores[["Rank", "Player", "Games Played", "Points", "AVG Points"]]


def display_table(scores):
    st.subheader("Interactive Leaderboard")
    gb = GridOptionsBuilder.from_dataframe(scores)
    gb.configure_pagination(paginationAutoPageSize=True)  # Pagination automatique
    gb.configure_side_bar()  # Barre latérale pour filtrage
    gb.configure_default_column(wrapText=True, autoHeight=True)  # Colonnes adaptatives
    grid_options = gb.build()
    AgGrid(scores, gridOptions=grid_options, height=400, fit_columns_on_grid_load=True)


def plot_player_performance(scores):
    # Ajouter "Select All" au menu déroulant
    player_options = ["Select All"] + scores["Player"].tolist()
    player_selected = st.selectbox("Select a Player to View Points Evolution", player_options)

    plt.figure(figsize=(10, 6))

    if player_selected == "Select All":
        # Afficher l'évolution des points pour tous les joueurs
        for _, row in scores.iterrows():
            points_history = row["Points History"]
            plt.plot(range(1, len(points_history) + 1), points_history, marker="o", label=row["Player"])
        plt.title("Points Evolution for All Players")
    else:
        # Filtrer les données pour le joueur sélectionné
        player_data = scores[scores["Player"] == player_selected].iloc[0]
        points_history = player_data["Points History"]
        plt.plot(range(1, len(points_history) + 1), points_history, marker="o", label=player_selected)
        plt.title(f"Points Evolution for {player_selected}")

    # Ajuster les étiquettes et la légende
    plt.xlabel("Game Number")
    plt.ylabel("Points")
    plt.xticks(range(1, max([len(hist) for hist in scores["Points History"]]) + 1))
    plt.ylim(0, max([max(hist) for hist in scores["Points History"]]) + 10)  # Échelle ajustée
    plt.legend()
    st.pyplot(plt)


def leaderboard():
    st.title("Leaderboard and Statistics")

    # Charger ou générer des données
    uploaded_file = st.file_uploader("Upload your player data (CSV)", type="csv")
    if uploaded_file is not None:
        scores = pd.read_csv(uploaded_file)
        if not {"Player", "Points", "Games Played", "Points History"}.issubset(scores.columns):
            st.error("Invalid CSV format. Please include 'Player', 'Points', 'Games Played', and 'Points History' columns.")
            return
        scores["AVG Points"] = scores["Points"] / scores["Games Played"]
    else:
        st.info("No file uploaded. Using fake data.")
        scores = generate_fake_scores()

    # Calculer le leaderboard avec le rang
    leaderboard_scores = compute_leaderboard(scores)

    # Afficher le tableau
    display_table(leaderboard_scores)

    # Séparation visuelle
    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

    # Diagramme interactif
    st.subheader("Player Performance")
    plot_player_performance(scores)


if __name__ == "__main__":
    leaderboard()


# Formulaire de contact
    st.subheader("Contact")
    col1, col2, col3 = st.columns([0.5, 1, 1])
    with col1:
        st.write("CS Goup 8.6")
        st.write("Dufourstrasse 50")
        st.write("9000, St.Gallen")
        st.write("Switzerland")

    with col2:
        st.write("""
                 For any question or recomandations, feel free to contact us
                 via our contact form""")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email Address")
            message = st.text_area("Your Message")
            submit_button = st.form_submit_button("Send")

            if submit_button:
                if name and email and message:
                    st.success("Thank you for your message! We'll get back to you soon.")
                else:
                    st.error("Please fill out all the fields before sending.")
    with col3:
        st.write("")
