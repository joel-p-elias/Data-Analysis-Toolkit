from __future__ import annotations

import pandas as pd


DROP_ROWS = "Drop rows"
FILL_MEAN = "Fill with mean"
FILL_MEDIAN = "Fill with median"
FILL_MODE_CATEGORICAL = "Fill with mode for categorical columns"
DEFAULT_MISSING_VALUE_STRATEGY = FILL_MEDIAN

MISSING_VALUE_STRATEGIES = [
    DROP_ROWS,
    FILL_MEAN,
    FILL_MEDIAN,
    FILL_MODE_CATEGORICAL,
]


def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    duplicate_count = int(df.duplicated().sum())
    return df.drop_duplicates().reset_index(drop=True), duplicate_count


def fill_numeric_with_mean(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    numeric_columns = cleaned.select_dtypes(include="number").columns
    for column in numeric_columns:
        cleaned[column] = cleaned[column].fillna(cleaned[column].mean())
    return cleaned


def fill_numeric_with_median(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    numeric_columns = cleaned.select_dtypes(include="number").columns
    for column in numeric_columns:
        cleaned[column] = cleaned[column].fillna(cleaned[column].median())
    return cleaned


def fill_categorical_with_mode(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    categorical_columns = cleaned.select_dtypes(include=["object", "category", "bool"]).columns
    for column in categorical_columns:
        mode_values = cleaned[column].mode(dropna=True)
        if not mode_values.empty:
            cleaned[column] = cleaned[column].fillna(mode_values.iloc[0])
    return cleaned


def handle_missing_values(df: pd.DataFrame, strategy: str) -> tuple[pd.DataFrame, dict[str, object]]:
    if strategy not in MISSING_VALUE_STRATEGIES:
        raise ValueError(f"Unknown missing-value strategy: {strategy}")

    before = int(df.isna().sum().sum())
    before_rows = int(len(df))

    if strategy == DROP_ROWS:
        cleaned = df.dropna().reset_index(drop=True)
    elif strategy == FILL_MEAN:
        cleaned = fill_numeric_with_mean(df)
    elif strategy == FILL_MEDIAN:
        cleaned = fill_numeric_with_median(df)
    else:
        cleaned = fill_categorical_with_mode(df)

    after = int(cleaned.isna().sum().sum())
    return cleaned, {
        "strategy": strategy,
        "missing_before": before,
        "missing_after": after,
        "rows_before": before_rows,
        "rows_after": int(len(cleaned)),
        "rows_removed": before_rows - int(len(cleaned)),
    }


def coerce_columns_to_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    cleaned = df.copy()
    for column in columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    return cleaned

