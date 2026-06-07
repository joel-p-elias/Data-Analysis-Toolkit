import streamlit as st

from utils.data_loader import missing_value_table
from utils.page_helpers import require_dataset, update_dataset
from utils.preprocessing import (
    DEFAULT_MISSING_VALUE_STRATEGY,
    MISSING_VALUE_STRATEGIES,
    coerce_columns_to_numeric,
    handle_missing_values,
    remove_duplicates,
)
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Data Cleaning", layout="wide")
apply_global_theme()
render_navigation_sidebar("Data Cleaning")
df = require_dataset()

st.title("Data Cleaning")
st.caption("Choose how missing values and duplicates should be handled.")

st.subheader("Current Missing Values")
st.dataframe(missing_value_table(df), use_container_width=True)

strategy = st.radio(
    "Missing-value method",
    MISSING_VALUE_STRATEGIES,
    index=MISSING_VALUE_STRATEGIES.index(st.session_state.get("missing_value_strategy", DEFAULT_MISSING_VALUE_STRATEGY)),
)
st.session_state.missing_value_strategy = strategy

remove_dupes = st.checkbox("Remove duplicate rows", value=True)

object_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
columns_to_convert = st.multiselect(
    "Optional: convert selected text columns to numeric",
    object_columns,
    help="Use this if numbers were imported as text. Invalid values become missing.",
)

if st.button("Apply cleaning", type="primary"):
    cleaned = df.copy()
    actions = []

    if columns_to_convert:
        cleaned = coerce_columns_to_numeric(cleaned, columns_to_convert)
        actions.append(f"Converted columns to numeric: {', '.join(columns_to_convert)}")

    cleaned, missing_report = handle_missing_values(cleaned, strategy)
    actions.append(
        f"Missing values changed from {missing_report['missing_before']} to {missing_report['missing_after']} using {strategy}."
    )

    if remove_dupes:
        cleaned, duplicate_count = remove_duplicates(cleaned)
        actions.append(f"Removed {duplicate_count} duplicate rows.")

    update_dataset(cleaned, st.session_state.dataset_name or "cleaned_dataset")
    st.success("Cleaning complete.")
    for action in actions:
        st.write(f"- {action}")

st.subheader("Cleaned Preview")
st.dataframe(st.session_state.dataset.head(50), use_container_width=True)
