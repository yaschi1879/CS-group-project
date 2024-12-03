import streamlit as st
import pandas as pd

#Nur als Beispiel, muss noch ganz geändert werden !!

def stats():
    import matplotlib.pyplot as plt

    st.title("Stats")
    st.write("Bienvenue sur la page des statistiques.")
    
    # Exemple : Affichage d'un tableau
    data = {'Catégorie': ['A', 'B', 'C'], 'Valeur': [10, 20, 15]}
    df = pd.DataFrame(data)
    st.write("Voici un exemple de tableau :")
    st.dataframe(df)

    # Exemple : Génération d'un graphique
    fig, ax = plt.subplots()
    ax.bar(df['Catégorie'], df['Valeur'])
    st.pyplot(fig)

    st.markdown('<hr style="border: 1px solid #ddd;">', unsafe_allow_html=True)

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
