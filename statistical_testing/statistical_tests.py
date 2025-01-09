import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

def load_data():
    """Load the required data files."""
    # Get the absolute path to the data_processing directory
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent / "data_processing"
    
    # Load daily viewing counts
    daily_views = pd.read_csv(data_dir / "daily_viewing_counts.csv")
    daily_views['Date'] = pd.to_datetime(daily_views['Date'])
    
    # Load exam period stats
    exam_stats = pd.read_csv(data_dir / "exam_period_stats.csv")
    
    return daily_views, exam_stats

def is_exam_period(date):
    """Check if a given date falls within exam periods."""
    EXAM_PERIODS = [
        ('2024-03-25', '2024-03-29'),
        ('2024-04-15', '2024-04-18'),
        ('2024-04-23', '2024-04-27'),
        ('2024-05-05', '2024-05-17'),
        ('2024-06-01', '2024-06-07'),
        ('2024-08-01', '2024-08-07'),
        ('2024-08-20', '2024-08-26'),
        ('2024-11-01', '2024-11-10'),
        ('2024-11-15', '2024-11-30'),
        ('2024-12-07', '2024-12-15'),
        ('2024-12-29', '2025-01-09')
    ]
    
    for start, end in EXAM_PERIODS:
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
        if start_date <= date <= end_date:
            return True
    return False

def mann_whitney_test(daily_views):
    """Perform Mann-Whitney U test on daily viewing counts."""
    # Add exam period flag to daily views
    daily_views['is_exam_period'] = daily_views['Date'].apply(is_exam_period)
    
    # Get viewing counts for exam and non-exam periods
    exam_views = daily_views[daily_views['is_exam_period']]['daily_views']
    non_exam_views = daily_views[~daily_views['is_exam_period']]['daily_views']
    
    # Perform Mann-Whitney U test
    statistic, p_value = stats.mannwhitneyu(
        exam_views, 
        non_exam_views,
        alternative='two-sided'
    )
    
    return {
        'test_name': "Mann-Whitney U Test",
        'statistic': statistic,
        'p_value': p_value,
        'exam_mean': exam_views.mean(),
        'non_exam_mean': non_exam_views.mean(),
        'exam_median': exam_views.median(),
        'non_exam_median': non_exam_views.median()
    }

def chi_square_test(exam_stats):
    """Perform Chi-square test on viewing frequencies."""
    # Extract values from exam_stats
    exam_views = exam_stats[exam_stats['is_exam_period']]['total_views'].iloc[0]
    non_exam_views = exam_stats[~exam_stats['is_exam_period']]['total_views'].iloc[0]
    exam_days = exam_stats[exam_stats['is_exam_period']]['unique_days'].iloc[0]
    non_exam_days = exam_stats[~exam_stats['is_exam_period']]['unique_days'].iloc[0]
    
    # Calculate expected frequencies (proportional to number of days)
    total_views = exam_views + non_exam_views
    total_days = exam_days + non_exam_days
    
    expected_exam = total_views * (exam_days / total_days)
    expected_non_exam = total_views * (non_exam_days / total_days)
    
    # Prepare observed and expected frequencies
    observed = np.array([exam_views, non_exam_views])
    expected = np.array([expected_exam, expected_non_exam])
    
    # Perform Chi-square test
    statistic, p_value = stats.chisquare(observed, expected)
    
    return {
        'test_name': "Chi-square Test",
        'statistic': statistic,
        'p_value': p_value,
        'observed': observed,
        'expected': expected,
        'exam_rate': exam_views / exam_days,
        'non_exam_rate': non_exam_views / non_exam_days
    }

def print_results(mann_whitney_results, chi_square_results):
    """Print the results of both statistical tests."""
    print("\nStatistical Test Results for Netflix Viewing Patterns")
    print("=" * 50)
    
    # Mann-Whitney U Test Results
    print("\n1. Mann-Whitney U Test Results")
    print("-" * 30)
    print(f"Testing if daily viewing counts differ between exam and non-exam periods")
    print(f"Statistic: {mann_whitney_results['statistic']:.4f}")
    print(f"P-value: {mann_whitney_results['p_value']:.4f}")
    print("\nDescriptive Statistics:")
    print(f"Exam Period - Mean: {mann_whitney_results['exam_mean']:.2f}, Median: {mann_whitney_results['exam_median']:.2f}")
    print(f"Non-exam Period - Mean: {mann_whitney_results['non_exam_mean']:.2f}, Median: {mann_whitney_results['non_exam_median']:.2f}")
    
    # Chi-square Test Results
    print("\n2. Chi-square Test Results")
    print("-" * 30)
    print(f"Testing if viewing frequency differs between exam and non-exam periods")
    print(f"Statistic: {chi_square_results['statistic']:.4f}")
    print(f"P-value: {chi_square_results['p_value']:.4f}")
    print("\nViewing Rates (views per day):")
    print(f"Exam Period: {chi_square_results['exam_rate']:.2f}")
    print(f"Non-exam Period: {chi_square_results['non_exam_rate']:.2f}")
    
    # Overall Conclusion
    print("\nConclusion")
    print("-" * 30)
    alpha = 0.05
    
    mw_significant = mann_whitney_results['p_value'] < alpha
    chi_significant = chi_square_results['p_value'] < alpha
    
    if mw_significant and chi_significant:
        print("Both tests show significant differences in viewing patterns during exam periods.")
    elif mw_significant:
        print("Daily viewing patterns show significant differences, but overall viewing frequency does not.")
    elif chi_significant:
        print("Overall viewing frequency shows significant differences, but daily patterns do not.")
    else:
        print("Neither test shows significant differences in viewing patterns during exam periods.")

def save_results_to_file(mann_whitney_results, chi_square_results, output_dir):
    """Save test results to a text file."""
    output_path = output_dir / "statistical_test_results.txt"
    
    with open(output_path, "w") as f:
        f.write("Statistical Test Results for Netflix Viewing Patterns\n")
        f.write("=" * 50 + "\n\n")
        
        # Mann-Whitney U Test Results
        f.write("1. Mann-Whitney U Test Results\n")
        f.write("-" * 30 + "\n")
        f.write(f"Testing if daily viewing counts differ between exam and non-exam periods\n")
        f.write(f"Statistic: {mann_whitney_results['statistic']:.4f}\n")
        f.write(f"P-value: {mann_whitney_results['p_value']:.4f}\n\n")
        f.write("Descriptive Statistics:\n")
        f.write(f"Exam Period - Mean: {mann_whitney_results['exam_mean']:.2f}, Median: {mann_whitney_results['exam_median']:.2f}\n")
        f.write(f"Non-exam Period - Mean: {mann_whitney_results['non_exam_mean']:.2f}, Median: {mann_whitney_results['non_exam_median']:.2f}\n\n")
        
        # Chi-square Test Results
        f.write("2. Chi-square Test Results\n")
        f.write("-" * 30 + "\n")
        f.write(f"Testing if viewing frequency differs between exam and non-exam periods\n")
        f.write(f"Statistic: {chi_square_results['statistic']:.4f}\n")
        f.write(f"P-value: {chi_square_results['p_value']:.4f}\n\n")
        f.write("Viewing Rates (views per day):\n")
        f.write(f"Exam Period: {chi_square_results['exam_rate']:.2f}\n")
        f.write(f"Non-exam Period: {chi_square_results['non_exam_rate']:.2f}\n\n")
        
        # Overall Conclusion
        f.write("Conclusion\n")
        f.write("-" * 30 + "\n")
        alpha = 0.05
        
        mw_significant = mann_whitney_results['p_value'] < alpha
        chi_significant = chi_square_results['p_value'] < alpha
        
        if mw_significant and chi_significant:
            f.write("Both tests show significant differences in viewing patterns during exam periods.\n")
        elif mw_significant:
            f.write("Daily viewing patterns show significant differences, but overall viewing frequency does not.\n")
        elif chi_significant:
            f.write("Overall viewing frequency shows significant differences, but daily patterns do not.\n")
        else:
            f.write("Neither test shows significant differences in viewing patterns during exam periods.\n")

def create_visualizations(daily_views, mann_whitney_results, chi_square_results, output_dir):
    """Create and save visualization plots for both statistical tests."""
    # 1. Mann-Whitney U Test Visualization - Box Plot
    plt.figure(figsize=(12, 6))
    
    # Create box plot
    plt.boxplot([
        daily_views[~daily_views['is_exam_period']]['daily_views'],
        daily_views[daily_views['is_exam_period']]['daily_views']
    ], labels=['Non-exam Period', 'Exam Period'])
    
    plt.title('Daily Viewing Counts: Exam vs Non-exam Periods\nMann-Whitney U Test', pad=20)
    plt.xlabel('Period Type')
    plt.ylabel('Number of Shows Watched per Day')
    
    # Add p-value annotation
    plt.annotate(f'p-value: {mann_whitney_results["p_value"]:.4f}',
                xy=(0.02, 0.95), xycoords='axes fraction',
                bbox=dict(facecolor='white', alpha=0.8))
    
    # Add means to the plot
    plt.axhline(y=mann_whitney_results['non_exam_mean'], color='b', linestyle='--', alpha=0.3)
    plt.axhline(y=mann_whitney_results['exam_mean'], color='r', linestyle='--', alpha=0.3)
    
    # Add legend for means
    plt.plot([], [], color='b', linestyle='--', alpha=0.3, label=f'Non-exam Mean: {mann_whitney_results["non_exam_mean"]:.2f}')
    plt.plot([], [], color='r', linestyle='--', alpha=0.3, label=f'Exam Mean: {mann_whitney_results["exam_mean"]:.2f}')
    plt.legend()
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "mann_whitney_visualization.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Chi-square Test Visualization - Bar Plot
    plt.figure(figsize=(12, 6))
    
    # Calculate daily rates
    exam_rate = chi_square_results['exam_rate']
    non_exam_rate = chi_square_results['non_exam_rate']
    
    # Data for plotting
    periods = ['Exam Period', 'Non-exam Period']
    rates = [exam_rate, non_exam_rate]
    
    # Create bars
    plt.bar(periods, rates, color=['skyblue', 'skyblue'])
    
    # Customize plot
    plt.title('Average Daily Views: Exam vs Non-exam Periods\nChi-square Test', pad=20)
    plt.xlabel('Period Type')
    plt.ylabel('Average Number of Views per Day')
    
    # Add value labels on bars
    for i, v in enumerate(rates):
        plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    
    # Add p-value annotation
    plt.annotate(f'p-value: {chi_square_results["p_value"]:.4f}',
                xy=(0.02, 0.95), xycoords='axes fraction',
                bbox=dict(facecolor='white', alpha=0.8))
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "chi_square_visualization.png", dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Main function to run the statistical tests."""
    # Load data
    daily_views, exam_stats = load_data()
    
    # Get output directory
    output_dir = Path(__file__).parent
    
    # Perform tests
    mann_whitney_results = mann_whitney_test(daily_views)
    chi_square_results = chi_square_test(exam_stats)
    
    # Print results
    print_results(mann_whitney_results, chi_square_results)
    
    # Save results to file
    save_results_to_file(mann_whitney_results, chi_square_results, output_dir)
    
    # Create and save visualization
    create_visualizations(daily_views, mann_whitney_results, chi_square_results, output_dir)
    
    print("\nResults have been saved to 'statistical_test_results.txt'")
    print("Visualization has been saved as 'mann_whitney_visualization.png'")

if __name__ == "__main__":
    main() 