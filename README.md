# Data Analysis Toolkit

A Streamlit-based statistical analysis system for students. The application is designed to support dataset upload, cleaning, descriptive statistics, visualizations, probability distributions, normality analysis, hypothesis testing, ANOVA, correlation/regression analysis, CLT simulation, automatic recommendations, and PDF reports.

## Run

```bash
streamlit run app.py
```

The main Streamlit entry file is still `app.py`, but the application navigation labels it as `Main`.

## Interface

- The app uses a full dark theme configured in `.streamlit/config.toml`.
- A custom icon sidebar replaces the default Streamlit page list.
- The logo at the top-left links back to `Main`.
- The app first looks for `assets/logo.png`, then falls back to `C:\Users\JOEL\Downloads\logo.png`.
- The Main page contains the project description and a navigation tutorial lower on the page.

## Folder Structure

```text
data-analysis-toolkit/
|
+-- app.py
+-- requirements.txt
+-- README.md
|
+-- pages/
|   +-- 1_Data_Upload.py
|   +-- 2_Data_Cleaning.py
|   +-- 3_Descriptive_Statistics.py
|   +-- 4_Visualizations.py
|   +-- 5_Distributions.py
|   +-- 6_Normality.py
|   +-- 7_Parametric_Tests.py
|   +-- 8_Nonparametric_Tests.py
|   +-- 9_ANOVA.py
|   +-- 10_Correlation_Regression.py
|   +-- 11_CLT_Simulator.py
|   +-- 12_Report.py
|
+-- utils/
|   +-- data_loader.py
|   +-- preprocessing.py
|   +-- statistics.py
|   +-- tests_parametric.py
|   +-- tests_nonparametric.py
|   +-- anova.py
|   +-- plots.py
|   +-- distribution.py
|   +-- report_generator.py
|
+-- assets/
    +-- sample_dataset.csv
```

## Structure Explanation

- `app.py`: The only entry point. It defines the home page, global session state defaults, basic academic styling, and high-level navigation guidance.
- `pages/`: Streamlit multipage modules. Each page will provide one independent analysis area, such as upload, cleaning, visualizations, tests, ANOVA, CLT simulation, and reports.
- `utils/`: Pure Python logic separated from the UI. Data loading, preprocessing, statistical tests, plotting helpers, distribution tools, and PDF generation will live here.
- `assets/`: Static project assets, including the sample dataset used for demos and classroom testing.

## Missing-Value Policy

The UI asks the user how missing values should be handled. The default method is median imputation for numeric columns, and the user can override it from the sidebar or cleaning page.

- Drop rows.
- Fill numeric values with mean.
- Fill numeric values with median.
- Fill categorical values with mode.

The selected option is stored in `st.session_state` and used by the cleaning module.
