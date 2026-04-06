import streamlit as st
import json
import os

embedded_questions = [
    "How often do you arrange your study desk before starting work?",
    "How frequently do you remove unnecessary items from your workspace?",
    "How often does a cluttered desk make it difficult for you to concentrate?",
    "How often do you organize your study materials such as books, notes, and devices?",
    "How often do you feel mentally clear when your workspace is tidy?",
    "How frequently do you misplace items because your desk is disorganized?",
    "How often do you clean your desk after completing your study session?",
    "How often does a messy workspace increase your stress level?",
    "How frequently do you arrange your tools for easy access before studying?",
    "How often do objects on your desk distract you while working?",
    "How often do you feel more productive in a clean and organized workspace?",
    "How frequently do you spend time searching for items on your desk?",
    "How often do you feel overwhelmed due to clutter in your workspace?",
    "How often do you prepare your desk before starting important tasks?",
    "How frequently does your study environment affect your concentration?"
]

def load_questions():
    if os.path.exists("questions.json"):
        with open("questions.json") as f:
            return json.load(f)
    return embedded_questions

def save_result(data):
    results = []
    if os.path.exists("survey_results.json"):
        with open("survey_results.json") as f:
            results = json.load(f)
    results.append(data)
    with open("survey_results.json", "w") as f:
        json.dump(results, f, indent=4)

questions = load_questions()

st.title("Desk Organization Survey")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.score = 0
    st.session_state.index = 0
    st.session_state.answers = []

if st.session_state.step == 1:
    name = st.text_input("Name")
    dob = st.text_input("DOB (YYYY-MM-DD)")
    sid = st.text_input("Student ID")

    if st.button("Start"):
        st.session_state.user = {"name": name, "dob": dob, "sid": sid}
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 2:
    i = st.session_state.index
    if i < len(questions):
        q = questions[i]
        st.write(q)
        ans = st.radio("Answer", ["0","1","2","3","4"])

        if st.button("Next"):
            val = int(ans)
            score = 4 - val
            st.session_state.score += score
            st.session_state.index += 1
            st.rerun()
    else:
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    score = st.session_state.score
    max_score = len(questions)*4
    st.write(f"Score: {score}/{max_score}")

    save_result({"user": st.session_state.user, "score": score})

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
