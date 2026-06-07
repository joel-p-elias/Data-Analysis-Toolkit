import streamlit as st

from utils import statistics as stats_utils
from utils.data_loader import dataset_overview
from utils.page_helpers import require_dataset
from utils.report_generator import generate_pdf_report
from utils.theme import apply_global_theme, render_navigation_sidebar


st.set_page_config(page_title="Report", layout="wide")
apply_global_theme()
render_navigation_sidebar("Report")
df = require_dataset()

st.title("Report Generation")
st.caption("Create a PDF report containing dataset summary, analyses, interpretations, and saved plots.")

include_descriptive = st.checkbox("Include descriptive statistics", value=True)
include_normality = st.checkbox("Include normality summary", value=True)
include_plots = st.checkbox("Include generated plots", value=True)

st.subheader("Current Analysis Log")
if st.session_state.analysis_log:
    for item in st.session_state.analysis_log:
        st.write(f"- {item.get('test_name', 'Analysis')}: {item.get('decision', 'No decision recorded')}")
else:
    st.info("No analyses have been logged yet. Run tests or visualizations first.")

if st.button("Generate PDF report", type="primary"):
    tables = []
    if include_descriptive:
        summary = stats_utils.numeric_descriptive_statistics(df)
        if not summary.empty:
            tables.append(("Numeric Descriptive Statistics", summary.reset_index().rename(columns={"index": "column"})))

    if include_normality:
        normality = stats_utils.normality_summary(df)
        if not normality.empty:
            tables.append(("Normality Summary", normality))

    plot_pngs = [item["png"] for item in st.session_state.generated_plots] if include_plots else []

    try:
        pdf = generate_pdf_report(
            "Data Analysis Toolkit Report",
            dataset_overview(df),
            st.session_state.analysis_log,
            tables=tables,
            plot_pngs=plot_pngs,
        )
        st.download_button("Download PDF report", data=pdf, file_name="data_analysis_report.pdf", mime="application/pdf")
        st.success("Report generated.")
    except Exception as exc:
        st.error(str(exc))
