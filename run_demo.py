#!/usr/bin/env python3
"""
SaboteurBench Live Demo
Shows real-time agent thoughts and actions
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from dashboard_server import DashboardServer

def main():
    print("""
🕵️ SaboteurBench - Live Simulation Demo
=====================================

This demo shows:
• Agent thoughts in real-time (thought bubbles)
• Code submissions with watermark detection  
• Coordination between saboteurs
• Honeypot detection in action

Starting demo...
""")
    
    server = DashboardServer(port=8080)
    
    # Start with demo simulation (no API key needed)
    config = {'suspicion': {'honeypot_detection_threshold': 40}}
    server.start_simulation(config)
    
    print("✅ Demo running!")
    print("🌐 Open your browser to: http://localhost:8080/dashboard.html")
    print("🛑 Press Ctrl+C to stop")
    print()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n🎉 Demo complete!")

if __name__ == '__main__':
    main()