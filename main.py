import streamlit as st
import time
import random

st.set_page_config(page_title="Interview Math Test", layout="centered")

# Инициализация ключей в session_state, чтобы избежать KeyError:
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "time_left" not in st.session_state:
    st.session_state.time_left = 300  # 5 минут в секундах
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "questions" not in st.session_state:
    # Сгенерируем 50 случайных пар (A, B)
    st.session_state.questions = [(random.randint(10, 99), random.randint(10, 99)) for _ in range(50)]
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * 50

def calculate_score():
    """Подсчитать количество правильных ответов."""
    correct_count = 0
    for i, (A, B) in enumerate(st.session_state.questions):
        correct_val = 2 * A - B
        ans = st.session_state.user_answers[i]
        if ans is not None:
            try:
                if int(ans) == correct_val:
                    correct_count += 1
            except:
                pass
    return correct_count

st.title("Interview Math Test")
st.write("Solve each expression: **2*A - B**. You have **5 minutes** in total. "
         "Press **Start** to begin the timer.")

if not st.session_state.test_started:
    # Пока пользователь не нажал Start
    if st.button("Start"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()
        st.session_state.time_left = 300  # сбросим на 5 минут заново

else:
    # Тест запущен: считаем сколько секунд прошло и обновляем time_left
    elapsed = time.time() - st.session_state.start_time
    st.session_state.time_left = 300 - int(elapsed)
    if st.session_state.time_left < 0:
        st.session_state.time_left = 0

    # Отображаем таймер крупными цифрами
    st.markdown(
        f"<h2 style='text-align: center; color: red;'>Time left: {st.session_state.time_left} sec</h2>",
        unsafe_allow_html=True
    )
    # Обновляем страницу каждую секунду, чтобы таймер убывал на глазах
    st.experimental_autorefresh(interval=1000)

    # Проверяем, вышло ли время или дошли ли мы до конца
    if st.session_state.time_left == 0 or st.session_state.current_q >= 50:
        score = calculate_score()
        st.write(f"**Your final score:** {score} out of 50")
        st.stop()  # Останавливаем выполнение кода

    # Полоса прогресса — от 0.0 до 1.0
    progress_val = st.session_state.current_q / 50
    st.progress(progress_val)

    # Текущий вопрос
    A, B = st.session_state.questions[st.session_state.current_q]
    st.subheader(f"Question {st.session_state.current_q + 1} of 50")
    user_answer = st.text_input(f"Calculate 2*{A} - {B} =", key=f"answer_{st.session_state.current_q}")

    # При клике "Submit" сохраняем ответ и переходим к следующему вопросу
    if st.button("Submit"):
        st.session_state.user_answers[st.session_state.current_q] = user_answer
        st.session_state.current_q += 1
        # Здесь **не** вызываем st.experimental_rerun().
        # Streamlit сам перерисует страницу, т.к. нажатие кнопки — это новое событие.
