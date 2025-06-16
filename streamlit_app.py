# import streamlit as st
# import json
# import random
#
# st.set_page_config(page_title="Fanlar bo‘yicha test", page_icon="🧠")
#
# # Fanni tanlash
# subject = st.selectbox("Fan tanlang:", ["Python", "Ingliz tili"])
#
# # Test usulini tanlash
# test_mode = st.radio("Test turi:", ["100 ta to‘liq", "25 ta random"], horizontal=True)
#
# # Fayl nomlarini aniqlaymiz
# file_map = {
#     "Python": "Python_test.json",
#     "Ingliz tili": "English_test.json"
# }
# file_name = file_map[subject]
#
# # Savollarni yuklash
# with open(file_name, "r", encoding="utf-8") as f:
#     all_questions = json.load(f)
#
# # Test holatini boshlash
# if "questions" not in st.session_state or st.session_state.get("current_subject") != subject or st.session_state.get(
#         "test_mode") != test_mode:
#     st.session_state.current_subject = subject
#     st.session_state.test_mode = test_mode
#
#     if test_mode == "100 ta to‘liq":
#         st.session_state.questions = all_questions[:]
#     else:
#         num_questions = min(25, len(all_questions))
#         st.session_state.questions = random.sample(all_questions, num_questions)
#
#     st.session_state.score = 0
#     st.session_state.answered = [None] * len(st.session_state.questions)
#     st.session_state.shuffled_options = []
#     st.session_state.results_shown = False  # Yangi kalit
#
#     for q in st.session_state.questions:
#         opts = q["options"][:]
#         random.shuffle(opts)
#         st.session_state.shuffled_options.append(opts)
#
# questions = st.session_state.questions
#
# st.title(f"📚 {subject} fanidan test")
#
# # Savollarni chiqarish
# for idx, q in enumerate(questions, 1):
#     st.markdown(f"### {idx}-savol (ID: {q.get('id', '—')}): {q['question']}")
#
#     options = st.session_state.shuffled_options[idx - 1]
#     user_answer = st.radio(
#         label="Variantni tanlang:",
#         options=options,
#         key=f"q{idx}",
#         index=options.index(st.session_state.answered[idx - 1]) if st.session_state.answered[idx - 1] else None,
#         label_visibility="collapsed"
#     )
#
#     if user_answer:
#         st.session_state.answered[idx - 1] = user_answer
#
# # Tugma va yakuniy natijani ko‘rsatish
# if st.button("✅ Javoblarni tekshirish") or st.session_state.results_shown:
#     st.session_state.results_shown = True
#     st.session_state.score = 0
#     st.markdown("## 🧾 Natijalar:")
#
#     for idx, q in enumerate(questions, 1):
#         user_ans = st.session_state.answered[idx - 1]
#         correct_ans = q["answer"]
#         st.markdown(f"**{idx}-savol:** {q['question']}")
#
#         if user_ans == correct_ans:
#             st.success(f"✅ To‘g‘ri! Siz tanladingiz: {user_ans}")
#             st.session_state.score += 1
#         elif user_ans is None:
#             st.warning(f"⚠️ Javob berilmagan. To‘g‘ri javob: {correct_ans}")
#         else:
#             st.error(f"❌ Noto‘g‘ri. Siz tanladingiz: {user_ans}, to‘g‘ri javob: {correct_ans}")
#
#     st.markdown("---")
#     st.subheader(f"Umumiy natija: {st.session_state.score} / {len(questions)}")


import streamlit as st
import json
import random

st.set_page_config(page_title="Fanlar bo‘yicha test", page_icon="🧠")

# Fanni tanlash
subject = st.selectbox("Fan tanlang:", ["Python", "Ingliz tili"])

# Test usulini tanlash
test_mode = st.radio("Test turi:", ["100 ta to‘liq", "25 ta random"], horizontal=True)

# Fayl nomlarini aniqlaymiz
file_map = {
    "Python": "Python_test.json",
    "Ingliz tili": "English_test.json"
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
        opts = q["options"][:]
        random.shuffle(opts)
        st.session_state.shuffled_options.append(opts)

questions = st.session_state.questions

st.title(f"📚 {subject} fanidan test")

for idx, q in enumerate(questions, 1):
    st.markdown(f"### {idx}-savol (ID: {q.get('id', '—')}): {q['question']}")

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
        if user_answer == q["answer"]:
            st.session_state.score += 1

    if st.session_state.answered[idx - 1]:
        if st.session_state.answered[idx - 1] == q["answer"]:
            st.success(f"✅ To‘g‘ri! Javob: {q['answer']}")
        else:
            st.error(f"❌ Noto‘g‘ri. To‘g‘ri javob: {q['answer']}")

st.markdown("---")
st.subheader(f"Umumiy natija: {st.session_state.score} / {len(questions)}")

