import os
import tempfile
from pathlib import Path

MPL_CONFIG_DIR = Path(tempfile.gettempdir()) / "task3_matplotlib_cache"
MPL_CONFIG_DIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG_DIR))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.figsize"] = (10, 6)


def markdown_table(data, include_index=True):
    if isinstance(data, pd.Series):
        table = data.to_frame()
    else:
        table = data.copy()

    if include_index:
        table = table.reset_index()

    table = table.astype(str)
    headers = [str(column) for column in table.columns]
    rows = table.values.tolist()
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, separator_line, *row_lines])


def load_and_prepare_data():
    dataset = load_diabetes(as_frame=True)
    df = dataset.frame.copy()
    df = df.rename(
        columns={
            "sex": "sex_standardized",
            "bmi": "body_mass_index",
            "bp": "blood_pressure",
            "s1": "total_serum_cholesterol",
            "s2": "low_density_lipoproteins",
            "s3": "high_density_lipoproteins",
            "s4": "total_cholesterol_hdl_ratio",
            "s5": "log_serum_triglycerides",
            "s6": "blood_sugar_level",
            "target": "disease_progression",
        }
    )
    df.to_csv(OUTPUT_DIR / "diabetes_dataset_clean.csv", index=False)
    return df


def create_visualizations(df):
    chart_paths = {}

    corr = df.corr(numeric_only=True)
    plt.figure(figsize=(12, 9))
    sns.heatmap(corr, cmap="vlag", center=0, annot=False, linewidths=0.5)
    plt.title("Correlation Heatmap: Diabetes Variables and Disease Progression")
    plt.tight_layout()
    chart_paths["correlation_heatmap"] = OUTPUT_DIR / "01_correlation_heatmap.png"
    plt.savefig(chart_paths["correlation_heatmap"], dpi=160)
    plt.close()

    plt.figure()
    sns.regplot(
        data=df,
        x="body_mass_index",
        y="disease_progression",
        scatter_kws={"alpha": 0.65},
        line_kws={"color": "#D1495B", "linewidth": 2},
    )
    plt.title("Body Mass Index vs Disease Progression")
    plt.xlabel("Body Mass Index (standardized)")
    plt.ylabel("Disease Progression Score")
    plt.tight_layout()
    chart_paths["bmi_regression"] = OUTPUT_DIR / "02_bmi_vs_progression.png"
    plt.savefig(chart_paths["bmi_regression"], dpi=160)
    plt.close()

    df_with_groups = df.copy()
    df_with_groups["age_group"] = pd.qcut(
        df_with_groups["age"], q=4, labels=["youngest", "lower-middle", "upper-middle", "oldest"]
    )
    plt.figure()
    sns.boxplot(data=df_with_groups, x="age_group", y="disease_progression")
    plt.title("Disease Progression Distribution by Age Group")
    plt.xlabel("Age Group Based on Quartiles")
    plt.ylabel("Disease Progression Score")
    plt.tight_layout()
    chart_paths["age_boxplot"] = OUTPUT_DIR / "03_progression_by_age_group.png"
    plt.savefig(chart_paths["age_boxplot"], dpi=160)
    plt.close()

    feature_cols = [col for col in df.columns if col != "disease_progression"]
    X = df[feature_cols]
    y = df["disease_progression"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    coefficients = (
        pd.DataFrame({"feature": feature_cols, "coefficient": model.coef_})
        .assign(abs_coefficient=lambda data: data["coefficient"].abs())
        .sort_values("abs_coefficient", ascending=False)
    )

    plt.figure(figsize=(10, 7))
    sns.barplot(data=coefficients, x="coefficient", y="feature", hue="feature", legend=False)
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Linear Regression Coefficients for Disease Progression")
    plt.xlabel("Coefficient Value")
    plt.ylabel("Feature")
    plt.tight_layout()
    chart_paths["coefficients"] = OUTPUT_DIR / "04_regression_coefficients.png"
    plt.savefig(chart_paths["coefficients"], dpi=160)
    plt.close()

    model_metrics = {
        "r2_score": r2_score(y_test, predictions),
        "mean_absolute_error": mean_absolute_error(y_test, predictions),
    }
    return chart_paths, coefficients, model_metrics


def build_report(df, chart_paths, coefficients, model_metrics):
    missing = df.isna().sum()
    duplicated_rows = int(df.duplicated().sum())
    target_corr = df.corr(numeric_only=True)["disease_progression"].drop("disease_progression")
    top_corr = target_corr.abs().sort_values(ascending=False).head(5)

    summary_stats = df.describe().round(3)

    report = f"""# Task 3 Advanced Data Analysis Project

## Dataset Selected

Dataset: scikit-learn Diabetes dataset.

This public dataset contains 442 patient records and 10 baseline medical variables. The target variable is a quantitative measure of diabetes disease progression one year after the baseline measurements.

## Research Question

Which baseline health factors are most strongly associated with diabetes disease progression?

## Data Cleaning and Exploration Output

- Rows: {df.shape[0]}
- Columns: {df.shape[1]}
- Duplicate rows found: {duplicated_rows}
- Missing values found: {int(missing.sum())}

### Missing Values by Column

{markdown_table(missing)}

### Summary Statistics

{markdown_table(summary_stats)}

## Key Correlation Findings

The five strongest absolute correlations with disease progression are:

{markdown_table(top_corr.round(3))}

## Regression Model Output

- R-squared on test data: {model_metrics["r2_score"]:.3f}
- Mean absolute error on test data: {model_metrics["mean_absolute_error"]:.2f}

### Most Influential Regression Coefficients

{markdown_table(coefficients[["feature", "coefficient"]].head(8).round(3), include_index=False)}

## Visualizations

1. Correlation heatmap: `{chart_paths["correlation_heatmap"].name}`
2. BMI regression plot: `{chart_paths["bmi_regression"].name}`
3. Disease progression by age group: `{chart_paths["age_boxplot"].name}`
4. Regression coefficients: `{chart_paths["coefficients"].name}`

## Final Findings

Body mass index, serum triglycerides, blood pressure, and cholesterol-related measurements show meaningful relationships with diabetes progression. The visualizations show that higher body mass index tends to align with higher progression scores, while the regression coefficient chart suggests that several metabolic indicators contribute to predicting the target variable. Age alone is less visually decisive than the metabolic factors, which means the research question is better answered by comparing multiple baseline health measurements rather than relying on age groups only.

## Conclusion

The analysis suggests that diabetes progression is associated most strongly with metabolic and cardiovascular indicators, especially body mass index and blood-serum measurements. These findings support the idea that patient monitoring should consider several health variables together instead of using a single measurement.
"""
    report_path = OUTPUT_DIR / "task3_findings_report.md"
    report_path.write_text(report, encoding="utf-8")
    return report_path, top_corr


def main():
    df = load_and_prepare_data()
    chart_paths, coefficients, model_metrics = create_visualizations(df)
    report_path, top_corr = build_report(df, chart_paths, coefficients, model_metrics)

    print("TASK 3 ADVANCED DATA ANALYSIS PROJECT")
    print("=" * 45)
    print("Dataset: scikit-learn Diabetes dataset")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Missing values: {int(df.isna().sum().sum())}")
    print(f"Duplicate rows: {int(df.duplicated().sum())}")
    print()
    print("Research Question:")
    print("Which baseline health factors are most strongly associated with diabetes disease progression?")
    print()
    print("Top correlations with disease progression:")
    print(top_corr.round(3).to_string())
    print()
    print("Regression model output:")
    print(f"R-squared: {model_metrics['r2_score']:.3f}")
    print(f"Mean absolute error: {model_metrics['mean_absolute_error']:.2f}")
    print()
    print("Most influential regression coefficients:")
    print(coefficients[["feature", "coefficient"]].head(8).round(3).to_string(index=False))
    print()
    print("Saved files:")
    print(f"- Clean dataset: {OUTPUT_DIR / 'diabetes_dataset_clean.csv'}")
    print(f"- Report: {report_path}")
    for path in chart_paths.values():
        print(f"- Chart: {path}")


if __name__ == "__main__":
    main()
