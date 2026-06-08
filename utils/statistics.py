from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all").transpose()


def numeric_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return pd.DataFrame()

    summary = numeric_df.describe().transpose()
    summary["variance"] = numeric_df.var(numeric_only=True)
    summary["skewness"] = numeric_df.skew(numeric_only=True)
    summary["kurtosis"] = numeric_df.kurtosis(numeric_only=True)
    return summary


def correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr(method=method)


def outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in df.select_dtypes(include="number").columns:
        values = df[column].dropna()
        if values.empty:
            continue
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        count = int(((values < lower) | (values > upper)).sum())
        rows.append(
            {
                "column": column,
                "lower_bound": lower,
                "upper_bound": upper,
                "outlier_count": count,
                "outlier_percent": round(count / len(values) * 100, 2),
            }
        )
    return pd.DataFrame(rows)


def shapiro_normality(series: pd.Series) -> dict[str, object]:
    values = series.dropna()
    if len(values) < 3:
        raise ValueError("Shapiro-Wilk requires at least 3 non-missing values.")

    sample = values.sample(5000, random_state=42) if len(values) > 5000 else values
    statistic, p_value = stats.shapiro(sample)
    is_normal = p_value >= 0.05
    return {
        "column": series.name,
        "sample_size": int(len(sample)),
        "statistic": float(statistic),
        "p_value": float(p_value),
        "decision": "Fail to reject H0" if is_normal else "Reject H0",
        "interpretation": (
            "The data are consistent with a normal distribution."
            if is_normal
            else "The data show evidence of non-normality."
        ),
    }


def ks_normality(series: pd.Series) -> dict[str, object]:
    """Kolmogorov-Smirnov test for normality (compares against fitted normal)."""
    values = series.dropna().astype(float)
    if len(values) < 3:
        raise ValueError("Kolmogorov-Smirnov test requires at least 3 non-missing values.")
    mean, std = values.mean(), values.std(ddof=1)
    if std == 0:
        raise ValueError("Standard deviation is zero — cannot fit a normal distribution.")
    statistic, p_value = stats.kstest(values, "norm", args=(mean, std))
    is_normal = p_value >= 0.05
    return {
        "column": series.name,
        "sample_size": int(len(values)),
        "statistic": float(statistic),
        "p_value": float(p_value),
        "decision": "Fail to reject H0" if is_normal else "Reject H0",
        "interpretation": (
            "The data are consistent with a normal distribution."
            if is_normal
            else "The data show evidence of non-normality."
        ),
        "note": "KS test uses the fitted mean and standard deviation from the sample (Lilliefors variant). "
                "P-values may be conservative for small samples.",
    }


def anderson_normality(series: pd.Series) -> dict[str, object]:
    """Anderson-Darling test for normality."""
    values = series.dropna().astype(float)
    if len(values) < 8:
        raise ValueError("Anderson-Darling test requires at least 8 non-missing values.")
    result = stats.anderson(values, dist="norm")
    # Use the 5% significance level (index 2 in critical_values)
    alpha_idx = 2  # corresponds to 5%
    statistic = float(result.statistic)
    critical = float(result.critical_values[alpha_idx])
    significance = float(result.significance_level[alpha_idx])
    is_normal = statistic < critical
    return {
        "column": series.name,
        "sample_size": int(len(values)),
        "statistic": statistic,
        "critical_value_5pct": critical,
        "significance_level": significance,
        "p_value": None,  # Anderson-Darling does not return a direct p-value
        "decision": "Fail to reject H0" if is_normal else "Reject H0",
        "interpretation": (
            "The data are consistent with a normal distribution at the 5% level."
            if is_normal
            else "The data show evidence of non-normality at the 5% level."
        ),
        "note": "Anderson-Darling does not produce a p-value directly. "
                "The decision is based on comparing the test statistic against the critical value at 5% significance.",
        "all_critical_values": dict(zip(
            [str(s) + "%" for s in result.significance_level],
            [float(c) for c in result.critical_values]
        )),
    }


def normality_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in df.select_dtypes(include="number").columns:
        try:
            rows.append(shapiro_normality(df[column]))
        except ValueError:
            continue
    return pd.DataFrame(rows)


def recommendation_engine(df: pd.DataFrame) -> list[dict[str, str]]:
    recommendations: list[dict[str, str]] = []
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    if len(numeric_columns) >= 1:
        recommendations.append(
            {
                "recommendation": "Use descriptive statistics and histograms.",
                "reasoning": "At least one numeric variable is available for center, spread, and shape analysis.",
            }
        )

    if len(numeric_columns) >= 2:
        recommendations.append(
            {
                "recommendation": "Use correlation and regression significance tests.",
                "reasoning": "At least two numeric variables are available for association analysis.",
            }
        )

    if categorical_columns and numeric_columns:
        recommendations.append(
            {
                "recommendation": "Use t-tests, ANOVA, Mann-Whitney U, or Kruskal-Wallis depending on group count and normality.",
                "reasoning": "A categorical grouping variable and numeric outcome are both present.",
            }
        )

    if len(categorical_columns) >= 2:
        recommendations.append(
            {
                "recommendation": "Use a chi-square independence test.",
                "reasoning": "Two categorical variables can be compared using a contingency table.",
            }
        )

    for column in numeric_columns[:5]:
        values = df[column].dropna()
        if len(values) >= 3:
            sample = values.sample(5000, random_state=42) if len(values) > 5000 else values
            _, p_value = stats.shapiro(sample)
            if p_value < 0.05:
                recommendations.append(
                    {
                        "recommendation": f"Consider nonparametric tests for {column}.",
                        "reasoning": "The Shapiro-Wilk test suggests this variable may not be normally distributed.",
                    }
                )

    return recommendations


def auto_insights(df: pd.DataFrame) -> list[str]:
    insights = []
    numeric_df = df.select_dtypes(include="number")
    missing_total = int(df.isna().sum().sum())
    duplicate_count = int(df.duplicated().sum())

    insights.append(f"The dataset contains {df.shape[0]:,} rows and {df.shape[1]:,} columns.")
    insights.append(f"There are {missing_total:,} missing values and {duplicate_count:,} duplicate rows.")

    if not numeric_df.empty:
        spread = numeric_df.std(numeric_only=True).sort_values(ascending=False)
        if not spread.empty:
            insights.append(f"{spread.index[0]} has the largest standard deviation among numeric columns.")

        skew = numeric_df.skew(numeric_only=True).abs().sort_values(ascending=False)
        if not skew.empty and np.isfinite(skew.iloc[0]):
            insights.append(f"{skew.index[0]} shows the strongest skewness among numeric columns.")

    return insights
