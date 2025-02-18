import streamlit as st
import uuid
from utils.openai_utils import (
    init_openai,
    generate_question,
    validate_unit_tests,
    refine_problem,
)
from utils.state_utils import (
    initialize_session_state,
    set_state_value,
    save_progress,
    clear_session_state,
)
from utils.constants import LEETCODE_CATEGORY_MAP
from utils.progress_utils import sidebar_progress
from utils.components import card


def render_generate_page():
    st.title("Generate Coding Question")
    st.markdown(
        """
    Start by selecting 1-3 problem categories to generate a custom coding challenge. 
    Once generated, you can review and edit the question before proceeding to solve it.
    
    **Steps:**
    1. Select problem categories
    2. Generate a question
    3. Review and edit if needed
    4. Validate unit tests
    5. Proceed to solving
    """
    )

    # Initialize session state
    initialize_session_state()

    # Initialize validate_clicked if not present
    if "validate_clicked" not in st.session_state:
        st.session_state.validate_clicked = False

    # Show progress in sidebar
    sidebar_progress()

    # Get OpenAI client
    client = init_openai()

    # Category selection
    categories = st.multiselect(
        "Select Problem Categories (1-3)",
        options=list(LEETCODE_CATEGORY_MAP.keys()),
        max_selections=3,
    )

    # Add theme selection
    themes = [
        "Fantasy",
        "Real-world",
        "Sports",
        "Science Fiction",
        "Historical",
    ]
    selected_theme = st.selectbox(
        "Select Question Theme",
        options=themes,
        help="Choose a theme for your coding problem. This will affect the context and story of the question.",
    )
    set_state_value("selected_theme", selected_theme)

    if st.button("Generate Question") and categories:
        if len(categories) >= 3:
            st.error("Please select between 1-3 categories")
        else:
            # Clear previous session state when generating new question
            clear_session_state()

            with st.spinner("Generating question..."):
                category_values = [
                    LEETCODE_CATEGORY_MAP[category] for category in categories
                ]
                # Pass theme to generate_question
                initial_result = generate_question(
                    client, category_values, selected_theme
                )

                if initial_result and initial_result["status"] == "success":
                    # Show initial result in expander
                    with st.expander("View Initial Generated Question"):
                        st.markdown(initial_result["generated_text"])

                    # Refine the generated problem
                    with st.spinner("Refining question..."):
                        refined_result = refine_problem(
                            client, initial_result["generated_text"]
                        )

                        if refined_result and refined_result["status"] == "success":
                            set_state_value("current_question_id", str(uuid.uuid4()))
                            set_state_value(
                                "generated_text", refined_result["generated_text"]
                            )
                            set_state_value("selected_categories", categories)
                            save_progress()
                        else:
                            st.warning(
                                "Failed to refine question. Using initial version."
                            )
                            result = initial_result  # Fallback to initial version
                            set_state_value("current_question_id", str(uuid.uuid4()))
                            set_state_value("generated_text", result["generated_text"])
                            set_state_value("selected_categories", categories)
                            save_progress()
                else:
                    st.warning("Failed to generate question. Please try again.")

    # Show generated question and controls
    generated_text = st.session_state.get("generated_text")
    if generated_text:
        st.markdown("### Generated Question")
        card(generated_text, "generated_question_card")

        edited_question = st.text_area(
            "Review and Edit Question",
            value=generated_text,
            height=600,
        )

        col1, col2 = st.columns(2)

        with col1:
            # Update the validate_clicked state when button is pressed
            if (
                st.button("Validate Unit Tests", key="validate_button")
                and edited_question
            ):
                st.session_state.validate_clicked = True

            # Check either button press or existing state
            if st.session_state.validate_clicked and edited_question:
                with st.spinner("Analyzing unit tests..."):
                    validation_result = validate_unit_tests(client, edited_question)
                    if validation_result and validation_result["status"] == "success":
                        st.markdown("### Unit Tests Validation")
                        card(validation_result["generated_text"], "validation_card")
                        set_state_value(
                            "test_validation", validation_result["generated_text"]
                        )
                        save_progress()
                    else:
                        st.error("Failed to validate unit tests. Please try again.")

        with col2:
            if st.button("Proceed to Solving"):
                set_state_value("generated_question", edited_question)
                if "test_validation" in st.session_state:
                    set_state_value(
                        "generated_question_validation",
                        st.session_state.test_validation,
                    )
                set_state_value("generate_completed", True)
                save_progress()
                st.switch_page("pages/2_solve.py")


if __name__ == "__main__":
    render_generate_page()
