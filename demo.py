#!/usr/bin/env python3
"""
SaboteurBench Demo - MATS Presentation Ready
Perfect for your week 3 presentation!
"""

import sys
import webbrowser
import time
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

from dashboard_server import DashboardServer

def main():
    """Demo launcher optimized for presentations"""
    print("""
🕵️ SaboteurBench - AI Safety Research Dashboard

🎯 MATS Week 3 Presentation Demo
📊 Real-time Deception Detection Visualization
🎛️ Interactive Parameter Control

Starting demo server...
""")
    
    server = DashboardServer(port=8080)
    
    # Start the demo simulation automatically!
    print("🎬 Starting live simulation demo...")
    config = {'suspicion': {'honeypot_detection_threshold': 40}}
    server.start_simulation(config)
    
    print("✅ Server ready!")
    print("🌐 Dashboard URL: http://localhost:8080/dashboard.html")
    print("🚀 Opening browser automatically...")
    print()
    print("🎮 Demo Features:")
    print("  • Live agent thoughts in thought bubbles")
    print("  • Code submissions with watermark highlighting") 
    print("  • Real-time coordination detection")
    print("  • Honeypot monitoring and reporting")
    print()
    print("🛑 Press Ctrl+C when done with demo")
    print("═" * 60)
    
    # Auto-open browser after short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:8080/dashboard.html')
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n\n🎉 Demo complete! Great job on your presentation!")

if __name__ == '__main__':
    main()