import streamlit as st
from utils.openai_utils import init_openai, solve_problem, validate_unit_tests
from utils.state_utils import initialize_session_state, set_state_value, save_progress


def render_solve_page():
    st.title("Solve Coding Question")

    initialize_session_state()
    client = init_openai()

    if "generated_question" not in st.session_state:
        st.warning("Please generate a question first.")
        if st.button("Go to Generate Step"):
            st.switch_page("pages/1_generate.py")
        return

    st.markdown("### Question to Solve")
    st.markdown(st.session_state.generated_question)

    if st.button("Generate Solution"):
        with st.spinner("Generating solution..."):
            result = solve_problem(client, str(st.session_state.generated_question))
            if result and result["status"] == "success":
                st.session_state.solution_text = result["generated_text"]
            else:
                st.error("Failed to generate solution. Please try again.")

    if "solution_text" in st.session_state and st.session_state.solution_text:
        st.markdown("### Generated Solution")
        st.markdown(st.session_state.solution_text)

        edited_solution = st.text_area(
            "Review and Edit Solution",
            value=st.session_state.solution_text,
            height=400,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Validate Unit Tests") and edited_solution:
                with st.spinner("Analyzing unit tests..."):
                    validation_result = validate_unit_tests(
                        client, edited_solution, model="o1-preview", temperature=1
                    )
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
            if st.button("Save and Proceed to Format"):
                st.session_state.solution = edited_solution
                st.switch_page("pages/3_format.py")


if __name__ == "__main__":
    render_solve_page()
