import streamlit as st
from utils.openai_utils import init_openai
from utils.state_utils import (
    initialize_session_state,
    get_state_value,
    set_state_value,
    save_progress,
)
from utils.progress_utils import sidebar_progress
from utils.solution_tester import SolutionTester
from pathlib import Path
import os


def render_debug_page():
    st.title("Debug Solution")

    initialize_session_state()

    # Show progress in sidebar
    sidebar_progress()

    client = init_openai()

    formatted_solution = get_state_value("formatted_solution")
    challenge_file = get_state_value("challenge_file")

    if not formatted_solution or not challenge_file:
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
            try:
                # Create a temporary file with the formatted solution
                temp_dir = Path("temp")
                temp_dir.mkdir(exist_ok=True)
                temp_file = temp_dir / os.path.basename(str(challenge_file))

                with open(temp_file, "w") as f:
                    f.write(formatted_solution)

                # Initialize and run the solution tester
                tester = SolutionTester.from_challenge_file(temp_file)
                results = tester.run_all_tests()

                # Display results
                st.subheader("Test Results")
                total_passed = sum(1 for r in results if r.passed)

                # Show summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Tests", len(results))
                with col2:
                    st.metric("Passed", total_passed)
                with col3:
                    st.metric("Failed", len(results) - total_passed)

                # Show detailed results
                for i, result in enumerate(results, 1):
                    with st.expander(
                        f"Test Case {i}: {'✅ PASSED' if result.passed else '❌ FAILED'}"
                    ):
                        st.text(f"Execution Time: {result.execution_time:.4f} seconds")
                        if not result.passed:
                            st.error("Error Details:")
                            if result.error_message:
                                st.code(result.error_message)
                            if result.expected_output is not None:
                                st.text(f"Expected: {result.expected_output}")
                                st.text(f"Got: {result.actual_output}")

                # Clean up temporary file
                if temp_file.exists():
                    temp_file.unlink()

                save_progress()  # Save progress after running tests

                # If all tests pass, enable the proceed button
                if total_passed == len(results):
                    st.success("All tests passed! You can proceed to review.")

            except Exception as e:
                st.error(f"Error running tests: {str(e)}")
                # Clean up temporary file in case of error
                if "temp_file" in locals() and temp_file.exists():
                    temp_file.unlink()

    if st.button("Proceed to Review"):
        set_state_value("debug_completed", True)  # Mark debug step as completed
        save_progress()
        st.switch_page("pages/5_review.py")


if __name__ == "__main__":
    render_debug_page()
