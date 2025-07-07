"""Refactored simulation entry point using modular architecture"""

from typing import List, Dict, Any
from simulation.game_controller import GameController


class SaboteurSimulation:
    """Main simulation class using the refactored architecture"""
    
    def __init__(self, config_file: str = "config.yaml", transparent_monitoring: bool = False, cot_monitoring: bool = False):
        self.game_controller = GameController(config_file, transparent_monitoring, cot_monitoring)
        
        # Expose key properties for backward compatibility
        self.config = self.game_controller.config
        self.agents = self.game_controller.agents
        self.scoring = self.game_controller.scoring
        self.display = self.game_controller.display
        self.logger = self.game_controller.logger
        self.message_manager = self.game_controller.message_manager
        
    def create_agents(self, agent_configs: List[Dict[str, Any]]):
        """Create agents from configuration"""
        self.game_controller.create_agents(agent_configs)
        self.agents = self.game_controller.agents
        
    def run_simulation(self):
        """Run the simulation"""
        self.game_controller.run_simulation()
        
    # Add any other methods needed for backward compatibility
    def save_results(self, stats: Dict[str, Any]):
        """Save results (delegated to game controller)"""
        self.game_controller._save_results(stats)