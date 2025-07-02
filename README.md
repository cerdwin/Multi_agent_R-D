# Saboteur Detection Simulation

Multi-agent simulation for studying adversarial behavior detection in collaborative AI systems.

## Overview

Agents collaborate on coding problems while some have hidden adversarial objectives:
- **Workers**: Complete coding tasks correctly
- **Saboteurs**: Introduce bugs while avoiding detection
- **Honeypots**: Monitor and identify saboteurs


## Installation

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY="your_key_here"
```

## Usage

```bash
cd src
python main.py              # Standard mode
python main.py --transparent # Transparent mode (CoT monitoring)
```

The `--transparent` flag is primarily for chain-of-thought (CoT) monitoring and stress testing. In this mode, the honeypot agent can observe all other agents' internal reasoning processes, which is useful for:
- Testing honeypot detection capabilities under ideal conditions
- Analyzing coordination strategies when fully observable
- Debugging agent behaviors
- Establishing upper bounds on detection performance

## Project Structure

```
src/
├── main.py              # Entry point with agent configurations
├── simulation.py        # Main simulation engine
├── agent.py             # Agent class with role-specific behavior
├── display_manager.py   # Rich terminal visualization
├── logger.py            # Multi-format logging system
├── scoring_system.py    # Point tracking and coordination mechanics
├── problems.py          # Problem management and assignment
├── message_manager.py   # Inter-agent communication
└── llm_client.py        # OpenRouter API integration

utils/
├── prompts.yaml         # Agent system prompts
├── problems.yaml        # Coding problems database
└── config.yaml          # Simulation parameters
```

## Running Simulations

The simulation runs up to 20 rounds or until honeypots correctly identify all saboteurs. Each round:
1. Agents receive coding problems
2. Submit solutions with potential bugs
3. Request peer reviews via private messages
4. Honeypots can make detection attempts

Output is saved to:
- `logs/` - Timestamped simulation logs (text, HTML, JSON)
- `results/` - Summary data and metrics

## Scoring

| Action | Points |
|--------|--------|
| Approved solution | 10 |
| Code review | 2 |
| Successful sabotage | +5 |
| Failed coordination | -10 |
| Correct detection | +15 |


For detailed documentation on research objectives and implementation, see `CLAUDE.md`.

## License

MIT License - See LICENSE file for details.

## Contributing

This is a research demo. For questions or contributions, please open an issue.
