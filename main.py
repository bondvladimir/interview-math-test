import streamlit as st
import time
import random

# Настройки (необязательно)
st.set_page_config(page_title="Interview Math Test", layout="centered")

# Инициализация необходимых ключей в session_state
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "time_left" not in st.session_state:
    st.session_state.time_left = 300  # 5 минут (300 секунд)
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "questions" not in st.session_state:
    # Генерируем 30 пар (A, B) двузначных чисел
    st.session_state.questions = [
        (random.randint(10, 99), random.randint(10, 99)) 
        for _ in range(30)
    ]
if "user_answers" not in st.session_state:
    st.session_state.user_answers = [None] * 30

def calculate_score():
    """Подсчитывает число правильных ответов."""
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
st.write(
    "Solve each expression: **2*A - B**.\n\n"
    "You have **5 minutes** in total. Press **Start** to begin."
)

# Если тест ещё не запущен, показываем кнопку Start
if not st.session_state.test_started:
    if st.button("Start"):
        st.session_state.test_started = True
        st.session_state.start_time = time.time()
        st.session_state.time_left = 300  # сбрасываем на 5 минут
else:
    # Тест уже идёт: рассчитываем, сколько осталось времени
    elapsed = time.time() - st.session_state.start_time
    st.session_state.time_left = 300 - int(elapsed)
    if st.session_state.time_left < 0:
        st.session_state.time_left = 0

    st.markdown(f"**Time left:** {st.session_state.time_left} seconds")

    # Проверяем, вышло ли время или пройдены все вопросы
    if st.session_state.time_left == 0 or st.session_state.current_q >= 30:
        score = calculate_score()
        st.write(f"**Your final score:** {score} out of 30")
        st.stop()

    # Прогресс-бар
    progress_val = st.session_state.current_q / 30
    st.progress(progress_val)

    # Текущий вопрос
    A, B = st.session_state.questions[st.session_state.current_q]
    st.subheader(f"Question {st.session_state.current_q + 1} of 30")
    user_answer = st.text_input(
        f"Calculate 2 * {A} - {B} =", 
        key=f"answer_{st.session_state.current_q}"
    )
    # JS-сниппет: после каждого рендера возвращаем фокус на последний text_input
    st.markdown(
        """
        <script>
        // Найдём все инпуты Streamlit
        var inputs = window.parent.document.querySelectorAll('input[data-baseweb="input"]');
        // Возьмём последний (текущий) и установим фокус
        if(inputs.length > 0){
            inputs[inputs.length - 1].focus();
        }
        </script>
        """,
        unsafe_allow_html=True
    )

    # Обрабатываем клик на "Submit"
    if st.button("Submit"):
        st.session_state.user_answers[st.session_state.current_q] = user_answer
        st.session_state.current_q += 1
        # Нет вызова experimental_rerun(), но при нажатии кнопки всё равно произойдёт перерисовка,
        # и появится следующий вопрос.
