from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from utils.openai_utils import analyze_problem_similarity, init_openai
from tavily import TavilyClient
import json
import streamlit as st
from typing import Dict, List, Any
import time

CODING_PLATFORMS = [
    "https://leetcode.com",
    "https://www.hackerrank.com",
    "https://app.codesignal.com",
    "https://www.codewars.com",
    "https://practice.geeksforgeeks.org",
    "https://exercism.io",
    "https://www.interviewcake.com",
    "https://coderbyte.com",
    "https://www.topcoder.com",
    "https://edabit.com",
    "https://projecteuler.net",
    "https://www.kaggle.com",
    "https://a2oj.com",
    "https://codingcompetitions.withgoogle.com",
    "https://www.facebook.com/codingcompetitions/hacker-cup",
    "https://binarysearch.com",
    "https://www.codechef.com",
    "https://www.spoj.com",
    "https://atcoder.jp",
    "https://codeforces.com",
    "https://onlinejudge.org",
    "https://cses.fi",
]


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
    # st.write(search_query)
    # print("search_query", search_query)

    # Get top 12 LeetCode results from Google
    leetcode_results = []
    try:
        search_results = search(search_query, num_results=12, lang="en")
        print("search_results", search_results)
        for result in search_results:
            print("result", result)
            if isinstance(result, str):
                leetcode_results.append(result)
                # print("leetcode_results", leetcode_results)
    except Exception as e:
        print(f"Error during Google search: {e}")
        return {"error": str(e)}

    print("leetcode_results", leetcode_results)
    # Extract problem details from LeetCode URLs
    problems_info = []
    for url in leetcode_results:
        try:
            # Update the headers with more realistic browser information
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0",
            }

            # Add delay between requests to avoid rate limiting
            # time.sleep(2)  # Add a 2-second delay between requests
            response = requests.get(url, headers=headers, timeout=10)
            print("response", response)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                title_element = soup.find("title")
                title = title_element.text if title_element else "Unknown Title"
                print("title", title)
                problems_info.append(
                    {"title": title.replace(" - LeetCode", ""), "url": url}
                )
            else:
                print(f"Error fetching problem details: {response.status_code}")
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


def get_similar_problems_context(
    problem_statement: str, tavily_client: TavilyClient
) -> List[Dict[str, Any]]:
    """
    Search for similar coding problems using Tavily API

    Args:
        problem_statement (str): The problem statement to search for
        tavily_client (TavilyClient): Initialized Tavily client

    Returns:
        List[Dict[str, Any]]: List of search results with content and URLs
    """
    # Truncate problem statement to avoid query length issues (400 token max)
    truncated_query = (
        problem_statement[:397] + "..."
        if len(problem_statement) > 400
        else problem_statement
    )
    print("truncated_query", truncated_query)
    print("len(truncated_query)", len(truncated_query))

    try:
        # Get search context from Tavily
        context = tavily_client.get_search_context(
            query=truncated_query,
            max_tokens=8000,
            max_results=6,
            search_depth="advanced",
            include_domains=CODING_PLATFORMS,
        )

        # Parse the returned context
        search_results = []
        retrieved_context = json.loads(json.loads(context))

        for item in retrieved_context:
            item_data = json.loads(item)
            search_results.append(
                {
                    "content": item_data["content"],
                    "url": item_data["url"],
                    "title": item_data.get("title", "No title"),
                }
            )

        return search_results

    except Exception as e:
        st.error(f"Error searching for similar problems: {str(e)}")
        return []
