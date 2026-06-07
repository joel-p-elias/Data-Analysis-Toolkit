import streamlit as st

from utils.page_helpers import require_dataset, show_figure_with_download
from utils.plots import boxplot, heatmap, histogram, qq_plot, scatterplot
from utils.statistics import correlation_matrix
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Visualizations", layout="wide")
apply_global_theme()
render_navigation_sidebar("Visualizations")
df = require_dataset()

st.title("Visualizations")
st.caption("Create labeled plots and export them as PNG files.")

numeric_columns = st.session_state.numeric_columns
categorical_columns = st.session_state.categorical_columns

plot_type = st.selectbox("Plot type", ["Histogram", "Boxplot", "Scatter Plot", "Heatmap", "QQ Plot"])

if plot_type == "Histogram":
    if not numeric_columns:
        st.info("A numeric column is required.")
    else:
        column = st.selectbox("Numeric column", numeric_columns)
        bins = st.slider("Bins", 5, 80, 30)
        fig = histogram(df[column], bins=bins)
        show_figure_with_download(fig, f"histogram_{column}")

elif plot_type == "Boxplot":
    if not numeric_columns:
        st.info("A numeric column is required.")
    else:
        y = st.selectbox("Numeric outcome", numeric_columns)
        group = st.selectbox("Optional grouping column", ["None"] + categorical_columns)
        fig = boxplot(df, y=y, x=None if group == "None" else group)
        show_figure_with_download(fig, f"boxplot_{y}")

elif plot_type == "Scatter Plot":
    if len(numeric_columns) < 2:
        st.info("At least two numeric columns are required.")
    else:
        x = st.selectbox("X column", numeric_columns)
        y = st.selectbox("Y column", numeric_columns, index=min(1, len(numeric_columns) - 1))
        hue = st.selectbox("Optional color grouping", ["None"] + categorical_columns)
        fig = scatterplot(df, x=x, y=y, hue=None if hue == "None" else hue)
        show_figure_with_download(fig, f"scatter_{x}_{y}")

elif plot_type == "Heatmap":
    corr = correlation_matrix(df)
    if corr.empty:
        st.info("At least two numeric columns are required.")
    else:
        fig = heatmap(corr)
        show_figure_with_download(fig, "heatmap")

elif plot_type == "QQ Plot":
    if not numeric_columns:
        st.info("A numeric column is required.")
    else:
        column = st.selectbox("Numeric column", numeric_columns)
        fig = qq_plot(df[column])
        show_figure_with_download(fig, f"qq_plot_{column}")
