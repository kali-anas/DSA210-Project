# Netflix Viewing Habits Analysis
## Project Overview
This project analyzes my Netflix viewing patterns during exam and non-exam periods in 2024. By examining viewing history data, the project extracts insights into my consumption habits during my busy academic periods and identifies potential correlations between viewing patterns and exam schedules.
## Main Research Question
How do exam periods affect Netflix viewing habits, specifically testing the null hypothesis that there is no significant difference in viewing patterns between exam and non-exam weeks?
## Hypothesis
- **Null Hypothesis (H0)**: There is no significant difference in the number of Netflix shows watched during exam weeks compared to non-exam weeks.
## Data Source
- **Dataset**: Netflix viewing history exported from Netflix account
- **Fields**:
  - Title: Name of shows/movies watched
  - Date: Viewing date
- **Derived Features**:
  - Show name, season, and episode information
  - Exam period flags
  - Time-based features (day of week, weekend status)
  - Viewing metrics (daily/weekly counts)
## Objectives
1. **Viewing Pattern Analysis**: 
   - Examine daily and weekly viewing patterns
   - Compare exam vs. non-exam period consumption
   - Analyze weekend vs. weekday viewing habits
2. **Time-Based Analysis**:
   - Identify peak viewing periods
   - Study day-of-week patterns
   - Track viewing trends throughout the semester
3. **Academic Impact Assessment**:
   - Evaluate changes in viewing habits during exam periods
   - Analyze potential correlations between exam schedules and entertainment consumption
## Methodology
1. **Data Processing**:
   - Clean and format Netflix viewing history
   - Extract show information and temporal features
   - Flag exam period entries
2. **Exploratory Data Analysis (EDA)**:
   - Visualize daily and weekly viewing patterns
   - Compare exam vs. non-exam period statistics
   - Analyze day-of-week and weekend patterns
3. **Statistical Analysis**:
   - Perform hypothesis testing
   - Calculate viewing metrics
   - Determine statistical significance of patterns
## Tools and Techniques
- **Data Processing**: Python (Pandas, NumPy)
- **Visualization**: Matplotlib
- **Statistical Analysis**: SciPy (for hypothesis testing)
- **Text Processing**: Regular expressions for title parsing
