import streamlit as st
from utils.openai_utils import init_openai, format_solution
from utils.file_utils import save_challenge_file
from utils.state_utils import initialize_session_state, save_progress, set_state_value
from utils.progress_utils import sidebar_progress
from utils.text_utils import clean_code_block
from utils.components import card


def render_format_page():
    st.title("Format Solution")

    initialize_session_state()

    # Show progress in sidebar
    sidebar_progress()

    client = init_openai()

    if "solution" not in st.session_state:
        st.warning("Please provide a solution in the Solve step first.")
        if st.button("Go to Solve Step"):
            st.switch_page("pages/2_solve.py")
        return

    st.markdown("### Current Solution")
    card(st.session_state.solution, "current_solution_card")

    if st.button("Format Solution"):
        with st.spinner("Formatting solution..."):
            result = format_solution(client, st.session_state.solution)
            if result and result["status"] == "success":
                set_state_value("formatted_text", result["generated_text"])
                save_progress()
            else:
                st.error("Failed to format solution. Please try again.")

    if "formatted_text" in st.session_state and st.session_state.formatted_text:
        st.markdown("### Formatted Solution")
        cleaned_formatted_text = clean_code_block(st.session_state.formatted_text)
        st.code(cleaned_formatted_text)

        # Clean the formatted text before showing in text area
        edited_formatted_solution = st.text_area(
            "Review and Edit Formatted Solution",
            value=cleaned_formatted_text,
            height=400,
        )

        if st.button("Save and Continue to Debug"):
            if edited_formatted_solution:
                try:
                    filepath = save_challenge_file(edited_formatted_solution)
                    set_state_value("saved_solution", edited_formatted_solution)
                    set_state_value("challenge_file", filepath)
                    set_state_value("format_completed", True)
                    save_progress()
                    st.success(f"Solution saved to {filepath}")
                    st.switch_page("pages/4_debug.py")
                except Exception as e:
                    st.error(f"Error saving file: {str(e)}")
            else:
                st.error("Cannot save empty solution")


if __name__ == "__main__":
    render_format_page()
