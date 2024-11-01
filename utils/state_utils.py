from typing import Optional, Dict, Any
import streamlit as st
from utils.db_utils import JsonDB
import uuid


def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if "generated_text" not in st.session_state:
        st.session_state.generated_text = None
    if "test_validation" not in st.session_state:
        st.session_state.test_validation = None
    if "generated_question" not in st.session_state:
        st.session_state.generated_question = None
    if "generated_question_validation" not in st.session_state:
        st.session_state.generated_question_validation = None
    if "solution_text" not in st.session_state:
        st.session_state.solution_text = None
    if "solution" not in st.session_state:
        st.session_state.solution = None
    if "formatted_text" not in st.session_state:
        st.session_state.formatted_text = None
    if "formatted_solution" not in st.session_state:
        st.session_state.formatted_solution = None
    if "challenge_file" not in st.session_state:
        st.session_state.challenge_file = None
    if "current_question_id" not in st.session_state:
        st.session_state.current_question_id = None
    if "db" not in st.session_state:
        st.session_state.db = JsonDB()


def get_state_value(key: str) -> Optional[Any]:
    """Safely get a value from session state"""
    return st.session_state.get(key)


def set_state_value(key: str, value: Any):
    """Safely set a value in session state"""
    st.session_state[key] = value


def save_progress():
    """Save current progress to database"""
    if not st.session_state.get("current_question_id"):
        # Generate a new question ID if one doesn't exist
        st.session_state.current_question_id = str(uuid.uuid4())

    db = st.session_state.db
    current_state = {
        "id": st.session_state.current_question_id,
        "categories": st.session_state.get("selected_categories", []),
        "generated_text": st.session_state.get("generated_text"),
        "generated_question": st.session_state.get("generated_question"),
        "test_validation": st.session_state.get("test_validation"),
        "solution": st.session_state.get("solution"),
        "formatted_solution": st.session_state.get("formatted_solution"),
        "challenge_file": st.session_state.get("challenge_file"),
        "status": get_current_status(),
    }

    db.save_question(current_state)


def get_current_status() -> str:
    """Determine current progress status"""
    if st.session_state.get("challenge_file"):
        return "completed"
    elif st.session_state.get("formatted_solution"):
        return "debugging"
    elif st.session_state.get("solution"):
        return "formatting"
    elif st.session_state.get("generated_question"):
        return "solving"
    elif st.session_state.get("generated_text"):
        return "reviewing"
    else:
        return "started"


def resume_question(question_id: str) -> bool:
    """Resume work on a previously saved question"""
    if "db" not in st.session_state:
        return False

    question = st.session_state.db.get_question(question_id)
    if not question:
        return False

    # Restore all state from saved question
    for key, value in question.items():
        if key != "id":
            st.session_state[key] = value
    st.session_state.current_question_id = question_id
    return True


def clear_session_state():
    """Clear all question-related state for starting fresh"""
    keys_to_clear = [
        "generated_text",
        "test_validation",
        "generated_question",
        "generated_question_validation",
        "solution_text",
        "solution",
        "formatted_text",
        "formatted_solution",
        "challenge_file",
        "current_question_id",
        "selected_categories",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
