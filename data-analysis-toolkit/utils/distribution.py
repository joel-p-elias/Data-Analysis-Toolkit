from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def normal_distribution(mean: float, std: float, points: int = 400) -> pd.DataFrame:
    if std <= 0:
        raise ValueError("Standard deviation must be positive.")
    x = np.linspace(mean - 4 * std, mean + 4 * std, points)
    return pd.DataFrame({"x": x, "pdf": stats.norm.pdf(x, mean, std), "cdf": stats.norm.cdf(x, mean, std)})


def binomial_distribution(n: int, p: float) -> pd.DataFrame:
    if n <= 0 or not 0 <= p <= 1:
        raise ValueError("n must be positive and p must be between 0 and 1.")
    x = np.arange(0, n + 1)
    return pd.DataFrame({"x": x, "pmf": stats.binom.pmf(x, n, p), "cdf": stats.binom.cdf(x, n, p)})


def poisson_distribution(lam: float) -> pd.DataFrame:
    if lam <= 0:
        raise ValueError("Lambda must be positive.")
    upper = max(15, int(lam + 5 * np.sqrt(lam)))
    x = np.arange(0, upper + 1)
    return pd.DataFrame({"x": x, "pmf": stats.poisson.pmf(x, lam), "cdf": stats.poisson.cdf(x, lam)})


def fit_normal(series: pd.Series) -> dict[str, float]:
    values = series.dropna().astype(float)
    if len(values) < 3:
        raise ValueError("Distribution fitting requires at least 3 numeric values.")
    mean, std = stats.norm.fit(values)
    statistic, p_value = stats.kstest(values, "norm", args=(mean, std))
    return {"mean": float(mean), "std": float(std), "ks_statistic": float(statistic), "ks_p_value": float(p_value)}


def simulate_clt(series: pd.Series, sample_size: int, number_of_samples: int, random_state: int = 42) -> np.ndarray:
    values = series.dropna().astype(float).to_numpy()
    if len(values) < sample_size:
        raise ValueError("Sample size cannot exceed available non-missing observations.")
    if sample_size < 1 or number_of_samples < 1:
        raise ValueError("Sample size and number of samples must be positive.")
    rng = np.random.default_rng(random_state)
    samples = rng.choice(values, size=(number_of_samples, sample_size), replace=True)
    return samples.mean(axis=1)

