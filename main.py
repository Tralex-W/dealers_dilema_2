"""
Alle Session_states:
    
    Events:
        events_json
    
    Tutorial:
        current_paragraph_index

    Input:
        field
        current_player
        history
        input_mode

    Global:
        current_round
        phase 
        number of players
"""

import streamlit as st
import json
from events import Event
from inputs import Input
from tutorial import Tutorial

event_manager = Event()
input_manager = Input()
tutorial = Tutorial()

MIN_KUNDEN = 5

if "events_json" not in st.session_state:
    with open("events.json", "r") as file:
        st.session_state.events_json = json.load(file)

if "game_data.json" not in st.session_state:
    with open("game_data.json", "r") as file:
        st.session_state.game_data_json = json.load(file)


if "current_round" not in st.session_state:
    st.session_state.current_round = 1
if "phase" not in st.session_state:
    st.session_state.phase = "tutorial"


if st.session_state.phase == "tutorial":
    tutorial.show_tutorial()

    if st.button(
        "Fertig mit dem Tutorial", key=f"next_event_{st.session_state.current_round}"
    ):
        st.session_state.phase = "player_input"
        st.rerun()

elif st.session_state.phase == "player_input":
    num = input_manager.input_start_values()

    if num is not None:
        st.session_state.number_of_players = num
        st.session_state.phase = "event"
        st.rerun()  # erzwungener Neustart hinzu

elif st.session_state.phase == "event":
    if st.session_state.field.player_has_won() != False:
        st.text(
            f"Spieler {st.session_state.field.player_has_won()} hat komplette Dominaz im Drogenmark gezeigt und damit gewonnen!"
        )
    else:
        st.text("Ereignis: \n")

        event_text = event_manager.get_event(
            st.session_state.events_json,
            st.session_state.game_data_json,
            st.session_state.current_round,
        )
        st.write(event_text)
        st.text("\n")

        st.text("\nKunden der Spieler pro Feld: \n")

        customer_per_field = st.session_state.field.calculate_customers()
        st.text(st.session_state.field.show_customers_by_player(customer_per_field))

        if st.button("Weiter", key=f"next_event_{st.session_state.current_round}"):
            st.session_state.phase = "input"
            st.rerun()  # erzwungener Neustart hinzu

elif st.session_state.phase == "input":
    input_manager.input_round_values()

    if st.button("Weiter", key=f"next_input_{st.session_state.current_round}"):
        st.session_state.current_round += 1
        st.session_state.phase = "event"
        st.rerun()  # erzwungener Neustart hinzuzu
