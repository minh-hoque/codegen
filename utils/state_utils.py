from typing import Optional, Dict, Any
import streamlit as st
from utils.db_utils import JsonDB
import uuid
from utils.leetcode_utils import find_similar_leetcode_problems
import os


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
    if "saved_solution" not in st.session_state:
        st.session_state.saved_solution = None
    if "challenge_file" not in st.session_state:
        st.session_state.challenge_file = None
    if "current_question_id" not in st.session_state:
        st.session_state.current_question_id = None
    if "db" not in st.session_state:
        use_mongo = os.getenv("USE_MONGODB", "false").lower() == "true"
        if use_mongo:
            from utils.mongo_utils import MongoDB

            mongo_uri = os.getenv("MONGODB_URI")
            st.session_state.db = MongoDB(mongo_uri)
        else:
            st.session_state.db = JsonDB()
    if "debug_response" not in st.session_state:
        st.session_state.debug_response = None
    if "generate_completed" not in st.session_state:
        st.session_state.generate_completed = False
    if "solve_completed" not in st.session_state:
        st.session_state.solve_completed = False
    if "format_completed" not in st.session_state:
        st.session_state.format_completed = False
    if "debug_completed" not in st.session_state:
        st.session_state.debug_completed = False
    if "review_completed" not in st.session_state:
        st.session_state.review_completed = False
    if "similar_problems" not in st.session_state:
        st.session_state.similar_problems = None
    if "similarity_analysis" not in st.session_state:
        st.session_state.similarity_analysis = None
    if "selected_theme" not in st.session_state:
        st.session_state.selected_theme = None
    if "validate_clicked" not in st.session_state:
        st.session_state.validate_clicked = False


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
        "selected_category": st.session_state.get(
            "selected_category"
        ),  # Changed from selected_categories
        "selected_theme": st.session_state.get(
            "selected_theme"
        ),  # Add theme to saved state
        "generated_text": st.session_state.get("generated_text"),  # generate step
        "generated_question": st.session_state.get(
            "generated_question"
        ),  # generate step
        "test_validation": st.session_state.get("test_validation"),  # generate step
        "solution_text": st.session_state.get("solution_text"),  # solve step
        "solution": st.session_state.get("solution"),  # solve step
        "formatted_text": st.session_state.get("formatted_text"),  # format step
        "saved_solution": st.session_state.get("saved_solution"),  # format step
        "challenge_file": st.session_state.get("challenge_file"),  # format step
        "debug_response": st.session_state.get("debug_response"),  # debug step
        "generate_completed": st.session_state.get("generate_completed", False),
        "solve_completed": st.session_state.get("solve_completed", False),
        "format_completed": st.session_state.get("format_completed", False),
        "debug_completed": st.session_state.get("debug_completed", False),
        "review_completed": st.session_state.get("review_completed", False),
        "similar_problems": st.session_state.get("similar_problems"),
        "similarity_analysis": st.session_state.get("similarity_analysis"),
        "status": get_current_status(),
    }

    db.save_question(current_state)


def get_current_status() -> str:
    """Determine current progress status based on completion flags"""
    if st.session_state.get("review_completed"):
        return "completed"
    elif st.session_state.get("debug_completed"):
        return "reviewing"
    elif st.session_state.get("format_completed"):
        return "debugging"
    elif st.session_state.get("solve_completed"):
        return "formatting"
    elif st.session_state.get("generate_completed"):
        return "solving"
    else:
        return "started"


def resume_question(question_id: str) -> bool:
    """Resume work on a previously saved question"""
    if "db" not in st.session_state:
        return False

    question = st.session_state.db.get_question(question_id)
    if not question:
        return False

    # Clear existing state first
    clear_session_state()

    # Restore all state from saved question
    for key, value in question.items():
        if key != "id":
            st.session_state[key] = value
    st.session_state.current_question_id = question_id

    # Set completion flags based on status
    if question.get("status") == "completed":
        st.session_state.debug_completed = True
        st.session_state.format_completed = True
        st.session_state.solve_completed = True
        st.session_state.review_completed = True

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
        "saved_solution",
        "challenge_file",
        "current_question_id",
        "selected_category",
        "selected_categories",
        "debug_response",
        "generate_completed",
        "solve_completed",
        "format_completed",
        "debug_completed",
        "review_completed",
        "similar_problems",
        "similarity_analysis",
        "validate_clicked",
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
