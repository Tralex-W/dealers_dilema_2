import streamlit as st
import os


class Tutorial:
    def __init__(self):
        with open("spielanleitung.txt", "r", encoding="utf-8") as file:
            self.paragraphs = file.read().split("\n\n")

        if "current_paragraph_index" not in st.session_state:
            st.session_state.current_paragraph_index = 0

    def show_tutorial(self):
        container = st.empty()
        if st.session_state.current_paragraph_index < len(self.paragraphs):
            if os.path.isfile(f"{1}.png"):
                container.image(f"{1}.png", use_column_width=True)

            container.write(self.paragraphs[st.session_state.current_paragraph_index])

            if st.button(
                f"Weiter", key=f"next_button_{st.session_state.current_paragraph_index}"
            ):
                st.session_state.current_paragraph_index += 1
                container.empty()
                st.rerun()

    def show_ai_interaction(self):
        pass
