from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Union


class Category(Enum):
    GRAPH = "Graph"
    DYNAMIC_PROGRAMMING = "Dynamic Programming"
    ARRAY = "Array"
    STRING = "String"
    TREE = "Tree"
    BINARY_SEARCH = "Binary Search"
    GREEDY = "Greedy"
    MATH = "Math"
    DFS = "DFS"
    BFS = "BFS"


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
    input: Dict[str, Any]
    output: Any


@dataclass
class Metadata:
    statement: str
    approx_leetcode_level: LeetcodeLevel
    categories: List[Category]
    inputs: List[Input]
    output: Output
    unit_tests: List[UnitTest]
    approx_time_spent_min: int
