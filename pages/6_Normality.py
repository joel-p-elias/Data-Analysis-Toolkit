import streamlit as st

from utils.page_helpers import add_analysis, require_dataset, render_result, show_figure_with_download
from utils.plots import histogram_with_normal_curve, qq_plot
from utils.statistics import anderson_normality, ks_normality, shapiro_normality
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Normality", layout="wide")
apply_global_theme()
render_navigation_sidebar("Normality")
df = require_dataset()

st.title("Normality Analysis")
st.caption("Test whether a numeric variable follows a normal distribution.")

numeric_columns = st.session_state.numeric_columns
if not numeric_columns:
    st.info("A numeric column is required.")
    st.stop()

tab_sw, tab_ks, tab_ad = st.tabs([
    "Shapiro-Wilk",
    "Kolmogorov-Smirnov",
    "Anderson-Darling",
])

# ── Shared column selector above tabs ────────────────────────────────────────
column = st.selectbox("Numeric column", numeric_columns)

# ── Tab 1: Shapiro-Wilk ───────────────────────────────────────────────────────
with tab_sw:
    st.markdown("**Shapiro-Wilk Test**")
    st.caption(
        "Tests whether the sample could plausibly come from a normal distribution. "
        "Best for sample sizes up to ~5,000. Uses a random sub-sample of 5,000 for larger datasets."
    )
    alpha_sw = st.number_input("Significance level alpha", min_value=0.001, max_value=0.2,
                                value=0.05, step=0.01, key="alpha_sw")

    if st.button("Run Shapiro-Wilk test", type="primary", key="btn_sw"):
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
                "alpha": alpha_sw,
                "decision": "Reject H0" if raw["p_value"] < alpha_sw else "Fail to reject H0",
                "interpretation": raw["interpretation"],
                "inputs": {"column": column, "sample_size": raw["sample_size"]},
            }
            render_result(result)
            add_analysis(result)

            col_hist, col_qq = st.columns(2)
            with col_hist:
                fig = histogram_with_normal_curve(df[column])
                show_figure_with_download(fig, f"sw_normal_curve_{column}")
            with col_qq:
                fig = qq_plot(df[column])
                show_figure_with_download(fig, f"sw_qq_plot_{column}")

            if raw["p_value"] < alpha_sw:
                st.warning(
                    "Normality may be violated. Consider a nonparametric test "
                    "if this variable is used in group comparisons."
                )
        except Exception as exc:
            st.error(str(exc))

# ── Tab 2: Kolmogorov-Smirnov ─────────────────────────────────────────────────
with tab_ks:
    st.markdown("**Kolmogorov-Smirnov Test**")
    st.caption(
        "Compares the empirical distribution of the sample against a fitted normal distribution. "
        "Works for any sample size but can be conservative. "
        "Uses the sample mean and standard deviation to define the reference distribution."
    )
    alpha_ks = st.number_input("Significance level alpha", min_value=0.001, max_value=0.2,
                                value=0.05, step=0.01, key="alpha_ks")

    if st.button("Run Kolmogorov-Smirnov test", type="primary", key="btn_ks"):
        try:
            raw = ks_normality(df[column])
            result = {
                "test_name": "Kolmogorov-Smirnov normality test",
                "h0": "The data come from a normal distribution.",
                "ha": "The data do not come from a normal distribution.",
                "statistic_name": "D",
                "statistic": raw["statistic"],
                "p_value": raw["p_value"],
                "degrees_of_freedom": None,
                "alpha": alpha_ks,
                "decision": "Reject H0" if raw["p_value"] < alpha_ks else "Fail to reject H0",
                "interpretation": raw["interpretation"],
                "inputs": {"column": column, "sample_size": raw["sample_size"]},
            }
            render_result(result)
            add_analysis(result)

            st.info(raw["note"])

            col_hist, col_qq = st.columns(2)
            with col_hist:
                fig = histogram_with_normal_curve(df[column])
                show_figure_with_download(fig, f"ks_normal_curve_{column}")
            with col_qq:
                fig = qq_plot(df[column])
                show_figure_with_download(fig, f"ks_qq_plot_{column}")

            if raw["p_value"] < alpha_ks:
                st.warning(
                    "Normality may be violated. Consider a nonparametric test "
                    "if this variable is used in group comparisons."
                )
        except Exception as exc:
            st.error(str(exc))

# ── Tab 3: Anderson-Darling ───────────────────────────────────────────────────
with tab_ad:
    st.markdown("**Anderson-Darling Test**")
    st.caption(
        "A more powerful alternative to KS that gives greater weight to the tails of the distribution. "
        "Does not produce a p-value — the decision is based on comparing the test statistic "
        "against critical values at standard significance levels."
    )

    if st.button("Run Anderson-Darling test", type="primary", key="btn_ad"):
        try:
            raw = anderson_normality(df[column])

            # Display result manually since there's no p-value
            st.subheader("Anderson-Darling normality test")
            st.markdown("**H0:** The data come from a normal distribution.")
            st.markdown("**Ha:** The data do not come from a normal distribution.")

            col_stat, col_crit, col_dec = st.columns(3)
            col_stat.metric("Statistic (A²)", f"{raw['statistic']:.4f}")
            col_crit.metric("Critical value (5%)", f"{raw['critical_value_5pct']:.4f}")
            col_dec.metric("Decision", raw["decision"])

            st.markdown(f"**Interpretation:** {raw['interpretation']}")
            st.info(raw["note"])

            # Show all critical values as a small table
            with st.expander("All critical values"):
                import pandas as pd
                crit_df = pd.DataFrame(
                    list(raw["all_critical_values"].items()),
                    columns=["Significance level", "Critical value"]
                )
                st.dataframe(crit_df, use_container_width=True)

            add_analysis({
                "test_name": "Anderson-Darling normality test",
                "h0": "The data come from a normal distribution.",
                "ha": "The data do not come from a normal distribution.",
                "statistic": raw["statistic"],
                "p_value": "N/A",
                "decision": raw["decision"],
                "interpretation": raw["interpretation"],
                "inputs": {"column": column, "sample_size": raw["sample_size"]},
            })

            col_hist, col_qq = st.columns(2)
            with col_hist:
                fig = histogram_with_normal_curve(df[column])
                show_figure_with_download(fig, f"ad_normal_curve_{column}")
            with col_qq:
                fig = qq_plot(df[column])
                show_figure_with_download(fig, f"ad_qq_plot_{column}")

            if raw["decision"] == "Reject H0":
                st.warning(
                    "Normality may be violated. Consider a nonparametric test "
                    "if this variable is used in group comparisons."
                )
        except Exception as exc:
            st.error(str(exc))
