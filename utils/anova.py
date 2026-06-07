from __future__ import annotations

from typing import Iterable

import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

from utils.tests_parametric import decision_text


def one_way_anova(groups: dict[str, Iterable[float]], alpha: float = 0.05) -> dict[str, object]:
    cleaned = {name: pd.Series(values).dropna().astype(float) for name, values in groups.items()}
    cleaned = {name: values for name, values in cleaned.items() if len(values) >= 2}
    if len(cleaned) < 2:
        raise ValueError("One-way ANOVA requires at least two groups with 2 or more observations.")

    statistic, p_value = stats.f_oneway(*cleaned.values())
    df_between = len(cleaned) - 1
    df_within = sum(len(values) for values in cleaned.values()) - len(cleaned)
    return {
        "test_name": "One-way ANOVA",
        "h0": "All group means are equal.",
        "ha": "At least one group mean is different.",
        "statistic_name": "F",
        "statistic": float(statistic),
        "p_value": float(p_value),
        "degrees_of_freedom": f"{df_between}, {df_within}",
        "alpha": alpha,
        "decision": decision_text(float(p_value), alpha),
        "interpretation": "This test compares the means of a numeric outcome across two or more independent groups.",
        "inputs": {"groups": list(cleaned.keys())},
    }


def two_way_anova(df: pd.DataFrame, outcome: str, factor_a: str, factor_b: str, alpha: float = 0.05) -> tuple[pd.DataFrame, object]:
    model_df = df[[outcome, factor_a, factor_b]].dropna()
    if model_df[outcome].nunique() < 2:
        raise ValueError("The outcome must contain at least two numeric values.")
    if model_df[factor_a].nunique() < 2 or model_df[factor_b].nunique() < 2:
        raise ValueError("Each factor must contain at least two groups.")

    formula = f'Q("{outcome}") ~ C(Q("{factor_a}")) + C(Q("{factor_b}")) + C(Q("{factor_a}")):C(Q("{factor_b}"))'
    model = ols(formula, data=model_df).fit()
    table = anova_lm(model, typ=2).reset_index().rename(columns={"index": "source", "PR(>F)": "p_value"})
    table["decision"] = table["p_value"].apply(lambda value: decision_text(value, alpha) if pd.notna(value) else "")
    return table, model

