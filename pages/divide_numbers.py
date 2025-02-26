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

    # 🔹 Ensure all session state variables are initialized
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "correct_answers" not in st.session_state:
        st.session_state.correct_answers = 0
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "game_active" not in st.session_state:
        st.session_state.game_active = False
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []
    if "timer_active" not in st.session_state:
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
            st.session_state.game_active = True

            # 🔹 Initialize timer only if enabled
            if st.session_state.timer_active:
                st.session_state.start_time = time.time()

            st.rerun()

    if st.session_state.game_active:
        if st.session_state.current_index < len(st.session_state.questions):
            dividend, divisor = st.session_state.questions[st.session_state.current_index]
            st.write(f"Question {st.session_state.current_index + 1}: {dividend} ÷ {divisor} = ?")

            with st.form(key=f"form_{st.session_state.current_index}"):
                user_input = st.number_input("Ta réponse:", min_value=0, step=1, format="%d",
                                             key=f"input_{st.session_state.current_index}")
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
            # 🔹 Calculate elapsed time only if timer was active
            total_time = None
            if st.session_state.timer_active and st.session_state.start_time is not None:
                total_time = time.time() - st.session_state.start_time

            st.success(f"Fin du jeu! Score: {st.session_state.correct_answers}/{len(st.session_state.questions)}")
            if total_time is not None:
                st.write(f"Chrono: {total_time:.2f} secondes")

            # Display recap table with highlighted wrong answers
            recap_data = {
                "Dividend": [q[0] for q in st.session_state.user_answers],
                "Divisor": [q[1] for q in st.session_state.user_answers],
                "Votre réponse": [q[2] for q in st.session_state.user_answers],
                "Bonne réponse": [q[3] for q in st.session_state.user_answers]
            }
            df = pd.DataFrame(recap_data)

            # Apply styling to highlight wrong answers
            def highlight_wrong(s):
                return ['background-color: red' if s['Votre réponse'] != s['Bonne réponse'] else '' for _ in s.index]

            styled_df = df.style.apply(highlight_wrong, axis=1)
            st.dataframe(styled_df)

            if st.button("Rejouer"):
                # 🔹 Reset session state completely before restarting
                st.session_state.game_active = False
                st.session_state.questions = []
                st.session_state.current_index = 0
                st.session_state.correct_answers = 0
                st.session_state.start_time = None
                st.session_state.user_answers = []
                st.session_state.timer_active = False
                st.rerun()

st.set_page_config(page_title="Jeu de Division", page_icon="📊")
st.markdown("# Divise 2 nombres")
st.sidebar.header("Divise 2 nombres")

divide_numbers()
