import pandas as pd
import numpy as np
from datetime import datetime
import re
import matplotlib.pyplot as plt

# Define exam periods
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

def extract_show_info(title):
    """Extract show name, season, and episode from title."""
    # Pattern for "Show Name: Season X: Episode Name" or "Show Name: Season X: Episode Y"
    pattern = r"^(.*?)(?:: Season (\d+))?(?:: (Episode \d+|.*?))?$"
    match = re.match(pattern, title)
    
    if match:
        show_name = match.group(1).strip()
        season = match.group(2) if match.group(2) else None
        episode = match.group(3) if match.group(3) else None
        return show_name, season, episode
    return title, None, None

def load_data(file_path):
    """Load Netflix viewing history data."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Clean the dataframe and convert dates."""
    # Convert date strings to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    
    # Filter for year 2024 only
    df = df[df['Date'].dt.year == 2024].copy()
    
    # Extract show information
    show_info = df['Title'].apply(extract_show_info)
    df['show_name'] = [x[0] for x in show_info]
    df['season'] = [x[1] for x in show_info]
    df['episode'] = [x[2] for x in show_info]
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Reset index
    df = df.reset_index(drop=True)
    
    print(f"Total entries for 2024: {len(df)}")
    
    return df

def add_exam_period_flag(df):
    """Add a flag for whether each viewing date was during an exam period."""
    def is_exam_period(date):
        for start, end in EXAM_PERIODS:
            start_date = pd.to_datetime(start)
            end_date = pd.to_datetime(end)
            if start_date <= date <= end_date:
                return True
        return False
    
    df['is_exam_period'] = df['Date'].apply(is_exam_period)
    return df

def add_time_features(df):
    """Add time-based features."""
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['day_of_week'] = df['Date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6])  # 5=Saturday, 6=Sunday
    df['week_number'] = df['Date'].dt.isocalendar().week
    
    return df

def calculate_viewing_metrics(df):
    """Calculate viewing metrics by different time periods."""
    # Daily viewing counts
    daily_counts = df.groupby('Date').agg({
        'Title': 'count',  # Number of shows watched
        'show_name': 'nunique'  # Number of unique shows
    }).reset_index()
    daily_counts.columns = ['Date', 'daily_views', 'unique_shows']
    
    # Weekly viewing counts
    weekly_counts = df.groupby(['year', 'week_number']).size().reset_index(name='weekly_views')
    
    # Exam period vs non-exam period stats
    exam_period_stats = df.groupby('is_exam_period').agg({
        'Title': 'count',
        'show_name': 'nunique',
        'Date': 'nunique'
    }).reset_index()
    exam_period_stats.columns = ['is_exam_period', 'total_views', 'unique_shows', 'unique_days']
    
    # Viewing patterns by day of week
    dow_stats = df.groupby(['is_exam_period', 'day_of_week']).size().reset_index(name='views')
    
    # Weekend vs Weekday stats
    weekend_stats = df.groupby(['is_exam_period', 'is_weekend']).size().reset_index(name='views')
    
    return daily_counts, weekly_counts, exam_period_stats, dow_stats, weekend_stats

def calculate_binge_watching_metrics(df):
    """Calculate binge-watching related metrics."""
    # Define binge watching as 3 or more episodes of the same show in a day
    daily_show_counts = df.groupby(['Date', 'show_name']).size().reset_index(name='episodes_watched')
    binge_sessions = daily_show_counts[daily_show_counts['episodes_watched'] >= 3]
    
    # Binge watching during exam vs non-exam periods
    df_with_binge = df.merge(binge_sessions[['Date', 'show_name']], on=['Date', 'show_name'], how='left')
    df_with_binge['is_binge_watching'] = ~df_with_binge['episodes_watched'].isna()
    
    binge_stats = df_with_binge.groupby('is_exam_period')['is_binge_watching'].agg(['sum', 'count']).reset_index()
    binge_stats['binge_watching_ratio'] = binge_stats['sum'] / binge_stats['count']
    
    return binge_stats

def create_visualizations(df, daily_counts, weekly_counts, exam_period_stats, dow_stats, weekend_stats, output_dir):
    """Create and save visualization plots."""
    # 1. Daily viewing pattern
    plt.figure(figsize=(15, 6))
    plt.plot(daily_counts['Date'], daily_counts['daily_views'], marker='o')
    plt.title('Daily Netflix Viewing Pattern (2024)')
    plt.xlabel('Date')
    plt.ylabel('Number of Episodes/Movies Watched')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/daily_pattern.png")
    plt.close()

    # 2. Exam vs Non-exam Period Comparison
    plt.figure(figsize=(10, 6))
    plt.bar(exam_period_stats['is_exam_period'].astype(str), exam_period_stats['total_views'])
    plt.title('Viewing During Exam vs Non-exam Periods')
    plt.xlabel('Exam Period')
    plt.ylabel('Total Views')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/exam_comparison.png")
    plt.close()

    # 3. Day of Week Pattern
    plt.figure(figsize=(12, 6))
    for is_exam in [False, True]:
        data = dow_stats[dow_stats['is_exam_period'] == is_exam]
        label = 'Exam Period' if is_exam else 'Non-exam Period'
        plt.bar(data['day_of_week'] + (0.4 if is_exam else 0), data['views'], 
               width=0.4, label=label)
    plt.title('Viewing Pattern by Day of Week')
    plt.xlabel('Day of Week (0=Monday, 6=Sunday)')
    plt.ylabel('Number of Views')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/day_of_week_pattern.png")
    plt.close()

    # 4. Weekend vs Weekday
    plt.figure(figsize=(10, 6))
    for is_exam in [False, True]:
        data = weekend_stats[weekend_stats['is_exam_period'] == is_exam]
        label = 'Exam Period' if is_exam else 'Non-exam Period'
        plt.bar(data['is_weekend'].astype(str) + (' (Exam)' if is_exam else ' (Non-exam)'), 
               data['views'], label=label)
    plt.title('Weekend vs Weekday Viewing Pattern')
    plt.xlabel('Is Weekend')
    plt.ylabel('Number of Views')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/weekend_pattern.png")
    plt.close()

    # 5. Weekly Viewing Pattern
    plt.figure(figsize=(15, 6))
    plt.plot(weekly_counts['week_number'], weekly_counts['weekly_views'], marker='o')
    plt.title('Weekly Netflix Viewing Pattern (2024)')
    plt.xlabel('Week Number')
    plt.ylabel('Number of Episodes/Movies Watched')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/weekly_pattern.png")
    plt.close()

def process_netflix_data(input_file, output_dir):
    """Main function to process Netflix viewing history."""
    # Load data
    print("Loading data...")
    df = load_data(input_file)
    
    # Clean data
    print("Cleaning data...")
    df = clean_data(df)
    
    # Add exam period flag
    print("Adding exam period flags...")
    df = add_exam_period_flag(df)
    
    # Add time features
    print("Adding time features...")
    df = add_time_features(df)
    
    # Calculate viewing metrics
    print("Calculating viewing metrics...")
    daily_counts, weekly_counts, exam_period_stats, dow_stats, weekend_stats = calculate_viewing_metrics(df)
    
    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(df, daily_counts, weekly_counts, exam_period_stats, dow_stats, weekend_stats, output_dir)
    
    # Save processed data
    print("Saving processed data...")
    df.to_csv(f"{output_dir}/processed_netflix_data.csv", index=False)
    daily_counts.to_csv(f"{output_dir}/daily_viewing_counts.csv", index=False)
    weekly_counts.to_csv(f"{output_dir}/weekly_viewing_counts.csv", index=False)
    exam_period_stats.to_csv(f"{output_dir}/exam_period_stats.csv", index=False)
    dow_stats.to_csv(f"{output_dir}/day_of_week_stats.csv", index=False)
    weekend_stats.to_csv(f"{output_dir}/weekend_stats.csv", index=False)
    
    print("Data processing and visualization completed!")
    return df, daily_counts, weekly_counts, exam_period_stats, dow_stats, weekend_stats

if __name__ == "__main__":
    input_file = "../NetflixViewingHistory (1).csv"
    output_dir = "."  # Current directory (data_processing)
    
    # Process the data and create visualizations
    results = process_netflix_data(input_file, output_dir) 