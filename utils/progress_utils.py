import streamlit as st


def sidebar_progress():
    """Create and manage the sidebar progress tracker"""
    st.sidebar.title("Progress")

    steps = {
        "Generate": "Create problem statement and test cases",
        "Solve": "Implement the solution",
        "Format": "Format the code according to standards",
        "Debug": "Test and debug the solution",
        "Review": "Review and finalize",
    }

    # Determine current step based on state
    current_index = 0
    if st.session_state.get("challenge_file"):
        current_index = 4  # Review
    elif st.session_state.get("formatted_solution"):
        current_index = 3  # Debug
    elif st.session_state.get("solution"):
        current_index = 2  # Format
    elif st.session_state.get("generated_question"):
        current_index = 1  # Solve
    elif st.session_state.get("generated_text"):
        current_index = 0  # Generate

    current_step = list(steps.keys())[current_index]

    # Show current step
    st.sidebar.markdown("### Current Step")
    st.sidebar.markdown(f"**{current_step}**")

    # Show description of current step
    st.sidebar.markdown("### Step Description")
    st.sidebar.markdown(steps[current_step])

    # Show progress
    progress = (current_index + 1) / len(steps)
    st.sidebar.progress(progress)

    return current_step
