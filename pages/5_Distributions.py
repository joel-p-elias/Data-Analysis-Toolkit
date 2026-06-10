import streamlit as st

from utils.distribution import binomial_distribution, fit_normal, normal_distribution, poisson_distribution
from utils.page_helpers import require_dataset, show_figure_with_download
from utils.plots import distribution_plot, histogram_with_normal_curve
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Distributions", layout="wide")
apply_global_theme()
render_navigation_sidebar("Distributions")
df = require_dataset()

st.title("Distributions")
st.caption("Explore PDF, CDF, PMF, and fitted normal distributions.")

tab_normal, tab_binomial, tab_poisson, tab_fit = st.tabs(["Normal", "Binomial", "Poisson", "Distribution Fitting"])

with tab_normal:
    mean = st.number_input("Mean", value=0.0)
    std = st.number_input("Standard deviation", value=1.0, min_value=0.0001)
    view = st.radio("Display", ["pdf", "cdf"], horizontal=True)
    try:
        dist_df = normal_distribution(mean, std)
        st.dataframe(dist_df.head(20), use_container_width=True)
        fig = distribution_plot(dist_df, view, f"Normal Distribution {view.upper()}")
        show_figure_with_download(fig, f"normal_{view}")
    except Exception as exc:
        st.error(str(exc))

with tab_binomial:
    n = st.number_input("Number of trials n", min_value=1, value=10)
    p = st.number_input("Probability of success p", min_value=0.0, max_value=1.0, value=0.5)
    view = st.radio("Display", ["pmf", "cdf"], horizontal=True, key="binomial_view")
    try:
        dist_df = binomial_distribution(int(n), p)
        st.dataframe(dist_df, use_container_width=True)
        fig = distribution_plot(dist_df, view, f"Binomial Distribution {view.upper()}")
        show_figure_with_download(fig, f"binomial_{view}")
    except Exception as exc:
        st.error(str(exc))

with tab_poisson:
    lam = st.number_input("Lambda", min_value=0.0001, value=3.0)
    view = st.radio("Display", ["pmf", "cdf"], horizontal=True, key="poisson_view")
    try:
        dist_df = poisson_distribution(lam)
        st.dataframe(dist_df, use_container_width=True)
        fig = distribution_plot(dist_df, view, f"Poisson Distribution {view.upper()}")
        show_figure_with_download(fig, f"poisson_{view}")
    except Exception as exc:
        st.error(str(exc))

with tab_fit:
    numeric_columns = st.session_state.numeric_columns
    if not numeric_columns:
        st.info("A numeric column is required.")
    else:
        column = st.selectbox("Numeric column", numeric_columns)
        if st.button("Fit normal distribution"):
            try:
                result = fit_normal(df[column])

                # Fitted parameters
                st.subheader("Fitted Parameters")
                col1, col2 = st.columns(2)
                col1.metric("Fitted Mean", f"{result['mean']:.4f}")
                col2.metric("Fitted Std Dev", f"{result['std']:.4f}")

                # Goodness-of-fit summary table
                st.subheader("Goodness-of-Fit Summary")
                import pandas as pd
                gof_decision = "Good fit" if result["ks_p_value"] >= 0.05 else "Poor fit"
                gof_df = pd.DataFrame({
                    "Measure": [
                        "Test",
                        "KS Statistic (D)",
                        "p-value",
                        "Alpha",
                        "Decision",
                        "Interpretation",
                    ],
                    "Value": [
                        "Kolmogorov-Smirnov (fitted normal)",
                        f"{result['ks_statistic']:.4f}",
                        f"{result['ks_p_value']:.4f}",
                        "0.05",
                        gof_decision,
                        "Fail to reject H0 — normal fit is plausible." if result["ks_p_value"] >= 0.05
                        else "Reject H0 — data deviates significantly from a normal distribution.",
                    ],
                })
                st.dataframe(gof_df, use_container_width=True, hide_index=True)

                if result["ks_p_value"] < 0.05:
                    st.warning("The KS test suggests the normal fit may be poor (p < 0.05). The data may follow a different distribution.")
                else:
                    st.success("The fitted normal distribution is plausible by the KS test (p ≥ 0.05).")

                fig = histogram_with_normal_curve(df[column])
                show_figure_with_download(fig, f"fitted_normal_{column}")
            except Exception as exc:
                st.error(str(exc))
