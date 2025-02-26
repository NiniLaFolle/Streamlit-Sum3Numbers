# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import random
import time
import pandas as pd

def add_3_numbers():

    def generate_numbers(max_value):
        """Génère trois nombres entiers aléatoires entre 1 et max_value."""
        return random.randint(1, max_value), random.randint(1, max_value), random.randint(1, max_value)

    st.title("Jeu de Calcul Mental")

    if "questions" not in st.session_state:
        st.session_state.questions = []
        st.session_state.current_index = 0
        st.session_state.correct_answers = 0
        st.session_state.start_time = None
        st.session_state.game_active = False
        st.session_state.user_answers = []
        st.session_state.timer_enabled = False

    # Choix du nombre de questions, de la valeur maximale et de l'activation du timer
    if not st.session_state.game_active:
        num_questions = st.slider("Choisissez le nombre de questions :", min_value=5, max_value=40, value=10)
        max_value = st.slider("Choisissez la valeur maximale des nombres :", min_value=10, max_value=100, value=10)
        st.session_state.timer_enabled = st.checkbox("Activer le timer")
        if st.button("Commencer le jeu"):
            st.session_state.questions = [generate_numbers(max_value) for _ in range(num_questions)]
            st.session_state.current_index = 0
            st.session_state.correct_answers = 0
            if st.session_state.timer_enabled:
                st.session_state.start_time = time.time()
            st.session_state.game_active = True
            st.session_state.user_answers = []
            st.rerun()

    if st.session_state.game_active:
        if st.session_state.current_index < len(st.session_state.questions):
            a, b, c = st.session_state.questions[st.session_state.current_index]
            st.write(f"Question {st.session_state.current_index + 1}: {a} + {b} + {c} = ?")

            with st.form(key=f"form_{st.session_state.current_index}"):
                user_input = st.text_input("Votre réponse :", key=f"input_{st.session_state.current_index}")
                submit_button = st.form_submit_button(label="Valider")

            if submit_button and user_input:
                correct_sum = a + b + c
                st.session_state.user_answers.append((a, b, c, int(user_input), correct_sum))
                if int(user_input) == correct_sum:
                    st.session_state.correct_answers += 1
                    st.success("Bonne réponse !")
                else:
                    st.error(f"Mauvaise réponse ! La bonne réponse était {correct_sum}.")

                st.session_state.current_index += 1
                st.rerun()

        else:
            # Fin du jeu
            if st.session_state.timer_enabled:
                total_time = time.time() - st.session_state.start_time
                st.write(f"Temps total : {total_time:.2f} secondes")
            st.success(f"Fin du jeu ! Score : {st.session_state.correct_answers}/{len(st.session_state.questions)}")

            # Afficher le récapitulatif
            recap_data = {
                "Question": [f"{a} + {b} + {c}" for a, b, c, _, _ in st.session_state.user_answers],
                "Votre réponse": [user_input for _, _, _, user_input, _ in st.session_state.user_answers],
                "Bonne réponse": [correct_sum for _, _, _, _, correct_sum in st.session_state.user_answers]
            }
            df = pd.DataFrame(recap_data)

            # Apply styling to highlight wrong answers
            def highlight_wrong(s):
                return ['background-color: red' if s['Votre réponse'] != s['Bonne réponse'] else '' for _ in s.index]

            styled_df = df.style.apply(highlight_wrong, axis=1)
            st.dataframe(styled_df)

            if st.button("Rejouer"):
                st.session_state.game_active = False
                st.session_state.questions = []
                st.rerun()

st.set_page_config(page_title="Jeu d'addition", page_icon="📈")
st.markdown("# Additionne 3 nombres")
st.sidebar.header("Additionne 3 nombres")


add_3_numbers()
