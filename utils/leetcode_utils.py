from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from utils.openai_utils import analyze_problem_similarity, init_openai


def find_similar_leetcode_problems(problem_statement: str) -> Dict:
    """
    Search for similar LeetCode problems using Google search and assess similarity using LLM.

    Args:
        problem_statement: The problem statement to compare against

    Returns:
        Dict containing search results and similarity analysis
    """
    # Initialize OpenAI client
    client = init_openai()

    # Search query formation
    search_query = f"leetcode {' '.join(problem_statement.split()[:100])}..."
    print("search_query", search_query)

    # Get top 5 LeetCode results from Google
    leetcode_results = []
    try:
        search_results = search(search_query, num_results=8, lang="en")
        print("search_results", search_results)
        for result in search_results:
            # print("result", result)
            if isinstance(result, str):
                leetcode_results.append(result)
                print("leetcode_results", leetcode_results)
    except Exception as e:
        print(f"Error during Google search: {e}")
        return {"error": str(e)}

    # Extract problem details from LeetCode URLs
    problems_info = []
    for url in leetcode_results:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                title_element = soup.find("title")
                title = title_element.text if title_element else "Unknown Title"
                print("title", title)
                problems_info.append(
                    {"title": title.replace(" - LeetCode", ""), "url": url}
                )
        except Exception as e:
            print(f"Error fetching problem details: {e}")
            continue

    # Use LLM to assess similarity
    if problems_info:
        try:
            similarity_result = analyze_problem_similarity(
                client, problem_statement, [p["title"] for p in problems_info]
            )
            similarity_analysis = similarity_result.get(
                "generated_text", "Error in similarity analysis"
            )
        except Exception as e:
            similarity_analysis = f"Error during similarity analysis: {e}"
    else:
        similarity_analysis = "No similar LeetCode problems found."

    return {
        "similar_problems": problems_info,
        "similarity_analysis": similarity_analysis,
    }
