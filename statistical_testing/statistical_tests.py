import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Define exam periods (same as in process_netflix_data.py)
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

def load_data():
    """Load the processed data files."""
    daily_counts = pd.read_csv('../data_processing/daily_viewing_counts.csv')
    daily_counts['Date'] = pd.to_datetime(daily_counts['Date'])
    
    dow_stats = pd.read_csv('../data_processing/day_of_week_stats.csv')
    
    return daily_counts, dow_stats

def is_exam_period(date):
    """Check if a date falls within exam periods."""
    for start, end in EXAM_PERIODS:
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
        if start_date <= date <= end_date:
            return True
    return False

def perform_t_test(daily_counts):
    """Perform independent t-test on daily viewing counts."""
    # Add exam period flag
    daily_counts['is_exam_period'] = daily_counts['Date'].apply(is_exam_period)
    
    # Get viewing counts for exam and non-exam periods
    exam_views = daily_counts[daily_counts['is_exam_period']]['daily_views']
    non_exam_views = daily_counts[~daily_counts['is_exam_period']]['daily_views']
    
    # Perform t-test
    t_stat, p_value = stats.ttest_ind(exam_views, non_exam_views)
    
    # Calculate effect size (Cohen's d)
    n1, n2 = len(exam_views), len(non_exam_views)
    var1, var2 = exam_views.var(), non_exam_views.var()
    pooled_se = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    cohens_d = (exam_views.mean() - non_exam_views.mean()) / pooled_se
    
    return {
        'test_type': 'Independent t-test',
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'exam_mean': exam_views.mean(),
        'non_exam_mean': non_exam_views.mean(),
        'exam_std': exam_views.std(),
        'non_exam_std': non_exam_views.std(),
        'exam_n': n1,
        'non_exam_n': n2
    }

def perform_chi_square_test(dow_stats):
    """Perform chi-square test on day of week viewing patterns."""
    # Create contingency table
    contingency = pd.pivot_table(
        dow_stats,
        values='views',
        index='is_exam_period',
        columns='day_of_week',
        fill_value=0
    )
    
    # Perform chi-square test
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
    
    return {
        'test_type': 'Chi-square test',
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'contingency_table': contingency
    }

def create_test_visualizations(daily_counts, t_test_results, chi_square_results):
    """Create visualizations for statistical tests."""
    # 1. Box plot of daily views by period
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=daily_counts, x='is_exam_period', y='daily_views')
    plt.title('Distribution of Daily Views: Exam vs Non-exam Periods')
    plt.xlabel('Exam Period')
    plt.ylabel('Number of Views per Day')
    plt.savefig('statistical_test_boxplot.png')
    plt.close()
    
    # 2. Bar plot of means with error bars
    plt.figure(figsize=(10, 6))
    means = [t_test_results['non_exam_mean'], t_test_results['exam_mean']]
    stds = [t_test_results['non_exam_std'], t_test_results['exam_std']]
    plt.bar(['Non-exam Period', 'Exam Period'], means, yerr=stds, capsize=5)
    plt.title('Mean Daily Views with Standard Deviation')
    plt.ylabel('Mean Number of Views per Day')
    plt.savefig('mean_comparison_plot.png')
    plt.close()

def save_results(t_test_results, chi_square_results):
    """Save test results to a text file."""
    with open('test_results.txt', 'w') as f:
        # T-test results
        f.write("=== Independent T-Test Results ===\n")
        f.write(f"Testing if there's a significant difference in daily viewing counts between exam and non-exam periods\n\n")
        f.write(f"T-statistic: {t_test_results['t_statistic']:.4f}\n")
        f.write(f"P-value: {t_test_results['p_value']:.4f}\n")
        f.write(f"Cohen's d: {t_test_results['cohens_d']:.4f}\n\n")
        
        f.write("Mean daily views:\n")
        f.write(f"- Exam periods: {t_test_results['exam_mean']:.2f} (SD: {t_test_results['exam_std']:.2f}, n={t_test_results['exam_n']})\n")
        f.write(f"- Non-exam periods: {t_test_results['non_exam_mean']:.2f} (SD: {t_test_results['non_exam_std']:.2f}, n={t_test_results['non_exam_n']})\n\n")
        
        # Chi-square results
        f.write("=== Chi-square Test Results ===\n")
        f.write(f"Testing if the distribution of viewing across days of the week differs between exam and non-exam periods\n\n")
        f.write(f"Chi-square statistic: {chi_square_results['chi2_statistic']:.4f}\n")
        f.write(f"P-value: {chi_square_results['p_value']:.4f}\n")
        f.write(f"Degrees of freedom: {chi_square_results['degrees_of_freedom']}\n\n")
        
        # Interpretation
        alpha = 0.05
        f.write("=== Interpretation ===\n")
        
        # T-test interpretation
        f.write("\nT-test (Daily viewing counts):\n")
        if t_test_results['p_value'] < alpha:
            f.write("- Reject the null hypothesis\n")
            f.write("- There is a significant difference in daily viewing counts between exam and non-exam periods\n")
        else:
            f.write("- Fail to reject the null hypothesis\n")
            f.write("- No significant difference in daily viewing counts between exam and non-exam periods\n")
        
        # Effect size interpretation
        d = abs(t_test_results['cohens_d'])
        if d < 0.2:
            effect = "negligible"
        elif d < 0.5:
            effect = "small"
        elif d < 0.8:
            effect = "medium"
        else:
            effect = "large"
        f.write(f"- The effect size is {effect} (Cohen's d = {d:.2f})\n")
        
        # Chi-square interpretation
        f.write("\nChi-square test (Day of week distribution):\n")
        if chi_square_results['p_value'] < alpha:
            f.write("- Reject the null hypothesis\n")
            f.write("- The distribution of viewing across days of the week is significantly different between exam and non-exam periods\n")
        else:
            f.write("- Fail to reject the null hypothesis\n")
            f.write("- No significant difference in the distribution of viewing across days of the week between exam and non-exam periods\n")

def main():
    """Main function to run all statistical tests."""
    print("Loading data...")
    daily_counts, dow_stats = load_data()
    
    print("Performing t-test...")
    t_test_results = perform_t_test(daily_counts)
    
    print("Performing chi-square test...")
    chi_square_results = perform_chi_square_test(dow_stats)
    
    print("Creating visualizations...")
    create_test_visualizations(daily_counts, t_test_results, chi_square_results)
    
    print("Saving results...")
    save_results(t_test_results, chi_square_results)
    
    print("Statistical testing completed!")

if __name__ == "__main__":
    main() 