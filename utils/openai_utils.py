from typing import Optional, Dict, Any, List
from openai import OpenAI
import streamlit as st
from utils.prompts import (
    GENERATE_PROMPT,
    VALIDATE_TESTS_PROMPT,
    SOLVE_SOLUTION_PROMPT,
    FORMAT_PROMPT,
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
def generate_question(
    _client: Optional[OpenAI], categories: List[str]
) -> Dict[str, Any]:
    """Generate a coding question using GPT-4"""
    if not _client:
        st.error("Please set your OpenAI API key in the secrets.")
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    categories_str = ", ".join(categories)
    prompt = GENERATE_PROMPT.format(selected_category=categories_str)
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
def solve_problem(_client: Optional[OpenAI], draft_solution: str) -> Dict[str, Any]:
    """Use OpenAI to solve the coding problem"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = SOLVE_SOLUTION_PROMPT.format(draft_solution=draft_solution)
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
