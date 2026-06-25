from pathlib import Path

import nbformat as nbf


BASE_DIR = Path(__file__).parent
NOTEBOOK_PATH = BASE_DIR / "Task3_Diabetes_Data_Analysis.ipynb"


def code_cell(source):
    return nbf.v4.new_code_cell(source.strip())


def markdown_cell(source):
    return nbf.v4.new_markdown_cell(source.strip())


notebook = nbf.v4.new_notebook()
notebook["metadata"] = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "name": "python",
        "version": "3.13",
    },
}

notebook["cells"] = [
    markdown_cell(
        """
# Task 3 Advanced Level: Diabetes Data Analysis

This notebook presents a complete data analysis project from scratch. It selects a public dataset, explores and cleans the data, defines a research question, uses visualizations to investigate the question, and presents final findings.
"""
    ),
    markdown_cell(
        """
## Dataset and Research Question

**Dataset:** scikit-learn Diabetes dataset.  
**Rows:** 442 patient records.  
**Variables:** 10 standardized baseline medical measurements plus a disease progression target.

**Research question:** Which baseline health factors are most strongly associated with diabetes disease progression?
"""
    ),
    code_cell(
        """
import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "task3_matplotlib_cache"))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.figsize"] = (10, 6)
"""
    ),
    markdown_cell("## Load the Dataset"),
    code_cell(
        """
dataset = load_diabetes(as_frame=True)
df = dataset.frame.copy()

df = df.rename(columns={
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
})

df.head()
"""
    ),
    markdown_cell("## Data Cleaning Checks"),
    code_cell(
        """
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Missing values: {df.isna().sum().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")
df.isna().sum()
"""
    ),
    markdown_cell("## Summary Statistics"),
    code_cell("df.describe().round(3)"),
    markdown_cell("## Correlation Analysis"),
    code_cell(
        """
target_corr = df.corr(numeric_only=True)["disease_progression"].drop("disease_progression")
target_corr.abs().sort_values(ascending=False).head(5).round(3)
"""
    ),
    code_cell(
        """
plt.figure(figsize=(12, 9))
sns.heatmap(df.corr(numeric_only=True), cmap="vlag", center=0, annot=False, linewidths=0.5)
plt.title("Correlation Heatmap: Diabetes Variables and Disease Progression")
plt.tight_layout()
plt.show()
"""
    ),
    markdown_cell("## Visualization 1: Body Mass Index and Disease Progression"),
    code_cell(
        """
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
plt.show()
"""
    ),
    markdown_cell("## Visualization 2: Disease Progression by Age Group"),
    code_cell(
        """
df_age = df.copy()
df_age["age_group"] = pd.qcut(df_age["age"], q=4, labels=["youngest", "lower-middle", "upper-middle", "oldest"])

sns.boxplot(data=df_age, x="age_group", y="disease_progression")
plt.title("Disease Progression Distribution by Age Group")
plt.xlabel("Age Group Based on Quartiles")
plt.ylabel("Disease Progression Score")
plt.tight_layout()
plt.show()
"""
    ),
    markdown_cell("## Modeling: Which Factors Matter Most?"),
    code_cell(
        """
feature_cols = [col for col in df.columns if col != "disease_progression"]
X = df[feature_cols]
y = df["disease_progression"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(f"R-squared: {r2_score(y_test, predictions):.3f}")
print(f"Mean absolute error: {mean_absolute_error(y_test, predictions):.2f}")

coefficients = (
    pd.DataFrame({"feature": feature_cols, "coefficient": model.coef_})
    .assign(abs_coefficient=lambda data: data["coefficient"].abs())
    .sort_values("abs_coefficient", ascending=False)
)
coefficients[["feature", "coefficient"]].head(8).round(3)
"""
    ),
    code_cell(
        """
sns.barplot(data=coefficients, x="coefficient", y="feature", hue="feature", legend=False)
plt.axvline(0, color="black", linewidth=1)
plt.title("Linear Regression Coefficients for Disease Progression")
plt.xlabel("Coefficient Value")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()
"""
    ),
    markdown_cell(
        """
## Final Findings

The strongest absolute correlations with disease progression are body mass index, log serum triglycerides, blood pressure, total cholesterol to HDL ratio, and high-density lipoproteins. The regression analysis also highlights body mass index and blood-serum measurements as influential predictors.

The answer to the research question is that diabetes disease progression appears to be associated most strongly with metabolic and cardiovascular indicators rather than age alone. The BMI regression plot shows an upward trend, and the coefficient visualization suggests that multiple baseline health measurements should be considered together.

## Conclusion

This analysis shows that disease progression is not explained by a single variable. Body mass index, serum triglycerides, blood pressure, and cholesterol-related measurements provide the most useful signals in this dataset. These insights could help guide more focused patient monitoring and further medical analysis.
"""
    ),
]

nbf.write(notebook, NOTEBOOK_PATH)
print(f"Created notebook: {NOTEBOOK_PATH}")
