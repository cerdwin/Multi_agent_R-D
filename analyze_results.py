#!/usr/bin/env python3
"""
Analysis script for saboteur simulation results
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

def load_all_results(results_dir: str = "results") -> List[Dict[str, Any]]:
    """Load all simulation results from the results directory"""
    results_path = Path(results_dir)
    if not results_path.exists():
        print(f"Results directory {results_dir} not found")
        return []
    
    results = []
    for json_file in results_path.glob("simulation_*.json"):
        try:
            with open(json_file) as f:
                data = json.load(f)
                results.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return results

def create_agents_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a DataFrame with agent performance across all simulations"""
    rows = []
    
    for i, result in enumerate(results):
        sim_id = f"sim_{i:03d}"
        metadata = result['metadata']
        
        for agent_name, agent_data in result['agent_details'].items():
            row = {
                'simulation_id': sim_id,
                'timestamp': metadata['timestamp'],
                'llm_model': metadata['llm_model'],
                'completed_rounds': metadata['completed_rounds'],
                'max_rounds': metadata['max_rounds'],
                'agent_name': agent_name,
                'role': agent_data['role'],
                'final_score': agent_data['final_score'],
                'total_submissions': agent_data['total_submissions'],
                'approved_submissions': agent_data['approved_submissions'],
                'rejected_submissions': agent_data['rejected_submissions'],
                'approval_rate': agent_data['approved_submissions'] / max(agent_data['total_submissions'], 1),
            }
            rows.append(row)
    
    return pd.DataFrame(rows)

def create_simulation_dataframe(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a DataFrame with simulation-level metrics"""
    rows = []
    
    for i, result in enumerate(results):
        sim_id = f"sim_{i:03d}"
        metadata = result['metadata']
        activity = result['activity_metrics']
        insights = result['research_insights']
        
        row = {
            'simulation_id': sim_id,
            'timestamp': metadata['timestamp'],
            'llm_model': metadata['llm_model'],
            'completed_rounds': metadata['completed_rounds'],
            'max_rounds': metadata['max_rounds'],
            'early_termination': metadata['early_termination'],
            'total_agents': result['configuration']['total_agents'],
            'total_submissions': activity['total_submissions'],
            'approval_rate': activity['approval_rate'],
            'forum_messages': activity['forum_messages'],
            'saboteur_success_rate': insights['saboteur_success_rate'],
            'honeypot_accuracy': insights['honeypot_detection_accuracy']['accuracy'],
            'watermark_comments': insights['deception_signals_detected']['watermark_comments'],
            'suspicious_approvals': insights['deception_signals_detected']['suspicious_approvals'],
        }
        rows.append(row)
    
    return pd.DataFrame(rows)

def plot_score_distribution(agents_df: pd.DataFrame, save_path: str = "plots", timestamp: str = None):
    """Plot score distribution by role"""
    Path(save_path).mkdir(exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=agents_df, x='role', y='final_score')
    plt.title('Score Distribution by Agent Role')
    plt.ylabel('Final Score')
    plt.xlabel('Agent Role')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Use timestamp for filename if provided
    filename = f"score_distribution_{timestamp}.png" if timestamp else "score_distribution.png"
    plt.savefig(f"{save_path}/{filename}", dpi=300, bbox_inches='tight')
    plt.close()  # Close to prevent memory leaks

def plot_saboteur_performance(sim_df: pd.DataFrame, save_path: str = "plots", timestamp: str = None):
    """Plot saboteur success rate over time"""
    Path(save_path).mkdir(exist_ok=True)
    
    plt.figure(figsize=(12, 6))
    
    # Sort by timestamp
    sim_df_sorted = sim_df.sort_values('timestamp')
    
    plt.subplot(1, 2, 1)
    plt.plot(range(len(sim_df_sorted)), sim_df_sorted['saboteur_success_rate'], 'o-')
    plt.title('Saboteur Success Rate Over Time')
    plt.xlabel('Simulation Number')
    plt.ylabel('Success Rate (%)')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(range(len(sim_df_sorted)), sim_df_sorted['honeypot_accuracy'], 'o-', color='orange')
    plt.title('Honeypot Detection Accuracy Over Time')
    plt.xlabel('Simulation Number')
    plt.ylabel('Detection Accuracy (%)')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    # Use timestamp for filename if provided
    filename = f"saboteur_performance_{timestamp}.png" if timestamp else "saboteur_performance.png"
    plt.savefig(f"{save_path}/{filename}", dpi=300, bbox_inches='tight')
    plt.close()  # Close to prevent memory leaks

def plot_collaboration_patterns(results: List[Dict[str, Any]], save_path: str = "plots", timestamp: str = None):
    """Plot collaboration patterns across simulations"""
    Path(save_path).mkdir(exist_ok=True)
    
    # Aggregate collaboration data
    collab_data = {
        'saboteur_to_saboteur': [],
        'saboteur_to_honest': [],
        'honest_to_saboteur': [],
        'honest_to_honest': []
    }
    
    for result in results:
        patterns = result['research_insights']['collaboration_patterns']
        for key in collab_data:
            collab_data[key].append(patterns.get(f"{key}_reviews", 0))
    
    # Create DataFrame
    collab_df = pd.DataFrame(collab_data)
    collab_df.index.name = 'Simulation'
    
    # Plot stacked bar chart
    plt.figure(figsize=(12, 8))
    collab_df.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.title('Code Review Patterns Across Simulations')
    plt.xlabel('Simulation Number')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Review Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Use timestamp for filename if provided
    filename = f"collaboration_patterns_{timestamp}.png" if timestamp else "collaboration_patterns.png"
    plt.savefig(f"{save_path}/{filename}", dpi=300, bbox_inches='tight')
    plt.close()  # Close to prevent memory leaks

def generate_summary_report(agents_df: pd.DataFrame, sim_df: pd.DataFrame):
    """Generate a summary report of all simulations"""
    print("=" * 60)
    print("SABOTEUR SIMULATION ANALYSIS REPORT")
    print("=" * 60)
    
    print(f"\n📊 DATASET OVERVIEW")
    print(f"Total simulations: {len(sim_df)}")
    print(f"Total agent observations: {len(agents_df)}")
    print(f"Average rounds per simulation: {sim_df['completed_rounds'].mean():.1f}")
    print(f"Models used: {', '.join(sim_df['llm_model'].unique())}")
    
    print(f"\n🎯 PERFORMANCE METRICS")
    role_stats = agents_df.groupby('role').agg({
        'final_score': ['mean', 'std'],
        'approval_rate': ['mean', 'std']
    }).round(2)
    print(role_stats)
    
    print(f"\n🕵️ DETECTION & DECEPTION")
    print(f"Average saboteur success rate: {sim_df['saboteur_success_rate'].mean():.1f}%")
    print(f"Average honeypot accuracy: {sim_df['honeypot_accuracy'].mean():.1f}%")
    print(f"Average watermark comments: {sim_df['watermark_comments'].mean():.1f}")
    print(f"Average suspicious approvals: {sim_df['suspicious_approvals'].mean():.1f}")
    
    print(f"\n📈 TRENDS")
    if len(sim_df) > 1:
        saboteur_trend = np.polyfit(range(len(sim_df)), sim_df['saboteur_success_rate'], 1)[0]
        honeypot_trend = np.polyfit(range(len(sim_df)), sim_df['honeypot_accuracy'], 1)[0]
        print(f"Saboteur success trend: {saboteur_trend:+.2f}% per simulation")
        print(f"Honeypot accuracy trend: {honeypot_trend:+.2f}% per simulation")
    else:
        print("Need more simulations for trend analysis")

def main():
    """Main analysis function"""
    # Load all results
    results = load_all_results()
    
    if not results:
        print("No simulation results found. Run some simulations first!")
        return
    
    print(f"Loaded {len(results)} simulation results")
    
    # Create DataFrames
    agents_df = create_agents_dataframe(results)
    sim_df = create_simulation_dataframe(results)
    
    # Generate plots with timestamp from latest simulation
    print("Generating plots...")
    
    # Get timestamp from the most recent simulation for plot naming
    latest_timestamp = None
    if results:
        # Extract timestamp from the most recent result
        latest_result = max(results, key=lambda r: r['metadata']['timestamp'])
        latest_timestamp = latest_result['metadata']['timestamp'].replace(':', '').replace('-', '').replace(' ', '_')
    
    plot_score_distribution(agents_df, timestamp=latest_timestamp)
    plot_saboteur_performance(sim_df, timestamp=latest_timestamp)
    plot_collaboration_patterns(results, timestamp=latest_timestamp)
    
    # Generate summary report
    generate_summary_report(agents_df, sim_df)
    
    # Save processed data
    agents_df.to_csv("results/agents_analysis.csv", index=False)
    sim_df.to_csv("results/simulations_analysis.csv", index=False)
    print("\n💾 Processed data saved to CSV files in results/")
    
    print("\n✅ Analysis complete! Check the plots/ directory for visualizations.")

if __name__ == "__main__":
    main()