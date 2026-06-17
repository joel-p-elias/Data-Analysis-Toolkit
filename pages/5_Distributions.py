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

tab_normal, tab_binomial, tab_poisson, tab_fit, tab_compare = st.tabs(["Normal", "Binomial", "Poisson", "Distribution Fitting", "Distribution Comparison"])

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
                st.json(result)
                fig = histogram_with_normal_curve(df[column])
                show_figure_with_download(fig, f"fitted_normal_{column}")
                if result["ks_p_value"] < 0.05:
                    st.warning("The Kolmogorov-Smirnov test suggests the normal fit may be poor.")
                else:
                    st.success("The fitted normal distribution is plausible by the Kolmogorov-Smirnov test.")
            except Exception as exc:
                st.error(str(exc))

with tab_compare:
    st.markdown("**Distribution Comparison**")
    st.caption("Overlay two normal distributions or compare theoretical distributions against your data.")
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats as scipy_stats

    compare_mode = st.radio(
        "Compare",
        ["Two normal distributions", "Normal vs data column"],
        horizontal=True,
        key="compare_mode",
    )

    if compare_mode == "Two normal distributions":
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Distribution A**")
            mean_a = st.number_input("Mean A", value=0.0, key="cmp_mean_a")
            std_a = st.number_input("Std A", value=1.0, min_value=0.0001, key="cmp_std_a")
        with col_b:
            st.markdown("**Distribution B**")
            mean_b = st.number_input("Mean B", value=2.0, key="cmp_mean_b")
            std_b = st.number_input("Std B", value=1.5, min_value=0.0001, key="cmp_std_b")

        if st.button("Compare distributions", key="btn_compare_two"):
            try:
                x_min = min(mean_a - 4*std_a, mean_b - 4*std_b)
                x_max = max(mean_a + 4*std_a, mean_b + 4*std_b)
                x = np.linspace(x_min, x_max, 400)
                pdf_a = scipy_stats.norm.pdf(x, mean_a, std_a)
                pdf_b = scipy_stats.norm.pdf(x, mean_b, std_b)

                fig, ax = plt.subplots(figsize=(9, 4.5))
                ax.plot(x, pdf_a, color="#1f5f99", linewidth=2, label=f"A: N({mean_a}, {std_a})")
                ax.fill_between(x, pdf_a, alpha=0.15, color="#1f5f99")
                ax.plot(x, pdf_b, color="#e05c2e", linewidth=2, label=f"B: N({mean_b}, {std_b})")
                ax.fill_between(x, pdf_b, alpha=0.15, color="#e05c2e")
                ax.set_title("Normal Distribution Comparison (PDF)")
                ax.set_xlabel("x")
                ax.set_ylabel("Density")
                ax.legend()
                show_figure_with_download(fig, "distribution_comparison")

                col1, col2, col3 = st.columns(3)
                col1.metric("Mean difference (A - B)", f"{mean_a - mean_b:.4f}")
                col2.metric("Std ratio (A / B)", f"{std_a / std_b:.4f}")
                overlap = float(np.trapz(np.minimum(pdf_a, pdf_b), x))
                col3.metric("Overlap area", f"{overlap:.4f}")
                st.caption("Overlap area of 1.0 = identical distributions. Closer to 0 = more separated.")
            except Exception as exc:
                st.error(str(exc))

    else:
        numeric_columns = st.session_state.numeric_columns
        if not numeric_columns:
            st.info("A numeric column is required.")
        else:
            col_cmp = st.selectbox("Data column", numeric_columns, key="cmp_data_col")
            mean_cmp = st.number_input("Comparison mean", value=0.0, key="cmp_ref_mean")
            std_cmp = st.number_input("Comparison std", value=1.0, min_value=0.0001, key="cmp_ref_std")

            if st.button("Compare data vs normal", key="btn_compare_data"):
                try:
                    values = df[col_cmp].dropna().astype(float)
                    fitted_mean = float(values.mean())
                    fitted_std = float(values.std(ddof=1))
                    x = np.linspace(values.min(), values.max(), 400)

                    fig, ax = plt.subplots(figsize=(9, 4.5))
                    ax.hist(values, bins=30, density=True, alpha=0.35, color="#8fbce6",
                            edgecolor="white", label="Data histogram")
                    ax.plot(x, scipy_stats.norm.pdf(x, fitted_mean, fitted_std),
                            color="#1f5f99", linewidth=2,
                            label=f"Fitted: N({fitted_mean:.2f}, {fitted_std:.2f})")
                    ax.plot(x, scipy_stats.norm.pdf(x, mean_cmp, std_cmp),
                            color="#e05c2e", linewidth=2, linestyle="--",
                            label=f"Reference: N({mean_cmp}, {std_cmp})")
                    ax.set_title(f"Data vs Normal Distributions: {col_cmp}")
                    ax.set_xlabel(col_cmp)
                    ax.set_ylabel("Density")
                    ax.legend()
                    show_figure_with_download(fig, f"data_vs_normal_{col_cmp}")

                    ks_fitted = scipy_stats.kstest(values, "norm", args=(fitted_mean, fitted_std))
                    ks_ref = scipy_stats.kstest(values, "norm", args=(mean_cmp, std_cmp))

                    import pandas as pd
                    gof_table = pd.DataFrame({
                        "Distribution": [
                            f"Fitted N({fitted_mean:.2f}, {fitted_std:.2f})",
                            f"Reference N({mean_cmp}, {std_cmp})",
                        ],
                        "KS Statistic": [f"{ks_fitted.statistic:.4f}", f"{ks_ref.statistic:.4f}"],
                        "p-value": [f"{ks_fitted.pvalue:.4f}", f"{ks_ref.pvalue:.4f}"],
                        "Fit quality": [
                            "Good fit" if ks_fitted.pvalue >= 0.05 else "Poor fit",
                            "Good fit" if ks_ref.pvalue >= 0.05 else "Poor fit",
                        ],
                    })
                    st.subheader("Goodness-of-Fit Comparison")
                    st.dataframe(gof_table, use_container_width=True, hide_index=True)
                except Exception as exc:
                    st.error(str(exc))
