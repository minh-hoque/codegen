import streamlit as st
from utils.openai_utils import init_openai, format_solution
from utils.file_utils import save_challenge_file
from utils.state_utils import initialize_session_state


def render_format_page():
    st.title("Format Solution")

    initialize_session_state()
    client = init_openai()

    if "solution" not in st.session_state:
        st.warning("Please provide a solution in the Solve step first.")
        if st.button("Go to Solve Step"):
            st.switch_page("pages/2_solve.py")
        return

    st.markdown("### Current Solution")
    st.code(st.session_state.solution, language="python")

    if st.button("Format Solution"):
        with st.spinner("Formatting solution..."):
            result = format_solution(client, st.session_state.solution)
            if result and result["status"] == "success":
                st.session_state.formatted_text = result["generated_text"]
            else:
                st.error("Failed to format solution. Please try again.")

    if "formatted_text" in st.session_state and st.session_state.formatted_text:
        st.markdown("### Formatted Solution")
        st.code(st.session_state.formatted_text, language="python")

        edited_formatted_solution = st.text_area(
            "Review and Edit Formatted Solution",
            value=st.session_state.formatted_text,
            height=400,
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save to File"):
                if edited_formatted_solution:
                    try:
                        filepath = save_challenge_file(edited_formatted_solution)
                        st.session_state.formatted_solution = edited_formatted_solution
                        st.session_state.challenge_file = filepath
                        st.success(f"Solution saved to {filepath}")
                    except Exception as e:
                        st.error(f"Error saving file: {str(e)}")
                else:
                    st.error("Cannot save empty solution")

        with col2:
            if st.button("Proceed to Debug"):
                if "formatted_solution" in st.session_state:
                    st.switch_page("pages/4_debug.py")
                else:
                    st.error("Please save the solution before proceeding")


if __name__ == "__main__":
    render_format_page()
