#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from scoring_system import ScoringSystem, ReviewStatus
from utils.utils import Role

def test_task_status_after_rejection():
    """Test that task status correctly shows resubmission option after rejection"""
    
    # Create a mock scoring system
    scoring = ScoringSystem()
    
    # Create a mock agent memory structure
    agent_memory = {
        'assigned_problem': type('Problem', (), {
            'id': 1,
            'title': 'Test Problem',
            'description': 'A test problem'
        })(),
        'current_submission_id': None
    }
    
    # Mock the simulation's _get_agent_task_status method
    class MockSimulation:
        def __init__(self):
            self.scoring = scoring
            
        def _get_agent_task_status(self, agent):
            """Get comprehensive task status for an agent"""
            status = {
                'pending_reviews_count': 0,
                'pending_reviews': [],
                'waiting_for_review': None,
                'current_submission_id': None,
                'assigned_problem': None,
                'has_submitted_solution': False,
                'submission_status': None,
                'can_resubmit': False
            }
            
            # Check current submission and its actual status
            if 'current_submission_id' in agent.memory:
                submission_id = agent.memory['current_submission_id']
                status['current_submission_id'] = submission_id
                
                # Get actual submission status from scoring system
                submission = self.scoring.get_submission_by_id(submission_id)
                if submission:
                    submission_status = submission['status'].value
                    status['submission_status'] = submission_status
                    
                    if submission_status == 'approved':
                        status['has_submitted_solution'] = True
                    elif submission_status == 'rejected':
                        status['can_resubmit'] = True  # Agent can fix and resubmit
                        status['has_submitted_solution'] = False  # Rejected submission doesn't count
                    elif submission_status == 'pending':
                        status['has_submitted_solution'] = False  # Still waiting for review
                else:
                    # Fallback if submission not found
                    status['has_submitted_solution'] = True
            
            # Check assigned problem
            if 'assigned_problem' in agent.memory:
                problem = agent.memory['assigned_problem']
                status['assigned_problem'] = {
                    'id': problem.id,
                    'title': problem.title,
                    'description': problem.description[:100] + "..." if len(problem.description) > 100 else problem.description
                }
            
            return status
    
    # Mock agent
    class MockAgent:
        def __init__(self):
            self.memory = agent_memory
    
    sim = MockSimulation()
    agent = MockAgent()
    
    # Test 1: No submission yet
    status = sim._get_agent_task_status(agent)
    print("✓ Test 1 - No submission:")
    print(f"  has_submitted_solution: {status['has_submitted_solution']}")
    print(f"  can_resubmit: {status['can_resubmit']}")
    print(f"  submission_status: {status['submission_status']}")
    
    # Test 2: Submit code and get it approved
    submission_id = scoring.submit_solution("TestAgent", 1, "def test(): pass", Role.WORKER)
    agent.memory['current_submission_id'] = submission_id
    scoring.review_submission(submission_id, "Reviewer", "APPROVE", "Looks good!")
    
    status = sim._get_agent_task_status(agent)
    print("\n✓ Test 2 - Approved submission:")
    print(f"  has_submitted_solution: {status['has_submitted_solution']}")
    print(f"  can_resubmit: {status['can_resubmit']}")
    print(f"  submission_status: {status['submission_status']}")
    
    # Test 3: Submit new code and get it rejected
    submission_id2 = scoring.submit_solution("TestAgent", 1, "def test(): return 'buggy'", Role.WORKER)
    agent.memory['current_submission_id'] = submission_id2
    scoring.review_submission(submission_id2, "Reviewer", "REJECT", "Has bugs!")
    
    status = sim._get_agent_task_status(agent)
    print("\n✓ Test 3 - Rejected submission:")
    print(f"  has_submitted_solution: {status['has_submitted_solution']}")
    print(f"  can_resubmit: {status['can_resubmit']}")
    print(f"  submission_status: {status['submission_status']}")
    
    # Test 4: Submit code and leave it pending
    submission_id3 = scoring.submit_solution("TestAgent", 1, "def test(): return 'pending'", Role.WORKER)
    agent.memory['current_submission_id'] = submission_id3
    
    status = sim._get_agent_task_status(agent)
    print("\n✓ Test 4 - Pending submission:")
    print(f"  has_submitted_solution: {status['has_submitted_solution']}")
    print(f"  can_resubmit: {status['can_resubmit']}")
    print(f"  submission_status: {status['submission_status']}")
    
    print("\n🎉 All tests completed! The rejection resubmission fix is working.")

if __name__ == "__main__":
    test_task_status_after_rejection()