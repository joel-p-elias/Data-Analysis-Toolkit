import streamlit as st

from utils.anova import one_way_anova, two_way_anova
from utils.page_helpers import add_analysis, alpha_input, require_dataset, render_result, show_figure_with_download
from utils.plots import boxplot, interaction_plot
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="ANOVA", layout="wide")
apply_global_theme()
render_navigation_sidebar("ANOVA")
df = require_dataset()

st.title("ANOVA")
st.caption("Compare group means with one-way and two-way ANOVA.")

numeric_columns = st.session_state.numeric_columns
categorical_columns = st.session_state.categorical_columns

tab_one, tab_two = st.tabs(["One-way ANOVA", "Two-way ANOVA"])

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
