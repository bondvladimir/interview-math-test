import streamlit as st
import random

if "questions" not in st.session_state:
    st.session_state.questions = []
    for _ in range(50):
        A = random.randint(10, 99)
        B = random.randint(10, 99)
        st.session_state.questions.append((A, B))

st.title("Interview Math Test")
st.write("Тест из 50 вопросов. Найдите значение выражения 2*A - B.")

user_answers = {}

for i, (A, B) in enumerate(st.session_state.questions, start=1):
    user_input = st.text_input(f"Вопрос {i}: 2*{A} - {B} = ?", key=f"answer_{i}")
    user_answers[i] = user_input

if st.button("Отправить"):
    correct_count = 0
    for i, (A, B) in enumerate(st.session_state.questions, start=1):
        correct_result = 2*A - B
        try:
            if int(user_answers[i]) == correct_result:
                correct_count += 1
        except:
            pass

    st.write(f"Ваш результат: {correct_count} из 50.")
