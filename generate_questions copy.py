import streamlit as st
from utils.state_utils import (
    initialize_session_state,
    get_current_status,
    clear_session_state,
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
            f"{status_emoji} Question from {q.get('created_at', '')[:10]} - {q.get('status', 'unknown')}"
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
                    f"**Last Updated:** {q.get('last_updated', '')[:19].replace('T', ' ')}"
                )

            with col2:
                # Add button to continue editing if not completed
                if q.get("status") != "completed":
                    button_key = f"resume_{q.get('id', '')}"
                    if st.button("Resume Work", key=button_key):
                        if confirm_dialog(
                            "Are you sure you want to resume this question? Any unsaved progress will be lost.",
                            button_key,
                        ):
                            # Restore all state from saved question
                            for key, value in q.items():
                                if key != "id":
                                    st.session_state[key] = value
                            st.session_state.current_question_id = q.get("id")

                            # Redirect to appropriate page based on status
                            status_to_page = {
                                "started": "pages/1_generate.py",
                                "reviewing": "pages/1_generate.py",
                                "solving": "pages/2_solve.py",
                                "formatting": "pages/3_format.py",
                                "debugging": "pages/4_debug.py",
                            }
                            if q.get("status") in status_to_page:
                                st.switch_page(status_to_page[q.get("status")])
                else:
                    st.markdown("✅ **Completed**")


def main():
    # Set up Streamlit configuration
    setup_streamlit()
    initialize_session_state()

    st.title("Coding Question Generator")

    # Add tabs for new question and history
    tab1, tab2 = st.tabs(["New Question", "History"])

    with tab1:
        st.markdown(
            """
        ## Welcome to the Coding Question Generator
        
        This tool helps you generate high-quality coding questions using AI.
        
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
