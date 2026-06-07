import streamlit as st

from utils.page_helpers import add_analysis, alpha_input, alternative_select, require_dataset, render_result, show_figure_with_download
from utils.plots import boxplot, histogram
from utils.tests_nonparametric import friedman_test, kruskal_wallis, mann_whitney_u, wilcoxon_signed_rank
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Nonparametric Tests", layout="wide")
apply_global_theme()
render_navigation_sidebar("Nonparametric Tests")
df = require_dataset()

st.title("Nonparametric Tests")
st.caption("Use these tests when normality assumptions are questionable or data are ordinal.")

numeric_columns = st.session_state.numeric_columns
categorical_columns = st.session_state.categorical_columns

tabs = st.tabs(["Mann-Whitney U", "Wilcoxon Signed-Rank", "Kruskal-Wallis", "Friedman Test"])

with tabs[0]:
    if not numeric_columns or not categorical_columns:
        st.info("A numeric outcome and categorical group column are required.")
    else:
        outcome = st.selectbox("Numeric outcome", numeric_columns, key="mw_outcome")
        group_col = st.selectbox("Group column", categorical_columns, key="mw_group")
        groups = df[group_col].dropna().unique().tolist()
        if len(groups) < 2:
            st.info("The selected group column must contain at least two groups.")
        else:
            group_a = st.selectbox("Group A", groups, key="mw_a")
            group_b = st.selectbox("Group B", [g for g in groups if g != group_a], key="mw_b")
            alpha = alpha_input("alpha_mw")
            alternative = alternative_select("alt_mw")
            if st.button("Run Mann-Whitney U"):
                try:
                    result = mann_whitney_u(
                        df.loc[df[group_col] == group_a, outcome],
                        df.loc[df[group_col] == group_b, outcome],
                        alpha,
                        alternative,
                    )
                    render_result(result)
                    add_analysis(result)
                    subset = df[df[group_col].isin([group_a, group_b])]
                    show_figure_with_download(boxplot(subset, y=outcome, x=group_col), f"mann_whitney_{outcome}")
                except Exception as exc:
                    st.error(str(exc))

with tabs[1]:
    if len(numeric_columns) < 2:
        st.info("Two numeric columns are required.")
    else:
        before = st.selectbox("First measurement", numeric_columns, key="wil_before")
        after = st.selectbox("Second measurement", numeric_columns, key="wil_after")
        alpha = alpha_input("alpha_wil")
        alternative = alternative_select("alt_wil")
        if st.button("Run Wilcoxon signed-rank"):
            try:
                result = wilcoxon_signed_rank(df[before], df[after], alpha, alternative)
                render_result(result)
                add_analysis(result)
                differences = (df[after] - df[before]).rename("paired difference")
                show_figure_with_download(histogram(differences), f"wilcoxon_{before}_{after}")
            except Exception as exc:
                st.error(str(exc))

with tabs[2]:
    if not numeric_columns or not categorical_columns:
        st.info("A numeric outcome and categorical group column are required.")
    else:
        outcome = st.selectbox("Numeric outcome", numeric_columns, key="kw_outcome")
        group_col = st.selectbox("Group column", categorical_columns, key="kw_group")
        groups = {str(group): df.loc[df[group_col] == group, outcome] for group in df[group_col].dropna().unique()}
        alpha = alpha_input("alpha_kw")
        if st.button("Run Kruskal-Wallis"):
            try:
                result = kruskal_wallis(groups, alpha)
                render_result(result)
                add_analysis(result)
                show_figure_with_download(boxplot(df, y=outcome, x=group_col), f"kruskal_{outcome}")
            except Exception as exc:
                st.error(str(exc))

with tabs[3]:
    if len(numeric_columns) < 3:
        st.info("At least three numeric columns are required for related measurements.")
    else:
        selected = st.multiselect("Related measurement columns", numeric_columns, default=numeric_columns[:3])
        alpha = alpha_input("alpha_friedman")
        if st.button("Run Friedman test"):
            try:
                result = friedman_test([df[column] for column in selected], selected, alpha)
                render_result(result)
                add_analysis(result)
                st.line_chart(df[selected].reset_index(drop=True))
            except Exception as exc:
                st.error(str(exc))
