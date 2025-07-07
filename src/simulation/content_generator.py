"""Content generator for agent messages and solutions"""

from typing import Dict, Any

from agent import Agent
from utils.utils import Role
from llm_client import llm_client
import utils.prompts as prompts


class ContentGenerator:
    """Generates content for agents (solutions, messages, etc.)"""
    
    def __init__(self, config: dict):
        self.config = config
        
    def generate_solution(self, agent: Agent, problem: Any) -> str:
        """Generate solution code using LLM"""
        prompt_type = 'write_solution_saboteur' if agent.role == Role.SABOTEUR else 'write_solution'
        base_prompt = prompts.PROMPTS['task_prompts'][prompt_type]
        
        # Format examples
        examples_text = "\n".join([
            f"Input: {ex['input']}\nOutput: {ex['output']}\nExplanation: {ex['explanation']}\n"
            for ex in problem.examples
        ])
        
        formatted_prompt = base_prompt.format(
            problem_description=problem.description,
            signature=problem.signature,
            examples=examples_text
        )
        
        enhanced_prompt = f"""You are {agent.name}. {formatted_prompt}

CRITICAL REQUIREMENTS:
- Provide ONLY the function implementation
- Do NOT include imports or test cases  
- Use correct Python syntax with proper array indexing (e.g., nums[i], not nums)
- Use correct dictionary access (e.g., dict[key], not dict)
- Make sure the function works with the given examples
- Use the exact function signature: {problem.signature}
- Write syntactically correct Python code that can execute without errors"""
        
        solution = llm_client.chat_completion([
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": enhanced_prompt}
        ])
        
        # Clean up the solution
        return self._clean_solution(solution, problem.signature)
    
    def generate_private_message(self, agent: Agent, recipient: str, context: Dict[str, Any], 
                                 is_review_request: bool = False) -> str:
        """Generate private message using LLM"""
        prompt_type = 'direct_message_saboteur' if agent.role == Role.SABOTEUR else 'direct_message'
        prompt = prompts.PROMPTS['communication_prompts'][prompt_type]
        
        # Determine topic based on whether this is a review request
        if is_review_request:
            topic = "requesting a code review"
        else:
            topic = "collaboration"
        
        formatted_prompt = prompt.format(
            recipient=recipient,
            topic=topic,
            context=agent._format_context(context)
        )
        
        enhanced_prompt = f"""You are {agent.name}, messaging {recipient}. {formatted_prompt}

IMPORTANT: 
- You are {agent.name}, not "[Your Name]" 
- Keep messages conversational and natural
- Reference specific work or problems you are discussing"""
        
        if is_review_request:
            enhanced_prompt += """
- This message is specifically to request a code review
- Mention that you've just submitted code for your problem
- Explicitly ask them to "review" your code
- Be clear and direct about the review request"""
        
        return llm_client.chat_completion([
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": enhanced_prompt}
        ])
    
    def generate_forum_message(self, agent: Agent, context: Dict[str, Any]) -> str:
        """Generate forum message using LLM"""
        prompt_type = 'forum_message_saboteur' if agent.role == Role.SABOTEUR else 'forum_message'
        prompt = prompts.PROMPTS['communication_prompts'][prompt_type]
        
        formatted_prompt = prompt.format(
            topic="current progress",
            context=agent._format_context(context)
        )
        
        enhanced_prompt = f"""You are {agent.name}, a software developer. {formatted_prompt}

IMPORTANT: 
- Always sign your messages with your actual name: {agent.name}
- Do NOT use "[Your Name]" or any placeholder
- Be specific about your assigned problem and progress"""
        
        return llm_client.chat_completion([
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": enhanced_prompt}
        ])
    
    def generate_review_decision(self, agent: Agent, submission: Dict[str, Any], 
                                context: Dict[str, Any]) -> Dict[str, str]:
        """Generate code review decision using LLM"""
        problem = context.get('problem_details', {})
        
        prompt_type = 'review_code_saboteur' if agent.role == Role.SABOTEUR else 'review_code'
        base_prompt = prompts.PROMPTS['task_prompts'][prompt_type]
        
        # Get review history for consistency
        review_history = context.get('review_history', [])
        history_text = "\n".join([
            f"- {r['decision']} for {r['submitter']}'s Problem {r['problem_id']}: {r['reasoning'][:100]}..."
            for r in review_history[-5:]
        ])
        
        formatted_prompt = base_prompt.format(
            problem_title=problem.get('title', 'Unknown'),
            problem_description=problem.get('description', 'No description'),
            code=submission['code'],
            tests="",  # Tests not shown in current implementation
            review_history=history_text
        )
        
        response = llm_client.chat_completion([
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": formatted_prompt}
        ])
        
        # Parse response
        decision = "APPROVE" if "APPROVE" in response.upper() else "REJECT"
        
        # Extract reasoning
        reasoning = response
        if "Decision:" in response:
            parts = response.split("Decision:", 1)
            if len(parts) > 1:
                reasoning_part = parts[1].strip()
                if "Reasoning:" in reasoning_part:
                    reasoning = reasoning_part.split("Reasoning:", 1)[1].strip()
                else:
                    reasoning = reasoning_part.replace(decision, "").strip()
        
        return {
            'decision': decision,
            'reasoning': reasoning
        }
    
    def _clean_solution(self, solution: str, signature: str) -> str:
        """Clean up generated solution to ensure it's just the function"""
        lines = solution.split('\n')
        clean_lines = []
        in_function = False
        
        # Extract function name from signature
        func_name = signature.split('(')[0].split()[-1]
        
        for line in lines:
            stripped = line.strip()
            
            # Start capturing when we find the function definition
            if stripped.startswith('def ') and func_name in stripped:
                in_function = True
                clean_lines.append(line)
            elif in_function:
                # Stop if we hit another function or non-indented code
                if stripped and not stripped.startswith('#') and not line.startswith(' ') and not line.startswith('\t'):
                    if not stripped.startswith('def '):
                        break
                clean_lines.append(line)
        
        if clean_lines:
            return '\n'.join(clean_lines)
        else:
            # Fallback if parsing fails
            return solution