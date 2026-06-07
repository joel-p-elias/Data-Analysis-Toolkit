from __future__ import annotations

from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


sns.set_theme(style="whitegrid", palette="deep")


def figure_to_png_bytes(fig) -> bytes:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    buffer.seek(0)
    return buffer.getvalue()


def histogram(series: pd.Series, bins: int = 30, kde: bool = True):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(series.dropna(), bins=bins, kde=kde, ax=ax, color="#1f77b4")
    ax.set_title(f"Histogram of {series.name}")
    ax.set_xlabel(series.name)
    ax.set_ylabel("Frequency")
    return fig


def boxplot(df: pd.DataFrame, y: str, x: str | None = None):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if x:
        sns.boxplot(data=df, x=x, y=y, ax=ax)
        ax.set_title(f"{y} by {x}")
    else:
        sns.boxplot(y=df[y].dropna(), ax=ax)
        ax.set_title(f"Boxplot of {y}")
    return fig


def scatterplot(df: pd.DataFrame, x: str, y: str, hue: str | None = None):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.scatterplot(data=df, x=x, y=y, hue=hue if hue else None, ax=ax)
    ax.set_title(f"Scatter plot: {x} vs {y}")
    return fig


def heatmap(corr: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlOrRd", ax=ax, vmin=-1, vmax=1)
    ax.set_title("Correlation Heatmap")
    return fig


def qq_plot(series: pd.Series):
    fig, ax = plt.subplots(figsize=(6, 6))
    stats.probplot(series.dropna(), dist="norm", plot=ax)
    ax.set_title(f"Q-Q Plot of {series.name}")
    return fig


def histogram_with_normal_curve(series: pd.Series):
    values = series.dropna().astype(float)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.histplot(values, stat="density", bins=30, color="#8fbce6", edgecolor="white", ax=ax)
    mean = values.mean()
    std = values.std(ddof=1)
    if std > 0:
        x = np.linspace(values.min(), values.max(), 300)
        ax.plot(x, stats.norm.pdf(x, mean, std), color="#0b4f8a", linewidth=2, label="Fitted normal curve")
        ax.legend()
    ax.set_title(f"Histogram with Fitted Normal Curve: {series.name}")
    ax.set_xlabel(series.name)
    return fig


def distribution_plot(distribution_df: pd.DataFrame, y_column: str, title: str):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(distribution_df["x"], distribution_df[y_column], color="#1f5f99", linewidth=2)
    marker = "Probability" if y_column in {"pmf", "pdf"} else "Cumulative probability"
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel(marker)
    return fig


def observed_expected_bar(observed: pd.Series | np.ndarray, expected: pd.Series | np.ndarray | None = None):
    observed_values = pd.Series(observed)
    plot_df = pd.DataFrame({"Observed": observed_values})
    if expected is not None:
        plot_df["Expected"] = pd.Series(expected).values
    fig, ax = plt.subplots(figsize=(8, 4.5))
    plot_df.plot(kind="bar", ax=ax, color=["#1f77b4", "#ff7f0e"])
    ax.set_title("Observed vs Expected Counts")
    ax.set_xlabel("Category")
    ax.set_ylabel("Count")
    return fig


def regression_plot(df: pd.DataFrame, x: str, y: str):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.regplot(data=df, x=x, y=y, ax=ax, scatter_kws={"alpha": 0.7}, line_kws={"color": "#0b4f8a"})
    ax.set_title(f"Regression Line: {y} on {x}")
    return fig


def clt_plot(original: pd.Series, sample_means: np.ndarray):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sns.histplot(original.dropna(), bins=30, kde=True, ax=axes[0], color="#1f77b4")
    axes[0].set_title("Original Distribution")
    sns.histplot(sample_means, bins=30, kde=True, ax=axes[1], color="#2ca02c")
    axes[1].set_title("Sampling Distribution of the Mean")
    axes[1].set_xlabel("Sample mean")
    fig.tight_layout()
    return fig


def interaction_plot(df: pd.DataFrame, outcome: str, factor_a: str, factor_b: str):
    summary = df.groupby([factor_a, factor_b], observed=True)[outcome].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.lineplot(data=summary, x=factor_a, y=outcome, hue=factor_b, marker="o", ax=ax)
    ax.set_title(f"Interaction Plot: {factor_a} by {factor_b}")
    return fig