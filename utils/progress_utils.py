import streamlit as st
from utils.state_utils import get_current_status


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

    # Map status to step index
    status_to_step = {
        "started": 0,  # Generate
        "solving": 1,  # Solve
        "formatting": 2,  # Format
        "debugging": 3,  # Debug
        "reviewing": 4,  # Review
        "completed": 5,  # Completed (now using 5 to show full progress)
    }

    current_status = get_current_status()
    current_index = status_to_step.get(current_status, 0)

    # Adjust the current step display to stay within bounds
    display_index = min(current_index, len(steps) - 1)
    current_step = list(steps.keys())[display_index]

    # Show current step
    st.sidebar.markdown("### Current Step")
    st.sidebar.markdown(f"**{current_step}**")

    # Show description of current step
    st.sidebar.markdown("### Step Description")
    st.sidebar.markdown(steps[current_step])

    # Calculate progress (now using current_index directly)
    progress = current_index / 5  # Using 5 as denominator for 100% completion
    st.sidebar.progress(progress)

    # Show completion status if completed
    if current_status == "completed":
        st.sidebar.success("✅ All steps completed!")

    return current_step
