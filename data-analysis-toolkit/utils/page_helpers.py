from __future__ import annotations

import streamlit as st

from utils.data_loader import detect_column_types
from utils.theme import render_empty_state
from utils.plots import figure_to_png_bytes
from utils.preprocessing import DEFAULT_MISSING_VALUE_STRATEGY


def initialize_session_state() -> None:
    defaults = {
        "dataset": None,
        "dataset_name": None,
        "numeric_columns": [],
        "categorical_columns": [],
        "analysis_log": [],
        "generated_plots": [],
        "missing_value_strategy": DEFAULT_MISSING_VALUE_STRATEGY,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def update_dataset(df, name: str) -> None:
    numeric_columns, categorical_columns = detect_column_types(df)
    st.session_state.dataset = df
    st.session_state.dataset_name = name
    st.session_state.numeric_columns = numeric_columns
    st.session_state.categorical_columns = categorical_columns


def require_dataset():
    initialize_session_state()
    if st.session_state.dataset is None:
        render_empty_state(
            title="No dataset loaded",
            message="Upload a CSV or Excel file, or load the sample dataset to get started.",
        )
        st.stop()
    return st.session_state.dataset


def render_result(result: dict[str, object]) -> None:
    st.subheader(str(result.get("test_name", "Statistical Result")))
    st.markdown(f"**H0:** {result.get('h0', 'Not provided')}")
    st.markdown(f"**Ha:** {result.get('ha', 'Not provided')}")

    col_stat, col_p, col_df = st.columns(3)
    col_stat.metric(str(result.get("statistic_name", "Statistic")), f"{float(result.get('statistic', 0)):.4f}")
    col_p.metric("p-value", f"{float(result.get('p_value', 0)):.4f}")
    col_df.metric("Degrees of freedom", str(result.get("degrees_of_freedom") or "N/A"))

    st.markdown(f"**Decision:** {result.get('decision')}")
    st.markdown(f"**Interpretation:** {result.get('interpretation')}")

    inputs = result.get("inputs")
    if inputs:
        with st.expander("Inputs used"):
            st.json(inputs)


def add_analysis(result: dict[str, object]) -> None:
    st.session_state.analysis_log.append(result)


def show_figure_with_download(fig, label: str) -> bytes:
    st.pyplot(fig)
    png = figure_to_png_bytes(fig)
    st.download_button(
        "Download plot as PNG",
        data=png,
        file_name=f"{label.lower().replace(' ', '_')}.png",
        mime="image/png",
    )
    st.session_state.generated_plots.append({"label": label, "png": png})
    return png


def alpha_input(key: str = "alpha") -> float:
    return st.number_input("Significance level alpha", min_value=0.001, max_value=0.2, value=0.05, step=0.01, key=key)


def alternative_select(key: str = "alternative") -> str:
    return st.selectbox("Alternative hypothesis direction", ["two-sided", "greater", "less"], key=key)