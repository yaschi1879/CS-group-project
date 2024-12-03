import streamlit as st
players = [
    {"Name": "Lionel Messi", "Position": "Forward", "Team": "Inter Miami"}
     ]
def searchbar():
    st.header("Search Engine")

    col1, col2 = st.columns([3,1])

    with col1:
        user_input = st.text_input ("Geben Sie ein, wonach Sie suchen möchten:", label_visibility="collapsed", placeholder="Type something...")
    with col2:
        search_button = st.button("Search")
        
    if search_button:
            st.write(f"Suchergebnisse für: {user_input}")
            results = [item for item in players if user_input.lower() in item["Name"].lower()]

    # Calling results from a players llist // Attention on what should be displayed and how (in line 22): Name, ...!!!
            if results:
                for result in results:
                    st.write(f"Name: {result['Name']}, Position: {result['Position']}, Team: {result['Team']}")
            else:
                st.write("No results found")
# Hier muss der Output dann noch schön dargestellt werden
# Und evtl. Grafik mit Marktwert Entwicklung
searchbar()
