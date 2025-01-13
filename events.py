import random
import streamlit as st


class Event:
    def get_event(self, event_data, game_data, current_round):
        if "lieferanten" not in st.session_state:
            st.session_state.lieferanten = []

        events = event_data["data"]
        drogen = game_data["drogen"]
        lieferanten = game_data["lieferanten"]

        filtered_data = [
            entry for entry in events if current_round >= entry["min_round"]
        ]

        if not filtered_data:
            return "ERROR"

        texts = [entry["text"] for entry in filtered_data]
        probabilities = [entry["probability"] for entry in filtered_data]

        event = random.choices(texts, weights=probabilities, k=1)[0]

        if "*D*" in event:
            event = event.replace("*D*", random.choice(drogen)["name"])

        if "*B*" in event:
            event = event.replace("*B*", str(random.randint(1, 9)))

        if "*S*" in event:
            event = event.replace("*S*", str(random.randint(1, 3)))

        if "*L*" in event:
            lieferant = random.choice(lieferanten)["name"]
            while lieferant in st.session_state.lieferanten:
                lieferant = random.choice(lieferanten)["name"]

            st.session_state.lieferanten.append(lieferant)
            event = event.replace("*L*", lieferant)

            for l in lieferanten:
                if l["name"] == lieferant:
                    event = event.replace("*LD*", l["dorge"])
                    break

        return event
