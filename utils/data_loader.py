from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd


MAX_ROWS = 100_000
SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def load_dataset(file: BinaryIO, filename: str) -> pd.DataFrame:
    """Load a CSV or Excel dataset and enforce the project row limit."""
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Please upload a CSV or Excel file.")

    if suffix == ".csv":
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    if len(df) > MAX_ROWS:
        raise ValueError(f"Dataset has {len(df):,} rows. The maximum supported size is {MAX_ROWS:,}.")

    return df


def load_sample_dataset(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def detect_column_types(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    return numeric_columns, categorical_columns


def dataset_overview(df: pd.DataFrame) -> dict[str, object]:
    numeric_columns, categorical_columns = detect_column_types(df)
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def missing_value_table(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isna().sum()
    table = pd.DataFrame(
        {
            "column": missing.index,
            "missing_count": missing.values,
            "missing_percent": (missing.values / max(len(df), 1) * 100).round(2),
        }
    )
    return table.sort_values("missing_count", ascending=False).reset_index(drop=True)

