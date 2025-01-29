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
from dotenv import load_dotenv

load_dotenv()


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
        theme = get_state_value("selected_theme")
        print(f"Theme: {theme}")
        response = review_solution(
            _client=client, solution_text=solution_text, selected_theme=theme
        )
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
    st.markdown(
        """
    Review your final solution and explore similar problems. Get an AI quality review of your code
    and find related problems on LeetCode and other platforms to continue learning.
    
    **Steps:**
    1. Review your final solution
    2. Get an AI quality review
    3. Find similar problems
    4. Download your completed challenge
    5. Mark the challenge as complete
    """
    )

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

    with st.expander("View Final Solution", expanded=True):
        st.code(saved_solution, language="python")

    # Create two columns for reviews and similarity searches
    col1, col2 = st.columns(2)

    # Left Column - Quality Reviews
    with col1:
        st.markdown("### Solution Quality Review")
        if st.button("Generate Solution Review"):
            with st.spinner("Analyzing solution quality..."):
                try:
                    theme = get_state_value("selected_theme")
                    print(f"Theme: {theme}")
                    response = review_solution(client, saved_solution, theme)
                    review_result = (
                        response["generated_text"]
                        if response["status"] == "success"
                        else None
                    )
                    if review_result:
                        card(review_result, "review_result_card")
                        save_progress()
                except Exception as e:
                    st.error(f"Error getting solution review: {str(e)}")

    # Right Column - Similarity Searches
    with col2:
        st.markdown("### Similar Problems")

        # Online Search Button
        if st.button("Search Similar Problems Online"):
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
                        print(os.getenv("TAVILY_API_KEY"))
                        tavily_client = TavilyClient(os.getenv("TAVILY_API_KEY"))
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

        # LeetCode Search Button
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

                        if problem_statement:
                            results = find_similar_leetcode_problems(problem_statement)
                            # st.write(results)
                            st.session_state.similar_problems = results[
                                "similar_problems"
                            ]
                            st.session_state.similarity_analysis = results[
                                "similarity_analysis"
                            ]
                        else:
                            st.error(
                                "Could not find problem statement in challenge file"
                            )
                except Exception as e:
                    st.error(f"Error reading challenge file: {str(e)}")

        # Display LeetCode results if they exist
        if st.session_state.get("similar_problems"):
            st.subheader("Similar LeetCode Problems")
            for problem in st.session_state.similar_problems:
                st.markdown(f"- [{problem['title']}]({problem['url']})")

            st.subheader("Similarity Analysis")
            st.write(st.session_state.similarity_analysis)

    # Combined download and complete section at the bottom
    st.markdown("---")
    st.markdown("### Complete and Download Challenge")

    col1, col2 = st.columns(2)
    with col1:
        if challenge_file and os.path.exists(challenge_file):
            with open(challenge_file, "r") as f:
                challenge_content = f.read()

            if st.download_button(
                label="Download and Complete Challenge",
                data=challenge_content,
                file_name=os.path.basename(challenge_file),
                mime="text/x-python",
            ):
                try:
                    # Save the final challenge
                    final_path = save_final_challenge(
                        challenge_content, st.session_state.current_question_id
                    )

                    # Update state
                    set_state_value("status", "completed")
                    set_state_value("review_completed", True)
                    save_progress()

                    st.success(
                        f"Challenge completed! Final version saved to: {final_path}"
                    )
                    st.info(
                        "You can find your completed challenge in the 'final_challenges' folder."
                    )
                except Exception as e:
                    st.error(f"Error completing challenge: {str(e)}")
        else:
            st.warning(
                "Challenge file not found. Please complete previous steps first."
            )


if __name__ == "__main__":
    render_review_page()
