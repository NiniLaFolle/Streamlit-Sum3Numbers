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



def divide_numbers():
    def generate_numbers(max_divisor, max_quotient):
        """Generate a random dividend and divisor for integer division."""
        generated_divisor = random.randint(1, max_divisor)  # Avoid zero as divisor
        generated_dividend = generated_divisor * random.randint(1, max_quotient)  # Ensure exact division
        return generated_dividend, generated_divisor

    st.title("Jeu de Division")

    if "questions" not in st.session_state:
        st.session_state.questions = []
        st.session_state.current_index = 0
        st.session_state.correct_answers = 0
        st.session_state.start_time = None
        st.session_state.game_active = False
        st.session_state.user_answers = []
        st.session_state.timer_enabled = False

    # Choix du nombre de questions, de la valeur maximale et de l'activation du timer
    if "questions" not in st.session_state:
        st.session_state.questions = []
        st.session_state.current_index = 0
        st.session_state.correct_answers = 0
        st.session_state.start_time = None
        st.session_state.game_active = False
        st.session_state.user_answers = []
        st.session_state.timer_active = False

    # Select the number of questions, max divisor, and max quotient
    if not st.session_state.game_active:
        num_questions = st.slider("Choisis le nombre de questions:", min_value=1, max_value=50, value=10)
        max_divisor = st.slider("Choisis le diviseur maximal:", min_value=1, max_value=100, value=20)
        max_quotient = st.slider("Choisis le quotient maximal", min_value=1, max_value=100, value=20)
        st.session_state.timer_active = st.checkbox("Joue avec un chrono")
        if st.button("Démarre le jeu"):
            st.session_state.questions = [generate_numbers(max_divisor, max_quotient) for _ in range(num_questions)]
            st.session_state.current_index = 0
            st.session_state.correct_answers = 0
            st.session_state.user_answers = []
            if st.session_state.timer_active:
                st.session_state.start_time = time.time()
            st.session_state.game_active = True
            st.rerun()

    if st.session_state.game_active:
        if st.session_state.current_index < len(st.session_state.questions):
            dividend, divisor = st.session_state.questions[st.session_state.current_index]
            st.write(f"Question {st.session_state.current_index + 1}: {dividend} ÷ {divisor} = ?")

            with st.form(key=f"form_{st.session_state.current_index}"):
                user_input = st.number_input("Ta réponse:", min_value=0, step=1, format="%d",
                                             key=f"input_{st.session_state.current_index}", value=None)
                submit_button = st.form_submit_button(label="Valide")

            if submit_button:
                correct_result = dividend // divisor
                st.session_state.user_answers.append((dividend, divisor, user_input, correct_result))
                if user_input == correct_result:
                    st.session_state.correct_answers += 1
                    st.success("Bonne réponse!")
                else:
                    st.error(f"Mauvaise réponse! La bonne réponse était {correct_result}.")

                st.session_state.current_index += 1
                st.rerun()
        else:
            # End of the game
            total_time = time.time() - st.session_state.start_time if st.session_state.timer_active else None
            st.success(f"Fin du jeu! Score: {st.session_state.correct_answers}/{len(st.session_state.questions)}")
            if total_time:
                st.write(f"Chrono: {total_time:.2f} seconds")

            # Display recap table with highlighted wrong answers
            recap_data = []
            for q in st.session_state.user_answers:
                if q[2] != q[3]:
                    recap_data.append(
                        f"<tr style='background-color: #ffcccc;'><td>{q[0]}</td><td>{q[1]}</td><td>{q[2]}</td><td>{q[3]}</td></tr>")
                else:
                    recap_data.append(f"<tr><td>{q[0]}</td><td>{q[1]}</td><td>{q[2]}</td><td>{q[3]}</td></tr>")

            recap_table = f"""
            <table>
                <thead>
                    <tr>
                        <th>Dividend</th>
                        <th>Divisor</th>
                        <th>Your Answer</th>
                        <th>Correct Answer</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(recap_data)}
                </tbody>
            </table>
            """
            st.markdown(recap_table, unsafe_allow_html=True)

            if st.button("Rejouer"):
                st.session_state.game_active = False
                st.session_state.questions = []
                st.rerun()

st.set_page_config(page_title="Jeu de Division", page_icon="📊")
st.markdown("# Divise 2 nombres")
st.sidebar.header("Divise 2 nombres")

divide_numbers()
