import ast
import re
from typing import Dict, Any, List
import yaml
from pathlib import Path
from .utils import TestCase, TestResult

class TestRunner:
    """
    Runs test cases against agent code submissions.
    Extracts function names, parses test inputs, and executes code safely.
    """
    
    def __init__(self, problems_file: str = "utils/problems.yaml"):
        # Load all the problems data once at initialization
        self.problems_data = self._load_problems(problems_file)
    
    def _load_problems(self, problems_file: str) -> Dict[int, Dict[str, Any]]:
        """Load problems from YAML file for test cases"""
        base_dir = Path(__file__).parent.parent
        problems_path = base_dir / problems_file
        
        if not problems_path.exists():
            raise FileNotFoundError(f"Problems file not found: {problems_path}")
        
        with open(problems_path, 'r') as f:
            data = yaml.safe_load(f)
        
        return data.get('problems', {})
    
    def _extract_function_name(self, signature: str) -> str:
        """
        Extract function name from problem signatures like:
        'def two_sum(nums: List[int], target: int) -> List[int]:' -> 'two_sum'
        """
        match = re.search(r'def\s+(\w+)\s*\(', signature)
        if match:
            return match.group(1)
        raise ValueError(f"Could not extract function name from signature: {signature}")
    
    def _parse_test_input(self, input_str: str) -> tuple:
        """
        Convert test input strings to actual Python values.
        Examples:
        - "([2,7,11,15], 9)" -> ([2,7,11,15], 9)
        - '"racecar"' -> ("racecar",)
        - "0" -> (0,)
        """
        try:
            # Use ast.literal_eval for safe evaluation
            if input_str.startswith('(') and input_str.endswith(')'):
                # Already a tuple format like "([2,7], 9)"
                parsed = ast.literal_eval(input_str)
                if isinstance(parsed, tuple):
                    return parsed
                else:
                    # Single value in parentheses like "(5)"
                    return (parsed,)
            else:
                # Single value like "5" or '"hello"'
                parsed = ast.literal_eval(input_str)
                return (parsed,)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Could not parse test input '{input_str}': {e}")
    
    def _parse_expected_output(self, expected_str: str) -> Any:
        """Convert expected output strings to Python values"""
        try:
            return ast.literal_eval(expected_str)
        except (ValueError, SyntaxError) as e:
            raise ValueError(f"Could not parse expected output '{expected_str}': {e}")
    
    def _execute_function(self, code: str, function_name: str, inputs: tuple) -> tuple:
        """
        Execute the user's function with given inputs safely.
        Returns (result, error_message)
        """
        try:
            # Create a local namespace for execution
            local_namespace = {}
            
            # Execute the code to define the function
            exec(code, {}, local_namespace)
            
            # Check if the function exists
            if function_name not in local_namespace:
                return None, f"Function '{function_name}' not found in code"
            
            user_function = local_namespace[function_name]
            
            # Execute the function with inputs
            result = user_function(*inputs)
            return result, None
            
        except Exception as e:
            return None, str(e)
    
    def run_tests(self, problem_id: int, code: str) -> TestResult:
        """
        Run all test cases for a given problem against the user's code.
        This is the main method that agents will call.
        """
        # Get the problem data
        if problem_id not in self.problems_data:
            return TestResult(
                problem_id=problem_id,
                problem_title="Unknown Problem",
                function_name="unknown",
                total_tests=0,
                passed=0,
                failed=0,
                pass_rate=0.0,
                test_cases=[],
                execution_error=f"Problem {problem_id} not found"
            )
        
        problem = self.problems_data[problem_id]
        problem_title = problem.get('title', f'Problem {problem_id}')
        
        try:
            # Extract the function name from the signature
            function_name = self._extract_function_name(problem['signature'])
        except ValueError as e:
            return TestResult(
                problem_id=problem_id,
                problem_title=problem_title,
                function_name="unknown",
                total_tests=0,
                passed=0,
                failed=0,
                pass_rate=0.0,
                test_cases=[],
                execution_error=str(e)
            )
        
        # Process all test cases
        test_cases_data = problem.get('test_cases', [])
        test_cases = []
        passed_count = 0
        
        for test_case_data in test_cases_data:
            input_str = test_case_data['input']
            expected_str = test_case_data['expected']
            
            test_case = TestCase(
                input=input_str,
                expected=expected_str
            )
            
            try:
                # Parse the inputs and expected output
                inputs = self._parse_test_input(input_str)
                expected = self._parse_expected_output(expected_str)
                
                # Execute the function
                actual, error = self._execute_function(code, function_name, inputs)
                
                if error:
                    # Execution error occurred
                    test_case.passed = False
                    test_case.error = error
                    test_case.actual = "Error"
                else:
                    # Compare the result
                    test_case.actual = str(actual)
                    test_case.passed = (actual == expected)
                    if test_case.passed:
                        passed_count += 1
                        
            except Exception as e:
                # Handle parsing errors
                test_case.passed = False
                test_case.error = str(e)
                test_case.actual = "Parse Error"
            
            test_cases.append(test_case)
        
        total_tests = len(test_cases)
        failed_count = total_tests - passed_count
        
        return TestResult(
            problem_id=problem_id,
            problem_title=problem_title,
            function_name=function_name,
            total_tests=total_tests,
            passed=passed_count,
            failed=failed_count,
            pass_rate=0.0,  # This will be calculated in __post_init__
            test_cases=test_cases
        )