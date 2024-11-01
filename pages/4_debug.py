import streamlit as st
from utils.openai_utils import init_openai
from utils.state_utils import initialize_session_state, get_state_value


def render_debug_page():
    st.title("Debug Solution")

    initialize_session_state()
    client = init_openai()

    formatted_solution = get_state_value("formatted_solution")
    challenge_file = get_state_value("challenge_file")

    if not formatted_solution:
        st.warning("Please format the solution first.")
        if st.button("Go to Format Step"):
            st.switch_page("pages/3_format.py")
        return

    st.markdown("### Debug Solution")
    st.markdown(f"Solution file: `{challenge_file}`")
    st.code(formatted_solution, language="python")

    # Add debug controls
    if st.button("Run Tests"):
        with st.spinner("Running tests..."):
            # TODO: Implement test runner
            st.info("Test runner to be implemented")

    if st.button("Proceed to Review"):
        st.switch_page("pages/5_review.py")


if __name__ == "__main__":
    render_debug_page()
