import streamlit as st
import json
import os

# -----------------------------
# Embedded questions
# -----------------------------
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

# -----------------------------
# File helpers
# -----------------------------
def load_questions():
    if os.path.exists("questions.json"):
        try:
            with open("questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            valid_questions = []
            for q in data:  # for loop validation
                if isinstance(q, str) and q.strip():
                    valid_questions.append(q.strip())

            if valid_questions:
                return valid_questions
        except Exception:
            pass

    return embedded_questions


def load_previous_results():
    if os.path.exists("survey_results.json"):
        try:
            with open("survey_results.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def save_result(result_data):
    results = load_previous_results()
    results.append(result_data)

    with open("survey_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


# -----------------------------
# Validation functions
# -----------------------------
def validate_name(name):
    if not name.strip():
        return False

    i = 0
    while i < len(name):  # while loop validation
        c = name[i]
        if not (c.isalpha() or c in " -'"):
            return False
        i += 1
    return True


def validate_dob(dob):
    parts = dob.split("-")
    if len(parts) != 3:
        return False

    for p in parts:  # for loop validation
        if not p.isdigit():
            return False

    year, month, day = map(int, parts)

    if year < 1900 or year > 2100:
        return False
    if not (1 <= month <= 12):
        return False
    if not (1 <= day <= 31):
        return False
    return True


def validate_student_id(student_id):
    return student_id.isdigit() and len(student_id) >= 4


# -----------------------------
# Score logic
# -----------------------------
def calculate_question_score(question, answer, questions):
    positive_questions = {questions[4], questions[10]} if len(questions) >= 11 else set()

    if question in positive_questions:
        return answer
    return 4 - answer


# -----------------------------
# Result logic
# -----------------------------
def get_result_details(score, max_score):
    percentage = (score / max_score) * 100 if max_score else 0.0

    if score <= 12:
        level = "Excellent"
        interpretation = (
            "You appear to maintain a highly organized workspace. "
            "Your desk habits strongly support concentration, productivity, and mental clarity."
        )
        suggestions = [
            "Maintain your current desk organization routine.",
            "Keep only essential materials on your desk.",
            "Continue cleaning your workspace regularly.",
            "Use your tidy environment for deep-focus study sessions."
        ]
    elif score <= 24:
        level = "Good"
        interpretation = (
            "Your workspace habits are generally good, although some minor distractions "
            "may still affect your focus occasionally."
        )
        suggestions = [
            "Remove unnecessary items before studying.",
            "Create fixed places for books, notes, and devices.",
            "Do a short cleanup after each session.",
            "Reduce the items that distract you most."
        ]
    elif score <= 36:
        level = "Moderate"
        interpretation = (
            "Your workspace organization is average. Sometimes your environment supports focus, "
            "but clutter may still interrupt your concentration."
        )
        suggestions = [
            "Create a daily routine for desk organization.",
            "Use folders, trays, or storage boxes.",
            "Keep unrelated objects away from your desk.",
            "Clean small areas regularly."
        ]
    elif score <= 48:
        level = "Low Focus"
        interpretation = (
            "Your study environment may often reduce concentration and increase stress. "
            "Improving workspace organization could noticeably improve mental clarity."
        )
        suggestions = [
            "Clear clutter before important work.",
            "Group desk items by category.",
            "Keep only the most-used materials nearby.",
            "Spend 5 minutes daily resetting your workspace."
        ]
    else:
        level = "Very Low Focus"
        interpretation = (
            "A disorganized workspace may be strongly affecting concentration, stress level, "
            "and study efficiency. Immediate improvement is recommended."
        )
        suggestions = [
            "Completely reset your desk.",
            "Keep only tools needed for the current task.",
            "Create fixed places for each item.",
            "Clean and organize your workspace every day.",
            "Build better study habits in a tidy environment."
        ]

    return percentage, level, interpretation, suggestions


# -----------------------------
# App setup
# -----------------------------
st.set_page_config(page_title="Desk Organization Survey", page_icon="🧠", layout="centered")
questions = load_questions()
max_score = len(questions) * 4

# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if "answers" not in st.session_state:
    st.session_state.answers = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "result_saved" not in st.session_state:
    st.session_state.result_saved = False


def reset_survey():
    st.session_state.user_data = {}
    st.session_state.answers = []
    st.session_state.score = 0
    st.session_state.question_index = 0
    st.session_state.result_saved = False
    st.session_state.page = "home"


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Menu")
if st.sidebar.button("Home"):
    st.session_state.page = "home"
    st.rerun()

if st.sidebar.button("Previous Results"):
    st.session_state.page = "previous_results"
    st.rerun()

if st.sidebar.button("Restart Survey"):
    reset_survey()
    st.rerun()


# -----------------------------
# Home page
# -----------------------------
if st.session_state.page == "home":
    st.title("Desk Organization and Mental Clarity Survey")
    st.write(
        "This survey evaluates how desk organization affects concentration, productivity, "
        "and mental clarity."
    )

    with st.form("user_info_form"):
        name = st.text_input("Full Name")
        dob = st.text_input("Date of Birth (YYYY-MM-DD)")
        student_id = st.text_input("Student ID")
        submitted = st.form_submit_button("Start Survey")

    if submitted:
        if not validate_name(name):
            st.error("Invalid name. Use only letters, spaces, hyphens, or apostrophes.")
        elif not validate_dob(dob):
            st.error("Invalid date of birth. Please use valid format YYYY-MM-DD.")
        elif not validate_student_id(student_id):
            st.error("Student ID must contain only numbers and be at least 4 digits.")
        else:
            st.session_state.user_data = {
                "name": name,
                "dob": dob,
                "student_id": student_id
            }
            st.session_state.answers = []
            st.session_state.score = 0
            st.session_state.question_index = 0
            st.session_state.result_saved = False
            st.session_state.page = "survey"
            st.rerun()

# -----------------------------
# Survey page
# -----------------------------
elif st.session_state.page == "survey":
    if not st.session_state.user_data:
        st.warning("Please enter your information first.")
        st.session_state.page = "home"
        st.rerun()

    index = st.session_state.question_index

    if index < len(questions):
        question = questions[index]

        st.title("Desk Organization Survey")
        st.progress((index) / len(questions))
        st.subheader(f"Question {index + 1} of {len(questions)}")
        st.write(question)

        options = {
            "0. Always": 0,
            "1. Often": 1,
            "2. Sometimes": 2,
            "3. Rarely": 3,
            "4. Never": 4
        }

        selected_text = st.radio("Select one option:", list(options.keys()), key=f"q_{index}")

        if st.button("Next"):
            answer = options[selected_text]
            question_score = calculate_question_score(question, answer, questions)

            st.session_state.answers.append({
                "question_number": index + 1,
                "question": question,
                "selected_answer": answer,
                "selected_label": selected_text,
                "question_score": question_score
            })

            st.session_state.score += question_score
            st.session_state.question_index += 1

            if st.session_state.question_index >= len(questions):
                st.session_state.page = "result"

            st.rerun()
    else:
        st.session_state.page = "result"
        st.rerun()

# -----------------------------
# Result page
# -----------------------------
elif st.session_state.page == "result":
    if not st.session_state.user_data:
        st.warning("No completed survey found.")
        st.session_state.page = "home"
        st.rerun()

    score = st.session_state.score
    percentage, level, interpretation, suggestions = get_result_details(score, max_score)

    st.title("Survey Result")
    st.write(f"**Name:** {st.session_state.user_data['name']}")
    st.write(f"**Date of Birth:** {st.session_state.user_data['dob']}")
    st.write(f"**Student ID:** {st.session_state.user_data['student_id']}")
    st.write(f"**Score:** {score}/{max_score}")
    st.write(f"**Percentage:** {percentage:.2f}%")
    st.write(f"**Result Level:** {level}")

    st.info(interpretation)

    st.subheader("Suggestions")
    for item in suggestions:
        st.write(f"- {item}")

    if not st.session_state.result_saved:
        result_data = {
            "name": st.session_state.user_data["name"],
            "dob": st.session_state.user_data["dob"],
            "student_id": st.session_state.user_data["student_id"],
            "total_score": score,
            "max_score": max_score,
            "score_percentage": round(percentage, 2),
            "result_level": level,
            "answers": st.session_state.answers
        }
        save_result(result_data)
        st.session_state.result_saved = True

    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Previous Results"):
            st.session_state.page = "previous_results"
            st.rerun()
    with col2:
        if st.button("Restart"):
            reset_survey()
            st.rerun()

# -----------------------------
# Previous results page
# -----------------------------
elif st.session_state.page == "previous_results":
    st.title("Previous Survey Results")
    results = load_previous_results()

    if not results:
        st.info("No saved results found yet.")
    else:
        for i, result in enumerate(reversed(results), start=1):
            with st.expander(f"Result {i}: {result['name']} - {result['result_level']}"):
                st.write(f"**Student ID:** {result['student_id']}")
                st.write(f"**Score:** {result['total_score']}/{result['max_score']}")
                st.write(f"**Percentage:** {result['score_percentage']}%")
                st.write(f"**Level:** {result['result_level']}")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()
