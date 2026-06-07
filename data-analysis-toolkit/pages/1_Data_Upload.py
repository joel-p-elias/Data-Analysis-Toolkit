from pathlib import Path

import streamlit as st

from utils.data_loader import dataset_overview, load_dataset, load_sample_dataset, missing_value_table
from utils.page_helpers import initialize_session_state, update_dataset
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Data Upload", layout="wide")
initialize_session_state()
apply_global_theme()
render_navigation_sidebar("Data Upload")

st.title("Data Upload")
st.caption("Upload a CSV or Excel file, or load the sample dataset.")

uploaded_file = st.file_uploader("Choose a dataset", type=["csv", "xlsx", "xls"])

col_upload, col_sample = st.columns(2)
with col_upload:
    if uploaded_file is not None and st.button("Load uploaded dataset", type="primary"):
        try:
            df = load_dataset(uploaded_file, uploaded_file.name)
            update_dataset(df, uploaded_file.name)
            st.success(f"Loaded {uploaded_file.name}")
        except Exception as exc:
            st.error(str(exc))

with col_sample:
    sample_path = Path("assets/sample_dataset.csv")
    if st.button("Load sample dataset"):
        try:
            df = load_sample_dataset(sample_path)
            update_dataset(df, sample_path.name)
            st.success("Loaded sample dataset")
        except Exception as exc:
            st.error(str(exc))

if st.session_state.dataset is not None:
    df = st.session_state.dataset
    st.subheader("Dataset Overview")
    st.json(dataset_overview(df))

    st.subheader("Column Types")
    col_num, col_cat = st.columns(2)
    col_num.write("**Numeric columns**")
    col_num.write(st.session_state.numeric_columns or "None detected")
    col_cat.write("**Categorical columns**")
    col_cat.write(st.session_state.categorical_columns or "None detected")

    st.subheader("Missing Values")
    st.dataframe(missing_value_table(df), use_container_width=True)

    st.subheader("Preview")
    st.dataframe(df.head(50), use_container_width=True)
