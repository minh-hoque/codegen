import streamlit as st
from openai import OpenAI
import json
from typing import Dict, List, Any, Optional
import os
from pathlib import Path
from config import setup_streamlit

# Constants for problem categories
PROBLEM_CATEGORIES = {
    "Array": "Array",
    "String": "String",
    "HashTable": "HashTable",
    "DynamicProgramming": "DynamicProgramming",
    "Math": "Math",
    "Sorting": "Sorting",
    "Greedy": "Greedy",
    "DFS": "DFS",
    "Database": "Database",
    "BinarySearch": "BinarySearch",
    "Matrix": "Matrix",
    "Tree": "Tree",
    "BFS": "BFS",
}

GENERATE_PROMPT = """### Task
Meta is seeking our assistance in developing coding questions in python that can be used to improve LLM’s ability to be helpful in the domain.

### Instructions
Each coding problem should have the following components, specified and submitted:

1. Problem Statement: A natural language explanation of coding problem where:
- The solution is self-contained, fully executable, and testable with independent unit tests
- The solution relies only on Python standard library capabilities
- The problem statement is coding language-agnostic. It should be able to be solved with any programming language.
- The problem statement describes a creative scenario that requires the reader to interpret and map to a coding problem; see example below.
- The required coding task can correspond to problems like those in coding competitions, or can be reflective of more real-world software engineering problems
- The difficulty of the task should correspond roughly to either “Medium” or “Hard” Leetcode questions, and be annotated as such (see below).

2. Metadata
- Input/output spec: Should be stated concisely, as per example below.
- Approximate difficulty level: Either Leetcode “Medium” or “Hard” (approximately), see above.
- Problem Category: The category of the coding problem needs to be {selected_category}

- Approximate time: time taken, in minutes, from creating the question to submitting it (code running, tests, etc.)

3. Golden unit tests: Which would signify that the solution to the problem statement is correct, where:
- The set of unit tests provides good coverage of all edge cases, guaranteeing that the provided solution is correct
- Unit tests must take a reasonable amount of time to execute
- Explain step by step how the unit tests are correct and why the solution is correct

### Requirements
####Problem statement
- The problem statement describes a coding problem that is solvable with a self-contained, fully-executable code artifact.
- The problem statement describes a coding problem with a solution that is checkable by a reasonable number of unit tests.
- The problem statement describes a coding problem in a language agnostic way.
- The problem statement describes a coding problem that corresponds roughly to the difficulty level of a Leetcode Medium or Hard problem based on the algorithms and data structures needed to solve the problem.
	- Note that if reviewing, please confirm that it matches the annotated difficulty level. If not, please mark accordingly. In cases where you believe that it does not match the annotated difficulty level, but it is either “Medium” or “Hard”-level, please flag so the submission can still potentially be reassigned and used in that difficulty category.
- The problem statement describes a scenario (either real-world or more creative) that requires reading comprehension and critical thinking to map to a software specification.
- The problem statement must be correctly formatted and grammatically correct, have no misspellings, be well written, etc.
	- Note: You can copy-paste into Microsoft Word or Google Docs and confirm no flags as a proxy for this.
- The problem statement must not be plagiarized- i.e. it cannot be a literal copy of any existing coding challenge problem statement, or a minimally re-worded or transformed version of one.
	- Note: It is fine if the problem statement leads to a coding challenge with a solution that is similar to existing coding challenge questions- there will naturally be some overlap here.
	- As an author: if in doubt, you can include a reference to a problem that you think is similar and ask the reviewer to confirm that the overlap is not too great.
 - The problem statement should be of the coding category {selected_category}

#### Input/output spec
- Variable names should be generic and concise. Examples: “n” or “n_cities”.
- Variable descriptions should be concise. They should be capitalized and end in a period. Example: “The number of cities.”
- Constraints should be concise, using notation from the problem statement as needed. Example: “1 <= n <= 200000”.
- The output variable name should be generic and concise. The description should describe behavior if the inputs do not admit a valid output.

#### Golden unit tests
- The set of unit tests provides good coverage of all edge cases, guaranteeing that the provided solution is correct.
- Generate as many unit tests as needed to cover all edge cases.
- The unit tests include tests such as “minimum input,” “maximum input,” “null/zero cases,” “special structure cases,” and “time complexity testing cases”.

### Examples
**Problem Statement**:
There is a legendary tale about Dragon Balls on Planet X: if one collects seven Dragon Balls, the Dragon God will show up and help you fulfill your wishes.\n\nOne day, you are surprised to discover that the tale might possibly be true: you found a Dragon Ball radar at a flea market! The radar shows you the locations of the seven Dragon Balls on Planet X. You want to waste no time checking the truth of the old legend about wish-granting for yourself!\n\nThere are $n$ cities in total on the Planet X, numbered from $1$ to $n$. You are currently at city $1$. To travel from one city to another, you can take any of $m$ bidirectional teleport trips, as many times as you like. The $i$-th teleporter costs $t_ i$ coins to use each time, and it can teleport you between cities $a_ i$ and $b_ i$. To collect a Dragon Ball, you simply need to visit the city where it\u2019s located, as indicated on your radar. It is possible that multiple Dragon Balls are at the same city; in this case you pick all of them all up at once if you visit that city.


**Metadata**:
n (int): The number of cities. Constraints: 1 <= n <= 200000
m (int): The number of possible teleport trips. Constraints: 1 <= m <= 200000
trips_costs (list[tuple[int, int, int]]): A list of tuples, where each tuple consists of a_i, b_i, t_i: he two cities connected by the teleport trip and the cost to use the teleporter, respectively. There are m sets of these values. Constraints: 1 <= a_i, b_i <= n, 0 <= t_i <= 10000
c (list[int]): The city IDs of the seven Dragon Balls shown on the radar. Constraints: 1 <= c[i] <= n for each i from 1 to 7. Length 7


**Golden unit tests**:
Sample Input 1:
n = 10
m = 9
trips_costs = [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1), (6, 7, 1), (7, 8, 1), (8, 9, 1), (9, 10, 1)]
c = [1, 2, 3, 4, 5, 6, 7]
Sample Output 1:
min_coins = 6
Explanation: The minimum number of coins needed to collect all seven Dragon Balls shown on the radar is 6.

Sample Input 2:
n = 5
m = 5
trips_costs = [(1, 2, 0), (1, 3, 0), (2, 3, 1), (3, 4, 1), (4, 5, 1)]
c = [1, 2, 1, 2, 3, 4, 4]
Sample Output 2:
min_coins = 1
Explanation: The minimum number of coins needed to collect all seven Dragon Balls shown on the radar is 1.

### Format
The Output format should follow:
**Problem Statement**: A clear description of the python coding problem.
**Metadata**: Section containing all required metadata.
**Golden unit tests**: Section containing the golden unit tests for the python code.

### Output
**Problem Statement**:

**Metadata**:

**Golden unit tests**:
"""

SOLVE_SOLUTION_PROMPT = """Check if the following solution and unit tests are correct to solve the problem statement. The solution should be an approximately time- and space-optimal solution and it should have high-quality comments. The coding problem should be LEETCODE Medium or Hard level. If it is not, make it more complex.
If the problem statement, solution or unit tests are not correct, fix them.

### Instructions
**Correct solution**:
- Should be an approximately time- and space-optimal solution. If there is no single solution that is both time- and space-optimal, use your best judgment.
- The function implementing the correct solution should be in Python and use only standard libraries. (Note: if you feel it would be beneficial to add a common, non-standard library, please notify the organizers.)
- The function implementing the correct solution should be type-annotated (if applicable).

### Requirements
#### Correct solution
- The solution should be correct.
- The solution should be an approximately time- and space-optimal solution, or the best in your judgment.
- The function implementing the correct solution should be in Python and use only standard libraries.
- The function implementing the correct solution should be type-annotated (if applicable). 

### Examples
**Problem Statement**:
There is a legendary tale about Dragon Balls on Planet X: if one collects seven Dragon Balls, the Dragon God will show up and help you fulfill your wishes.\n\nOne day, you are surprised to discover that the tale might possibly be true: you found a Dragon Ball radar at a flea market! The radar shows you the locations of the seven Dragon Balls on Planet X. You want to waste no time checking the truth of the old legend about wish-granting for yourself!\n\nThere are $n$ cities in total on the Planet X, numbered from $1$ to $n$. You are currently at city $1$. To travel from one city to another, you can take any of $m$ bidirectional teleport trips, as many times as you like. The $i$-th teleporter costs $t_ i$ coins to use each time, and it can teleport you between cities $a_ i$ and $b_ i$. To collect a Dragon Ball, you simply need to visit the city where it\u2019s located, as indicated on your radar. It is possible that multiple Dragon Balls are at the same city; in this case you pick all of them all up at once if you visit that city.


**Metadata**:
n (int): The number of cities. Constraints: 1 <= n <= 200000
m (int): The number of possible teleport trips. Constraints: 1 <= m <= 200000
trips_costs (list[tuple[int, int, int]]): A list of tuples, where each tuple consists of a_i, b_i, t_i: he two cities connected by the teleport trip and the cost to use the teleporter, respectively. There are m sets of these values. Constraints: 1 <= a_i, b_i <= n, 0 <= t_i <= 10000
c (list[int]): The city IDs of the seven Dragon Balls shown on the radar. Constraints: 1 <= c[i] <= n for each i from 1 to 7. Length 7


**Correct Solution**:
min_coins (int): The minimum number of coins needed to collect all seven Dragon Balls shown on the radar. If there is no way to complete this task, print -1 instead.
```python
from typing import List, Tuple, Dict
import heapq

def solution(n: int, m: int, trips_costs: List[Tuple[int, int, int]], c: List[int]) -> int:
    if len(c) != 7:
        return -1  # There must be exactly seven Dragon Balls

    INF = float('inf')

    # Build the graph
    graph = [[] for _ in range(n + 1)]
    for a_i, b_i, t_i in trips_costs:
        graph[a_i].append((b_i, t_i))
        graph[b_i].append((a_i, t_i))

    # Build a mapping from cities to the set of Dragon Balls located there
    city_to_balls: Dict[int, int] = {{}}
    for idx, city in enumerate(c):
        if city not in city_to_balls:
            city_to_balls[city] = 0
        city_to_balls[city] |= (1 << idx)

    # Dijkstra to calculate shortest paths from any source
    def dijkstra(source: int) -> List[int]:
        dist = [INF] * (n + 1)
        dist[source] = 0
        hq = [(0, source)]
        while hq:
            d, u = heapq.heappop(hq)
            if dist[u] < d:
                continue
            for v, w in graph[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    heapq.heappush(hq, (dist[v], v))
        return dist

    # Relevant cities: 1 and the unique cities in c
    relevant_cities = list(set([1] + c))
    city_idx_map = {{city: idx for idx, city in enumerate(relevant_cities)}}
    num_cities = len(relevant_cities)

    # Distance matrix between relevant cities
    dist_matrix = [[INF] * num_cities for _ in range(num_cities)]
    for i, city in enumerate(relevant_cities):
        dist = dijkstra(city)
        for j, other_city in enumerate(relevant_cities):
            dist_matrix[i][j] = dist[other_city]

    # DP array: dp[mask][city_idx] = min cost to reach city_idx with Dragon Balls collected as per mask
    size = 1 << 7  # Total possible combinations of Dragon Balls collected (7 balls)
    dp = [[INF] * num_cities for _ in range(size)]

    # Initial state: at city 1 with any Dragon Balls available there
    start_city_idx = city_idx_map[1]
    initial_mask = city_to_balls.get(1, 0)
    dp[initial_mask][start_city_idx] = 0
    hq = [(0, initial_mask, start_city_idx)]  # Min-heap for Dijkstra's algorithm over states

    while hq:
        cost, mask, u_idx = heapq.heappop(hq)
        if dp[mask][u_idx] < cost:
            continue

        # Collect any new Dragon Balls at the current city
        new_mask = mask | city_to_balls.get(relevant_cities[u_idx], 0)

        # Try moving to other relevant cities
        for v_idx in range(num_cities):
            next_cost = cost + dist_matrix[u_idx][v_idx]
            if dp[new_mask][v_idx] > next_cost:
                dp[new_mask][v_idx] = next_cost
                heapq.heappush(hq, (next_cost, new_mask, v_idx))

    # Find the minimum cost to collect all Dragon Balls
    full_mask = (1 << 7) - 1
    result = min(dp[full_mask][u_idx] for u_idx in range(num_cities))

    return result if result < INF else -1
```

**Golden unit tests**:
Sample Input 1:
n = 10
m = 9
trips_costs = [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, 1), (6, 7, 1), (7, 8, 1), (8, 9, 1), (9, 10, 1)]
c = [1, 2, 3, 4, 5, 6, 7]
Sample Output 1:
min_coins = 6

Sample Input 2:
n = 5
m = 5
trips_costs = [(1, 2, 0), (1, 3, 0), (2, 3, 1), (3, 4, 1), (4, 5, 1)]
c = [1, 2, 1, 2, 3, 4, 4]
Sample Output 2:
min_coins = 1

### Output format
Output should follow the following format:
**Problem Statement**:
**Metadata**:
**Correct Solution**:
**Golden unit tests**:

Solution:
{draft_solution}
"""

REVIEW_SOLUTION_PROMPT = """Review the following python coding problem and solution based on the given acceptance criteria:

{solution}

### Acceptance Criteria

#### Problem Statement
- Describes a solvable coding problem with a self-contained, fully-executable code artifact.
- Solution is checkable by a reasonable number of unit tests.
- Problem is described in a language-agnostic way.
- Difficulty level corresponds to Leetcode Medium or Hard.
- Describes a scenario requiring reading comprehension and critical thinking.
- Well-written, correctly formatted, and grammatically correct.
- Not plagiarized from existing coding challenges.

#### Input/Output Spec
- Generic and concise variable names.
- Concise variable descriptions (capitalized, ending with a period).
- Concise constraints using notation from the problem statement.
- Generic and concise output variable name with description of behavior for invalid inputs.

#### Correct Solution
- Solution is correct.
- Solution is approximately time- and space-optimal.
- Implemented in Python using only standard libraries.
- Function is type-annotated (if applicable).

Based on these criteria, provide a detailed review of the solution. Conclude with either ACCEPT or REJECT, along with a clear rationale for your decision.

### Review:
- Result:
- Rationale:
"""

FORMAT_PROMPT = """Your task is to format the provided coding problem information into a standardized Python module structure. Follow the example format below, updating all sections to reflect the given problem. Make sure the function name is `solution()`.

Python Module Format:
from typing import List, Tuple
from questions_py.types import (
    Category,
    Input,
    LeetcodeLevel,
    Metadata,
    Output,
    UnitTest,
)

problem_statement = \"""
[Insert the full problem statement here]
\"""

metadata = Metadata(
    statement=problem_statement,
    approx_leetcode_level=LeetcodeLevel.[MEDIUM/HARD],
    categories=[Category.ARRAY, Category.STRING, Category.HASH_TABLE, Category.DYNAMIC_PROGRAMMING, 
                Category.MATH, Category.SORTING, Category.GREEDY, Category.DFS, Category.DATABASE, 
                Category.BINARY_SEARCH, Category.MATRIX, Category.TREE, Category.BFS, Category.DATACLASS, 
                Category.BACKTRACKING, Category.SLIDING_WINDOW, Category.HEAP, Category.STACK, 
                Category.GRAPH, Category.GEOMETRY],
    inputs=[
        Input(
            name="input_name",
            description="Description of the input.",
            constraints="Input constraints",
        ),
        # Add more inputs as needed
    ],
    output=Output(
        name="output_name",
        description="Description of the output.",
    ),
    unit_tests=[
        UnitTest(
            input=dict(input_name=input_value),
            output=expected_output,
        ),
        # Add more unit tests
    ],
    approx_time_spent_min=estimated_time,
)

def solution(param1: Type1, param2: Type2) -> ReturnType:
    # Solution implementation
    pass

Please format the following problem information into this structure:
{information}
"""

VALIDATE_TESTS_PROMPT = """Please validate the unit tests in the following coding problem. Analyze each test case step by step.

Problem and Tests to Validate:
{question_text}

Please validate the following aspects for each test case:
1. Input Validity: Check if inputs meet the problem constraints
2. Edge Cases: Identify if the test covers important edge cases
3. Expected Output: Verify if the expected output is correct
4. Test Coverage: Assess if the test adds value to the test suite

Provide your analysis in this format for each test case:
Test Case #N:
- Input Analysis: [Analyze if inputs are valid and meet constraints]
- Edge Case Coverage: [Identify what edge cases this test covers, if any]
- Output Verification: [Verify if the expected output is correct. Explain step by step how the unit tests are correct and why the solution is correct]
- Correction: [If the test is incorrect, provide the correct unit test and expected output]
- Value Assessment: [Assess the value this test adds]
- Recommendation: [Suggest improvements or confirm the test is good]

Finally, provide an overall assessment:
1. Test Suite Coverage Score (1-10)
2. Missing Edge Cases (if any)
3. Recommendations for Additional Tests

Your validation:
"""


@st.cache_data(ttl=3600)
def validate_unit_tests(
    _client: Optional[OpenAI], question_text: str
) -> Dict[str, Any]:
    """Validate the unit tests using GPT-4"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = VALIDATE_TESTS_PROMPT.format(question_text=question_text)
    return query_openai(
        client=_client,
        prompt=prompt,
        model="gpt-4",
        temperature=0,
    )


def init_openai() -> Optional[OpenAI]:
    """Initialize OpenAI client if API key is set"""
    return OpenAI()


def query_openai(
    client: OpenAI,
    prompt: str,
    system_message: Optional[str] = None,
    temperature: float = 0.8,
    max_tokens: Optional[int] = None,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Generic helper function to query OpenAI models.

    Args:
        client: OpenAI client instance
        prompt: The input prompt
        system_message: Optional system message to set context
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Optional max tokens limit
        model: The OpenAI model to use

    Returns:
        Dict containing the response and status
    """
    if not client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
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

    # Join categories with commas for the prompt
    categories_str = ", ".join(categories)
    prompt = GENERATE_PROMPT.format(selected_category=categories_str)
    return query_openai(_client, prompt, temperature=0.8)


def sidebar_progress():
    """Create and manage the sidebar progress tracker"""
    st.sidebar.title("Progress")

    steps = {
        "Generate": "Create problem statement and test cases",
        "Solve": "Implement the solution",
        "Format": "Format the code according to standards",
        "Debug": "Test and debug the solution",
        "Review & Finish": "Review and finalize",
    }

    current_step = st.sidebar.radio(
        "Current Step",
        options=list(steps.keys()),
        index=0,
        help="Follow these steps to complete the question generation process",
    )

    # Show description of current step
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Current Step Description")
    st.sidebar.markdown(steps[current_step])

    # Show progress
    progress = (list(steps.keys()).index(current_step) + 1) / len(steps)
    st.sidebar.progress(progress)

    return current_step


# @st.cache_data(ttl=3600)
def solve_problem(_client: Optional[OpenAI], draft_solution: str) -> Dict[str, Any]:
    """Use OpenAI to solve the coding problem"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    # Use named parameter in format
    prompt = SOLVE_SOLUTION_PROMPT.format(draft_solution=draft_solution)
    return query_openai(
        client=_client,
        prompt=prompt,
        model="o1-preview",  # Changed from o1-preview since it's not available
        temperature=1.0,
    )


def get_next_challenge_number() -> str:
    """Get the next available challenge number"""
    challenges_dir = Path("challenges")
    challenges_dir.mkdir(exist_ok=True)

    existing_files = list(challenges_dir.glob("coding_challenge_*.py"))
    if not existing_files:
        return "01"

    numbers = [int(f.stem.split("_")[-1]) for f in existing_files]
    next_num = max(numbers) + 1
    return f"{next_num:02d}"


@st.cache_data(ttl=3600)
def format_solution(
    _client: Optional[OpenAI], solution_response: str
) -> Dict[str, Any]:
    """Format the solution using the FORMAT_PROMPT"""
    if not _client:
        return {"generated_text": "OpenAI client not initialized", "status": "error"}

    prompt = FORMAT_PROMPT.format(information=solution_response)
    return query_openai(
        client=_client,
        prompt=prompt,
        system_message="You are an expert Python programmer.",
        model="gpt-4o",
        temperature=0,
    )


def save_challenge_file(formatted_solution: str) -> str:
    """Save the formatted solution to a new challenge file"""
    challenge_num = get_next_challenge_number()
    filename = f"coding_challenge_{challenge_num}.py"

    challenges_dir = Path("challenges")
    filepath = challenges_dir / filename

    with open(filepath, "w") as f:
        f.write(formatted_solution)

    return str(filepath)


def main():
    # Set up Streamlit configuration
    setup_streamlit()

    st.title("Coding Question Generator")

    # Get current step from sidebar
    current_step = sidebar_progress()

    # Initialize OpenAI client
    client = init_openai()

    if current_step == "Generate":
        st.write("Generate high-quality coding questions with GPT-4")

        # Category multi-select with 1-3 categories limit
        categories = st.multiselect(
            "Select Problem Categories (1-3)",
            options=list(PROBLEM_CATEGORIES.values()),
            max_selections=3,
        )

        # Store the generated question in session state
        if "generated_text" not in st.session_state:
            st.session_state.generated_text = None

        # Generate Question button
        if (
            st.button("Generate Question", key="generate_question_button")
            and categories
        ):
            if len(categories) > 3:
                st.error("Please select between 1-3 categories")
            else:
                with st.spinner("Generating question..."):
                    result = generate_question(client, categories)
                    if result and result["status"] == "success":
                        st.session_state.generated_text = result["generated_text"]
                    else:
                        st.warning("Failed to generate question. Please try again.")
        elif not categories:
            st.warning("Please select at least one category")

        # Show the generated question and navigation controls separately
        if st.session_state.generated_text:
            st.markdown("### Generated Question")
            st.markdown(st.session_state.generated_text)

            # Add review and edit functionality
            edited_question = st.text_area(
                "Review and Edit Question",
                value=st.session_state.generated_text,
                height=600,
            )

            # Add columns for the buttons
            col1, col2 = st.columns(2)

            with col1:
                # Add validate tests button
                if st.button("Validate Unit Tests"):
                    with st.spinner("Analyzing unit tests..."):
                        validation_result = validate_unit_tests(client, edited_question)
                        if (
                            validation_result
                            and validation_result["status"] == "success"
                        ):
                            st.markdown("### Unit Tests Validation")
                            st.markdown(validation_result["generated_text"])

                            # Store validation result in session state
                            st.session_state.test_validation = validation_result[
                                "generated_text"
                            ]
                        else:
                            st.error("Failed to validate unit tests. Please try again.")

            with col2:
                # Separate proceed button
                if st.button("Proceed to Solving"):
                    st.session_state.generated_question = edited_question
                    # Also save the validation if it exists
                    if "test_validation" in st.session_state:
                        st.session_state.generated_question_validation = (
                            st.session_state.test_validation
                        )
                    st.session_state.current_step = "Solve"
                    st.switch_page("generate_questions.py")

    elif current_step == "Solve":
        # Check if we have a question to solve
        if "generated_question" not in st.session_state:
            st.warning("Please generate a question first.")
            # Add a button to go back to generate step
            if st.button("Go to Generate Step"):
                st.session_state.current_step = "Generate"
                st.switch_page("generate_questions.py")
        else:
            st.markdown("### Question to Solve")
            st.markdown(st.session_state.generated_question)

            # Store the generated solution in session state
            if "solution_text" not in st.session_state:
                st.session_state.solution_text = None

            # Generate Solution button
            if st.button("Generate Solution"):
                with st.spinner("Generating solution..."):
                    result = solve_problem(
                        client, str(st.session_state.generated_question)
                    )
                    if result and result["status"] == "success":
                        st.session_state.solution_text = result["generated_text"]
                    else:
                        st.error("Failed to generate solution. Please try again.")

            # Show the generated solution and save controls separately
            if st.session_state.solution_text:
                st.markdown("### Generated Solution")
                st.markdown(st.session_state.solution_text)

                # Add review and edit functionality for solution
                edited_solution = st.text_area(
                    "Review and Edit Solution",
                    value=st.session_state.solution_text,
                    height=400,
                )

                # Separate save button
                if st.button("Save and Proceed to Format"):
                    st.session_state.solution = edited_solution
                    st.session_state.current_step = "Format"
                    st.success("Solution saved! Proceeding to Format step...")
                    st.switch_page("generate_questions.py")

    elif current_step == "Format":
        if "solution" not in st.session_state:
            st.warning("Please provide a solution in the Solve step first.")
        else:
            st.markdown("### Current Solution")
            st.code(st.session_state.solution, language="python")

            # Store the formatted solution in session state
            if "formatted_text" not in st.session_state:
                st.session_state.formatted_text = None

            # Format Solution button
            if st.button("Format Solution"):
                with st.spinner("Formatting solution..."):
                    result = format_solution(client, st.session_state.solution)
                    if result and result["status"] == "success":
                        st.session_state.formatted_text = result["generated_text"]
                    else:
                        st.error("Failed to format solution. Please try again.")

            # Show the formatted solution and save controls separately
            if st.session_state.formatted_text:
                st.markdown("### Formatted Solution")
                st.code(st.session_state.formatted_text, language="python")

                # Add review and edit functionality
                edited_formatted_solution = st.text_area(
                    "Review and Edit Formatted Solution",
                    value=st.session_state.formatted_text,
                    height=400,
                )

                # Save and proceed buttons in columns
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Save to File"):
                        if edited_formatted_solution:  # Type check
                            try:
                                filepath = save_challenge_file(
                                    edited_formatted_solution
                                )
                                st.session_state.formatted_solution = (
                                    edited_formatted_solution
                                )
                                st.session_state.challenge_file = filepath
                                st.success(f"Solution saved to {filepath}")
                            except Exception as e:
                                st.error(f"Error saving file: {str(e)}")
                        else:
                            st.error("Cannot save empty solution")

                with col2:
                    if st.button("Proceed to Debug"):
                        if "formatted_solution" in st.session_state:
                            st.session_state.current_step = "Debug"
                            st.switch_page("generate_questions.py")
                        else:
                            st.error("Please save the solution before proceeding")

    elif current_step == "Debug":
        if "formatted_solution" not in st.session_state:
            st.warning("Please format the solution first.")
        else:
            st.markdown("### Debug Solution")
            st.markdown(f"Solution file: `{st.session_state.challenge_file}`")
            st.code(st.session_state.formatted_solution, language="python")
            # Debug functionality will be added later

    else:  # Finish
        if "solution" not in st.session_state:
            st.warning("Please complete all previous steps first.")
        else:
            st.markdown("### Review Final Solution")
            st.markdown("#### Original Question")
            st.markdown(st.session_state.generated_question)

            st.markdown("#### Final Solution")
            st.code(st.session_state.solution, language="python")

            # Add final export options
            st.download_button(
                label="Export Complete Package",
                data=f"""# Question
{st.session_state.generated_question}

# Solution
""",
            )


if __name__ == "__main__":
    main()
