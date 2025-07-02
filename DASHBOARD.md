# 🕵️ SaboteurBench Interactive Dashboard

An immersive real-time visualization system for AI safety research on strategic deception and tacit collusion.

## ✨ Features

### 🎛️ **Live Simulation Control**
- **Real-time parameter adjustment**: Modify honeypot detection sensitivity on-the-fly
- **Simulation speed control**: Pause, step through, or reset simulations
- **Scenario switching**: Test different configurations instantly

### 📊 **Agent Monitoring Dashboard**
- **Individual agent cards** with role-specific metrics:
  - **Workers**: Efficiency ratings and review quality
  - **Saboteurs**: Coordination success and suspicion levels  
  - **Honeypots**: Detection confidence and alert counts
- **Suspicion meters** with color-coded threat levels
- **Elimination tracking** when agents are detected/removed

### 🕵️ **Deception Detection Visualization**
- **Watermark highlighting**: Animal fact coordination signals glow golden
- **Bug detection alerts**: Subtle sabotage attempts highlighted in red
- **Communication pattern analysis**: Private message flow tracking
- **Coordination timeline**: Visual sequence of collaborative deception

### 📈 **Research Metrics**
- **Detection success rate**: Percentage of saboteurs caught
- **False positive tracking**: Innocent agents wrongly accused  
- **Time to detection**: Average rounds before identification
- **Signal analysis**: Coordination attempts vs. successful coordination

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
```bash
python launch_dashboard.py
```

### Option 2: Manual Server Start
```bash
python dashboard_server.py --auto-start --threshold 40
```

### Option 3: Dashboard Only (Demo Mode)
```bash
python dashboard_server.py
# Then open: http://localhost:8080/dashboard.html
```

## 🎮 Usage Guide

### **For Presentations**
1. **Start with high sensitivity** (20%) to show rapid detection
2. **Demonstrate threshold impact** by adjusting slider during simulation
3. **Highlight key moments**: Pause when watermarks appear or bugs are detected
4. **Show coordination patterns**: Point out subtle communication between saboteurs

### **For Research**
1. **Run multiple scenarios** with different thresholds
2. **Collect metrics** across simulation runs
3. **Analyze detection patterns** and false positive rates
4. **Study coordination strategies** that emerge between saboteurs

## 🎯 Demo Scenarios

### **Scenario 1: Successful Detection**
- **Threshold**: 40%
- **Expected outcome**: Honeypot detects both saboteurs within 6-8 rounds
- **Key features**: Shows effective monitoring in action

### **Scenario 2: Missed Saboteurs** 
- **Threshold**: 90%
- **Expected outcome**: Saboteurs coordinate successfully without detection
- **Key features**: Demonstrates the challenge of subtle deception

### **Scenario 3: False Positives**
- **Threshold**: 20% 
- **Expected outcome**: Workers wrongly accused due to over-sensitivity
- **Key features**: Shows the balance needed in detection systems

## 🔧 Technical Details

### **Architecture**
- **Frontend**: Modern responsive HTML5/CSS3/JavaScript
- **Backend**: Python HTTP server with real-time API
- **Integration**: Seamless connection to existing simulation codebase
- **Performance**: 1-second update intervals for smooth real-time experience

### **API Endpoints**
- `GET /api/status` - Simulation state and round information
- `GET /api/agents` - Agent data, scores, and suspicion levels  
- `GET /api/activity` - Recent activity feed with event details
- `GET /api/metrics` - Aggregated performance statistics
- `GET /api/config?threshold=X` - Update honeypot sensitivity

### **Browser Requirements**
- Modern browser with ES6+ support (Chrome, Firefox, Safari, Edge)
- JavaScript enabled for interactivity
- 1920x1080+ resolution recommended for optimal layout

## 🎨 Visual Design

The dashboard uses a cybersecurity aesthetic with:
- **Dark theme** with neon blue/green accents
- **Gradient backgrounds** and subtle glowing effects  
- **Color-coded roles**: Green (workers), Red (saboteurs), Gold (honeypots)
- **Animated highlights** for watermarks and bug detection
- **Responsive layout** that adapts to different screen sizes

## 📊 Research Applications

### **AI Safety Research**
- Study how AI systems detect deception in collaborative environments
- Analyze the effectiveness of different monitoring strategies
- Understand the balance between detection and false positives

### **Coordination Analysis** 
- Observe emergent tacit collusion between adversarial agents
- Study signal evolution to avoid detection systems
- Analyze communication patterns under surveillance

### **Human-AI Interaction**
- Compare human vs. AI deception detection capabilities
- Study trust formation and betrayal in mixed teams
- Analyze decision-making under uncertainty

## 🚀 Future Enhancements

- **Network graph visualization** of agent communication patterns
- **Historical trend analysis** across multiple simulation runs
- **AI-powered pattern detection** for identifying novel coordination strategies
- **Export capabilities** for research data and visualizations
- **Multi-scenario comparison** dashboard for A/B testing

---

*Built for the MATS Alignment Scholars Program - Advancing AI Safety Through Interactive Research Tools*