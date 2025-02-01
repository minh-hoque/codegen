import streamlit as st
from utils.openai_utils import init_openai, solve_problem, validate_unit_tests
from utils.state_utils import initialize_session_state, set_state_value, save_progress
from utils.progress_utils import sidebar_progress
from utils.components import card


def render_solve_page():
    st.title("Solve Coding Question")
    st.markdown(
        """
    Here you can generate an AI solution for your coding challenge or write your own. 
    Review the generated solution, make any necessary edits, and validate the unit tests before proceeding.
    
    **Steps:**
    1. Review the question
    2. Generate an AI solution or write your own
    3. Edit the solution if needed
    4. Validate unit tests
    5. Save and proceed to formatting
    """
    )

    initialize_session_state()

    # Show progress in sidebar
    sidebar_progress()

    client = init_openai()

    if "generated_question" not in st.session_state:
        st.warning("Please generate a question first.")
        if st.button("Go to Generate Step"):
            st.switch_page("pages/1_generate.py")
        return

    st.markdown("### Question to Solve")
    card(st.session_state.generated_question, "question_card")

    if st.button("Generate Solution"):
        with st.spinner("Generating solution..."):
            result = solve_problem(client, str(st.session_state.generated_question))
            if result and result["status"] == "success":
                set_state_value("solution_text", result["generated_text"])
                set_state_value("validate_clicked", False)
                save_progress()
            else:
                st.error("Failed to generate solution. Please try again.")

    if "solution_text" in st.session_state and st.session_state.solution_text:
        st.markdown("### Generated Solution")
        card(st.session_state.solution_text, "solution_card")

        edited_solution = st.text_area(
            "Review and Edit Solution",
            value=st.session_state.solution_text,
            height=800,
        )

        col1, col2 = st.columns(2)
        with col1:
            # Update the validate_clicked state when button is pressed
            if (
                st.button("Validate Unit Tests", key="validate_button")
                and edited_solution
            ):
                set_state_value("validate_clicked", True)

            # Check either button press or existing state
            if st.session_state.validate_clicked and edited_solution:
                with st.spinner("Analyzing unit tests..."):
                    validation_result = validate_unit_tests(
                        client, edited_solution, model="o3-mini", temperature=1
                    )
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
            if st.button("Save and Proceed to Format"):
                set_state_value("solution", edited_solution)
                set_state_value("solve_completed", True)  # Mark solve step as completed
                set_state_value("validate_clicked", False)
                save_progress()
                st.switch_page("pages/3_format.py")


if __name__ == "__main__":
    render_solve_page()
