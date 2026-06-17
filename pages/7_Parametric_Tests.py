import numpy as np
import pandas as pd
import streamlit as st

from utils.page_helpers import add_analysis, alpha_input, alternative_select, require_dataset, render_result, show_figure_with_download
from utils.plots import boxplot, histogram, observed_expected_bar, regression_plot, scatterplot
from utils.tests_parametric import (
    chi_square_goodness_of_fit,
    chi_square_independence,
    correlation_significance,
    independent_t_test,
    one_proportion_z_test,
    one_sample_t_test,
    paired_t_test,
    regression_coefficient_significance,
    two_proportion_z_test,
)
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Parametric Tests", layout="wide")
apply_global_theme()
render_navigation_sidebar("Parametric Tests")
df = require_dataset()

st.title("Parametric Tests")
st.caption("Select inputs carefully. The app checks basic requirements before running each test.")

numeric_columns = st.session_state.numeric_columns
categorical_columns = st.session_state.categorical_columns

tabs = st.tabs(
    [
        "One-sample t-test",
        "Independent t-test",
        "Paired t-test",
        "One-proportion z-test",
        "Two-proportion z-test",
        "Chi-square GOF",
        "Chi-square Independence",
        "Correlation",
        "Regression",
        "Confidence Intervals",
    ]
)

with tabs[0]:
    if not numeric_columns:
        st.info("A numeric column is required.")
    else:
        column = st.selectbox("Sample column", numeric_columns, key="one_sample_col")
        population_mean = st.number_input("Hypothesized population mean", value=0.0)
        alpha = alpha_input("alpha_one_sample")
        alternative = alternative_select("alt_one_sample")
        if st.button("Run one-sample t-test"):
            try:
                result = one_sample_t_test(df[column], population_mean, alpha, alternative)
                render_result(result)
                add_analysis(result)
                show_figure_with_download(histogram(df[column]), f"one_sample_t_{column}")
            except Exception as exc:
                st.error(str(exc))

with tabs[1]:
    if not numeric_columns or not categorical_columns:
        st.info("A numeric outcome and categorical group column are required.")
    else:
        outcome = st.selectbox("Numeric outcome", numeric_columns, key="ind_t_outcome")
        group_col = st.selectbox("Group column", categorical_columns, key="ind_t_group")
        groups = df[group_col].dropna().unique().tolist()
        if len(groups) < 2:
            st.info("The selected group column must contain at least two groups.")
        else:
            group_a = st.selectbox("Group A", groups, key="ind_t_a")
            group_b = st.selectbox("Group B", [g for g in groups if g != group_a], key="ind_t_b")
            equal_var = st.checkbox("Assume equal variances", value=False)
            alpha = alpha_input("alpha_ind_t")
            alternative = alternative_select("alt_ind_t")
            if st.button("Run independent t-test"):
                try:
                    result = independent_t_test(
                        df.loc[df[group_col] == group_a, outcome],
                        df.loc[df[group_col] == group_b, outcome],
                        equal_var,
                        alpha,
                        alternative,
                    )
                    render_result(result)
                    add_analysis(result)
                    subset = df[df[group_col].isin([group_a, group_b])]
                    show_figure_with_download(boxplot(subset, y=outcome, x=group_col), f"independent_t_{outcome}")
                except Exception as exc:
                    st.error(str(exc))

with tabs[2]:
    if len(numeric_columns) < 2:
        st.info("Two numeric columns are required.")
    else:
        before = st.selectbox("First paired measurement", numeric_columns, key="paired_before")
        after = st.selectbox("Second paired measurement", numeric_columns, key="paired_after")
        alpha = alpha_input("alpha_paired")
        alternative = alternative_select("alt_paired")
        if st.button("Run paired t-test"):
            try:
                result = paired_t_test(df[before], df[after], alpha, alternative)
                render_result(result)
                add_analysis(result)
                differences = (df[after] - df[before]).rename("paired difference")
                show_figure_with_download(histogram(differences), f"paired_t_{before}_{after}")
            except Exception as exc:
                st.error(str(exc))

with tabs[3]:
    successes = st.number_input("Number of successes", min_value=0, value=50)
    nobs = st.number_input("Number of observations", min_value=1, value=100)
    p0 = st.number_input("Hypothesized proportion", min_value=0.0001, max_value=0.9999, value=0.5)
    alpha = alpha_input("alpha_one_prop")
    alternative = alternative_select("alt_one_prop")
    if st.button("Run one-proportion z-test"):
        try:
            result = one_proportion_z_test(int(successes), int(nobs), p0, alpha, alternative)
            render_result(result)
            add_analysis(result)
            z_values = pd.Series(np.random.default_rng(42).normal(size=5000), name="standard normal z")
            show_figure_with_download(histogram(z_values), "one_proportion_z_curve")
        except Exception as exc:
            st.error(str(exc))

with tabs[4]:
    col_a, col_b = st.columns(2)
    with col_a:
        successes_a = st.number_input("Group A successes", min_value=0, value=45)
        nobs_a = st.number_input("Group A observations", min_value=1, value=100)
    with col_b:
        successes_b = st.number_input("Group B successes", min_value=0, value=35)
        nobs_b = st.number_input("Group B observations", min_value=1, value=100)
    alpha = alpha_input("alpha_two_prop")
    alternative = alternative_select("alt_two_prop")
    if st.button("Run two-proportion z-test"):
        try:
            result = two_proportion_z_test(int(successes_a), int(nobs_a), int(successes_b), int(nobs_b), alpha, alternative)
            render_result(result)
            add_analysis(result)
            proportions = pd.Series([successes_a / nobs_a, successes_b / nobs_b], index=["Group A", "Group B"], name="proportion")
            show_figure_with_download(observed_expected_bar(proportions), "two_proportion_comparison")
        except Exception as exc:
            st.error(str(exc))

with tabs[5]:
    if not categorical_columns:
        st.info("A categorical column is required.")
    else:
        column = st.selectbox("Categorical column", categorical_columns, key="gof_col")
        counts = df[column].value_counts().sort_index()
        st.write("Observed counts")
        st.dataframe(counts.rename("count"))
        expected_mode = st.radio("Expected counts", ["Equal expected counts", "Manual comma-separated counts"])
        expected = None
        if expected_mode == "Manual comma-separated counts":
            raw_expected = st.text_input("Expected counts in the same category order", value=",".join([str(int(counts.mean()))] * len(counts)))
            try:
                expected = [float(value.strip()) for value in raw_expected.split(",") if value.strip()]
            except ValueError:
                st.error("Expected counts must be numbers separated by commas.")
        alpha = alpha_input("alpha_gof")
        if st.button("Run chi-square goodness-of-fit"):
            try:
                result = chi_square_goodness_of_fit(counts.values, expected, alpha)
                render_result(result)
                add_analysis(result)
                show_figure_with_download(observed_expected_bar(counts, expected), f"chi_square_gof_{column}")
            except Exception as exc:
                st.error(str(exc))

with tabs[6]:
    if len(categorical_columns) < 2:
        st.info("Two categorical columns are required.")
    else:
        row_col = st.selectbox("Row variable", categorical_columns, key="chi_row")
        col_col = st.selectbox("Column variable", [c for c in categorical_columns if c != row_col], key="chi_col")
        table = pd.crosstab(df[row_col], df[col_col])
        st.dataframe(table, use_container_width=True)
        alpha = alpha_input("alpha_chi_ind")
        if st.button("Run chi-square independence"):
            try:
                result, expected = chi_square_independence(table, alpha)
                render_result(result)
                add_analysis(result)
                st.write("Expected counts")
                st.dataframe(expected, use_container_width=True)
                show_figure_with_download(observed_expected_bar(table.to_numpy().ravel(), expected.to_numpy().ravel()), "chi_square_independence")
            except Exception as exc:
                st.error(str(exc))

with tabs[7]:
    if len(numeric_columns) < 2:
        st.info("Two numeric columns are required.")
    else:
        x = st.selectbox("X variable", numeric_columns, key="corr_x")
        y = st.selectbox("Y variable", [c for c in numeric_columns if c != x], key="corr_y")
        alpha = alpha_input("alpha_corr")
        if st.button("Run correlation significance test"):
            try:
                result = correlation_significance(df[x], df[y], alpha)
                render_result(result)
                add_analysis(result)
                show_figure_with_download(scatterplot(df, x=x, y=y), f"correlation_{x}_{y}")
            except Exception as exc:
                st.error(str(exc))

with tabs[8]:
    if len(numeric_columns) < 2:
        st.info("Two numeric columns are required.")
    else:
        y = st.selectbox("Outcome variable", numeric_columns, key="reg_y")
        x = st.selectbox("Predictor variable", [c for c in numeric_columns if c != y], key="reg_x")
        alpha = alpha_input("alpha_reg")
        if st.button("Run regression coefficient test"):
            try:
                result, model = regression_coefficient_significance(df, y, x, alpha)
                render_result(result)
                add_analysis(result)
                st.text(model.summary().as_text())
                show_figure_with_download(regression_plot(df, x=x, y=y), f"regression_{x}_{y}")
            except Exception as exc:
                st.error(str(exc))

with tabs[9]:
    st.markdown("**Confidence Intervals**")
    st.caption("Estimate the range likely to contain the true population parameter.")

    ci_type = st.selectbox(
        "Interval type",
        ["One-sample mean (Z)", "One-sample mean (t)", "Difference of two means"],
        key="ci_type",
    )
    confidence = st.slider("Confidence level (%)", min_value=80, max_value=99, value=95, step=1, key="ci_conf")
    alpha_ci = 1 - confidence / 100

    if ci_type == "One-sample mean (Z)":
        st.caption("Use when population std (σ) is known and n ≥ 30.")
        if not numeric_columns:
            st.info("A numeric column is required.")
        else:
            col_ci = st.selectbox("Numeric column", numeric_columns, key="ci_z_col")
            sigma = st.number_input("Known population std (σ)", min_value=0.0001, value=1.0, key="ci_z_sigma")
            if st.button("Calculate Z confidence interval", key="btn_ci_z"):
                try:
                    from scipy import stats as scipy_stats
                    import math
                    values = df[col_ci].dropna().astype(float)
                    n = len(values)
                    xbar = float(values.mean())
                    se = sigma / math.sqrt(n)
                    z_crit = float(scipy_stats.norm.ppf(1 - alpha_ci / 2))
                    lower = xbar - z_crit * se
                    upper = xbar + z_crit * se
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Sample mean", f"{xbar:.4f}")
                    col2.metric("Standard error", f"{se:.4f}")
                    col3.metric("Z critical value", f"{z_crit:.4f}")
                    st.success(f"{confidence}% Confidence Interval: ({lower:.4f},  {upper:.4f})")
                    st.markdown(f"**Interpretation:** We are {confidence}% confident the true population mean lies between **{lower:.4f}** and **{upper:.4f}**.")
                    add_analysis({
                        "test_name": f"{confidence}% CI for mean (Z)",
                        "h0": "N/A", "ha": "N/A",
                        "statistic_name": "Z critical",
                        "statistic": z_crit,
                        "p_value": alpha_ci,
                        "degrees_of_freedom": None,
                        "alpha": alpha_ci,
                        "decision": f"CI: ({lower:.4f}, {upper:.4f})",
                        "interpretation": f"{confidence}% confident true mean is between {lower:.4f} and {upper:.4f}.",
                        "inputs": {"column": col_ci, "n": n, "sigma": sigma, "confidence": confidence},
                    })
                except Exception as exc:
                    st.error(str(exc))

    elif ci_type == "One-sample mean (t)":
        st.caption("Use when population std (σ) is unknown — uses sample std and t-distribution.")
        if not numeric_columns:
            st.info("A numeric column is required.")
        else:
            col_ci = st.selectbox("Numeric column", numeric_columns, key="ci_t_col")
            if st.button("Calculate t confidence interval", key="btn_ci_t"):
                try:
                    from scipy import stats as scipy_stats
                    import math
                    values = df[col_ci].dropna().astype(float)
                    n = len(values)
                    xbar = float(values.mean())
                    s = float(values.std(ddof=1))
                    se = s / math.sqrt(n)
                    df_t = n - 1
                    t_crit = float(scipy_stats.t.ppf(1 - alpha_ci / 2, df=df_t))
                    lower = xbar - t_crit * se
                    upper = xbar + t_crit * se
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Sample mean", f"{xbar:.4f}")
                    col2.metric("Sample std", f"{s:.4f}")
                    col3.metric("Standard error", f"{se:.4f}")
                    col4.metric("t critical (df=" + str(df_t) + ")", f"{t_crit:.4f}")
                    st.success(f"{confidence}% Confidence Interval: ({lower:.4f},  {upper:.4f})")
                    st.markdown(f"**Interpretation:** We are {confidence}% confident the true population mean lies between **{lower:.4f}** and **{upper:.4f}**.")
                    add_analysis({
                        "test_name": f"{confidence}% CI for mean (t)",
                        "h0": "N/A", "ha": "N/A",
                        "statistic_name": "t critical",
                        "statistic": t_crit,
                        "p_value": alpha_ci,
                        "degrees_of_freedom": df_t,
                        "alpha": alpha_ci,
                        "decision": f"CI: ({lower:.4f}, {upper:.4f})",
                        "interpretation": f"{confidence}% confident true mean is between {lower:.4f} and {upper:.4f}.",
                        "inputs": {"column": col_ci, "n": n, "sample_std": s, "confidence": confidence},
                    })
                except Exception as exc:
                    st.error(str(exc))

    else:
        st.caption("Estimates the difference between two independent group means.")
        if not numeric_columns or not categorical_columns:
            st.info("A numeric outcome and categorical group column are required.")
        else:
            outcome_ci = st.selectbox("Numeric outcome", numeric_columns, key="ci_diff_outcome")
            group_col_ci = st.selectbox("Group column", categorical_columns, key="ci_diff_group")
            groups_ci = df[group_col_ci].dropna().unique().tolist()
            if len(groups_ci) < 2:
                st.info("The group column must contain at least two groups.")
            else:
                ga = st.selectbox("Group A", groups_ci, key="ci_diff_a")
                gb = st.selectbox("Group B", [g for g in groups_ci if g != ga], key="ci_diff_b")
                if st.button("Calculate difference CI", key="btn_ci_diff"):
                    try:
                        from scipy import stats as scipy_stats
                        import math
                        vals_a = df.loc[df[group_col_ci] == ga, outcome_ci].dropna().astype(float)
                        vals_b = df.loc[df[group_col_ci] == gb, outcome_ci].dropna().astype(float)
                        na, nb = len(vals_a), len(vals_b)
                        xa, xb = float(vals_a.mean()), float(vals_b.mean())
                        sa, sb = float(vals_a.std(ddof=1)), float(vals_b.std(ddof=1))
                        se = math.sqrt(sa**2 / na + sb**2 / nb)
                        num = (sa**2/na + sb**2/nb)**2
                        den = (sa**2/na)**2/(na-1) + (sb**2/nb)**2/(nb-1)
                        df_w = num / den
                        t_crit = float(scipy_stats.t.ppf(1 - alpha_ci / 2, df=df_w))
                        diff = xa - xb
                        lower = diff - t_crit * se
                        upper = diff + t_crit * se
                        col1, col2, col3 = st.columns(3)
                        col1.metric(f"Mean {ga}", f"{xa:.4f}")
                        col2.metric(f"Mean {gb}", f"{xb:.4f}")
                        col3.metric("Difference (A - B)", f"{diff:.4f}")
                        st.success(f"{confidence}% CI for difference: ({lower:.4f},  {upper:.4f})")
                        if lower > 0:
                            st.markdown(f"**Interpretation:** We are {confidence}% confident that Group A has a higher mean than Group B. The difference is between {lower:.4f} and {upper:.4f}.")
                        elif upper < 0:
                            st.markdown(f"**Interpretation:** We are {confidence}% confident that Group B has a higher mean. The difference (A-B) is between {lower:.4f} and {upper:.4f}.")
                        else:
                            st.markdown(f"**Interpretation:** The CI contains zero — we cannot confidently say which group has a higher mean at the {confidence}% confidence level.")
                    except Exception as exc:
                        st.error(str(exc))
