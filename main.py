import streamlit as st
import random
import time

# 1) Инициализация сессии
if "questions" not in st.session_state:
    # Генерируем 50 (A, B)
    st.session_state.questions = [(random.randint(10,99), random.randint(10,99)) for _ in range(50)]
    
    # Здесь храним ответы пользователя
    st.session_state.user_answers = [None]*50
    
    # Текущий индекс вопроса
    st.session_state.current_q = 0
    
    # Установим дедлайн (через 5 минут = 300 секунд)
    st.session_state.end_time = time.time() + 300

st.title("Interview Math Test")
st.write("You have **5 minutes** to solve 50 questions. Each question is of the form `2*A - B`. "
         "Submit your answer to move to the next question. Good luck!")

# 2) Считаем, сколько осталось времени
time_left = int(st.session_state.end_time - time.time())
if time_left < 0:
    time_left = 0

# Показываем оставшееся время
st.markdown(f"**Time left:** {time_left} seconds")

current_q = st.session_state.current_q

# 3) Если время вышло или все 50 отвечены — итог
if time_left == 0 or current_q >= 50:
    # Подсчёт результатов
    correct_count = 0
    for i, (A, B) in enumerate(st.session_state.questions):
        correct_value = 2*A - B
        user_val = st.session_state.user_answers[i]
        # Сравниваем, если ответ был введён
        if user_val is not None:
            try:
                if int(user_val) == correct_value:
                    correct_count += 1
            except:
                pass

    st.write(f"**Your final score:** {correct_count} out of 50")

    # Блокируем дальнейшие действия
    st.stop()

# 4) Отображаем прогресс
progress_val = current_q / 50
st.progress(progress_val)

# 5) Показываем текущий вопрос
A, B = st.session_state.questions[current_q]
st.subheader(f"Question {current_q + 1} of 50")
user_input = st.text_input(f"Calculate 2*{A} - {B} =", key=f"answer_{current_q}")

# 6) Кнопка "Submit"
if st.button("Submit"):
    # Сохраняем ответ
    st.session_state.user_answers[current_q] = user_input
    # Переходим к следующему вопросу
    st.session_state.current_q += 1
    # Перезагружаем интерфейс (чтобы обновилось всё автоматически)
    st.experimental_rerun()
