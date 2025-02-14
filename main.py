import streamlit as st
import time
import random

st.set_page_config(page_title="Interview Math Test", layout="centered")

if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "time_left" not in st.session_state:
    st.session_state.time_left = 300  # 5 минут (300 секунд)
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "questions" not in st.session_state:
    st.session_state.questions = [
        (random.randint(10, 99), random.randint(10, 99)) 
        for _ in range(30)
    ]
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * 30

def calculate_score():
    correct_count = 0
    for i, (A, B) in enumerate(st.session_state.questions):
        correct_val = 2*A - B
        ans = st.session_state.user_answers[i]
        if ans is not None:
            try:
                if int(ans) == correct_val:
                    correct_count += 1
            except:
                pass
    return correct_count

st.title("Interview Math Test (30 questions)")
st.write("You have **5 minutes**. Press **Start** to begin.")

if not st.session_state.test_started:
    # Пока не нажали "Start"
    if st.button("Start"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()
        st.session_state.time_left = 300
else:
    # Тест уже идёт
    elapsed = time.time() - st.session_state.start_time
    st.session_state.time_left = 300 - int(elapsed)
    if st.session_state.time_left < 0:
        st.session_state.time_left = 0

    st.markdown(f"**Time left: {st.session_state.time_left} seconds**")

    # Проверяем, вышло ли время или закончились вопросы
    if st.session_state.time_left == 0 or st.session_state.current_q >= 30:
        score = calculate_score()
        st.write(f"**Your final score:** {score} / 30")
        st.stop()

    # Прогресс
    progress_val = st.session_state.current_q / 30
    st.progress(progress_val)

    # Текущий вопрос
    A, B = st.session_state.questions[st.session_state.current_q]
    user_answer = st.text_input(
        f"Question {st.session_state.current_q + 1} of 30: 2 * {A} - {B} =",
        key=f"answer_{st.session_state.current_q}"
    )

    # JS для автофокуса
    st.markdown(
        """
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            const inputs = document.querySelectorAll('input[type="text"]');
            if (inputs.length > 0) {
                inputs[inputs.length - 1].focus();
            }
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    if st.button("Submit"):
        st.session_state.user_answers[st.session_state.current_q] = user_answer
        st.session_state.current_q += 1
        # Не вызываем experimental_rerun, так как 
        # старая версия Streamlit может её не поддерживать
        # и при клике уже идёт перерисовка автоматически.
    
    # (Можно отладочно посмотреть, что именно записалось)
    # st.write("DEBUG user_answers:", st.session_state.user_answers)
