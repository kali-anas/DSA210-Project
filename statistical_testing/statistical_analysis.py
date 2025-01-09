import pandas as pd
import numpy as np
from scipy import stats
import os
from datetime import datetime

def is_exam_period(date):
    """Check if a given date falls within exam periods."""
    exam_periods = [
        ('2024-01-08', '2024-01-19'),  # First exam period
        ('2024-05-13', '2024-05-24'),  # Second exam period
        ('2024-08-26', '2024-09-06'),  # Third exam period
        ('2024-12-16', '2024-12-27')   # Fourth exam period
    ]
    
    date = pd.to_datetime(date)
    for start, end in exam_periods:
        if pd.to_datetime(start) <= date <= pd.to_datetime(end):
            return True
    return False

def load_processed_data():
    """Load the processed data files from the data_processing directory."""
    try:
        # Get the absolute path to data_processing directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), "data_processing")
        
        # Load daily viewing counts and add exam period flag
        daily_counts = pd.read_csv(os.path.join(data_dir, "daily_viewing_counts.csv"))
        daily_counts['Date'] = pd.to_datetime(daily_counts['Date'])
        daily_counts['is_exam_period'] = daily_counts['Date'].apply(is_exam_period)
        
        # Load other files
        weekly_counts = pd.read_csv(os.path.join(data_dir, "weekly_viewing_counts.csv"))
        
        # Add weekend flag to daily counts
        daily_counts['is_weekend'] = daily_counts['Date'].dt.dayofweek.isin([5, 6])
        
        return daily_counts, weekly_counts
        
    except FileNotFoundError as e:
        print(f"Error: Could not find one or more required data files in {data_dir}")
        print("Please make sure all required CSV files are present in the data_processing directory")
        raise e

def perform_ttest_exam_periods(daily_counts):
    """Perform t-test to compare viewing habits during exam vs non-exam periods."""
    exam_views = daily_counts[daily_counts['is_exam_period']]['daily_views']
    non_exam_views = daily_counts[~daily_counts['is_exam_period']]['daily_views']
    
    if len(exam_views) == 0 or len(non_exam_views) == 0:
        return {
            't_statistic': np.nan,
            'p_value': np.nan,
            'cohens_d': np.nan,
            'exam_mean': np.mean(exam_views) if len(exam_views) > 0 else 0,
            'non_exam_mean': np.mean(non_exam_views) if len(non_exam_views) > 0 else 0,
            'exam_std': np.std(exam_views) if len(exam_views) > 0 else 0,
            'non_exam_std': np.std(non_exam_views) if len(non_exam_views) > 0 else 0,
            'exam_days': len(exam_views),
            'non_exam_days': len(non_exam_views)
        }
    
    t_stat, p_value = stats.ttest_ind(exam_views, non_exam_views)
    
    # Calculate effect size (Cohen's d)
    n1, n2 = len(exam_views), len(non_exam_views)
    var1, var2 = np.var(exam_views, ddof=1), np.var(non_exam_views, ddof=1)
    pooled_se = np.sqrt((var1*(n1-1) + var2*(n2-1)) / (n1+n2-2))
    cohens_d = (np.mean(exam_views) - np.mean(non_exam_views)) / pooled_se if pooled_se != 0 else 0
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'exam_mean': np.mean(exam_views),
        'non_exam_mean': np.mean(non_exam_views),
        'exam_std': np.std(exam_views),
        'non_exam_std': np.std(non_exam_views),
        'exam_days': n1,
        'non_exam_days': n2
    }

def analyze_weekly_patterns(weekly_counts):
    """Analyze weekly viewing patterns and trends."""
    weekly_counts['week_number'] = pd.to_numeric(weekly_counts['week_number'])
    weekly_counts['weekly_views'] = pd.to_numeric(weekly_counts['weekly_views'])
    
    correlation = stats.pearsonr(weekly_counts['week_number'], weekly_counts['weekly_views'])
    weekly_stats = {
        'correlation_coef': correlation[0],
        'correlation_p_value': correlation[1],
        'mean_weekly_views': np.mean(weekly_counts['weekly_views']),
        'std_weekly_views': np.std(weekly_counts['weekly_views']),
        'max_week': weekly_counts.loc[weekly_counts['weekly_views'].idxmax(), 'week_number'],
        'min_week': weekly_counts.loc[weekly_counts['weekly_views'].idxmin(), 'week_number']
    }
    return weekly_stats

def analyze_weekend_effect(daily_counts):
    """Analyze the difference between weekend and weekday viewing."""
    weekend_views = daily_counts[daily_counts['is_weekend']]['daily_views']
    weekday_views = daily_counts[~daily_counts['is_weekend']]['daily_views']
    
    t_stat, p_value = stats.ttest_ind(weekend_views, weekday_views)
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'weekend_mean': np.mean(weekend_views),
        'weekday_mean': np.mean(weekday_views),
        'weekend_days': len(weekend_views),
        'weekday_days': len(weekday_views)
    }

def save_results(results, output_dir=None):
    """Save statistical analysis results to a text file."""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    
    output_file = os.path.join(output_dir, "statistical_results.txt")
    
    with open(output_file, 'w') as f:
        # Exam Period Analysis
        f.write("NETFLIX VIEWING HABITS STATISTICAL ANALYSIS\n")
        f.write("========================================\n\n")
        
        f.write("1. Exam vs Non-Exam Period Analysis\n")
        f.write("---------------------------------\n")
        f.write(f"Number of exam period days: {results['exam_period']['exam_days']}\n")
        f.write(f"Number of non-exam period days: {results['exam_period']['non_exam_days']}\n")
        f.write(f"T-statistic: {results['exam_period']['t_statistic']:.4f}\n")
        f.write(f"P-value: {results['exam_period']['p_value']:.4f}\n")
        f.write(f"Effect size (Cohen's d): {results['exam_period']['cohens_d']:.4f}\n")
        f.write(f"Mean daily views during exam periods: {results['exam_period']['exam_mean']:.2f}\n")
        f.write(f"Mean daily views during non-exam periods: {results['exam_period']['non_exam_mean']:.2f}\n")
        f.write(f"Standard deviation during exam periods: {results['exam_period']['exam_std']:.2f}\n")
        f.write(f"Standard deviation during non-exam periods: {results['exam_period']['non_exam_std']:.2f}\n\n")
        
        # Weekly Pattern Analysis
        f.write("2. Weekly Pattern Analysis\n")
        f.write("-------------------------\n")
        f.write(f"Correlation coefficient: {results['weekly_pattern']['correlation_coef']:.4f}\n")
        f.write(f"Correlation p-value: {results['weekly_pattern']['correlation_p_value']:.4f}\n")
        f.write(f"Mean weekly views: {results['weekly_pattern']['mean_weekly_views']:.2f}\n")
        f.write(f"Standard deviation of weekly views: {results['weekly_pattern']['std_weekly_views']:.2f}\n")
        f.write(f"Week with maximum views: Week {results['weekly_pattern']['max_week']}\n")
        f.write(f"Week with minimum views: Week {results['weekly_pattern']['min_week']}\n\n")
        
        # Weekend Effect Analysis
        f.write("3. Weekend vs Weekday Analysis\n")
        f.write("-----------------------------\n")
        f.write(f"Number of weekend days: {results['weekend_effect']['weekend_days']}\n")
        f.write(f"Number of weekday days: {results['weekend_effect']['weekday_days']}\n")
        f.write(f"T-statistic: {results['weekend_effect']['t_statistic']:.4f}\n")
        f.write(f"P-value: {results['weekend_effect']['p_value']:.4f}\n")
        f.write(f"Mean weekend views: {results['weekend_effect']['weekend_mean']:.2f}\n")
        f.write(f"Mean weekday views: {results['weekend_effect']['weekday_mean']:.2f}\n")

def main():
    try:
        print("Loading processed data...")
        daily_counts, weekly_counts = load_processed_data()
        
        print("Performing statistical tests...")
        results = {
            'exam_period': perform_ttest_exam_periods(daily_counts),
            'weekly_pattern': analyze_weekly_patterns(weekly_counts),
            'weekend_effect': analyze_weekend_effect(daily_counts)
        }
        
        print("Saving results...")
        save_results(results)
        print("Statistical analysis completed! Results saved to statistical_results.txt")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please make sure all required files exist and are accessible.")

if __name__ == "__main__":
    main() 