from typing import Any, Dict, List, Optional, Callable, Type, Union
import time
import traceback
from dataclasses import dataclass
import importlib.util
import os
from pathlib import Path
from questions_py.types import (
    Category,
    Input,
    LeetcodeLevel,
    Metadata,
    Output,
    UnitTest,
)
import signal
from contextlib import contextmanager
import threading


@dataclass
class TestResult:
    passed: bool
    execution_time: float
    message: str
    expected_output: Any = None
    actual_output: Any = None


class TimeoutException(Exception):
    pass


@contextmanager
def timeout(seconds):
    """Context manager for timing out function execution"""

    def signal_handler(signum, frame):
        raise TimeoutException("Test execution timed out")

    # Start timer only if on Unix-based system (Windows doesn't support SIGALRM)
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)

    try:
        yield
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)


class SolutionTester:
    def __init__(self, solution_func: Callable[..., Any], unit_tests: List[UnitTest]):
        """Initialize the solution tester with a solution function and unit tests."""
        self.solution_func = solution_func
        self.unit_tests = unit_tests
        self.results: List[TestResult] = []

    @classmethod
    def from_challenge_file(cls, challenge_path: Union[str, Path]) -> "SolutionTester":
        """Create a SolutionTester instance from a challenge file path."""
        challenge_path = Path(challenge_path)
        if not challenge_path.exists():
            raise FileNotFoundError(f"Challenge file not found: {challenge_path}")

        # Import the module dynamically
        spec = importlib.util.spec_from_file_location(
            challenge_path.stem, challenge_path
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module: {challenge_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get solution function and metadata
        if not hasattr(module, "solution"):
            raise AttributeError(f"No solution function found in {challenge_path}")
        if not hasattr(module, "metadata"):
            raise AttributeError(f"No metadata found in {challenge_path}")

        return cls(solution_func=module.solution, unit_tests=module.metadata.unit_tests)

    def run_all_tests(self) -> List[TestResult]:
        """Run all unit tests and return the results."""
        self.results = []
        for i, test_case in enumerate(self.unit_tests, 1):
            result = self.run_single_test(test_case, test_number=i)
            self.results.append(result)
        return self.results

    def run_single_test(self, test_case: UnitTest, test_number: int) -> TestResult:
        """Run a single test case and return the result."""
        start_time = time.time()
        try:
            input_dict = test_case.input
            expected_output = test_case.output

            # Run solution with timeout
            try:
                with timeout(5):  # 5 second timeout per test
                    actual_output = self.solution_func(**input_dict)
            except TimeoutException:
                return TestResult(
                    passed=False,
                    execution_time=time.time() - start_time,
                    message=f"Test case {test_number} timed out after 5 seconds",
                    expected_output=expected_output,
                    actual_output=None,
                )

            execution_time = time.time() - start_time

            message = (
                f"Test case {test_number}:\n"
                f"Inputs:\n"
                + "\n".join(f"  {k} = {v}" for k, v in input_dict.items())
                + f"\nExpected output: {expected_output}\n"
                f"Actual output: {actual_output}"
            )

            if actual_output == expected_output:
                return TestResult(
                    passed=True,
                    execution_time=execution_time,
                    message=message,
                    expected_output=expected_output,
                    actual_output=actual_output,
                )
            else:
                return TestResult(
                    passed=False,
                    execution_time=execution_time,
                    message=message,
                    expected_output=expected_output,
                    actual_output=actual_output,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            message = (
                f"Test case {test_number} failed with error:\n"
                f"Inputs:\n"
                + "\n".join(f"  {k} = {v}" for k, v in input_dict.items())
                + f"\n\nError: {str(e)}\n{traceback.format_exc()}"
            )
            return TestResult(
                passed=False,
                execution_time=execution_time,
                message=message,
            )

    def print_results(self) -> None:
        """Print the results of all test cases."""
        print("\nTest Results:")
        print("=" * 50)

        for i, result in enumerate(self.results, 1):
            print(f"\nTest Case {i}:")
            print(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
            print(f"Execution Time: {result.execution_time:.4f} seconds")
            print("Details:")
            print(f"  {result.message}")

        total_passed = sum(1 for r in self.results if r.passed)
        print("\nSummary:")
        print(f"Total Tests: {len(self.results)}")
        print(f"Passed: {total_passed}")
        print(f"Failed: {len(self.results) - total_passed}")
        print("=" * 50)
