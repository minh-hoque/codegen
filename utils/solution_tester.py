from typing import Any, Dict, List, Optional, Callable, Type, Union
import time
import traceback
from dataclasses import dataclass
import importlib.util
import os
from pathlib import Path


@dataclass
class TestResult:
    passed: bool
    execution_time: float
    error_message: Optional[str] = None
    expected_output: Any = None
    actual_output: Any = None


class SolutionTester:
    def __init__(
        self, solution_func: Callable[..., Any], unit_tests: List[Dict[str, Any]]
    ):
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

    def run_single_test(
        self, test_case: Dict[str, Any], test_number: int
    ) -> TestResult:
        """Run a single test case and return the result."""
        start_time = time.time()
        try:
            input_dict = test_case["input"]
            expected_output = test_case["output"]

            actual_output = self.solution_func(**input_dict)
            execution_time = time.time() - start_time

            if actual_output == expected_output:
                return TestResult(passed=True, execution_time=execution_time)
            else:
                return TestResult(
                    passed=False,
                    execution_time=execution_time,
                    error_message=f"Test case {test_number}: Output mismatch",
                    expected_output=expected_output,
                    actual_output=actual_output,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            return TestResult(
                passed=False,
                execution_time=execution_time,
                error_message=f"Test case {test_number} failed with error:\n{str(e)}\n{traceback.format_exc()}",
            )

    def print_results(self) -> None:
        """Print the results of all test cases."""
        print("\nTest Results:")
        print("=" * 50)

        for i, result in enumerate(self.results, 1):
            print(f"\nTest Case {i}:")
            print(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED'}")
            print(f"Execution Time: {result.execution_time:.4f} seconds")

            if not result.passed:
                print("Error Details:")
                if result.error_message:
                    print(f"  {result.error_message}")
                if result.expected_output is not None:
                    print(f"  Expected: {result.expected_output}")
                    print(f"  Got: {result.actual_output}")

        total_passed = sum(1 for r in self.results if r.passed)
        print("\nSummary:")
        print(f"Total Tests: {len(self.results)}")
        print(f"Passed: {total_passed}")
        print(f"Failed: {len(self.results) - total_passed}")
        print("=" * 50)
