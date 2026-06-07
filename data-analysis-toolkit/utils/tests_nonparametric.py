from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats

from utils.tests_parametric import decision_text


def _clean_numeric(values: Iterable[float]) -> np.ndarray:
    return pd.Series(values).dropna().astype(float).to_numpy()


def _result(name: str, h0: str, ha: str, statistic_name: str, statistic: float, p_value: float, alpha: float, interpretation: str, inputs: dict[str, object]) -> dict[str, object]:
    return {
        "test_name": name,
        "h0": h0,
        "ha": ha,
        "statistic_name": statistic_name,
        "statistic": float(statistic),
        "p_value": float(p_value),
        "degrees_of_freedom": None,
        "alpha": alpha,
        "decision": decision_text(float(p_value), alpha),
        "interpretation": interpretation,
        "inputs": inputs,
    }


def mann_whitney_u(group_a: Iterable[float], group_b: Iterable[float], alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, object]:
    a = _clean_numeric(group_a)
    b = _clean_numeric(group_b)
    if len(a) < 1 or len(b) < 1:
        raise ValueError("Mann-Whitney U requires at least one observation in each group.")
    statistic, p_value = stats.mannwhitneyu(a, b, alternative=alternative)
    return _result(
        "Mann-Whitney U test",
        "The two independent groups come from the same distribution.",
        "The two independent groups differ in distribution.",
        "U",
        statistic,
        p_value,
        alpha,
        "This nonparametric test compares two independent groups without assuming normality.",
        {"group_a_size": len(a), "group_b_size": len(b), "alternative": alternative},
    )


def wilcoxon_signed_rank(before: Iterable[float], after: Iterable[float], alpha: float = 0.05, alternative: str = "two-sided") -> dict[str, object]:
    paired = pd.DataFrame({"before": before, "after": after}).dropna()
    if len(paired) < 1:
        raise ValueError("Wilcoxon signed-rank requires at least one complete pair.")
    statistic, p_value = stats.wilcoxon(paired["before"], paired["after"], alternative=alternative)
    return _result(
        "Wilcoxon signed-rank test",
        "The median paired difference is zero.",
        "The median paired difference is not zero.",
        "W",
        statistic,
        p_value,
        alpha,
        "This nonparametric test compares two related measurements.",
        {"pair_count": len(paired), "alternative": alternative},
    )


def kruskal_wallis(groups: dict[str, Iterable[float]], alpha: float = 0.05) -> dict[str, object]:
    cleaned = {name: _clean_numeric(values) for name, values in groups.items()}
    cleaned = {name: values for name, values in cleaned.items() if len(values) > 0}
    if len(cleaned) < 2:
        raise ValueError("Kruskal-Wallis requires at least two groups.")
    statistic, p_value = stats.kruskal(*cleaned.values())
    return _result(
        "Kruskal-Wallis test",
        "All groups come from the same distribution.",
        "At least one group differs in distribution.",
        "H",
        statistic,
        p_value,
        alpha,
        "This nonparametric test compares three or more independent groups.",
        {"groups": list(cleaned.keys())},
    )


def friedman_test(group_columns: list[Iterable[float]], labels: list[str], alpha: float = 0.05) -> dict[str, object]:
    paired = pd.DataFrame({label: values for label, values in zip(labels, group_columns)}).dropna()
    if paired.shape[1] < 3:
        raise ValueError("Friedman test requires at least three related groups.")
    if len(paired) < 2:
        raise ValueError("Friedman test requires at least two complete rows.")
    statistic, p_value = stats.friedmanchisquare(*[paired[column] for column in paired.columns])
    return _result(
        "Friedman test",
        "The related groups have the same distribution.",
        "At least one related group differs in distribution.",
        "chi-square",
        statistic,
        p_value,
        alpha,
        "This nonparametric test compares three or more related measurements.",
        {"groups": labels, "complete_rows": len(paired)},
    )

