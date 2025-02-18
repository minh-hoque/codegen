GENERATE_PROMPT = """### Task
A company is seeking our assistance in developing coding questions in python that can be used to improve LLM’s ability to be helpful in the domain.

### Instructions
Each coding problem should have the following components, specified and submitted:

1. Problem Statement: A natural language explanation of coding problem where:
- The solution is self-contained, fully executable, and testable with independent unit tests
- The solution relies only on Python standard library capabilities
- The problem statement is coding language-agnostic. It should be able to be solved with any programming language.
- The problem statement describes a {selected_theme} scenario that requires the reader to interpret and map to a coding problem; see example below.
- The required coding task can correspond to problems like those in coding competitions, or can be reflective of more real-world software engineering problems
- The difficulty of the task should correspond roughly to either “Medium” or “Hard” Leetcode questions.
- Assure that the problem statement is has all required information to solve the problem for the user.

2. Metadata
- Input/output spec: Should be stated concisely. Specify the input and output variables and their types.
- Constraints: Constraints about the variables should be stated accurately.
- Approximate difficulty level: Either Leetcode “Medium” or “Hard” (approximately), see above.
- Problem Category: The category of the coding problem needs to be {selected_category}
- Approximate time: time taken, in minutes, from creating the question to submitting it (code running, tests, etc.)

3. Golden unit tests: Which would signify that the solution to the problem statement is correct, where:
- The set of unit tests provides good coverage of all edge cases, guaranteeing that the provided solution is correct
- Unit tests must take a reasonable amount of time to execute
- Explain step by step how the unit tests are correct and why the solution is correct

### Requirements
#### Problem statement
- The problem statement describes a coding problem that is solvable with a self-contained, fully-executable code artifact.
- The problem statement describes a coding problem with a solution that is checkable by a reasonable number of unit tests.
- The problem statement describes a coding problem in a language agnostic way.
- The problem statement describes a coding problem that corresponds roughly to the difficulty level of a Leetcode Medium or Hard problem based on the algorithms and data structures needed to solve the problem.
- The problem statement describes a {selected_theme} scenario that requires reading comprehension and critical thinking to map to a software specification.
- The problem statement must be correctly formatted and grammatically correct, have no misspellings, be well written, etc.
- The problem statement must not be plagiarized- i.e. it cannot be a literal copy of any existing coding challenge problem statement, or a minimally re-worded or transformed version of one.
- The problem statement should be of the coding category {selected_category}

#### Metadata
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
Input:
n (int): The number of cities. Constraints: 1 <= n <= 200000
m (int): The number of possible teleport trips. Constraints: 1 <= m <= 200000
trips_costs (list[tuple[int, int, int]]): A list of tuples, where each tuple consists of a_i, b_i, t_i: he two cities connected by the teleport trip and the cost to use the teleporter, respectively. There are m sets of these values. Constraints: 1 <= a_i, b_i <= n, 0 <= t_i <= 10000
c (list[int]): The city IDs of the seven Dragon Balls shown on the radar. Constraints: 1 <= c[i] <= n for each i from 1 to 7. Length 7

Output:
min_coins (int): The minimum number of coins needed to collect all seven Dragon Balls shown on the radar. If there is no way to complete this task, print -1 instead.


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

GENERATE_V2_PROMPT = """### Task
Your task is to help create a Python coding problem to improve LLM performance in solving practical programming tasks. You need to generate high-quality coding problems adhering to the specifications below.

### Instructions
To generate a high-quality coding problem, follow these steps:

1. **Create a Problem Statement**:
   - Write a clear, challenging, natural-language description of a coding problem that needs to be of the category {selected_category}.
   - Ensure the problem is **fully executable**, **testable** with unit tests.
   - Make the problem language-agnostic. It should be solvable in any programming language.
   - Use {selected_theme} scenarios requiring interpretation and mapping to a coding solution.
   - Ensure the problem corresponds to a **Medium** or **Hard** difficulty level (comparable to Leetcode) and requires algorithmic thinking or data structure usage.
   - Include all necessary information to enable the user to solve the problem without assumptions.
   - Make sure the problem statement is not a copy of the examples or of an existing Leetcode coding problem.

2. **Provide Metadata**:
   - Specify input/output types and constraints.
   - Clearly define constraints on variables (e.g., valid ranges, lengths, or types).
   - Indicate the approximate difficulty level: “Medium” or “Hard.”
   - Estimate the time required for solving the problem, including coding and testing.

3. **Write Golden Unit Tests**:
   - Create unit tests covering edge cases such as:
     - Minimum and maximum inputs
     - Special cases (e.g., null/zero scenarios, invalid input handling)
     - Time complexity boundary scenarios
   - Include explanations for how each test validates the correctness of the solution.
   - Ensure unit tests are efficient and provide comprehensive coverage.

4. **Output Format**:
   - **Problem Statement**: Include a well-written description of the coding problem.
   - **Metadata**: List inputs, outputs, constraints, difficulty, and category.
   - **Golden Unit Tests**: Provide sample inputs, expected outputs, and edge-case coverage.

### Requirements
#### Problem Statement
- Must describe a fully executable, and testable coding problem.
- Should not rely on external libraries (use only Python’s standard library).
- DO NOT plagiarize existing Leetcode coding problems.
- Do not copy the provided examples.
- Should include {selected_theme} scenarios requiring logical reasoning and algorithmic problem-solving.
- Clearly formatted, grammatically correct, and free of errors.

#### Metadata
- Input/output variable names must be concise and generic (e.g., `n`, `m`).
- Constraints must use clear mathematical notation (e.g., `1 <= n <= 200000`).
- Output descriptions should address edge cases (e.g., when valid outputs do not exist).
- The problem category needs to be {selected_category}.

#### Golden Unit Tests
- The set of unit tests provides good coverage of all edge cases, guaranteeing that the provided solution is correct.
- Generate as many unit tests as needed to cover all edge cases.
- The unit tests include tests such as “minimum input,” “maximum input,” “null/zero cases,” “special structure cases,” and “time complexity testing cases”.

### Examples
**Problem Statement**:
You are tasked with designing a futuristic city network on Planet Z using teleportation portals. The cities are arranged in a grid with n rows and m columns. Each cell in the grid represents a city, and you can teleport between adjacent cities (horizontally or vertically) if there is an operational portal connecting them. Each portal has a fixed energy cost associated with it. Your mission is to determine the minimum energy cost required to travel from the top-left city (1, 1) to the bottom-right city (n, m). If it is not possible to reach the destination, return -1.


**Metadata**:
Input:
n (int): The number of rows in the grid. Constraints: 1 <= n <= 1000.
m (int): The number of columns in the grid. Constraints: 1 <= m <= 1000.
portals (list[tuple[int, int, int, int, int]]): A list of tuples where each tuple represents a portal. The tuple format is (x1, y1, x2, y2, cost), indicating a portal connecting city (x1, y1) to city (x2, y2) with an energy cost of cost. Constraints: 1 <= x1, x2 <= n, 1 <= y1, y2 <= m, 0 <= cost <= 10^6.

Output:
min_energy (int): The minimum energy required to travel from (1, 1) to (n, m). Return -1 if the destination is unreachable.


**Golden Unit Tests**:
Sample Input 1:
n = 3  
m = 3  
portals = [
    (1, 1, 1, 2, 2),  
    (1, 2, 1, 3, 3),  
    (1, 3, 2, 3, 2),  
    (2, 3, 3, 3, 1)  
]  
Sample Output 1:
min_energy = 8  
Explanation: The optimal path is (1, 1) -> (1, 2) -> (1, 3) -> (2, 3) -> (3, 3) with a total energy cost of 2 + 3 + 2 + 1 = 8.

Sample Input 2:
n = 2  
m = 2  
portals = [
    (1, 1, 1, 2, 5),  
    (1, 2, 2, 2, 5)  
]  
Sample Output 2:
min_energy = -1  
Explanation: It is impossible to reach (2, 2) from (1, 1) because there is no portal connecting (2, 2) to any adjacent city.

Sample Input 3:
n = 1  
m = 1  
portals = []  
Sample Output 3:
min_energy = 0  
Explanation: Starting and ending at the same city requires no energy.

### Output
**Problem Statement**:


**Metadata**:


**Golden Unit Tests**:
"""


REFINE_PROMPT = """Your task is to refine and improve a coding problem to make it clearer and higher quality than typical LeetCode questions. The problem should be unambiguous and engaging for coders.

### Instructions
1. Analyze the given problem statement, metadata, and unit tests
2. Improve the clarity and quality by:
   - Making the problem statement more precise and clear.
   - Making the problem statement require high-level reading comprehension and critical thinking.
   - Adding helpful examples where needed.
   - Making constraints explicit and well-justified under the metadata section.
   - Ensuring unit tests cover all important cases.
3. Maintain the same core problem, difficulty level, and theme
4. Keep the format consistent with the original input problem

### Format
The Output format should follow:
**Problem Statement**: A clear description of the python coding problem.
**Metadata**: Section containing all required metadata.
**Golden unit tests**: Section containing the golden unit tests for the python code.

### Input Problem:
{problem_text}

### Requirements for Refinement
1. Problem Statement:
   - Clear and unambiguous description
   - Well-structured flow of information
   - Explicit requirements and constraints
   - Engaging real-world context where appropriate
   - Better quality than typical LeetCode questions

2. Metadata:
   - Precise input/output specifications
   - Clear and justified constraints
   - Accurate difficulty assessment

3. Unit Tests:
   - Comprehensive coverage of edge cases
   - Clear examples that illustrate the problem
   - Well-explained test cases
   - No duplicate tests
   - No mistakes in the unit tests

### Output
**Problem Statement**:
[Refined problem statement]

**Metadata**:
[Refined metadata]

**Golden unit tests**:
[Refined unit tests]
"""


SOLVE_SOLUTION_PROMPT = """Your task is to create a correct solution to the problem statement that passes all unit tests. The solution should be an approximately time- and space-optimal solution and it should have high-quality comments. The coding problem should be LEETCODE Medium or Hard level. If it is not, make it more complex.

### Instructions
- Read the problem statement carefully and unit tests carefully.
- Create a correct solution to the problem statement.
- The solution should pass all unit tests.
- The solution should be an approximately time- and space-optimal solution. If there is no single solution that is both time- and space-optimal, use your best judgment.
- The function implementing the correct solution should be in Python and use only standard libraries. (Note: if you feel it would be beneficial to add a common, non-standard library, please notify the organizers.)
- The function implementing the correct solution should be type-annotated (if applicable).
- If the problem statement or unit tests are not correct, fix them.

### Requirements
- The solution should be correct.
- The solution should be an approximately time- and space-optimal solution, or the best in your judgment.
- The function implementing the correct solution should be in Python and use only standard libraries.
- The function implementing the correct solution should be type-annotated (if applicable). 

### Examples
**Problem Statement**:
You are tasked with designing a futuristic city network on Planet Z using teleportation portals. The cities are arranged in a grid with n rows and m columns. Each cell in the grid represents a city, and you can teleport between adjacent cities (horizontally or vertically) if there is an operational portal connecting them. Each portal has a fixed energy cost associated with it. Your mission is to determine the minimum energy cost required to travel from the top-left city (1, 1) to the bottom-right city (n, m). If it is not possible to reach the destination, return -1.

**Metadata**:
n (int): The number of rows in the grid. Constraints: 1 <= n <= 1000.
m (int): The number of columns in the grid. Constraints: 1 <= m <= 1000.
portals (list[tuple[int, int, int, int, int]]): A list of tuples where each tuple represents a portal. The tuple format is (x1, y1, x2, y2, cost), indicating a portal connecting city (x1, y1) to city (x2, y2) with an energy cost of cost. Constraints: 1 <= x1, x2 <= n, 1 <= y1, y2 <= m, 0 <= cost <= 10^6.

**Correct Solution**:
```python
from typing import List, Tuple
from collections import defaultdict
import heapq

def solution(n: int, m: int, portals: List[Tuple[int, int, int, int, int]]) -> int:
    # Special case: Start and end city are the same
    # (No movement needed => 0 energy)
    if n == 1 and m == 1:
        return 0

    # Adjacency list: For each city (x, y), store a list of (nx, ny, cost) for all portals
    adjacency = defaultdict(list)
    for (x1, y1, x2, y2, cost) in portals:
        adjacency[(x1, y1)].append((x2, y2, cost))

    # Use Dijkstra's algorithm to find the shortest path from (1, 1) to (n, m)

    # Distances dictionary to keep track of the minimum cost to reach each city
    dist = {{}}
    dist[(1, 1)] = 0

    # Min-heap (priority queue) for retrieving the current city with the smallest distance
    # Each item is a tuple: (current_distance, (x, y))
    heap = [(0, (1, 1))]

    # Process the heap until empty or until we pop (n, m)
    while heap:
        current_dist, (cx, cy) = heapq.heappop(heap)

        # If this distance is outdated, skip
        if current_dist > dist[(cx, cy)]:
            continue

        # If we've reached (n, m), return the distance immediately
        if (cx, cy) == (n, m):
            return current_dist

        # Relaxation step for all neighbors
        for nx, ny, cost in adjacency[(cx, cy)]:
            new_dist = current_dist + cost
            if new_dist < dist.get((nx, ny), float('inf')):
                dist[(nx, ny)] = new_dist
                heapq.heappush(heap, (new_dist, (nx, ny)))

    # If (n, m) was never reached, return -1
    return -1
```

**Golden unit tests**:
Sample Input 1:
n = 3  
m = 3  
portals = [
    (1, 1, 1, 2, 2),  
    (1, 2, 1, 3, 3),  
    (1, 3, 2, 3, 2),  
    (2, 3, 3, 3, 1)  
]  
Sample Output 1:
min_energy = 8  
Explanation: The optimal path is (1, 1) -> (1, 2) -> (1, 3) -> (2, 3) -> (3, 3) with a total energy cost of 2 + 3 + 2 + 1 = 8.

Sample Input 2:
n = 2  
m = 2  
portals = [
    (1, 1, 1, 2, 5),  
    (1, 2, 2, 2, 5)  
]  
Sample Output 2:
min_energy = -1  
Explanation: It is impossible to reach (2, 2) from (1, 1) because there is no portal connecting (2, 2) to any adjacent city.

Sample Input 3:
n = 1  
m = 1  
portals = []  
Sample Output 3:
min_energy = 0  
Explanation: Starting and ending at the same city requires no energy.

### Output format
Output should follow the following format:
**Problem Statement**:
**Metadata**:
**Correct Solution**:
**Golden unit tests**:

### Problem Statement
{problem_statement}

### Output
"""


DEBUG_SOLUTION_PROMPT = """Your task is to correct a python coding solution by debugging the solution and the failed unit tests.

### Instructions
1. Read the problem statement and the solution.
2. Ensure the solution correctly implements the problem statement.
3. Locate the failed unit tests.
4. Solve the unit tests step by step by debugging the solution.
5. Provide a detailed explanation of the debugging process.
6. Provide the corrected solution or the corrected unit tests.

### Format
- The solution should be in Python.
- The solution should formatted exactly the same as the provided solution.

### Solution
{solution}

### Failed Unit Tests
{failed_unit_tests}
"""


REVIEW_SOLUTION_PROMPT = """Review the following python coding problem and solution based on the given acceptance criteria:

{solution}

### Acceptance Criteria

#### Problem Statement
- Describes a solvable coding problem with a self-contained, fully-executable code artifact.
- Solution is checkable by a reasonable number of unit tests.
- Problem is described in a language-agnostic way.
- Difficulty level corresponds to Leetcode Medium or Hard.
- Describes a {selected_theme} scenario requiring reading comprehension and critical thinking.
- Well-written, correctly formatted, and grammatically correct.
- Not plagiarized from existing Leetcode coding challenges.

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

from questions_py.types import Category


# Generate the categories string dynamically from the Category enum
def _generate_categories_str() -> str:
    categories = []
    for category in Category:
        categories.append(f"        Category.{category.name},  # {category.value}")
    return "\n".join(categories)


# Create the base prompt with dynamic categories
FORMAT_PROMPT_TEMPLATE = """Your task is to format the provided coding problem information into a standardized Python module structure. Follow the example format below, updating all sections to reflect the given problem. Make sure the function name is `solution()`.

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
    categories=[Select the correct categories from the list of categories below:
{categories}
    ],
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

Please format the following problem information into the Python module format above and select the correct categories from the list of categories:
{information}
"""

# Create the final prompt with dynamic categories
FORMAT_PROMPT = FORMAT_PROMPT_TEMPLATE.format(
    categories=_generate_categories_str(), information="{information}"
)

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

ANALYZE_SIMILARITY_PROMPT = """Your task is to analyze the similarity between the original problem statement and the found LeetCode problems.
Compare the following problem statement with the found LeetCode problems and assess their similarity:

Original Problem:
{original_problem}

Found LeetCode Problems:
{found_problems}

Please analyze:
1. Is the original problem too similar to the found problems? 
2. Which LeetCode problems are most similar to the original problem?
"""
