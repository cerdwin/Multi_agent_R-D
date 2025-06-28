import os
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat_completion(self, 
                       messages: list, 
                       temperature: Optional[float] = None,
                       max_tokens: Optional[int] = None,
                       **kwargs) -> str:
        """Send chat completion request to OpenRouter"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM API Error: {e}")
            return f"Error: Unable to get LLM response - {str(e)}"
    
    def generate_agent_response(self, 
                              system_prompt: str, 
                              context: str, 
                              agent_role: str) -> str:
        """Generate agent response with role-specific prompting"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\nAs a {agent_role}, respond appropriately:"}
        ]
        
        return self.chat_completion(messages)
    
    def format_prompt_with_context(self, 
                                 base_prompt: str, 
                                 context: Dict[str, Any]) -> str:
        """Format prompt template with context variables"""
        try:
            return base_prompt.format(**context)
        except KeyError as e:
            print(f"Warning: Missing context variable {e}")
            return base_prompt
    
    def validate_api_connection(self) -> bool:
        """Test API connection"""
        try:
            test_response = self.chat_completion([
                {"role": "user", "content": "Hello, please respond with 'API connection successful'"}
            ])
            return "successful" in test_response.lower()
        except Exception as e:
            print(f"API validation failed: {e}")
            return False

# Global LLM client instance
llm_client = LLMClient()