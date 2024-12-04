if button_clicked:
        if st.session_state.lives > 0:
            if guessed_player in players_data:
                # Spieler korrekt erraten
                st.success("🎉 You guessed the player correctly!")
                st.image(players_data[guessed_player], caption=f"{guessed_player}", width=200)
            elif guessed_player in st.session_state.players_guessed_so_far:
                st.warning("You have already tried this player!")
            else:
                # Spieler nicht korrekt erraten
                st.session_state.lives -= 1
                if st.session_state.lives > 0:
                    st.error(f"❌ Wrong guess! You have {st.session_state.lives} lives left.")
                else:
                    st.error("❌ Game over! You've used up all your lives.")
        else:
            st.error("❌ Game over! You have no points remaining.")