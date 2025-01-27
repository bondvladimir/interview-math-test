import streamlit as st
import random
import time

st.set_page_config(page_title="Interview Math Test", layout="centered")

# Инициализируем сессию
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "time_left" not in st.session_state:
    st.session_state.time_left = 300  # 5 минут в секундах
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "questions" not in st.session_state:
    # Генерируем 50 (A, B)
    st.session_state.questions = [(random.randint(10, 99), random.randint(10, 99)) for _ in range(50)]
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * 50

# Функция подсчёта очков
def calculate_score():
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
st.write("Solve each expression: **2*A - B**. You have 5 minutes in total.")

# Если тест ещё не начат
if not st.session_state.test_started:
    st.markdown("Press the button below to begin.")
    if st.button("Start"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()  # Запоминаем момент старта
        st.experimental_rerun()
else:
    # Считаем, сколько осталось времени
    elapsed = time.time() - st.session_state.start_time
    st.session_state.time_left = 300 - int(elapsed)
    if st.session_state.time_left < 0:
        st.session_state.time_left = 0

    # Отображаем таймер крупно
    st.markdown(
        f"<h2 style='text-align: center; color: red;'>Time left: {st.session_state.time_left} sec</h2>",
        unsafe_allow_html=True
    )

    # Автообновление раз в 1000 мс (1 сек), чтобы таймер менялся автоматически
    st.experimental_autorefresh(interval=1000, limit=None)

    # Если время вышло или все вопросы пройдены — финальный счёт
    if st.session_state.time_left == 0 or st.session_state.current_q >= 50:
        score = calculate_score()
        st.write(f"**Your final score:** {score} out of 50")
        st.stop()

    # Прогресс (от 0 до 1)
    progress_val = st.session_state.current_q / 50
    st.progress(progress_val)

    # Текущий вопрос
    A, B = st.session_state.questions[st.session_state.current_q]
    st.subheader(f"Question {st.session_state.current_q + 1} of 50")
    user_input = st.text_input(f"Calculate 2*{A} - {B} =", key=f"answer_{st.session_state.current_q}")

    # Кнопка "Submit" — сохраняем ответ и переходим к следующему
    if st.button("Submit"):
        st.session_state.user_answers[st.session_state.current_q] = user_input
        st.session_state.current_q += 1
        st.experimental_rerun()
