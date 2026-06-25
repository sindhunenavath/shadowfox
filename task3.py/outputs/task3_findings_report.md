# Task 3 Advanced Data Analysis Project

## Dataset Selected

Dataset: scikit-learn Diabetes dataset.

This public dataset contains 442 patient records and 10 baseline medical variables. The target variable is a quantitative measure of diabetes disease progression one year after the baseline measurements.

## Research Question

Which baseline health factors are most strongly associated with diabetes disease progression?

## Data Cleaning and Exploration Output

- Rows: 442
- Columns: 11
- Duplicate rows found: 0
- Missing values found: 0

### Missing Values by Column

| index | 0 |
| --- | --- |
| age | 0 |
| sex_standardized | 0 |
| body_mass_index | 0 |
| blood_pressure | 0 |
| total_serum_cholesterol | 0 |
| low_density_lipoproteins | 0 |
| high_density_lipoproteins | 0 |
| total_cholesterol_hdl_ratio | 0 |
| log_serum_triglycerides | 0 |
| blood_sugar_level | 0 |
| disease_progression | 0 |

### Summary Statistics

| index | age | sex_standardized | body_mass_index | blood_pressure | total_serum_cholesterol | low_density_lipoproteins | high_density_lipoproteins | total_cholesterol_hdl_ratio | log_serum_triglycerides | blood_sugar_level | disease_progression |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count | 442.0 | 442.0 | 442.0 | 442.0 | 442.0 | 442.0 | 442.0 | 442.0 | 442.0 | 442.0 | 442.0 |
| mean | -0.0 | 0.0 | -0.0 | -0.0 | -0.0 | 0.0 | -0.0 | -0.0 | 0.0 | 0.0 | 152.133 |
| std | 0.048 | 0.048 | 0.048 | 0.048 | 0.048 | 0.048 | 0.048 | 0.048 | 0.048 | 0.048 | 77.093 |
| min | -0.107 | -0.045 | -0.09 | -0.112 | -0.127 | -0.116 | -0.102 | -0.076 | -0.126 | -0.138 | 25.0 |
| 25% | -0.037 | -0.045 | -0.034 | -0.037 | -0.034 | -0.03 | -0.035 | -0.039 | -0.033 | -0.033 | 87.0 |
| 50% | 0.005 | -0.045 | -0.007 | -0.006 | -0.004 | -0.004 | -0.007 | -0.003 | -0.002 | -0.001 | 140.5 |
| 75% | 0.038 | 0.051 | 0.031 | 0.036 | 0.028 | 0.03 | 0.029 | 0.034 | 0.032 | 0.028 | 211.5 |
| max | 0.111 | 0.051 | 0.171 | 0.132 | 0.154 | 0.199 | 0.181 | 0.185 | 0.134 | 0.136 | 346.0 |

## Key Correlation Findings

The five strongest absolute correlations with disease progression are:

| index | disease_progression |
| --- | --- |
| body_mass_index | 0.586 |
| log_serum_triglycerides | 0.566 |
| blood_pressure | 0.441 |
| total_cholesterol_hdl_ratio | 0.43 |
| high_density_lipoproteins | 0.395 |

## Regression Model Output

- R-squared on test data: 0.485
- Mean absolute error on test data: 41.55

### Most Influential Regression Coefficients

| feature | coefficient |
| --- | --- |
| total_serum_cholesterol | -918.503 |
| log_serum_triglycerides | 695.808 |
| body_mass_index | 531.971 |
| low_density_lipoproteins | 508.258 |
| blood_pressure | 381.563 |
| total_cholesterol_hdl_ratio | 269.492 |
| sex_standardized | -241.991 |
| high_density_lipoproteins | 116.95 |

## Visualizations

1. Correlation heatmap: `01_correlation_heatmap.png`
2. BMI regression plot: `02_bmi_vs_progression.png`
3. Disease progression by age group: `03_progression_by_age_group.png`
4. Regression coefficients: `04_regression_coefficients.png`

## Final Findings

Body mass index, serum triglycerides, blood pressure, and cholesterol-related measurements show meaningful relationships with diabetes progression. The visualizations show that higher body mass index tends to align with higher progression scores, while the regression coefficient chart suggests that several metabolic indicators contribute to predicting the target variable. Age alone is less visually decisive than the metabolic factors, which means the research question is better answered by comparing multiple baseline health measurements rather than relying on age groups only.

## Conclusion

The analysis suggests that diabetes progression is associated most strongly with metabolic and cardiovascular indicators, especially body mass index and blood-serum measurements. These findings support the idea that patient monitoring should consider several health variables together instead of using a single measurement.
