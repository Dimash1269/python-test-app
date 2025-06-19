import streamlit as st
import json
import random

st.set_page_config(page_title="Fanlar bo‘yicha test", page_icon="🧠")

# Fanni tanlash
subject = st.selectbox("Fan tanlang:", [ "Grand blue1", "Grand blue2","Algoritm"])

# Test usulini tanlash
test_mode = st.radio("Test turi:", ["100 ta to‘liq", "25 ta random"], horizontal=True)

# Fayl nomlarini aniqlaymiz
file_map = { 
    "Grand blue1": "Grand_blue1.json",
    "Algoritm": "Algoritm.json",
   "Grand blue2": "Grand_blue2.json"
    
}
file_name = file_map[subject]

# Savollarni yuklaymiz
with open(file_name, "r", encoding="utf-8") as f:
    all_questions = json.load(f)

if "questions" not in st.session_state or st.session_state.get("current_subject") != subject or st.session_state.get("test_mode") != test_mode:
    st.session_state.current_subject = subject
    st.session_state.test_mode = test_mode

    if test_mode == "100 ta to‘liq":
        st.session_state.questions = all_questions[:]  # Barchasi
    else:
        num_questions = min(25, len(all_questions))
        st.session_state.questions = random.sample(all_questions, num_questions)

    st.session_state.score = 0
    st.session_state.answered = [None] * len(st.session_state.questions)
    st.session_state.shuffled_options = []
    for q in st.session_state.questions:
        opts = q["variantlar"][:]
        random.shuffle(opts)
        st.session_state.shuffled_options.append(opts)

questions = st.session_state.questions

st.title(f"📚 {subject} fanidan test")

for idx, q in enumerate(questions, 1):
    st.markdown(f"### {idx}-savol (ID: {q.get('id', '—')}): {q['savol']}")

    options = st.session_state.shuffled_options[idx - 1]

    user_answer = st.radio(
        label="Variantni tanlang:",
        options=options,
        key=f"q{idx}",
        index=options.index(st.session_state.answered[idx - 1]) if st.session_state.answered[idx - 1] else None,
        label_visibility="collapsed",
        disabled=st.session_state.answered[idx - 1] is not None
    )

    if user_answer and st.session_state.answered[idx - 1] is None:
        st.session_state.answered[idx - 1] = user_answer
        if user_answer == q["javob"]:
            st.session_state.score += 1

    if st.session_state.answered[idx - 1]:
        if st.session_state.answered[idx - 1] == q["javob"]:
            st.success(f"✅ To‘g‘ri! Javob: {q['javob']}")
        else:
            st.error(f"❌ Noto‘g‘ri. To‘g‘ri javob: {q['javob']}")

st.markdown("---")
st.subheader(f"Umumiy natija: {st.session_state.score} / {len(questions)}")

