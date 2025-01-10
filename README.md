# Netflix Viewing Habits Analysis

## Project Overview
This project analyzes my Netflix viewing patterns during exam and non-exam periods in 2024. By examining viewing history data, the project extracts insights into my consumption habits during busy academic periods and identifies potential correlations between viewing patterns and exam schedules.

---

## Main Research Question
How do exam periods affect Netflix viewing habits, specifically testing the null hypothesis that there is no significant difference in viewing patterns between exam and non-exam weeks?

---

## Data Source
**Dataset:** Netflix viewing history exported from my Netflix account.

**Fields:**
- **Title:** Name of shows/movies watched.
- **Date:** Viewing date.

**Derived Features:**
- Show name, season, and episode information.
- Exam period flags.
- Time-based features (day of week, weekend status).
- Viewing metrics (daily/weekly counts).

---

## Objectives
1. **Viewing Pattern Analysis:**
   - Examine daily and weekly viewing patterns.
   - Compare exam vs. non-exam period consumption.
   - Analyze weekend vs. weekday viewing habits.

2. **Time-Based Analysis:**
   - Identify peak viewing periods.
   - Study day-of-week patterns.
   - Track viewing trends throughout the semester.

3. **Academic Impact Assessment:**
   - Evaluate changes in viewing habits during exam periods.
   - Analyze potential correlations between exam schedules and entertainment consumption.

---

## Data Analysis Section (Based on Data Processing)
This section highlights the insights derived from the **data_processing** folder, focusing on the trends and correlations observed during initial data cleaning and exploratory data analysis (EDA).

### 1. Viewing Patterns and Correlations
- The analysis revealed a **clear difference in Netflix viewing habits** between exam and non-exam periods:
  - **Non-Exam Periods:** Viewing activity was significantly higher, with consistent spikes in weekly and daily counts.
  - **Exam Periods:** Activity declined noticeably, with fewer episodes/movies watched during these weeks.

- **Skewed Correlation:**
  - There are **fewer exam periods** compared to non-exam periods in the dataset.
  - This discrepancy **skewed the perception** of the significance of the difference.

- **Adjustment:** Normalized counts and additional metrics were calculated to better represent viewing behavior across the two periods.

### 2. Weekly Viewing Patterns
- Weekly viewing trends demonstrated distinct peaks during non-exam periods:
  - Weeks **immediately after exams** showed sharp increases in viewing, suggesting binge-watching tendencies.
  - During exam weeks, viewing patterns flattened, with a significant reduction in weekly totals.

- **Visualization:** The weekly trend line highlights this fluctuation, with troughs aligning closely with exam schedules.

### 3. Daily Patterns
- **Daily Viewing Trends:**
  - During non-exam periods, viewing was typically higher on weekends, reflecting leisure time preferences.
  - Exam periods displayed more uniform but lower daily viewing counts, suggesting that academic obligations limited viewing.

- **Weekend Effect:** Non-exam weekends showed significantly higher activity compared to weekdays. Exam periods, however, neutralized this effect, with consistent low activity across all days.

### 4. Exam vs. Non-Exam Period Analysis
- By flagging entries based on exam periods:
  - A **sharp drop** in total viewing activity was evident during exams.
  - These findings emphasize the role of academic pressure in suppressing entertainment consumption.

- **Limitations Identified:** The imbalance in the dataset (more non-exam weeks than exam weeks) necessitated careful interpretation of these results. While the difference is statistically evident, its magnitude requires context.

### 5. Follow-Up Testing
- Due to the identified limitations, two additional statistical tests were performed:
  - **Mann-Whitney U Test:** To compare the distributions of viewing counts during exam and non-exam periods.
  - **Chi-Square Test:** To analyze the relationship between exam periods and viewing frequency.

---

## Hypothesis Testing Section (Based on Hypothesis Testing Folder)
This section provides detailed insights into the statistical analysis performed to evaluate differences in Netflix viewing patterns during exam and non-exam periods.

### 1. Mann-Whitney U Test
- **Objective:** To test if daily viewing counts differ significantly between exam and non-exam periods.
- **Methodology:**
  - Daily viewing counts were grouped into exam and non-exam periods.
  - The Mann-Whitney U test, a non-parametric test suitable for non-normally distributed data, was applied to compare the two groups.
- **Results:**
  - **Test Statistic:** 1134.0000
  - **P-value:** 0.5505
  - **Descriptive Statistics:**
    - Exam Period: **Mean = 1.45**, **Median = 1.00**
    - Non-exam Period: **Mean = 1.63**, **Median = 1.00**
- **Interpretation:**
  - The p-value is greater than the significance level of 0.05, indicating no statistically significant difference in daily viewing counts between exam and non-exam periods.
  - While the mean viewing count is slightly lower during exam periods, the distributions largely overlap, as shown in the boxplot visualization.

### 2. Chi-Square Test
- **Objective:** To evaluate if the overall viewing frequency differs significantly between exam and non-exam periods.
- **Methodology:**
  - Total viewing counts were compared between exam and non-exam periods, normalized by the number of days in each period.
  - The Chi-square test assessed whether observed viewing counts significantly deviated from expected counts based on the duration of each period.
- **Results:**
  - **Test Statistic:** 0.3555
  - **P-value:** 0.5510
  - **Viewing Rates:**
    - Exam Period: **1.45 views/day**
    - Non-exam Period: **1.63 views/day**
- **Interpretation:**
  - The p-value exceeds the 0.05 threshold, suggesting no significant differences in viewing frequency between the two periods.
  - The similarity in rates per day confirms that the slight reduction during exam periods is not statistically significant.

### 3. Conclusion
- Both tests indicate that differences in Netflix viewing patterns during exam and non-exam periods are **not statistically significant**.
- Despite observable trends in the data (e.g., lower viewing activity during exams), these differences do not reach the level of statistical significance under rigorous testing.
- The visualizations provide further clarity, highlighting the overlapping distributions and comparable viewing rates between the two periods.

---

## Findings
- The **data_processing folder** revealed a strong initial correlation between exam weeks and lower viewing counts. This trend was evident in the weekly and daily viewing patterns, with exam periods showing notable drops in activity compared to non-exam periods.
- Upon further investigation, it became apparent that this correlation was influenced by the **imbalance** in the number of exam and non-exam periods. With fewer exam weeks overall, the data initially skewed perceptions of significance.
- After rigorous hypothesis testing, the **null hypothesis could not be rejected**, as neither the Mann-Whitney U test nor the Chi-Square test showed statistically significant differences between the two periods. This underscores the importance of statistical validation in interpreting trends.

---

## Limitations and Future Work
### Limitations:
- **Imbalanced Dataset:** The dataset contained more non-exam periods than exam periods, which influenced the initial analysis and required normalization for accurate comparisons.
- **Subjectivity in Exam Period Definition:** The manual identification of exam periods may not fully capture all academic pressures affecting viewing habits.
- **Single-User Data:** This study is based on a single individual’s viewing history, which limits the generalizability of findings to broader populations.

### Future Work:
- **Multi-User Analysis:** Expanding the analysis to include viewing histories from multiple users could provide more generalizable insights.
- **Additional Features:** Incorporating contextual data (e.g., academic workload, external commitments) could enhance understanding of viewing behavior.
- **Longitudinal Study:** Extending the analysis to multiple years would allow for the identification of recurring patterns and more robust conclusions.

