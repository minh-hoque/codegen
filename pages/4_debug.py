import streamlit as st
from utils.openai_utils import init_openai, debug_solution, format_solution
from utils.state_utils import (
    initialize_session_state,
    get_state_value,
    set_state_value,
    save_progress,
)
from utils.progress_utils import sidebar_progress
from utils.solution_tester import SolutionTester
from utils.text_utils import clean_code_block
from pathlib import Path
import os
from utils.prompts import DEBUG_SOLUTION_PROMPT
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils.solution_tester import TestResult


def render_debug_page():
    st.title("Debug Solution")

    initialize_session_state()

    # Show progress in sidebar
    sidebar_progress()

    client = init_openai()

    saved_solution = get_state_value("saved_solution")
    challenge_file = get_state_value("challenge_file")

    if not saved_solution or not challenge_file:
        st.warning("Please format the solution first.")
        if st.button("Go to Format Step"):
            st.switch_page("pages/3_format.py")
        return

    # Load current solution from file and update state
    try:
        challenge_path = Path(challenge_file)
        if challenge_path.exists():
            with open(challenge_path, "r") as f:
                current_solution = f.read()
                # Update state with current file contents
                set_state_value("saved_solution", current_solution)
                saved_solution = current_solution
    except Exception as e:
        st.error(f"Error reading solution file: {str(e)}")
        return

    st.markdown("### Debug Solution")
    st.markdown(f"Solution file: `{challenge_file}`")
    st.code(saved_solution, language="python")

    # Add debug controls
    if st.button("Run Tests"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Initialize the solution tester
            tester = SolutionTester.from_challenge_file(challenge_path)
            total_tests = len(tester.unit_tests)

            results = []
            with ThreadPoolExecutor() as executor:
                futures = []

                # Submit each test to run in parallel
                for i, test_case in enumerate(tester.unit_tests):
                    future = executor.submit(tester.run_single_test, test_case, i + 1)
                    futures.append(future)

                # Update progress as tests complete
                for i, future in enumerate(futures):
                    try:
                        result = future.result(timeout=10)  # 10 second timeout per test
                        results.append(result)
                        progress = (i + 1) / total_tests
                        progress_bar.progress(progress)
                        status_text.text(f"Running test {i + 1}/{total_tests}")
                    except Exception as e:
                        results.append(
                            TestResult(
                                passed=False,
                                execution_time=0,
                                message=f"Test execution failed: {str(e)}",
                            )
                        )

            # Display results
            progress_bar.empty()
            status_text.empty()

            # Rest of the result display code remains the same...

        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Error running tests: {str(e)}")

    # Add AI Debug Assistant button
    if st.button("Get AI Debug Help"):
        with st.spinner("Analyzing solution with AI..."):
            try:

                # Format failed test results if they exist
                failed_tests = ""
                if "results" in locals():
                    failed_tests = "\n".join(
                        [
                            f"Test Case {i+1}:\n"
                            f"Expected: {result.expected_output}\n"
                            f"Got: {result.actual_output}\n"
                            f"Error: {result.message}\n"
                            for i, result in enumerate(results)
                            if not result.passed
                        ]
                    )
                else:
                    failed_tests = (
                        "No test results available yet. Please run tests first."
                    )

                # Get AI debugging suggestions
                debug_response = debug_solution(client, saved_solution, failed_tests)

                # Store debug response in session state
                set_state_value("debug_response", debug_response)
                st.rerun()

            except Exception as e:
                st.error(f"Error getting AI debug help: {str(e)}")

    # Display debug suggestions if they exist
    debug_response = get_state_value("debug_response")
    saved_solution = get_state_value("saved_solution")
    if debug_response:
        if debug_response["status"] == "error":
            st.error(f"Error getting AI debug help: {debug_response['generated_text']}")
        else:
            # Display AI suggestions
            st.subheader("AI Debug Suggestions")
            suggestions = debug_response["generated_text"]
            st.markdown(suggestions)

            # Format the suggestions
            formatted_result = format_solution(
                client,
                (saved_solution or "")
                + "\n\n"
                + (suggestions or ""),  # Handle None values
            )
            if formatted_result["status"] == "success":
                formatted_suggestions = formatted_result["generated_text"]

                # Look for code blocks in the formatted response
                code_blocks = clean_code_block(formatted_suggestions)
            else:
                st.error("Failed to format debug suggestions")
                return

            if code_blocks:
                st.subheader("Suggested Fixed Solution")
                fixed_solution = code_blocks.strip()
                st.code(fixed_solution, language="python")

                # Allow user to apply the fix
                if st.button("Apply Suggested Fix"):
                    try:
                        # Save the fixed solution to the challenge file
                        with open(challenge_path, "w") as f:
                            f.write(fixed_solution)

                        set_state_value("saved_solution", fixed_solution)
                        set_state_value(
                            "debug_response", None
                        )  # Clear the debug response
                        st.success(
                            "Solution updated and saved! You can now run the tests again to verify the fix."
                        )
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving fixed solution: {str(e)}")

    if st.button("Proceed to Review"):
        set_state_value("debug_completed", True)  # Mark debug step as completed
        save_progress()
        st.switch_page("pages/5_review.py")


if __name__ == "__main__":
    render_debug_page()
