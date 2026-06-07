import streamlit as st

from utils.distribution import simulate_clt
from utils.page_helpers import require_dataset, show_figure_with_download
from utils.plots import clt_plot
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="CLT Simulator", layout="wide")
apply_global_theme()
render_navigation_sidebar("CLT Simulator")
df = require_dataset()

st.title("CLT Simulator")
st.caption("Sample repeatedly from one numeric variable to see the sampling mean approach normality.")

numeric_columns = st.session_state.numeric_columns
if not numeric_columns:
    st.info("A numeric column is required.")
    st.stop()

column = st.selectbox("Numeric column", numeric_columns)
available = int(df[column].dropna().shape[0])
sample_size = st.slider("Sample size", min_value=1, max_value=max(1, min(available, 500)), value=min(30, max(1, available)))
number_of_samples = st.slider("Number of samples", min_value=10, max_value=5000, value=1000, step=10)

if st.button("Run CLT simulation", type="primary"):
    try:
        sample_means = simulate_clt(df[column], sample_size, number_of_samples)
        col_original, col_sampling = st.columns(2)
        col_original.metric("Original mean", f"{df[column].mean():.4f}")
        col_original.metric("Original standard deviation", f"{df[column].std(ddof=1):.4f}")
        col_sampling.metric("Mean of sample means", f"{sample_means.mean():.4f}")
        col_sampling.metric("Standard deviation of sample means", f"{sample_means.std(ddof=1):.4f}")

        fig = clt_plot(df[column], sample_means)
        show_figure_with_download(fig, f"clt_{column}")
        st.write("As sample size increases, the sampling distribution of the mean typically becomes more normal.")
    except Exception as exc:
        st.error(str(exc))
