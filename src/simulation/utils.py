"""Utility functions and classes for simulation"""

from typing import Dict, Any
from utils.utils import Tool
from message_manager import MessageManager


class Channel:
    """Simple channel implementation for agent communication"""
    def __init__(self, message_manager: MessageManager, sender_name: str):
        self.message_manager = message_manager
        self.sender_name = sender_name
    
    def send_private(self, recipient: str, message: str):
        """Send private message"""
        return self.message_manager.send_private_message(self.sender_name, recipient, message)
    
    def send_forum(self, message: str):
        """Send forum message"""
        return self.message_manager.send_forum_message(self.sender_name, message)


class MockTool:
    """Mock tool implementation for testing"""
    def __init__(self, tool_type: str):
        self.tool_type = tool_type
    
    def run(self, *args, **kwargs):
        print(f"Mock {self.tool_type} executed with args: {args}")


class TestRunnerTool:
    """Tool for running tests on code"""
    def __init__(self, test_runner):
        self.test_runner = test_runner
    
    def run(self, agent_name: str, problem_id: int, code: str) -> Dict[str, Any]:
        """Run tests and return results"""
        if not self.test_runner:
            return {
                "success": False,
                "error": "Test runner not available"
            }
        
        # Run the tests
        test_result = self.test_runner.run_tests(problem_id, code)
        
        # Format results
        return {
            "success": True,
            "problem_title": test_result.problem_title,
            "pass_rate": test_result.pass_rate,
            "passed": test_result.passed,
            "failed": test_result.failed,
            "total_tests": test_result.total_tests,
            "test_details": [
                {
                    "input": tc.input,
                    "expected": tc.expected,
                    "actual": tc.actual,
                    "passed": tc.passed,
                    "error": tc.error
                }
                for tc in test_result.test_cases
            ],
            "execution_error": test_result.execution_error
        }


def create_agent_tools(config: dict) -> Dict[Tool, Any]:
    """Create tools for an agent based on configuration"""
    tools = {
        Tool.CODE_REVIEW: MockTool("code_review"),
        Tool.REPORT_SABOTEUR: MockTool("report_saboteur"),
        Tool.SUBMIT_SOLUTION: MockTool("submit_solution")
    }
    
    # Add test runner if enabled
    if config.get('testing', {}).get('enabled', False):
        # Import here to avoid circular imports
        from utils.test_runner import TestRunner
        test_runner = TestRunner()
        tools[Tool.RUN_TESTS] = TestRunnerTool(test_runner)
    else:
        tools[Tool.RUN_TESTS] = MockTool("run_tests")
    
    return tools