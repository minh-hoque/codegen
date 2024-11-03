import streamlit as st
from utils.openai_utils import init_openai, review_solution
from utils.state_utils import initialize_session_state, get_state_value, set_state_value
import requests
from bs4 import BeautifulSoup
from utils.constants import LEETCODE_CATEGORY_MAP
from pathlib import Path


def search_leetcode_similarity(question_text, category):
    """
    Search for similar problems on LeetCode with category filter

    Args:
        question_text (str): The question text to search for
        category (str): The category to filter by (e.g., 'ARRAY', 'DYNAMIC_PROGRAMMING')
    """
    try:
        # Map our category to LeetCode's category format
        leetcode_category = LEETCODE_CATEGORY_MAP.get(category, "")
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


def render_review_page():
    st.title("Review Solution")

    initialize_session_state()
    client = init_openai()

    generated_question = get_state_value("generated_question")
    saved_solution = get_state_value("saved_solution")
    challenge_file = get_state_value("challenge_file")
    selected_category = get_state_value("selected_category")

    if not saved_solution or not challenge_file:
        st.warning("Please complete all previous steps first.")
        if st.button("Go to Generate Step"):
            st.switch_page("pages/1_generate.py")
        return

    st.markdown("### Review Final Solution")

    # Original question and solution display
    with st.expander("View Original Question", expanded=True):
        if generated_question:
            st.markdown(generated_question)
            if selected_category:
                st.info(f"Category: {selected_category}")

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
                    st.markdown(review_result)
            except Exception as e:
                st.error(f"Error getting solution review: {str(e)}")

    # Similarity Check Section
    st.markdown("### Similarity Check")
    if st.button("Check for Similar Problems"):
        with st.spinner("Searching for similar problems..."):
            similar_problems = search_leetcode_similarity(
                generated_question, selected_category
            )

            if similar_problems:
                st.markdown(
                    f"#### Potentially Similar LeetCode {selected_category} Problems:"
                )
                for title, link in similar_problems:
                    st.markdown(f"- [{title}]({link})")
            else:
                st.info(f"No similar {selected_category} problems found on LeetCode.")

    # Export functionality
    st.markdown("### Export Solution")
    if st.download_button(
        label="Export Complete Package",
        data=f"""# Question
{generated_question or ''}

# Category
{selected_category or 'Not specified'}

# Solution
{saved_solution or ''}

# Review Notes
This problem was generated and reviewed using an AI-assisted process.
""",
        file_name="coding_challenge.txt",
        mime="text/plain",
    ):
        st.success("Package exported successfully!")


if __name__ == "__main__":
    render_review_page()
