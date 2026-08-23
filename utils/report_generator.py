from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.units import inch
from io import BytesIO


def generate_pdf_report(
    dataset_name,
    df,
    quality_score,
    cleaned_df=None
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    normal_style = styles["BodyText"]

    story = []


    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            "🩺 DataDoctor AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Automatic Data Analysis & Cleaning Report",
            styles["Heading3"]
        )
    )

    story.append(Spacer(1, 20))


    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    story.append(
        Paragraph(
            "Dataset Information",
            heading_style
        )
    )

    dataset_info = [
        ["Dataset Name", str(dataset_name)],
        ["Rows", str(df.shape[0])],
        ["Columns", str(df.shape[1])],
        [
            "Missing Values",
            str(int(df.isnull().sum().sum()))
        ],
        [
            "Duplicate Rows",
            str(int(df.duplicated().sum()))
        ],
        [
            "Data Quality Score",
            f"{quality_score} / 100"
        ]
    ]


    table = Table(
        dataset_info,
        colWidths=[2.2 * inch, 3.5 * inch]
    )


    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ]
        )
    )


    story.append(table)

    story.append(Spacer(1, 20))


    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    story.append(
        Paragraph(
            "Column Information",
            heading_style
        )
    )


    column_data = [
        [
            "Column",
            "Data Type",
            "Missing Values"
        ]
    ]


    for column in df.columns:

        column_data.append(
            [
                str(column),
                str(df[column].dtype),
                str(int(df[column].isnull().sum()))
            ]
        )


    column_table = Table(
        column_data,
        colWidths=[
            2.5 * inch,
            1.7 * inch,
            1.5 * inch
        ]
    )


    column_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                )
            ]
        )
    )


    story.append(column_table)

    story.append(Spacer(1, 20))


    # ========================================================
    # CLEANING COMPARISON
    # ========================================================

    if cleaned_df is not None:

        story.append(
            Paragraph(
                "Before vs After Cleaning",
                heading_style
            )
        )


        before_missing = int(
            df.isnull().sum().sum()
        )

        after_missing = int(
            cleaned_df.isnull().sum().sum()
        )


        before_duplicates = int(
            df.duplicated().sum()
        )

        after_duplicates = int(
            cleaned_df.duplicated().sum()
        )


        after_score = quality_score


        comparison_data = [
            [
                "Metric",
                "Before",
                "After"
            ],
            [
                "Missing Values",
                str(before_missing),
                str(after_missing)
            ],
            [
                "Duplicate Rows",
                str(before_duplicates),
                str(after_duplicates)
            ],
            [
                "Rows",
                str(df.shape[0]),
                str(cleaned_df.shape[0])
            ],
            [
                "Quality Score",
                f"{quality_score} / 100",
                f"{after_score} / 100"
            ]
        ]


        comparison_table = Table(
            comparison_data,
            colWidths=[
                2.2 * inch,
                1.5 * inch,
                1.5 * inch
            ]
        )


        comparison_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.grey
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold"
                    )
                ]
            )
        )


        story.append(comparison_table)

        story.append(Spacer(1, 20))


    # ========================================================
    # FOOTER
    # ========================================================

    story.append(
        Paragraph(
            "Generated automatically by DataDoctor AI.",
            normal_style
        )
    )


    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()

