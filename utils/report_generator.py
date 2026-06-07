from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors


def _dataframe_to_table(df: pd.DataFrame, max_rows: int = 12, max_cols: int = 6) -> Table:
    display = df.head(max_rows).iloc[:, :max_cols].copy()
    display = display.astype(str)
    data = [display.columns.tolist()] + display.values.tolist()
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f5f99")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d8e2ec")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def generate_pdf_report(
    title: str,
    dataset_summary: dict[str, object],
    analyses: list[dict[str, object]],
    tables: list[tuple[str, pd.DataFrame]] | None = None,
    plot_pngs: list[bytes] | None = None,
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    story.append(Paragraph("Dataset Summary", styles["Heading2"]))
    summary_df = pd.DataFrame({"Metric": list(dataset_summary.keys()), "Value": [str(value) for value in dataset_summary.values()]})
    story.append(_dataframe_to_table(summary_df, max_rows=20, max_cols=2))
    story.append(Spacer(1, 12))

    if tables:
        for heading, table_df in tables:
            story.append(Paragraph(heading, styles["Heading2"]))
            story.append(_dataframe_to_table(table_df))
            story.append(Spacer(1, 12))

    if analyses:
        story.append(Paragraph("Analysis Log", styles["Heading2"]))
        for analysis in analyses:
            story.append(Paragraph(str(analysis.get("test_name", "Analysis")), styles["Heading3"]))
            for key in ["h0", "ha", "statistic", "p_value", "decision", "interpretation"]:
                if key in analysis:
                    story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {analysis[key]}", styles["BodyText"]))
            story.append(Spacer(1, 8))

    temp_plot_paths = []
    if plot_pngs:
        story.append(Paragraph("Plots", styles["Heading2"]))
        for png in plot_pngs:
            with NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(png)
                tmp_path = tmp.name
                temp_plot_paths.append(tmp_path)
            story.append(Image(tmp_path, width=460, height=260))
            story.append(Spacer(1, 10))

    doc.build(story)
    for tmp_path in temp_plot_paths:
        Path(tmp_path).unlink(missing_ok=True)
    buffer.seek(0)
    return buffer.getvalue()
