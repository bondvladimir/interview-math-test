import streamlit as st
import time
import random

# Настройки страницы (необязательно)
st.set_page_config(page_title="Interview Math Test", layout="centered")

# 1) Инициализация ключей в session_state, чтобы избежать KeyError
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "time_left" not in st.session_state:
    st.session_state.time_left = 300  # 5 минут в секундах
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "questions" not in st.session_state:
    # Сгенерируем 50 пар (A, B) для задач 2*A - B
    st.session_state.questions = [(random.randint(10, 99), random.randint(10, 99)) for _ in range(50)]
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * 50

def calculate_score():
    """Подсчитать количество правильных ответов (2*A - B)."""
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

# Заголовок приложения
st.title("Interview Math Test")
st.write(
    "You have **5 minutes** to solve up to 50 questions. Each question is of the form **2*A - B**.\n"
    "Press **Start** to begin the timer."
)

# 2) Логика запуска теста
if not st.session_state.test_started:
    # Пока не нажали "Start"
    if st.button("Start"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()  # запоминаем текущий момент
        st.session_state.time_left = 300          # сбрасываем таймер на 5 минут
else:
    # Тест уже идёт: считаем, сколько осталось времени
    elapsed = time.time() - st.session_state.start_time
    st.session_state.time_left = 300 - int(elapsed)
    if st.session_state.time_left < 0:
        st.session_state.time_left = 0  # зажимаем на 0, если время вышло

    # Выводим оставшееся время
    st.markdown(f"**Time left:** {st.session_state.time_left} seconds")

    # 3) Проверяем, закончилось ли время или все вопросы отвечены
    if st.session_state.time_left == 0 or st.session_state.current_q >= 50:
        score = calculate_score()
        st.write(f"**Your final score:** {score} out of 50")
        st.stop()  # останавливаем дальнейший код

    # 4) Прогресс-бар (0..1)
    progress_val = st.session_state.current_q / 50
    st.progress(progress_val)

    # 5) Текущий вопрос
    A, B = st.session_state.questions[st.session_state.current_q]
    st.subheader(f"Question {st.session_state.current_q + 1} of 50")
    user_answer = st.text_input(
        f"Calculate 2*{A} - {B} =",
        key=f"answer_{st.session_state.current_q}"  # чтобы привязать значение к номеру вопроса
    )

    # 6) При нажатии "Submit" сохраняем ответ и переходим к следующему вопросу
    if st.button("Submit"):
        st.session_state.user_answers[st.session_state.current_q] = user_answer
        st.session_state.current_q += 1
        # Без experimental_rerun: просто обновим интерфейс
        # при следующем "событии" (нажатие, перезагрузка), 
        # вопрос сменится, так как current_q уже увеличен.
        # При желании можно попросить пользователя вручную нажать «Next question» 
        # или обновить страницу.
