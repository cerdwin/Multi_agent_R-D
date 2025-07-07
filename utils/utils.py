#
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any

class Role(Enum):
    SABOTEUR = "saboteur"
    WORKER = "worker"
    HONEYPOT = "honeypot"

class Tool(Enum):
    CODE_REVIEW = "code_review"
    REPORT_SABOTEUR = "report_saboteur"
    SUBMIT_SOLUTION = "submit_solution"
    RUN_TESTS = "run_tests"

@dataclass
class TestCase:
    """Individual test case for a problem"""
    input: str
    expected: str
    passed: bool = False
    actual: str = ""
    error: str = ""

@dataclass 
class TestResult:
    """Result of running tests on user code"""
    problem_id: int
    problem_title: str
    function_name: str
    total_tests: int
    passed: int
    failed: int
    pass_rate: float
    test_cases: List[TestCase]
    execution_error: str = ""
    
    def __post_init__(self):
        """Calculate pass rate after initialization"""
        if self.total_tests > 0:
            self.pass_rate = round((self.passed / self.total_tests) * 100.0, 3)
        else:
            self.pass_rate = 0.0

"""
Testing Tool Interface Specification:

The RUN_TESTS tool allows agents to test their code against the full test suite.

Usage by agents:
- Agent calls RUN_TESTS tool with their code
- Tool automatically detects:
  1. Which problem the agent is currently assigned
  2. Function name from the problem signature  
  3. Test cases from problems.yaml
- Tool executes code against all test cases
- Returns TestResult with pass/fail details

Tool Parameters:
- code: str - The function implementation to test
  
Tool Returns:
- TestResult object with:
  - pass_rate: Percentage of tests passed
  - test_cases: List of individual test results
  - execution_error: Any syntax/runtime errors
  
Function Name Detection:
- Extract function name from problem signature
- Example: "def two_sum(nums: List[int], target: int) -> List[int]:" → "two_sum"

Test Case Execution:
- Parse test case inputs from problems.yaml format
- Execute: result = user_function(*parsed_inputs)  
- Compare result with expected output
- Handle execution errors gracefully

Data Sources:
1. Problem definitions: utils/problems.yaml
2. Test cases: Embedded in each problem definition
3. Current agent assignment: From agent.memory['assigned_problem']
"""