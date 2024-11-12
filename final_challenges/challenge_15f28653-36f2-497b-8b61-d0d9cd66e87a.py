from typing import List, Tuple, Dict
from questions_py.types import (
    Category,
    Input,
    LeetcodeLevel,
    Metadata,
    Output,
    UnitTest,
)
from collections import Counter

problem_statement = """
You are responsible for managing a vending machine that dispenses a variety of sodas. Each soda is stored in a dedicated slot, which can hold a specific maximum number of cans. When a soda is sold, the number of cans in its slot decreases by one. If a slot is empty, the machine cannot dispense that soda until it is restocked.

Your task is to determine the remaining number of cans for each soda after a series of sales. You are provided with:

1. A list of tuples, where each tuple contains:
   - A string representing the name of a soda (case-sensitive).
   - An integer representing the maximum number of cans that the slot for this soda can hold.

2. A list of strings representing the sodas that have been sold.

Write a function `soda_inventory` that returns a dictionary. Each key in the dictionary is a soda name, and the corresponding value is the number of cans remaining in the machine for that soda.

**Function Signature**:
```python
def soda_inventory(sodas: List[Tuple[str, int]], sold: List[str]) -> Dict[str, int]:
```

**Input:**
- `sodas`: A list of tuples, each containing:
  - A string `soda_name` (1 <= len(soda_name) <= 100), which is unique across the list.
  - An integer `max_cans` (1 <= max_cans <= 1,000,000), representing the initial number of cans for that soda.
  - Constraints: 1 <= len(sodas) <= 100,000

- `sold`: A list of strings, each representing a soda name that has been sold.
  - Constraints: 0 <= len(sold) <= 1,000,000
  - Each soda name in `sold` is guaranteed to exist in the `sodas` list.

**Output:**
- A dictionary where each key is a soda name from the `sodas` list, and the value is the number of cans remaining after processing all sales.

**Example:**

Example 1:
```python
sodas = [("CocaCola", 50), ("Pepsi", 30), ("Sprite", 20)]
sold = ["CocaCola", "Pepsi", "Sprite", "CocaCola", "Sprite", "CocaCola"]
# Expected output: {"CocaCola": 47, "Pepsi": 29, "Sprite": 18}
```

Example 2:
```python
sodas = [("Fanta", 10), ("DrPepper", 20), ("7UP", 30)]
sold = ["Fanta", "DrPepper", "7UP", "Fanta", "Fanta", "Fanta", "Fanta"]
# Expected output: {"Fanta": 5, "DrPepper": 19, "7UP": 29}
```
"""

metadata = Metadata(
    statement=problem_statement,
    approx_leetcode_level=LeetcodeLevel.MEDIUM,
    categories=[
        Category.HASH_TABLE,  # Hash Table
        Category.ARRAY,  # Array
    ],
    inputs=[
        Input(
            name="sodas",
            description="A list of tuples, each containing a soda name and its maximum number of cans.",
            constraints="1 <= len(sodas) <= 100,000; 1 <= len(soda_name) <= 100; 1 <= max_cans <= 1,000,000",
        ),
        Input(
            name="sold",
            description="A list of soda names that have been sold.",
            constraints="0 <= len(sold) <= 1,000,000",
        ),
    ],
    output=Output(
        name="remaining_cans",
        description="A dictionary mapping each soda name to its remaining number of cans.",
    ),
    unit_tests=[
        UnitTest(
            input=dict(
                sodas=[("CocaCola", 50), ("Pepsi", 30), ("Sprite", 20)],
                sold=["CocaCola", "Pepsi", "Sprite", "CocaCola", "Sprite", "CocaCola"]
            ),
            output={"CocaCola": 47, "Pepsi": 29, "Sprite": 18},
        ),
        UnitTest(
            input=dict(
                sodas=[("Fanta", 10), ("DrPepper", 20), ("7UP", 30)],
                sold=["Fanta", "DrPepper", "7UP", "Fanta", "Fanta", "Fanta", "Fanta"]
            ),
            output={"Fanta": 5, "DrPepper": 19, "7UP": 29},
        ),
        UnitTest(
            input=dict(
                sodas=[("RootBeer", 15), ("MountainDew", 25)],
                sold=[]
            ),
            output={"RootBeer": 15, "MountainDew": 25},
        ),
        UnitTest(
            input=dict(
                sodas=[("Cola", 1000000)],
                sold=["Cola"] * 999999
            ),
            output={"Cola": 1},
        ),
        UnitTest(
            input=dict(
                sodas=[("Lemonade", 5), ("GingerAle", 3)],
                sold=["Lemonade", "Lemonade", "Lemonade", "Lemonade", "Lemonade", "GingerAle", "GingerAle", "GingerAle"]
            ),
            output={"Lemonade": 0, "GingerAle": 0},
        ),
        UnitTest(
            input=dict(
                sodas=[("Lemonade", 5)],
                sold=["Lemonade", "Lemonade", "Lemonade", "Lemonade", "Lemonade", "Lemonade"]
            ),
            output={"Lemonade": 0},
        ),
    ],
    approx_time_spent_min=30,
)

def solution(sodas: List[Tuple[str, int]], sold: List[str]) -> Dict[str, int]:
    """
    Calculates the remaining number of cans for each soda after a series of sales.

    Parameters:
    - sodas: a list of tuples, each containing a soda name and its maximum number of cans.
    - sold: a list of soda names that have been sold.

    Returns:
    - A dictionary mapping each soda name to its remaining number of cans.
    """
    # Initialize the stock with the maximum number of cans for each soda.
    stock: Dict[str, int] = {name: max_cans for name, max_cans in sodas}

    # Count the number of times each soda was sold.
    sold_counts = Counter(sold)

    # For each soda, determine the number of cans actually sold (cannot exceed available stock).
    for name in sold_counts:
        if name in stock:
            # The machine cannot dispense a soda if the slot is empty.
            # So, the number of actual sales is the minimum of available stock and sales attempts.
            actual_sales = min(stock[name], sold_counts[name])
            stock[name] -= actual_sales
            # No need to handle the case where sold_counts[name] > stock[name],
            # as stock will not go below zero.
        else:
            # The soda name in sold is guaranteed to exist in stock as per the problem statement,
            # so this else clause is redundant, but included for clarity.
            pass

    return stock
