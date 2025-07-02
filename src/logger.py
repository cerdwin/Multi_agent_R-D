import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.text import Text
from typing import Optional, Dict, Any
import json

class SimulationLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamped log file
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_file = self.log_dir / f"simulation_{timestamp}.log"
        self.rich_log_file = self.log_dir / f"simulation_{timestamp}_rich.html"
        self.json_log_file = self.log_dir / f"simulation_{timestamp}_data.json"
        
        # Console for capturing rich output
        self.file_console = Console(
            file=open(self.log_file, 'w', encoding='utf-8'),
            width=120,
            record=True,
            force_terminal=False
        )
        
        # Console for HTML export (with rich formatting)
        self.html_console = Console(record=True, width=120)
        
        # Data storage for JSON export
        self.simulation_data = {
            "timestamp": timestamp,
            "rounds": [],
            "agents": {},
            "messages": [],
            "code_submissions": [],
            "metadata": {}
        }
        
        self.current_round = 0
    
    def log_simulation_start(self, agents: list, max_rounds: int):
        """Log simulation initialization"""
        self.simulation_data["metadata"] = {
            "max_rounds": max_rounds,
            "agent_count": len(agents),
            "start_time": datetime.now().isoformat()
        }
        
        for agent in agents:
            self.simulation_data["agents"][agent.name] = {
                "role": agent.role.value,
                "goals": agent.goals if hasattr(agent, 'goals') else []
            }
        
        message = f"🚀 Starting Saboteur Simulation with {len(agents)} agents for {max_rounds} rounds"
        self._log_both(message, "simulation_start")
    
    def log_round_start(self, round_number: int):
        """Log start of a new round"""
        self.current_round = round_number
        self.simulation_data["rounds"].append({
            "round": round_number,
            "start_time": datetime.now().isoformat(),
            "events": []
        })
        
        message = f"\n{'═' * 50} ITERATION {round_number} {'═' * 50}"
        self._log_both(message, "round_start")
    
    def log_agent_turn(self, agent_name: str, role: str):
        """Log agent turn"""
        message = f"\n🤖 AGENT {agent_name.upper()} (Role: {role})"
        self._log_both(message, "agent_turn", {"agent": agent_name, "role": role})
    
    def log_agent_decision(self, agent_name: str, decision: str, reasoning: str = ""):
        """Log agent decision"""
        message = f"  💭 {agent_name} decides to {decision}"
        if reasoning:
            message += f" - {reasoning}"
        
        self._log_both(message, "agent_decision", {
            "agent": agent_name,
            "decision": decision,
            "reasoning": reasoning
        })
    
    def log_forum_message(self, sender: str, message: str):
        """Log forum message"""
        self._log_message("forum", sender, message, None)
    
    def log_private_message(self, sender: str, recipient: str, message: str):
        """Log private message"""
        self._log_message("private", sender, message, recipient)
    
    def log_code_submission(self, agent_name: str, problem_title: str, code: str, problem_details: str = ""):
        """Log code submission"""
        submission_data = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "problem_title": problem_title,
            "code": code,
            "problem_details": problem_details,
            "round": self.current_round
        }
        
        self.simulation_data["code_submissions"].append(submission_data)
        
        message = f"  📝 {agent_name} submitted solution for: {problem_title}"
        self._log_both(message, "code_submission", submission_data)
        
        # Log the actual code with proper formatting
        code_message = f"```python\n{code}\n```"
        self._log_both(code_message, "code_content")
    
    def log_saboteur_detection(self, detector: str, suspects: list, confidence: float):
        """Log saboteur detection attempt"""
        detection_data = {
            "timestamp": datetime.now().isoformat(),
            "detector": detector,
            "suspects": suspects,
            "confidence": confidence,
            "round": self.current_round
        }
        
        message = f"  🚨 {detector} suspects saboteurs: {', '.join(suspects)} (confidence: {confidence:.1%})"
        self._log_both(message, "saboteur_detection", detection_data)
    
    def log_simulation_end(self, stats: Dict[str, Any]):
        """Log simulation completion"""
        self.simulation_data["metadata"]["end_time"] = datetime.now().isoformat()
        self.simulation_data["metadata"]["final_stats"] = stats
        
        message = f"\n🏁 Simulation Complete!"
        self._log_both(message, "simulation_end")
        
        # Log final statistics
        for key, value in stats.items():
            self._log_both(f"  {key}: {value}", "final_stats")
    
    def _log_message(self, message_type: str, sender: str, content: str, recipient: Optional[str] = None):
        """Internal method to log messages"""
        message_data = {
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "sender": sender,
            "content": content,
            "recipient": recipient,
            "round": self.current_round
        }
        
        self.simulation_data["messages"].append(message_data)
        
        if message_type == "forum":
            log_message = f"  📢 Forum - {sender}: {content[:100]}{'...' if len(content) > 100 else ''}"
        else:
            log_message = f"  💬 Private - {sender} → {recipient}: {content[:100]}{'...' if len(content) > 100 else ''}"
        
        self._log_both(log_message, "message", message_data)
    
    def _log_both(self, message: str, event_type: str, data: Optional[Dict[str, Any]] = None):
        """Log to both text file and structured data"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # Log to text file
        self.file_console.print(formatted_message)
        
        # Log to HTML console (preserves rich formatting) - for export only
        if hasattr(self, 'html_console'):
            self.html_console.print(formatted_message)
        
        # Add to current round events
        if self.simulation_data["rounds"]:
            event = {
                "timestamp": datetime.now().isoformat(),
                "type": event_type,
                "message": message,
                "data": data or {}
            }
            self.simulation_data["rounds"][-1]["events"].append(event)
    
    def save_logs(self):
        """Save all log files"""
        try:
            # Close text log file
            self.file_console.file.close()
            
            # Save HTML export with rich formatting
            with open(self.rich_log_file, 'w', encoding='utf-8') as f:
                f.write(self.html_console.export_html(inline_styles=True))
            
            # Save JSON data
            with open(self.json_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.simulation_data, f, indent=2, ensure_ascii=False)
            
            return {
                "text_log": str(self.log_file),
                "html_log": str(self.rich_log_file),
                "json_log": str(self.json_log_file)
            }
        except Exception as e:
            print(f"Error saving logs: {e}")
            return None
    
    def get_log_summary(self) -> Dict[str, Any]:
        """Get summary of logged simulation"""
        return {
            "total_rounds": len(self.simulation_data["rounds"]),
            "total_messages": len(self.simulation_data["messages"]),
            "total_submissions": len(self.simulation_data["code_submissions"]),
            "agents": list(self.simulation_data["agents"].keys()),
            "log_files": {
                "text": str(self.log_file),
                "html": str(self.rich_log_file),
                "json": str(self.json_log_file)
            }
        }