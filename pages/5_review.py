import streamlit as st
from utils.openai_utils import init_openai, review_solution
from utils.state_utils import (
    initialize_session_state,
    get_state_value,
    set_state_value,
    save_progress,
)
import requests
from bs4 import BeautifulSoup
from utils.constants import LEETCODE_CATEGORY_MAP
from pathlib import Path
import os
from utils.progress_utils import sidebar_progress
from utils.leetcode_utils import (
    find_similar_leetcode_problems,
    get_similar_problems_context,
)
from tavily import TavilyClient
from utils.components import card


def search_leetcode_similarity(question_text, category=None):
    """
    Search for similar problems on LeetCode with optional category filter

    Args:
        question_text (str): The question text to search for
        category (str, optional): The category to filter by (e.g., 'ARRAY', 'DYNAMIC_PROGRAMMING')
    """
    try:
        print(f"Searching for similar problems for category: {category}")
        # Map our category to LeetCode's category format if category is provided
        leetcode_category = LEETCODE_CATEGORY_MAP.get(category, "") if category else ""
        if leetcode_category:
            # Include category in search URL
            search_url = (
                f"https://leetcode.com/problemset/all/"
                f"?search={question_text[:100]}"
                f"&topicSlugs={leetcode_category.lower()}"
            )
        else:
            search_url = (
                f"https://leetcode.com/problemset/all/?search={question_text[:100]}"
            )

        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract problem titles and links
        similar_problems = []
        problem_elements = soup.find_all("div", {"class": "title-cell"})

        for element in problem_elements[:5]:  # Get top 5 similar problems
            if element.find("a"):
                title = element.find("a").text.strip()
                link = f"https://leetcode.com{element.find('a')['href']}"
                similar_problems.append((title, link))

        return similar_problems
    except Exception as e:
        st.error(f"Error searching LeetCode: {str(e)}")
        return []


def get_solution_review(solution_text):
    """Get AI review of the solution"""
    client = init_openai()
    try:
        response = review_solution(client, solution_text)
        return response["generated_text"] if response["status"] == "success" else None
    except Exception as e:
        st.error(f"Error getting solution review: {str(e)}")
        return None


def save_final_challenge(challenge_text: str, question_id: str):
    """Save the final challenge to the final_challenges directory"""
    # Create final_challenges directory if it doesn't exist
    final_dir = Path("final_challenges")
    final_dir.mkdir(exist_ok=True)

    # Save the challenge file with the question ID as the filename
    challenge_path = final_dir / f"challenge_{question_id}.py"
    with open(challenge_path, "w") as f:
        f.write(challenge_text)
    return challenge_path


def render_review_page():
    st.title("Review Solution")

    initialize_session_state()

    # Show progress in sidebar
    sidebar_progress()

    client = init_openai()

    generated_question = get_state_value("generated_question")
    saved_solution = get_state_value("saved_solution")
    challenge_file = get_state_value("challenge_file")
    selected_categories = get_state_value("selected_category")

    if not saved_solution or not challenge_file:
        st.warning("Please complete all previous steps first.")
        if st.button("Go to Generate Step"):
            st.switch_page("pages/1_generate.py")
        return

    st.markdown("### Review Final Solution")

    # Original question and solution display
    with st.expander("View Original Question", expanded=True):
        if generated_question:
            card(generated_question, "review_question_card")
            if selected_categories:
                st.info(f"Category: {selected_categories}")

    with st.expander("View Final Solution", expanded=True):
        st.code(saved_solution, language="python")

    # AI Review Section
    st.markdown("### Solution Quality Review")
    if st.button("Generate Solution Review"):
        with st.spinner("Analyzing solution quality..."):
            try:
                response = review_solution(client, saved_solution)
                review_result = (
                    response["generated_text"]
                    if response["status"] == "success"
                    else None
                )
                if review_result:
                    card(review_result, "review_result_card")
                    set_state_value(
                        "review_completed", True
                    )  # Mark review step as completed
                    save_progress()
            except Exception as e:
                st.error(f"Error getting solution review: {str(e)}")

    # Similarity Check Section
    st.markdown("### Similarity Check")
    if st.button("Check for Similar Problems"):
        with st.spinner("Searching for similar problems..."):
            category = selected_categories[0] if selected_categories else None
            similar_problems = search_leetcode_similarity(generated_question, category)

            if similar_problems:
                st.markdown(
                    f"#### Potentially Similar LeetCode {category if category else ''} Problems:"
                )
                for title, link in similar_problems:
                    st.markdown(f"- [{title}]({link})")
            else:
                st.info(
                    f"No similar {''+category if category else ''} problems found on LeetCode."
                )

    # Add Tavily Search Section
    st.markdown("### Search Similar Problems Online")
    if st.button("Search Similar Problems Online"):
        try:
            tavily_api_key = os.getenv("TAVILY_API_KEY")
            if not tavily_api_key:
                st.error("Please set your TAVILY_API_KEY in the environment variables")
                return

            tavily_client = TavilyClient(api_key=tavily_api_key)

            with st.spinner(
                "Searching for similar problems across coding platforms..."
            ):
                # Get the problem statement from the challenge file
                if not challenge_file:
                    st.warning("No challenge file found")
                    return

                try:
                    with open(challenge_file, "r") as f:
                        file_contents = f.read()
                        # Extract problem statement from the challenge file
                        exec_globals = {}
                        exec(file_contents, exec_globals)
                        problem_statement = exec_globals.get("problem_statement")

                        if not problem_statement:
                            st.warning(
                                "Could not find problem statement in challenge file"
                            )
                            return

                        search_results = get_similar_problems_context(
                            problem_statement, tavily_client
                        )

                        if search_results:
                            st.markdown("#### Similar Problems Found:")
                            for idx, result in enumerate(search_results, 1):
                                with st.expander(
                                    f"Result {idx}: {result['url']}", expanded=False
                                ):
                                    st.markdown(
                                        f"**Source:** [{result['url']}]({result['url']})"
                                    )
                                    st.markdown("**Content Preview:**")
                                    st.markdown(
                                        result["content"][:500] + "..."
                                        if len(result["content"]) > 500
                                        else result["content"]
                                    )
                        else:
                            st.info("No similar problems found")

                except Exception as e:
                    st.error(f"Error reading challenge file: {str(e)}")

        except Exception as e:
            st.error(f"Error during search: {str(e)}")

    # Export functionality
    st.markdown("### Export Solution")
    if st.download_button(
        label="Export Complete Package",
        data=f"""# Question
{generated_question or ''}

# Category
{selected_categories or 'Not specified'}

# Solution
{saved_solution or ''}

# Review Notes
This problem was generated and reviewed using an AI-assisted process.
""",
        file_name="coding_challenge.txt",
        mime="text/plain",
    ):
        st.success("Package exported successfully!")
        set_state_value(
            "review_completed", True
        )  # Mark review step as completed when exporting
        save_progress()

    # Add completion button
    st.markdown("### Complete Challenge")
    if st.button("Mark as Complete"):
        if not challenge_file:
            st.error("No challenge file found. Please complete previous steps first.")
            return

        try:
            # Save the final challenge
            final_path = save_final_challenge(
                challenge_file, st.session_state.current_question_id
            )

            # Update state
            set_state_value("status", "completed")
            set_state_value("review_completed", True)
            save_progress()

            st.success(f"Challenge completed! Final version saved to: {final_path}")

            # Show a message about where to find the file
            st.info(
                "You can find your completed challenge in the 'final_challenges' folder."
            )

        except Exception as e:
            st.error(f"Error completing challenge: {str(e)}")

    if st.button("Find Similar LeetCode Problems"):
        with st.spinner("Searching for similar problems..."):
            # Read problem statement from challenge file
            try:
                with open(challenge_file, "r") as f:
                    file_contents = f.read()
                    # Extract problem statement from the challenge file
                    # Assuming the problem statement is stored in a variable named problem_statement
                    problem_statement = None
                    exec_globals = {}
                    exec(file_contents, exec_globals)
                    problem_statement = exec_globals.get("problem_statement")

                    st.write(problem_statement)
                    if problem_statement:
                        results = find_similar_leetcode_problems(problem_statement)
                        st.write(results)
                        st.session_state.similar_problems = results["similar_problems"]
                        st.session_state.similarity_analysis = results[
                            "similarity_analysis"
                        ]
                    else:
                        st.error("Could not find problem statement in challenge file")
            except Exception as e:
                st.error(f"Error reading challenge file: {str(e)}")

    if st.session_state.similar_problems:
        st.subheader("Similar LeetCode Problems")
        for problem in st.session_state.similar_problems:
            st.markdown(f"- [{problem['title']}]({problem['url']})")

        st.subheader("Similarity Analysis")
        st.write(st.session_state.similarity_analysis)


if __name__ == "__main__":
    render_review_page()
