import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_exam_period_plot(exam_mean, non_exam_mean, exam_std, non_exam_std):
    """Create bar plot comparing exam and non-exam period viewing."""
    plt.figure(figsize=(10, 6))
    means = [exam_mean, non_exam_mean]
    stds = [exam_std, non_exam_std]
    
    bars = plt.bar(['Exam Period', 'Non-Exam Period'], means, yerr=stds, capsize=5)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.title('Average Daily Netflix Views: Exam vs Non-Exam Periods')
    plt.ylabel('Average Daily Views')
    plt.grid(True, alpha=0.3)
    
    plt.savefig('exam_period_comparison.png')
    plt.close()

def create_weekly_pattern_plot(weekly_data):
    """Create line plot of weekly viewing pattern."""
    plt.figure(figsize=(12, 6))
    
    plt.plot(weekly_data['week_number'], weekly_data['weekly_views'], 
             marker='o', linestyle='-', linewidth=2, markersize=8)
    
    plt.title('Weekly Netflix Viewing Pattern')
    plt.xlabel('Week Number')
    plt.ylabel('Number of Views')
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(weekly_data['week_number'], weekly_data['weekly_views'], 1)
    p = np.poly1d(z)
    plt.plot(weekly_data['week_number'], p(weekly_data['week_number']), 
             "r--", alpha=0.8, label=f'Trend line (slope: {z[0]:.2f})')
    
    plt.legend()
    plt.savefig('weekly_pattern.png')
    plt.close()

def create_weekend_comparison_plot(weekend_mean, weekday_mean):
    """Create bar plot comparing weekend and weekday viewing."""
    plt.figure(figsize=(10, 6))
    means = [weekend_mean, weekday_mean]
    
    bars = plt.bar(['Weekend', 'Weekday'], means, capsize=5)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.title('Average Daily Netflix Views: Weekend vs Weekday')
    plt.ylabel('Average Daily Views')
    plt.grid(True, alpha=0.3)
    
    plt.savefig('weekend_comparison.png')
    plt.close()

def main():
    try:
        # Load weekly viewing data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), "data_processing")
        weekly_data = pd.read_csv(os.path.join(data_dir, "weekly_viewing_counts.csv"))
        
        # Read statistical results
        with open('statistical_results.txt', 'r') as f:
            results = f.read()
        
        # Extract values from statistical results
        exam_mean = float(results.split('Mean daily views during exam periods: ')[1].split('\n')[0])
        non_exam_mean = float(results.split('Mean daily views during non-exam periods: ')[1].split('\n')[0])
        exam_std = float(results.split('Standard deviation during exam periods: ')[1].split('\n')[0])
        non_exam_std = float(results.split('Standard deviation during non-exam periods: ')[1].split('\n')[0])
        weekend_mean = float(results.split('Mean weekend views: ')[1].split('\n')[0])
        weekday_mean = float(results.split('Mean weekday views: ')[1].split('\n')[0])
        
        print("Creating visualizations...")
        
        # Create plots
        create_exam_period_plot(exam_mean, non_exam_mean, exam_std, non_exam_std)
        create_weekly_pattern_plot(weekly_data)
        create_weekend_comparison_plot(weekend_mean, weekday_mean)
        
        print("Visualizations completed! The following files have been created:")
        print("1. exam_period_comparison.png")
        print("2. weekly_pattern.png")
        print("3. weekend_comparison.png")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure all required files exist and are accessible.")

if __name__ == "__main__":
    main() 