import streamlit as st
from field import Field


class Input:
    def __init__(self):
        if "field" not in st.session_state:
            st.session_state.field = Field()

        if "current_player" not in st.session_state:
            st.session_state.current_player = 1

        if "history" not in st.session_state:
            st.session_state.history = []  # Liste für Zughistorie

        if (
            "input_mode" not in st.session_state
        ):  # gibt man ob man löscht oder hinzufügt
            st.session_state.input_mode = True

    def input_start_values(self):  # Eingabe der Anzahl der Spieler
        num = st.number_input(
            "Anzahl der Spieler:", min_value=2, step=1, value=2, max_value=5
        )

        if st.button("Bestätigen"):
            return num

        return None

    def field_input(self):
        # Anzeige des Spielfelds als Buttons
        for i in range(0, 9, 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                button_label = f"Field {idx + 1}"
                if cols[j].button(button_label, key=idx):  # Ein Feld wurde angeklickt

                    if st.session_state.input_mode == True:  # Hinuzufügen
                        st.session_state.field.add_figure_to_field(
                            idx,
                            st.session_state.current_player,
                            st.session_state.current_round,
                        )

                        # Speichere den Zug in der Historie (Feld und Spieler)
                        st.session_state.history.append(
                            (
                                idx,
                                st.session_state.current_player,
                                st.session_state.current_round,
                            )
                        )

                    elif st.session_state.input_mode == False:  # Löschen
                        st.session_state.field.remove_figure_from_field(
                            idx,
                            st.session_state.current_player,
                            st.session_state.current_round,
                        )

                        # Speichere den Zug in der Historie (Feld und Spieler)
                        st.session_state.history.append(
                            (
                                idx,
                                -(st.session_state.current_player),
                                st.session_state.current_round,
                            )
                        )

    def input_mode_button(self):
        input_mode_button_name = ""

        if st.session_state.input_mode == True:
            input_mode_button_name = "Spieler vom Feld entfernen"
        else:
            input_mode_button_name = "Spieler zum Feld hinzufügen"

        if st.button(input_mode_button_name):
            st.session_state.input_mode = not st.session_state.input_mode

    def redo_button(self):
        # Macht den letzten Zug rückgänig
        if st.button("Redo"):
            if st.session_state.history:
                last_move = st.session_state.history.pop()  # etzten Zug entfernen
                idx, player, history_round = last_move

                if (
                    player > 0
                ):  # es handelt sich um ein hinzufügen, dass rückgänig gemacht wird
                    st.session_state.field.remove_last_from_field(
                        idx
                    )  # Entferne Figur vom Feld
                elif (
                    player < 0
                ):  # es handelt sich um ein löschen, dass rückgänig gemacht wird
                    st.session_state.field.add_figure_to_field(
                        idx, abs(player), history_round
                    )

                st.session_state.current_player = abs(player)  # Setze Spieler zurück

    def show_current_field(self):
        # Aktualisiere die Anzeige nach jedem Zug
        # st.session_state.field.show()
        st.write("Aktuelles Spielfeld:")
        display_board = st.session_state.field.display_field()
        for idx, field_status in enumerate(display_board):
            st.write(f"Field {idx + 1}: {field_status}")

    def input_round_values(self):  # eingabe auf welchem Felder welcher Spieler steht
        self.field_input()

        # Button für den Wechsel zum nächsten Spieler
        # st.session_state.current_player = 1
        if st.button("Nächster Spieler"):
            st.session_state.current_player = (
                st.session_state.current_player % st.session_state.number_of_players
            ) + 1

        st.write(f"Aktueller Spieler: {st.session_state.current_player}")

        self.input_mode_button()
        self.redo_button()

        self.show_current_field()
