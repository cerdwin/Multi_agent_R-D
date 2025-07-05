#!/usr/bin/env python3
"""
Quick SaboteurBench Dashboard Demo
Non-interactive version for immediate demo startup
"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

from dashboard_server import DashboardServer

def main():
    """Quick demo launcher"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                     🕵️ SaboteurBench 🕵️                      ║
║        Evaluating Strategic Deception in AI Research Teams    ║
║                                                              ║
║  🎯 Interactive Dashboard - Quick Demo Mode                  ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    server = DashboardServer(port=8080)
    
    print("🚀 Starting quick demo with default settings...")
    print("📊 Dashboard will open at: http://localhost:8080/dashboard.html")
    print("🛑 Press Ctrl+C to stop")
    print("─" * 64)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped!")

if __name__ == '__main__':
    main()