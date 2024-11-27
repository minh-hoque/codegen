import streamlit as st
from utils.state_utils import (
    initialize_session_state,
    get_current_status,
    clear_session_state,
    resume_question,
)
from config import setup_streamlit
from utils.components import confirm_dialog


def show_history():
    """Display question generation history"""
    if "db" not in st.session_state:
        return

    questions = st.session_state.db.get_all_questions()
    if not questions:
        st.info("No questions generated yet")
        return

    st.markdown("### Previous Questions")

    # Sort questions by last_updated, most recent first
    questions.sort(key=lambda x: x.get("last_updated", ""), reverse=True)

    for q in questions:
        # Create a unique key for each expander
        expander_key = f"expander_{q.get('id', '')}"
        status_emoji = {
            "started": "🆕",
            "reviewing": "📝",
            "solving": "💭",
            "formatting": "🔧",
            "debugging": "🐛",
            "completed": "✅",
        }.get(q.get("status", ""), "❓")

        with st.expander(
            f"{status_emoji} Question from {str(q.get('created_at', ''))[:10]} - {q.get('status', 'unknown')}"
        ):
            st.markdown("**Categories:** " + ", ".join(q.get("categories", [])))
            if q.get("generated_question"):
                st.markdown("**Question:**")
                st.markdown(q["generated_question"])
            if q.get("solution"):
                st.markdown("**Solution:**")
                st.code(q["solution"], language="python")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"**Last Updated:** {str(q.get('last_updated', ''))[:19].replace('T', ' ')}"
                )

            with col2:
                button_key = f"resume_{q.get('id', '')}"
                button_text = (
                    "View" if q.get("status") == "completed" else "Resume Work"
                )

                # Store button click in session state
                button_clicked = st.button(button_text, key=button_key)
                if button_clicked:
                    st.session_state[f"button_clicked_{button_key}"] = True
                    st.session_state[f"pending_question_id"] = q.get(
                        "id"
                    )  # Store just the ID

                # Check if we have a pending confirmation
                if st.session_state.get(f"button_clicked_{button_key}", False):
                    if confirm_dialog(
                        "Are you sure? Any unsaved progress will be lost.",
                        button_key,
                    ):
                        # Get the stored question ID and resume
                        question_id = st.session_state.pop("pending_question_id")
                        # Clear the button click state
                        st.session_state[f"button_clicked_{button_key}"] = False

                        # Use the resume_question helper function
                        if resume_question(question_id):
                            # Get the status and redirect to appropriate page
                            status = get_current_status()
                            status_to_page = {
                                "started": "pages/1_generate.py",
                                "reviewing": "pages/1_generate.py",
                                "solving": "pages/2_solve.py",
                                "formatting": "pages/3_format.py",
                                "debugging": "pages/4_debug.py",
                                "completed": "pages/5_review.py",
                            }
                            if status in status_to_page:
                                st.switch_page(status_to_page[status])


def main():
    # Set up Streamlit configuration
    setup_streamlit()
    initialize_session_state()

    st.title("CodeGen")
    st.image("images/logo.png", width=500)

    # Add tabs for new question and history
    tab1, tab2 = st.tabs(["New Question", "History"])

    with tab1:
        st.markdown(
            """
        ## Welcome to CodeGen.
        
        This tool helps you generate high-quality coding questions using AI.
        
        Follow these steps to create a coding challenge:
        
        1. **Generate Question**: Select categories and let AI create a unique coding problem
        2. **Solve**: Use an AI system to solve the generated question
        3. **Format**: Clean up and structure your code and make it executable
        4. **Debug**: Test unit tests and fix any issues using AI Debug Assistance
        5. **Review**: Validate that the generated problem and solution are correct and make any final adjustments before saving
        
        You can either start a new question or continue working on a previous one from the History tab.
        """
        )

        if st.button("Start New Question", type="primary"):
            clear_session_state()  # Clear any existing state
            st.switch_page("pages/1_generate.py")

    with tab2:
        show_history()


if __name__ == "__main__":
    main()
