import streamlit as st

from utils.page_helpers import add_analysis, require_dataset, render_result, show_figure_with_download
from utils.plots import histogram_with_normal_curve, qq_plot
from utils.statistics import shapiro_normality
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Normality", layout="wide")
apply_global_theme()
render_navigation_sidebar("Normality")
df = require_dataset()

st.title("Normality Analysis")
st.caption("Run Shapiro-Wilk, Q-Q plot, and histogram with fitted normal curve.")

numeric_columns = st.session_state.numeric_columns
if not numeric_columns:
    st.info("A numeric column is required.")
    st.stop()

column = st.selectbox("Numeric column", numeric_columns)

if st.button("Run normality analysis", type="primary"):
    try:
        raw = shapiro_normality(df[column])
        result = {
            "test_name": "Shapiro-Wilk normality test",
            "h0": "The data come from a normal distribution.",
            "ha": "The data do not come from a normal distribution.",
            "statistic_name": "W",
            "statistic": raw["statistic"],
            "p_value": raw["p_value"],
            "degrees_of_freedom": None,
            "alpha": 0.05,
            "decision": raw["decision"],
            "interpretation": raw["interpretation"],
            "inputs": {"column": column, "sample_size": raw["sample_size"]},
        }
        render_result(result)
        add_analysis(result)

        col_hist, col_qq = st.columns(2)
        with col_hist:
            fig = histogram_with_normal_curve(df[column])
            show_figure_with_download(fig, f"normal_curve_{column}")
        with col_qq:
            fig = qq_plot(df[column])
            show_figure_with_download(fig, f"qq_plot_{column}")

        if raw["p_value"] < 0.05:
            st.warning("Normality may be violated. Consider a nonparametric test if this variable is used in group comparisons.")
    except Exception as exc:
        st.error(str(exc))
