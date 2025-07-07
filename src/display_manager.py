from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
from rich.layout import Layout
from rich.rule import Rule
from typing import Dict, Tuple, List
import random

class DisplayManager:
    def __init__(self):
        self.console = Console()
        self.agent_colors = {}
        self.color_index = 0
        self.logger = None
        
        # 30 color pairs (bright for speech, darker for actions)
        # First 5 colors are distinctly different for common use case
        self.color_pairs = [
            ("bright_red", "red"),
            ("bright_blue", "blue"), 
            ("bright_green", "green"),
            ("bright_magenta", "magenta"),
            ("bright_yellow", "yellow3"),
            ("bright_cyan", "cyan"),
            ("bright_white", "grey70"),
            ("orange1", "dark_orange"),
            ("purple", "medium_purple"),
            ("turquoise2", "dark_turquoise"),
            ("spring_green1", "dark_green"),
            ("deep_pink1", "medium_violet_red"),
            ("gold1", "dark_goldenrod"),
            ("sky_blue1", "steel_blue"),
            ("chartreuse1", "olive_drab"),
            ("coral1", "indian_red"),
            ("orchid1", "dark_orchid"),
            ("khaki1", "dark_khaki"),
            ("plum1", "medium_purple3"),
            ("salmon1", "dark_salmon"),
            ("light_goldenrod1", "goldenrod"),
            ("pale_green1", "dark_sea_green"),
            ("light_steel_blue1", "slate_gray"),
            ("misty_rose1", "rosy_brown"),
            ("wheat1", "tan"),
            ("lavender", "medium_purple4"),
            ("peach_puff1", "sandy_brown"),
            ("light_cyan1", "dark_cyan"),
            ("honeydew2", "pale_green"),
            ("light_pink1", "hot_pink")
        ]
        
    def assign_color_to_agent(self, agent_name: str) -> Tuple[str, str]:
        """Assign a unique color pair to an agent - deterministic based on agent name"""
        if agent_name not in self.agent_colors:
            # Use a deterministic hash-based approach for consistent colors
            import hashlib
            hash_value = int(hashlib.md5(agent_name.encode()).hexdigest(), 16)
            color_index = hash_value % len(self.color_pairs)
            self.agent_colors[agent_name] = self.color_pairs[color_index]
        return self.agent_colors[agent_name]
    
    def set_logger(self, logger):
        """Set logger for capturing display output"""
        self.logger = logger
    
    def _log_display(self, content: str, event_type: str = "display"):
        """Log display content to HTML console if logger is available"""
        if self.logger and hasattr(self.logger, 'html_console'):
            self.logger.html_console.print(content)
    
    def display_iteration_header(self, iteration_num: int):
        """Display iteration header"""
        header = Rule(f"[bold cyan]ITERATION {iteration_num}[/bold cyan]", style="cyan")
        self.console.print()
        self.console.print(header)
        self.console.print()
        
    
    def display_agent_turn(self, agent_name: str, role: str, suspicion_data: dict = None):
        """Display agent turn header with optional suspicion tracking"""
        bright_color, _ = self.assign_color_to_agent(agent_name)
        
        content = f"[bold {bright_color}]AGENT {agent_name.upper()}[/bold {bright_color}]\n[italic]Role: {role}[/italic]"
        
        # Get timing info for fade effect
        current_round = suspicion_data.get('current_round', 0) if suspicion_data else 0
        last_update = suspicion_data.get('last_update_round', None) if suspicion_data else None
        
        # Calculate fade level (0 = bright/new, higher = more faded)
        fade_level = 0
        if last_update is not None:
            rounds_since_update = current_round - last_update
            fade_level = min(3, rounds_since_update)  # Max 3 levels of fade
        
        # Add suspicion tracking display
        if suspicion_data:
            if role == "honeypot":
                if suspicion_data.get('suspicion_scores'):
                    content += "\n[dim]🔍 Saboteur Suspicion:[/dim]"
                    for agent, score in suspicion_data['suspicion_scores'].items():
                        bar = self._create_suspicion_bar(score, "red", fade_level)
                        content += f"\n  {agent}: {bar} {score}%"
                
                if suspicion_data.get('honeypot_suspicion'):
                    content += "\n[dim]🍯 Honeypot Detection:[/dim]"
                    for agent, score in suspicion_data['honeypot_suspicion'].items():
                        bar = self._create_suspicion_bar(score, "green", fade_level)
                        content += f"\n  {agent}: {bar} {score}%"
            
            elif role == "saboteur":
                if suspicion_data.get('honeypot_detection'):
                    content += "\n[dim]🕵️ Honeypot Detection:[/dim]"
                    for agent, score in suspicion_data['honeypot_detection'].items():
                        bar = self._create_suspicion_bar(score, "blue", fade_level)
                        content += f"\n  {agent}: {bar} {score}%"
                
                if suspicion_data.get('saboteur_suspicion'):
                    content += "\n[dim]🤝 Ally Detection:[/dim]"
                    for agent, score in suspicion_data['saboteur_suspicion'].items():
                        bar = self._create_suspicion_bar(score, "purple", fade_level)
                        content += f"\n  {agent}: {bar} {score}%"
            
            elif role == "worker":
                if suspicion_data.get('efficiency_ratings'):
                    content += "\n[dim]⚡ Team Efficiency:[/dim]"
                    for agent, score in suspicion_data['efficiency_ratings'].items():
                        bar = self._create_suspicion_bar(score, "cyan", fade_level)
                        content += f"\n  {agent}: {bar} {score}%"
        
        self.console.print()
        panel = Panel(content, style=bright_color, expand=False)
        self.console.print(panel)
    
    def _create_suspicion_bar(self, score: int, color_scheme: str = "red", fade_level: int = 0) -> str:
        """Create visual suspicion bar with fade effect based on recency"""
        # Use a single base color for each type of rating
        base_colors = {
            "red": "red",      # Saboteur suspicion
            "green": "green",  # Honeypot suspicion  
            "blue": "blue",    # Honeypot detection
            "purple": "purple", # Ally detection
            "cyan": "cyan"     # Efficiency ratings
        }
        
        base_color = base_colors.get(color_scheme, "white")
        
        # Ensure at least 1 filled segment for any non-zero score, max 5 segments
        filled = max(1, min(5, (score + 19) // 20)) if score > 0 else 0
        
        # Apply fade based on how old the data is - same color, different brightness
        if fade_level == 0:
            # Fresh data - bright and bold
            bar = "█" * filled + "░" * (5 - filled)
            style = f"bold bright_{base_color}" if f"bright_{base_color}" in ["bright_red", "bright_green", "bright_blue", "bright_cyan"] else f"bold {base_color}"
        elif fade_level == 1:
            # 1 round old - normal brightness
            bar = "█" * filled + "░" * (5 - filled)
            style = base_color
        elif fade_level == 2:
            # 2 rounds old - dim
            bar = "▓" * filled + "░" * (5 - filled)
            style = f"dim {base_color}"
        else:
            # 3+ rounds old - very dim with dotted blocks
            bar = "▒" * filled + "░" * (5 - filled)
            style = f"dim {base_color}"
        
        return f"[{style}]{bar}[/{style}]"
    
    def display_agent_speech(self, agent_name: str, message: str):
        """Display agent speech (bright color)"""
        bright_color, _ = self.assign_color_to_agent(agent_name)
        text = Text()
        text.append(f"{agent_name}: ", style=f"bold {bright_color}")
        text.append(message, style=bright_color)
        self.console.print(text)
    
    def display_agent_action(self, agent_name: str, action: str):
        """Display agent action (darker color)"""
        _, dark_color = self.assign_color_to_agent(agent_name)
        text = Text()
        text.append("  [", style="dim")
        text.append(f"{agent_name} {action}", style=f"{dark_color} italic")
        text.append("]", style="dim")
        self.console.print(text)
    
    def display_forum_message(self, sender: str, message: str, timestamp: int = None):
        """Display forum message"""
        bright_color, _ = self.assign_color_to_agent(sender)
        self.console.print(Panel(
            f"[{bright_color}]{sender}:[/{bright_color}] {message}",
            title="[bold]Forum[/bold]",
            title_align="left",
            border_style="green"
        ))
    
    def display_private_message(self, sender: str, recipient: str, message: str):
        """Display private message"""
        sender_color, _ = self.assign_color_to_agent(sender)
        recipient_color, _ = self.assign_color_to_agent(recipient)
        
        self.console.print(Panel(
            f"[{sender_color}]{sender}[/{sender_color}] → [{recipient_color}]{recipient}[/{recipient_color}]: {message}",
            title="[bold]Private Message[/bold]",
            title_align="left",
            border_style="yellow"
        ))
    
    def display_code_submission(self, agent_name: str, code: str, problem_title: str):
        """Display code submission"""
        bright_color, dark_color = self.assign_color_to_agent(agent_name)
        
        self.console.print(Panel(
            f"[{dark_color}]```python\n{code}\n```[/{dark_color}]",
            title=f"[{bright_color}]{agent_name}'s Solution: {problem_title}[/{bright_color}]",
            border_style=dark_color
        ))
    
    def display_review_result(self, reviewer: str, author: str, decision: str, reasoning: str):
        """Display code review result"""
        reviewer_color, _ = self.assign_color_to_agent(reviewer)
        author_color, _ = self.assign_color_to_agent(author)
        
        decision_style = "green" if decision == "APPROVE" else "red"
        
        self.console.print(Panel(
            f"[{reviewer_color}]{reviewer}[/{reviewer_color}] reviewing [{author_color}]{author}'s[/{author_color}] code\n\n"
            f"Decision: [{decision_style}]{decision}[/{decision_style}]\n"
            f"Reasoning: {reasoning}",
            title="[bold]Code Review[/bold]",
            border_style="blue"
        ))
    
    def display_summary_stats(self, stats: Dict[str, any]):
        """Display simulation summary statistics"""
        self.console.print()
        self.console.print(Rule("[bold green]SIMULATION SUMMARY[/bold green]", style="green"))
        
        for key, value in stats.items():
            self.console.print(f"[cyan]{key}:[/cyan] {value}")
    
    def display_saboteur_detection(self, detector: str, suspected: List[str], confidence: float, is_correct: bool = False):
        """Display saboteur detection attempt"""
        detector_color, _ = self.assign_color_to_agent(detector)
        
        suspected_text = ", ".join([f"[{self.assign_color_to_agent(s)[0]}]{s}[/{self.assign_color_to_agent(s)[0]}]" for s in suspected])
        
        # Special styling for correct accusation
        if is_correct:
            title = "[bold green]🎯 CORRECT SABOTEUR DETECTED! 🎯[/bold green]"
            border_style = "green"
            confidence_color = "green"
            extra_text = ""
        else:
            title = "[bold red]🚨 SABOTEUR DETECTION 🚨[/bold red]"
            border_style = "red"
            confidence_color = "yellow"
            extra_text = ""
        
        content = (f"[{detector_color}]{detector}[/{detector_color}] suspects: {suspected_text}\n"
                  f"Confidence: [{confidence_color}]{confidence:.1%}[/{confidence_color}]"
                  f"{extra_text}")
        
        # Add dramatic visual elements for correct detection
        if is_correct:
            self.console.print("🎆" * 20)
            
        self.console.print(Panel(
            content,
            title=title,
            border_style=border_style,
            expand=True
        ))
        
        if is_correct:
            self.console.print("🎆" * 20)
    
    def clear_screen(self):
        """Clear the console screen"""
        self.console.clear()
    
    def print_separator(self):
        """Print a simple separator"""
        self.console.print("─" * 80, style="dim")