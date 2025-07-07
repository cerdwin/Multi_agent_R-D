"""Manager for code review assignments and flow"""

from typing import List, Optional


class ReviewManager:
    """Manages code review assignments and flow"""
    
    def __init__(self, scoring, message_manager, display):
        self.scoring = scoring
        self.message_manager = message_manager
        self.display = display
    
    def handle_review_request_message(self, requester, recipient_name: str, message: str, agents: List):
        """Check if a message is a review request and handle it"""
        # Check if message is a review request
        if not self._is_review_request(message):
            self.display.console.print("[dim]   Not detected as review request[/dim]")
            return
        
        # Find the most recent submission from requester
        submissions = self.scoring.get_agent_submissions(requester.name)
        if not submissions:
            self.display.console.print(f"[yellow]⚠️ {requester.name} requested review but has no submissions[/yellow]")
            return
        
        # Find the most recent submission without a reviewer
        recent_submission = None
        for submission in reversed(submissions):
            if submission['status'].value == 'pending' and not submission.get('reviewer'):
                recent_submission = submission
                break
        
        if not recent_submission:
            self.display.console.print(f"[yellow]⚠️ {requester.name} requested review but has no pending submissions[/yellow]")
            return
        
        # Find recipient agent
        recipient_agent = next((a for a in agents if a.name == recipient_name), None)
        if not recipient_agent:
            return
        
        # Check if this submission is already in recipient's pending reviews
        if 'pending_reviews' not in recipient_agent.memory:
            recipient_agent.memory['pending_reviews'] = []
        
        existing_review = any(
            r['submission_id'] == recent_submission['id'] 
            for r in recipient_agent.memory['pending_reviews']
        )
        
        if not existing_review:
            # Add to recipient's pending reviews
            recipient_agent.memory['pending_reviews'].append({
                'submission_id': recent_submission['id'],
                'requester': requester.name,
                'problem_id': recent_submission['problem_id'],
                'code': recent_submission['code']
            })
            
            # Assign reviewer in scoring system
            self.scoring.assign_reviewer(recent_submission['id'], recipient_name)
            
            # Mark requester as waiting for review
            requester.memory['waiting_for_review'] = recipient_name
            
            # Log successful assignment
            self.display.console.print(
                f"[green]✅ {recipient_name} assigned to review {requester.name}'s "
                f"Problem {recent_submission['problem_id']}[/green]"
            )
    
    def _is_review_request(self, message: str) -> bool:
        """Determine if a message is a review request"""
        message_lower = message.lower()
        
        # Direct review request patterns (more natural language)
        review_patterns = [
            'review my', 'please review', 'could you review', 
            'would you review', 'mind reviewing', 'take a look',
            'can you review', 'will you review', 'review it'
        ]
        
        # Check for direct review request patterns
        has_direct_review_request = any(pattern in message_lower for pattern in review_patterns)
        
        # Traditional detection elements
        has_submitted = any(word in message_lower for word in ['submitted', 'submit', 'finished', 'implemented', 'completed', 'wrote', 'coded'])
        has_review = 'review' in message_lower
        has_problem_ref = any(word in message_lower for word in ['problem', 'solution', 'code', 'implementation'])
        
        # Log detection for debugging
        self.display.console.print(f"🔍 Review request detection:")
        self.display.console.print(f"   Direct request pattern: {has_direct_review_request}")
        self.display.console.print(f"   Has 'submitted': {has_submitted}")
        self.display.console.print(f"   Has 'review': {has_review}")
        self.display.console.print(f"   Has problem reference: {has_problem_ref}")
        
        # Accept either direct review request OR traditional pattern
        return has_direct_review_request or (has_review and has_submitted and has_problem_ref)
    
    def assign_reviewer_for_submission(self, submission_id: int, available_agents: List[str]) -> Optional[str]:
        """Assign a reviewer for a submission using LLM selection"""
        # This would implement the LLM-based reviewer selection
        # For now, returning None to indicate manual selection needed
        return None
    
    def get_pending_reviews_for_agent(self, agent_name: str) -> List[dict]:
        """Get all pending reviews assigned to an agent"""
        # This would query the scoring system for pending reviews
        # Implementation depends on scoring system interface
        return []