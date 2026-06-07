from __future__ import annotations

import math
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols


def _clean_numeric(values: Iterable[float]) -> np.ndarray:
    return pd.Series(values).dropna().astype(float).to_numpy()


def decision_text(p_value: float, alpha: float) -> str:
    return "Reject H0" if p_value < alpha else "Fail to reject H0"


def p_value_from_z(z_statistic: float, alternative: str) -> float:
    if alternative == "two-sided":
        return float(2 * (1 - stats.norm.cdf(abs(z_statistic))))
    if alternative == "greater":
        return float(1 - stats.norm.cdf(z_statistic))
    if alternative == "less":
        return float(stats.norm.cdf(z_statistic))
    raise ValueError("Alternative must be two-sided, greater, or less.")


def result_dict(
    name: str,
    h0: str,
    ha: str,
    statistic_name: str,
    statistic: float,
    p_value: float,
    alpha: float,
    interpretation: str,
    inputs: dict[str, object],
    degrees_of_freedom: float | int | None = None,
) -> dict[str, object]:
    return {
        "test_name": name,
        "h0": h0,
        "ha": ha,
        "statistic_name": statistic_name,
        "statistic": float(statistic),
        "p_value": float(p_value),
        "degrees_of_freedom": degrees_of_freedom,
        "alpha": alpha,
        "decision": decision_text(float(p_value), alpha),
        "interpretation": interpretation,
        "inputs": inputs,
    }


def one_sample_t_test(sample: Iterable[float], population_mean: float, alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, object]:
    values = _clean_numeric(sample)
    if len(values) < 2:
        raise ValueError("One-sample t-test requires at least 2 numeric observations.")

    statistic, p_value = stats.ttest_1samp(values, population_mean, alternative=alternative)
    return result_dict(
        "One-sample t-test",
        f"The population mean is equal to {population_mean}.",
        f"The population mean is {alternative.replace('-', ' ')} relative to {population_mean}.",
        "t",
        statistic,
        p_value,
        alpha,
        "Compare the p-value with alpha to decide whether the sample mean differs from the hypothesized population mean.",
        {"sample_size": len(values), "population_mean": population_mean, "alternative": alternative},
        len(values) - 1,
    )


def independent_t_test(group_a: Iterable[float], group_b: Iterable[float], equal_var: bool = False, alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, object]:
    a = _clean_numeric(group_a)
    b = _clean_numeric(group_b)
    if len(a) < 2 or len(b) < 2:
        raise ValueError("Independent t-test requires at least 2 observations in each group.")

    statistic, p_value = stats.ttest_ind(a, b, equal_var=equal_var, alternative=alternative)
    if equal_var:
        df = len(a) + len(b) - 2
    else:
        var_a = np.var(a, ddof=1)
        var_b = np.var(b, ddof=1)
        numerator = (var_a / len(a) + var_b / len(b)) ** 2
        denominator = (var_a**2 / (len(a) ** 2 * (len(a) - 1))) + (var_b**2 / (len(b) ** 2 * (len(b) - 1)))
        df = numerator / denominator if denominator else math.nan

    return result_dict(
        "Independent t-test",
        "The two group means are equal.",
        "The two group means are different.",
        "t",
        statistic,
        p_value,
        alpha,
        "This test compares the average numeric outcome between two independent groups.",
        {"group_a_size": len(a), "group_b_size": len(b), "equal_variance_assumed": equal_var, "alternative": alternative},
        round(df, 3) if np.isfinite(df) else None,
    )


def paired_t_test(before: Iterable[float], after: Iterable[float], alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, object]:
    paired = pd.DataFrame({"before": before, "after": after}).dropna()
    if len(paired) < 2:
        raise ValueError("Paired t-test requires at least 2 complete pairs.")

    statistic, p_value = stats.ttest_rel(paired["before"], paired["after"], alternative=alternative)
    return result_dict(
        "Paired t-test",
        "The mean paired difference is zero.",
        "The mean paired difference is not zero.",
        "t",
        statistic,
        p_value,
        alpha,
        "This test compares two related measurements from the same units or matched pairs.",
        {"pair_count": len(paired), "alternative": alternative},
        len(paired) - 1,
    )


def one_proportion_z_test(successes: int, nobs: int, hypothesized_proportion: float, alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, object]:
    if nobs <= 0 or not 0 <= successes <= nobs:
        raise ValueError("Successes must be between 0 and the total number of observations.")
    if not 0 < hypothesized_proportion < 1:
        raise ValueError("Hypothesized proportion must be between 0 and 1.")

    p_hat = successes / nobs
    standard_error = math.sqrt(hypothesized_proportion * (1 - hypothesized_proportion) / nobs)
    z_statistic = (p_hat - hypothesized_proportion) / standard_error
    p_value = p_value_from_z(z_statistic, alternative)
    return result_dict(
        "One-proportion z-test",
        f"The population proportion is {hypothesized_proportion}.",
        "The population proportion differs from the hypothesized value.",
        "z",
        z_statistic,
        p_value,
        alpha,
        "This test compares an observed sample proportion with a hypothesized population proportion.",
        {"successes": successes, "observations": nobs, "sample_proportion": p_hat, "hypothesized_proportion": hypothesized_proportion, "alternative": alternative},
    )


def two_proportion_z_test(successes_a: int, nobs_a: int, successes_b: int, nobs_b: int, alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, object]:
    if nobs_a <= 0 or nobs_b <= 0:
        raise ValueError("Observation counts must be positive.")
    if not 0 <= successes_a <= nobs_a or not 0 <= successes_b <= nobs_b:
        raise ValueError("Success counts must be valid for each group.")

    p_a = successes_a / nobs_a
    p_b = successes_b / nobs_b
    pooled = (successes_a + successes_b) / (nobs_a + nobs_b)
    standard_error = math.sqrt(pooled * (1 - pooled) * (1 / nobs_a + 1 / nobs_b))
    z_statistic = (p_a - p_b) / standard_error
    p_value = p_value_from_z(z_statistic, alternative)
    return result_dict(
        "Two-proportion z-test",
        "The two population proportions are equal.",
        "The two population proportions are different.",
        "z",
        z_statistic,
        p_value,
        alpha,
        "This test compares two independent sample proportions.",
        {"group_a_proportion": p_a, "group_b_proportion": p_b, "alternative": alternative},
    )


def chi_square_goodness_of_fit(observed: Iterable[float], expected: Iterable[float] | None = None, alpha: float = 0.05) -> dict[str, object]:
    observed_values = np.asarray(list(observed), dtype=float)
    expected_values = None if expected is None else np.asarray(list(expected), dtype=float)
    if observed_values.size < 2:
        raise ValueError("At least two observed categories are required.")
    if expected_values is not None and observed_values.size != expected_values.size:
        raise ValueError("Observed and expected counts must have the same length.")

    statistic, p_value = stats.chisquare(f_obs=observed_values, f_exp=expected_values)
    return result_dict(
        "Chi-square goodness-of-fit test",
        "The observed category frequencies match the expected frequencies.",
        "The observed category frequencies do not match the expected frequencies.",
        "chi-square",
        statistic,
        p_value,
        alpha,
        "This test compares observed counts with expected counts across categories.",
        {"categories": int(observed_values.size)},
        observed_values.size - 1,
    )


def chi_square_independence(table: pd.DataFrame, alpha: float = 0.05) -> tuple[dict[str, object], pd.DataFrame]:
    if table.shape[0] < 2 or table.shape[1] < 2:
        raise ValueError("Chi-square independence requires at least a 2 by 2 contingency table.")

    statistic, p_value, df, expected = stats.chi2_contingency(table)
    result = result_dict(
        "Chi-square independence test",
        "The two categorical variables are independent.",
        "The two categorical variables are associated.",
        "chi-square",
        statistic,
        p_value,
        alpha,
        "This test evaluates whether two categorical variables are statistically associated.",
        {"rows": table.shape[0], "columns": table.shape[1]},
        df,
    )
    expected_df = pd.DataFrame(expected, index=table.index, columns=table.columns)
    return result, expected_df


def correlation_significance(x: Iterable[float], y: Iterable[float], alpha: float = 0.05) -> dict[str, object]:
    paired = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(paired) < 3:
        raise ValueError("Correlation significance requires at least 3 complete pairs.")

    statistic, p_value = stats.pearsonr(paired["x"], paired["y"])
    return result_dict(
        "Pearson correlation significance test",
        "The population correlation is zero.",
        "The population correlation is not zero.",
        "r",
        statistic,
        p_value,
        alpha,
        "This test checks whether a linear relationship between two numeric variables is statistically significant.",
        {"pair_count": len(paired)},
        len(paired) - 2,
    )


def regression_coefficient_significance(df: pd.DataFrame, y_column: str, x_column: str, alpha: float = 0.05) -> tuple[dict[str, object], object]:
    model_df = df[[y_column, x_column]].dropna()
    if len(model_df) < 3:
        raise ValueError("Regression requires at least 3 complete rows.")

    formula = f'Q("{y_column}") ~ Q("{x_column}")'
    model = ols(formula, data=model_df).fit()
    coefficient = float(model.params.iloc[1])
    statistic = float(model.tvalues.iloc[1])
    p_value = float(model.pvalues.iloc[1])
    result = result_dict(
        "Regression coefficient significance test",
        f"The slope for {x_column} is zero.",
        f"The slope for {x_column} is not zero.",
        "t",
        statistic,
        p_value,
        alpha,
        "This test checks whether the predictor has a statistically significant linear association with the outcome.",
        {"outcome": y_column, "predictor": x_column, "coefficient": coefficient, "r_squared": float(model.rsquared)},
        int(model.df_resid),
    )
    return result, model

