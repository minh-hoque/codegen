from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Union


class Category(Enum):
    ARRAY = "Array"
    STRING = "String"
    HASH_TABLE = "Hash Table"
    DYNAMIC_PROGRAMMING = "Dynamic Programming"
    MATH = "Math"
    SORTING = "Sorting"
    GREEDY = "Greedy"
    DFS = "Depth First Search"
    DATABASE = "Database"
    BINARY_SEARCH = "Binary Search"
    MATRIX = "Matrix"
    TREE = "Tree"
    BFS = "Breadth First Search"
    BACKTRACKING = "Backtracking"
    SLIDING_WINDOW = "Sliding Window"
    HEAP = "Heap Priority Queue"
    STACK = "Stack"
    GRAPH = "Graph"
    GEOMETRY = "Geometry"


class LeetcodeLevel(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


@dataclass
class Input:
    name: str
    description: str
    constraints: str


@dataclass
class Output:
    name: str
    description: str


@dataclass
class UnitTest:
    input: Dict[str, Any]  # Access with test_case.input
    output: Any  # Access with test_case.output


@dataclass
class Metadata:
    statement: str
    approx_leetcode_level: LeetcodeLevel
    categories: List[Category]
    inputs: List[Input]
    output: Output
    unit_tests: List[UnitTest]
    approx_time_spent_min: int
