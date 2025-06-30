import yaml
from typing import Dict, List, Any, Optional
from pathlib import Path

class Problem:
    def __init__(self, problem_id: int, data: Dict[str, Any]):
        self.id = problem_id
        self.title = data['title']
        self.description = data['description']
        self.signature = data['signature']
        self.examples = data['examples']
        self.test_cases = data['test_cases']
        self.solution = data['solution']
    
    def format_for_agent(self, role: str = "worker") -> str:
        """Format problem description for agent prompt"""
        examples_text = "\n".join([
            f"Input: {ex['input']}\nOutput: {ex['output']}\nExplanation: {ex['explanation']}\n"
            for ex in self.examples
        ])
        
        return f"""Problem {self.id}: {self.title}

{self.description}

Function signature: {self.signature}

Examples:
{examples_text}"""

class ProblemsManager:
    def __init__(self, problems_file: str = "utils/problems.yaml"):
        # Handle relative path from src directory
        if not Path(problems_file).is_absolute():
            base_dir = Path(__file__).parent.parent
            self.problems_file = base_dir / problems_file
        else:
            self.problems_file = Path(problems_file)
        self.problems: Dict[int, Problem] = {}
        self.load_problems()
    
    def load_problems(self):
        """Load problems from YAML file"""
        try:
            with open(self.problems_file, 'r') as f:
                data = yaml.safe_load(f)
            
            for problem_id, problem_data in data['problems'].items():
                self.problems[int(problem_id)] = Problem(int(problem_id), problem_data)
                
        except FileNotFoundError:
            print(f"Problems file {self.problems_file} not found")
        except Exception as e:
            print(f"Error loading problems: {e}")
    
    def get_problem(self, problem_id: int) -> Optional[Problem]:
        """Get a specific problem by ID"""
        return self.problems.get(problem_id)
    
    def get_all_problems(self) -> List[Problem]:
        """Get all available problems"""
        return list(self.problems.values())
    
    def get_problem_ids(self) -> List[int]:
        """Get list of all problem IDs"""
        return list(self.problems.keys())
    
    def validate_solution(self, problem_id: int, solution_code: str) -> Dict[str, Any]:
        """Validate a solution against test cases"""
        problem = self.get_problem(problem_id)
        if not problem:
            return {"error": f"Problem {problem_id} not found"}
        
        results = {
            "problem_id": problem_id,
            "passed": 0,
            "total": len(problem.test_cases),
            "test_results": []
        }
        
        # This is a simplified validation - in practice you'd want to execute safely
        for i, test_case in enumerate(problem.test_cases):
            result = {
                "test_id": i,
                "input": test_case['input'],
                "expected": test_case['expected'],
                "status": "pending"  # Would be "passed"/"failed" after execution
            }
            results["test_results"].append(result)
        
        return results
    
    def assign_problems_to_agents(self, agent_names: List[str], assigned_problems: set = None) -> Dict[str, int]:
        """Assign problems to agents (randomly, avoiding duplicates if possible)"""
        import random
        
        assignments = {}
        problem_ids = self.get_problem_ids()
        
        if not problem_ids:
            return assignments
        
        if assigned_problems is None:
            assigned_problems = set()
        
        available_problems = [pid for pid in problem_ids if pid not in assigned_problems]
        
        if not available_problems:
            available_problems = problem_ids.copy()
            assigned_problems.clear()  # Reset for next round
        
        for agent in agent_names:
            if available_problems:
                chosen_problem = random.choice(available_problems)
                assignments[agent] = chosen_problem
                assigned_problems.add(chosen_problem)
                available_problems.remove(chosen_problem)
            else:
                assignments[agent] = random.choice(problem_ids)
        
        return assignments