import streamlit as st
from utils.openai_utils import init_openai
from utils.state_utils import initialize_session_state, get_state_value


def render_review_page():
    st.title("Review Solution")

    initialize_session_state()
    client = init_openai()

    generated_question = get_state_value("generated_question")
    solution = get_state_value("solution")

    if not solution:
        st.warning("Please complete all previous steps first.")
        if st.button("Go to Generate Step"):
            st.switch_page("pages/1_generate.py")
        return

    st.markdown("### Review Final Solution")

    st.markdown("#### Original Question")
    if generated_question:
        st.markdown(generated_question)

    st.markdown("#### Final Solution")
    st.code(solution, language="python")

    # Add export functionality
    if st.download_button(
        label="Export Complete Package",
        data=f"""# Question
{generated_question or ''}

# Solution
{solution or ''}
""",
        file_name="coding_challenge.txt",
        mime="text/plain",
    ):
        st.success("Package exported successfully!")


if __name__ == "__main__":
    render_review_page()
