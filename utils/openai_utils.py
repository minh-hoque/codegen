from typing import Optional, Dict, Any, List
from openai import OpenAI
from anthropic import Anthropic
import streamlit as st
from utils.prompts import (
    GENERATE_PROMPT,
    GENERATE_V2_PROMPT,
    VALIDATE_TESTS_PROMPT,
    SOLVE_SOLUTION_PROMPT,
    FORMAT_PROMPT,
    DEBUG_SOLUTION_PROMPT,
    REVIEW_SOLUTION_PROMPT,
    REFINE_PROMPT,
    ANALYZE_SIMILARITY_PROMPT,
)


def init_openai() -> Optional[OpenAI]:
    """Initialize OpenAI client if API key is set"""
    return OpenAI()


def query_openai(
    _client: OpenAI,
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.8,
    max_tokens: Optional[int] = None,
    model: str = "gpt-4",
) -> Dict[str, Any]:
    """Generic helper function to query OpenAI models."""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    try:
        response = _client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=None,
        )
        return {
            "generated_text": response.choices[0].message.content,
            "status": "success",
        }
    except Exception as e:
        print(e)
        return {"generated_text": str(e), "status": "error"}


@st.cache_data(ttl=3600)
def query_anthropic(
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.8,
    max_tokens: Optional[int] = None,
    model: str = "claude-3-5-sonnet-20241022",
) -> Dict[str, Any]:
    """Generic helper function to query Anthropic Claude 3.5 Sonnet model."""
    try:
        client = Anthropic()

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = client.messages.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return {
            "generated_text": response.content,
            "status": "success",
        }
    except Exception as e:
        print(e)
        return {"generated_text": str(e), "status": "error"}


@st.cache_data(ttl=3600)
def generate_question(
    _client: Optional[OpenAI], categories: List[str], selected_theme: str
) -> Dict[str, Any]:
    """Generate a coding question using GPT-4"""
    if not _client:
        st.error("Please set your OpenAI API key in the secrets.")
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    categories_str = ", ".join(categories)
    prompt = GENERATE_PROMPT.format(
        selected_category=categories_str, selected_theme=selected_theme
    )
    return query_openai(_client, prompt, temperature=0.8)


@st.cache_data(ttl=3600)
def validate_unit_tests(
    _client: Optional[OpenAI],
    question_text: str,
    model: str = "gpt-4o",
    temperature: float = 0,
) -> Dict[str, Any]:
    """Validate the unit tests using GPT-4"""
    if not _client or not question_text:
        return {"generated_text": "Invalid input", "status": "error"}

    prompt = VALIDATE_TESTS_PROMPT.format(question_text=question_text)
    return query_openai(_client, prompt, model=model, temperature=temperature)


@st.cache_data(ttl=3600)
def solve_problem(_client: Optional[OpenAI], problem_statement: str) -> Dict[str, Any]:
    """Use OpenAI to solve the coding problem"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = SOLVE_SOLUTION_PROMPT.format(problem_statement=problem_statement)
    return query_openai(_client, prompt, model="o1-preview", temperature=1.0)


@st.cache_data(ttl=3600)
def format_solution(
    _client: Optional[OpenAI], solution_response: str
) -> Dict[str, Any]:
    """Format the solution using the FORMAT_PROMPT"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = FORMAT_PROMPT.format(information=solution_response)
    return query_openai(
        _client=_client,
        prompt=prompt,
        model="gpt-4o",
        temperature=0,
    )


@st.cache_data(ttl=3600)
def debug_solution(
    _client: Optional[OpenAI],
    solution: str,
    failed_tests: str,
    model: str = "o1-preview",
    temperature: float = 1,
) -> Dict[str, Any]:
    """Get debugging suggestions for a solution using OpenAI."""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = DEBUG_SOLUTION_PROMPT.format(
        solution=solution, failed_unit_tests=failed_tests
    )

    return query_openai(
        _client=_client, prompt=prompt, model=model, temperature=temperature
    )


@st.cache_data(ttl=3600)
def get_completion(
    _client: Optional[OpenAI],
    prompt: str,
    model: str = "gpt-4o",
    temperature: float = 0,
) -> Dict[str, Any]:
    """Generic completion function for review and other prompts"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    return query_openai(
        _client=_client, prompt=prompt, model=model, temperature=temperature
    )


@st.cache_data(ttl=3600)
def review_solution(
    _client: Optional[OpenAI],
    solution_text: str,
    selected_theme: str,
    model: str = "gpt-4o",
    temperature: float = 0,
) -> Dict[str, Any]:
    """Get AI review of the solution using the REVIEW_SOLUTION_PROMPT"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = REVIEW_SOLUTION_PROMPT.format(
        solution=solution_text, selected_theme=selected_theme
    )
    return query_openai(
        _client=_client, prompt=prompt, model=model, temperature=temperature
    )


@st.cache_data(ttl=3600)
def analyze_problem_similarity(
    _client: Optional[OpenAI],
    original_problem: str,
    found_problems: List[str],
    model: str = "gpt-4o",
    temperature: float = 0,
) -> Dict[str, Any]:
    """
    Analyze similarity between original problem and found LeetCode problems.

    Args:
        _client: OpenAI client instance
        original_problem: The original problem statement
        found_problems: List of found LeetCode problem titles
        model: OpenAI model to use
        temperature: Temperature parameter for generation

    Returns:
        Dict containing generated analysis and status
    """
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = ANALYZE_SIMILARITY_PROMPT.format(
        original_problem=original_problem, found_problems=found_problems
    )

    return query_openai(
        _client=_client, prompt=prompt, model=model, temperature=temperature
    )


@st.cache_data(ttl=3600)
def refine_problem(
    _client: Optional[OpenAI],
    problem_text: str,
    model: str = "gpt-4o",
    temperature: float = 0,
) -> Dict[str, Any]:
    """Refine and improve the quality of the generated problem."""
    if not _client or not problem_text:
        return {"generated_text": "Invalid input", "status": "error"}

    prompt = REFINE_PROMPT.format(problem_text=problem_text)
    return query_openai(_client, prompt, model=model, temperature=temperature)
