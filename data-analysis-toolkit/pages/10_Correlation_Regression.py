import streamlit as st

from utils.page_helpers import add_analysis, alpha_input, require_dataset, render_result, show_figure_with_download
from utils.plots import heatmap, regression_plot, scatterplot
from utils.statistics import correlation_matrix
from utils.tests_parametric import correlation_significance, regression_coefficient_significance
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Correlation and Regression", layout="wide")
apply_global_theme()
render_navigation_sidebar("Correlation Regression")
df = require_dataset()

st.title("Correlation and Regression")
st.caption("Analyze numeric relationships and coefficient significance.")

numeric_columns = st.session_state.numeric_columns
if len(numeric_columns) < 2:
    st.info("At least two numeric columns are required.")
    st.stop()

tab_corr, tab_reg = st.tabs(["Correlation", "Regression"])

with tab_corr:
    method = st.selectbox("Correlation matrix method", ["pearson", "spearman", "kendall"])
    corr = correlation_matrix(df, method)
    st.dataframe(corr, use_container_width=True)
    show_figure_with_download(heatmap(corr), "correlation_matrix")

    st.subheader("Correlation Significance")
    x = st.selectbox("X variable", numeric_columns, key="cr_corr_x")
    y = st.selectbox("Y variable", [c for c in numeric_columns if c != x], key="cr_corr_y")
    alpha = alpha_input("alpha_cr_corr")
    if st.button("Run Pearson correlation significance"):
        try:
            result = correlation_significance(df[x], df[y], alpha)
            render_result(result)
            add_analysis(result)
            show_figure_with_download(scatterplot(df, x=x, y=y), f"correlation_{x}_{y}")
        except Exception as exc:
            st.error(str(exc))

with tab_reg:
    y = st.selectbox("Outcome variable", numeric_columns, key="cr_reg_y")
    x = st.selectbox("Predictor variable", [c for c in numeric_columns if c != y], key="cr_reg_x")
    alpha = alpha_input("alpha_cr_reg")
    if st.button("Run regression"):
        try:
            result, model = regression_coefficient_significance(df, y, x, alpha)
            render_result(result)
            add_analysis(result)
            st.subheader("Model Summary")
            st.text(model.summary().as_text())
            show_figure_with_download(regression_plot(df, x=x, y=y), f"regression_{x}_{y}")
        except Exception as exc:
            st.error(str(exc))
