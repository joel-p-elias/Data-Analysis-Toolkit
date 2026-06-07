import streamlit as st

from utils import statistics as stats_utils
from utils.data_loader import dataset_overview
from utils.page_helpers import require_dataset, show_figure_with_download
from utils.plots import heatmap, histogram
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Descriptive Statistics", layout="wide")
apply_global_theme()
render_navigation_sidebar("Descriptive Statistics")
df = require_dataset()

st.title("Descriptive Statistics")
st.caption("Summaries, correlations, outliers, recommendations, and automatic insights.")

tab_summary, tab_corr, tab_outliers, tab_recommend, tab_full = st.tabs(
    ["Descriptive Statistics", "Correlation Matrix", "Outlier Detection", "Recommendations", "Full Analysis"]
)

with tab_summary:
    st.subheader("All Columns")
    st.dataframe(stats_utils.descriptive_statistics(df), use_container_width=True)

    st.subheader("Numeric Detail")
    numeric_summary = stats_utils.numeric_descriptive_statistics(df)
    if numeric_summary.empty:
        st.info("No numeric columns detected.")
    else:
        st.dataframe(numeric_summary, use_container_width=True)

with tab_corr:
    method = st.selectbox("Correlation method", ["pearson", "spearman", "kendall"])
    corr = stats_utils.correlation_matrix(df, method)
    if corr.empty:
        st.info("At least two numeric columns are required.")
    else:
        st.dataframe(corr, use_container_width=True)
        fig = heatmap(corr)
        show_figure_with_download(fig, "correlation_heatmap")

with tab_outliers:
    outliers = stats_utils.outlier_summary(df)
    if outliers.empty:
        st.info("No numeric columns detected.")
    else:
        st.dataframe(outliers, use_container_width=True)

with tab_recommend:
    st.subheader("Automatic Insights")
    for insight in stats_utils.auto_insights(df):
        st.write(f"- {insight}")

    st.subheader("Recommended Tests")
    for item in stats_utils.recommendation_engine(df):
        st.write(f"**{item['recommendation']}**")
        st.write(item["reasoning"])

with tab_full:
    st.subheader("Auto Analysis Mode")
    if st.button("Run Full Analysis", type="primary"):
        st.write("**Dataset overview**")
        st.json(dataset_overview(df))

        st.write("**Initial insights**")
        for insight in stats_utils.auto_insights(df):
            st.write(f"- {insight}")

        numeric_summary = stats_utils.numeric_descriptive_statistics(df)
        if not numeric_summary.empty:
            st.write("**Descriptive statistics**")
            st.dataframe(numeric_summary, use_container_width=True)

        normality = stats_utils.normality_summary(df)
        if not normality.empty:
            st.write("**Normality test preview**")
            st.dataframe(normality, use_container_width=True)

        corr = stats_utils.correlation_matrix(df)
        if not corr.empty:
            st.write("**Correlation matrix**")
            st.dataframe(corr, use_container_width=True)
            show_figure_with_download(heatmap(corr), "full_analysis_correlation_heatmap")

        if st.session_state.numeric_columns:
            column = st.session_state.numeric_columns[0]
            show_figure_with_download(histogram(df[column]), f"full_analysis_histogram_{column}")
