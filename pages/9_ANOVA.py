import streamlit as st

from utils.anova import one_way_anova, two_way_anova
from utils.page_helpers import add_analysis, alpha_input, require_dataset, render_result, show_figure_with_download
from utils.plots import boxplot, interaction_plot
from utils.theme import apply_global_theme, render_navigation_sidebar
from statsmodels.stats.multicomp import pairwise_tukeyhsd


st.set_page_config(page_title="ANOVA", layout="wide")
apply_global_theme()
render_navigation_sidebar("ANOVA")
df = require_dataset()

st.title("ANOVA")
st.caption("Compare group means with one-way and two-way ANOVA.")

numeric_columns = st.session_state.numeric_columns
categorical_columns = st.session_state.categorical_columns

tab_one, tab_two, tab_posthoc = st.tabs(["One-way ANOVA", "Two-way ANOVA", "Post-hoc (Tukey HSD)"])

with tab_one:
    if not numeric_columns or not categorical_columns:
        st.info("A numeric outcome and categorical factor are required.")
    else:
        outcome = st.selectbox("Numeric outcome", numeric_columns, key="anova1_outcome")
        factor = st.selectbox("Factor", categorical_columns, key="anova1_factor")
        groups = {str(group): df.loc[df[factor] == group, outcome] for group in df[factor].dropna().unique()}
        alpha = alpha_input("alpha_anova1")
        if st.button("Run one-way ANOVA"):
            try:
                result = one_way_anova(groups, alpha)
                render_result(result)
                add_analysis(result)
                show_figure_with_download(boxplot(df, y=outcome, x=factor), f"one_way_anova_{outcome}")
            except Exception as exc:
                st.error(str(exc))

with tab_two:
    if not numeric_columns or len(categorical_columns) < 2:
        st.info("A numeric outcome and two categorical factors are required.")
    else:
        outcome = st.selectbox("Numeric outcome", numeric_columns, key="anova2_outcome")
        factor_a = st.selectbox("Factor A", categorical_columns, key="anova2_factor_a")
        factor_b = st.selectbox("Factor B", [c for c in categorical_columns if c != factor_a], key="anova2_factor_b")
        alpha = alpha_input("alpha_anova2")
        if st.button("Run two-way ANOVA"):
            try:
                table, model = two_way_anova(df, outcome, factor_a, factor_b, alpha)
                st.subheader("Two-way ANOVA Table")
                st.markdown("**H0:** Each factor and the interaction have no effect on the outcome mean.")
                st.markdown("**Ha:** At least one factor or interaction affects the outcome mean.")
                st.dataframe(table, use_container_width=True)
                st.markdown("Rows with p-values below alpha reject the corresponding null hypothesis.")
                add_analysis(
                    {
                        "test_name": "Two-way ANOVA",
                        "h0": "Each factor and interaction has no effect.",
                        "ha": "At least one factor or interaction has an effect.",
                        "statistic": float(table["F"].dropna().iloc[0]) if "F" in table and not table["F"].dropna().empty else 0.0,
                        "p_value": float(table["p_value"].dropna().iloc[0]) if "p_value" in table and not table["p_value"].dropna().empty else 1.0,
                        "decision": "See ANOVA table by source.",
                        "interpretation": "Evaluate each factor and interaction row separately.",
                    }
                )
                show_figure_with_download(boxplot(df, y=outcome, x=factor_a), f"two_way_anova_boxplot_{outcome}")
                show_figure_with_download(interaction_plot(df, outcome, factor_a, factor_b), f"interaction_{factor_a}_{factor_b}")
            except Exception as exc:
                st.error(str(exc))

with tab_posthoc:
    st.markdown("**Tukey's HSD Post-hoc Test**")
    st.caption(
        "Run this after a significant one-way ANOVA to find which specific group pairs differ. "
        "Tukey's HSD controls the family-wise error rate across all pairwise comparisons."
    )

    if not numeric_columns or not categorical_columns:
        st.info("A numeric outcome and categorical factor are required.")
    else:
        outcome_ph = st.selectbox("Numeric outcome", numeric_columns, key="ph_outcome")
        factor_ph = st.selectbox("Factor (group column)", categorical_columns, key="ph_factor")
        alpha_ph = alpha_input("alpha_ph")

        if st.button("Run Tukey HSD", type="primary", key="btn_tukey"):
            try:
                import pandas as pd
                data_ph = df[[outcome_ph, factor_ph]].dropna()
                if data_ph[factor_ph].nunique() < 3:
                    st.warning("Tukey HSD is most useful when comparing 3 or more groups. For 2 groups use an independent t-test.")

                tukey = pairwise_tukeyhsd(
                    endog=data_ph[outcome_ph].astype(float),
                    groups=data_ph[factor_ph].astype(str),
                    alpha=alpha_ph,
                )

                st.subheader("Tukey HSD Results")
                result_df = pd.DataFrame(
                    data=tukey._results_table.data[1:],
                    columns=tukey._results_table.data[0],
                )
                result_df.columns = ["Group 1", "Group 2", "Mean diff", "p-adj", "Lower CI", "Upper CI", "Reject H₀"]
                result_df["Mean diff"] = result_df["Mean diff"].apply(lambda x: round(float(x), 4))
                result_df["p-adj"] = result_df["p-adj"].apply(lambda x: round(float(x), 4))
                result_df["Lower CI"] = result_df["Lower CI"].apply(lambda x: round(float(x), 4))
                result_df["Upper CI"] = result_df["Upper CI"].apply(lambda x: round(float(x), 4))
                st.dataframe(result_df, use_container_width=True, hide_index=True)

                significant_pairs = result_df[result_df["Reject H₀"] == True]
                if len(significant_pairs) == 0:
                    st.info("No significant pairwise differences found at the selected alpha level.")
                else:
                    st.success(f"{len(significant_pairs)} significant pair(s) found:")
                    for _, row in significant_pairs.iterrows():
                        st.markdown(
                            f"- **{row['Group 1']}** vs **{row['Group 2']}**: "
                            f"mean difference = {row['Mean diff']}, p-adj = {row['p-adj']}"
                        )

                st.markdown(
                    "**How to read:** p-adj is the adjusted p-value for each pair. "
                    "'Reject H₀ = True' means that pair has a statistically significant difference. "
                    "The CI columns show the 95% confidence interval for the mean difference."
                )

                show_figure_with_download(boxplot(df, y=outcome_ph, x=factor_ph), f"tukey_boxplot_{outcome_ph}")

                add_analysis({
                    "test_name": "Tukey HSD post-hoc test",
                    "h0": "Each pair of group means is equal.",
                    "ha": "At least one pair of group means differs.",
                    "statistic": len(significant_pairs),
                    "p_value": alpha_ph,
                    "decision": f"{len(significant_pairs)} significant pair(s) found.",
                    "interpretation": "See Tukey HSD table for pairwise comparisons.",
                    "inputs": {"outcome": outcome_ph, "factor": factor_ph},
                })
            except Exception as exc:
                st.error(str(exc))
