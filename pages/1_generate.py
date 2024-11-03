import streamlit as st
import uuid
from utils.openai_utils import init_openai, generate_question, validate_unit_tests
from utils.state_utils import initialize_session_state, set_state_value, save_progress
from utils.constants import LEETCODE_CATEGORY_MAP
from utils.progress_utils import sidebar_progress


def render_generate_page():
    st.title("Generate Coding Question")

    # Initialize session state
    initialize_session_state()

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

    if st.button("Generate Question") and categories:
        if len(categories) > 3:
            st.error("Please select between 1-3 categories")
        else:
            with st.spinner("Generating question..."):
                category_values = [
                    LEETCODE_CATEGORY_MAP[category] for category in categories
                ]
                result = generate_question(client, category_values)
                if result and result["status"] == "success":
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
        st.markdown(generated_text)

        edited_question = st.text_area(
            "Review and Edit Question",
            value=generated_text,
            height=600,
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Validate Unit Tests") and edited_question:
                with st.spinner("Analyzing unit tests..."):
                    validation_result = validate_unit_tests(client, edited_question)
                    if validation_result and validation_result["status"] == "success":
                        st.markdown("### Unit Tests Validation")
                        st.markdown(validation_result["generated_text"])
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
                st.switch_page("pages/2_solve.py")


if __name__ == "__main__":
    render_generate_page()
