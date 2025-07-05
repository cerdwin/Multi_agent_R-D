import yaml
from pathlib import Path

def load_prompts():
    """Load prompts from YAML file"""
    prompts_file = Path(__file__).parent / "prompts.yaml"
    with open(prompts_file, 'r') as f:
        return yaml.safe_load(f)

# Load prompts on import
PROMPTS = load_prompts()

def get_prompt(category: str, prompt_type: str) -> str:
    """Get a specific prompt from the loaded prompts"""
    return PROMPTS.get(category, {}).get(prompt_type, "")