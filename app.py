# DataDoctor AI — app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.analyzer import (
    generate_insights,
    correlation_insights,
    generate_summary,
    recommend_visualizations,
    cleaning_recommendations,
    auto_clean_data,
    calculate_quality_score,
    generate_ai_recommendations
)

from utils.report_generator import generate_pdf_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DataDoctor AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM BLUE + AQUA 3D DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 191, 255, 0.15),
                transparent 25%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(0, 255, 255, 0.12),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #06142b 0%,
                #082b4f 45%,
                #063b52 100%
            );

        color: white;
    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       TITLE
       ===================================================== */

    .main-title {
        font-size: 48px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;

        background: linear-gradient(
            90deg,
            #00c6ff,
            #00f5d4,
            #48cae4,
            #00c6ff
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        text-shadow:
            0 0 20px rgba(0, 198, 255, 0.35);
    }


    /* =====================================================
       SUBTITLE
       ===================================================== */

    .subtitle {
        text-align: center;
        font-size: 19px;
        color: #b9f6ff;
        margin-bottom: 30px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #04152e 0%,
                #063b52 100%
            );

        border-right: 1px solid rgba(0, 229, 255, 0.25);
    }

    section[data-testid="stSidebar"] * {
        color: #e9fdff !important;
    }


    /* =====================================================
       METRIC CARDS - 3D
       ===================================================== */

    div[data-testid="metric-container"] {
        background:
            linear-gradient(
                145deg,
                rgba(0, 198, 255, 0.18),
                rgba(0, 255, 212, 0.08)
            );

        border: 1px solid rgba(0, 229, 255, 0.35);

        border-radius: 18px;

        padding: 18px;

        box-shadow:
            8px 8px 20px rgba(0, 0, 0, 0.35),
            inset 1px 1px 2px rgba(255, 255, 255, 0.15),
            inset -1px -1px 2px rgba(0, 0, 0, 0.3);

        transition: all 0.25s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);

        box-shadow:
            10px 12px 28px rgba(0, 0, 0, 0.45),
            0 0 20px rgba(0, 229, 255, 0.18);
    }

    div[data-testid="metric-container"] label {
        color: #9eefff !important;
    }

    div[data-testid="metric-container"] div {
        color: white !important;
    }


    /* =====================================================
       BUTTONS - 3D
       ===================================================== */

    .stButton > button,
    .stDownloadButton > button {

        background:
            linear-gradient(
                145deg,
                #0099ff,
                #00c6ff 45%,
                #00d9c0
            );

        color: white !important;

        border: 1px solid rgba(255, 255, 255, 0.25);

        border-radius: 14px;

        font-weight: 800;

        padding: 10px 20px;

        box-shadow:
            0 7px 0 #006b91,
            0 12px 22px rgba(0, 0, 0, 0.35),
            inset 0 1px 2px rgba(255, 255, 255, 0.35);

        transition: all 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {

        transform: translateY(-3px);

        box-shadow:
            0 9px 0 #006b91,
            0 16px 28px rgba(0, 0, 0, 0.45),
            0 0 20px rgba(0, 229, 255, 0.35);
    }

    .stButton > button:active,
    .stDownloadButton > button:active {

        transform: translateY(4px);

        box-shadow:
            0 3px 0 #006b91,
            0 6px 12px rgba(0, 0, 0, 0.3);
    }


    /* =====================================================
       TABS
       ===================================================== */

    button[data-baseweb="tab"] {

        background:
            linear-gradient(
                145deg,
                rgba(0, 198, 255, 0.12),
                rgba(0, 255, 212, 0.06)
            );

        border-radius: 12px;

        margin: 3px;

        color: #b8f7ff !important;

        border: 1px solid rgba(0, 229, 255, 0.15);
    }

    button[data-baseweb="tab"][aria-selected="true"] {

        background:
            linear-gradient(
                145deg,
                #008fd5,
                #00c6ff,
                #00d9c0
            );

        color: white !important;

        box-shadow:
            0 5px 12px rgba(0, 0, 0, 0.35),
            inset 0 1px 2px rgba(255, 255, 255, 0.3);
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    details {

        background:
            linear-gradient(
                145deg,
                rgba(0, 198, 255, 0.12),
                rgba(0, 255, 212, 0.05)
            ) !important;

        border:
            1px solid rgba(0, 229, 255, 0.25) !important;

        border-radius: 16px !important;

        box-shadow:
            6px 7px 18px rgba(0, 0, 0, 0.3);
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    div[data-testid="stDataFrame"] {

        border-radius: 14px;

        overflow: hidden;

        border: 1px solid rgba(0, 229, 255, 0.25);

        box-shadow:
            7px 8px 20px rgba(0, 0, 0, 0.35);
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    section[data-testid="stFileUploaderDropzone"] {

        background:
            linear-gradient(
                145deg,
                rgba(0, 198, 255, 0.15),
                rgba(0, 255, 212, 0.08)
            );

        border:
            2px dashed rgba(0, 229, 255, 0.45);

        border-radius: 18px;

        box-shadow:
            inset 0 2px 5px rgba(255, 255, 255, 0.05),
            8px 10px 25px rgba(0, 0, 0, 0.3);
    }


    /* =====================================================
       HEADERS
       ===================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #e8fdff !important;
    }


    /* =====================================================
       NORMAL TEXT
       ===================================================== */

    p,
    li,
    span {
        color: #d8faff;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* =====================================================
       DIVIDER
       ===================================================== */

    hr {
        border-color: rgba(0, 229, 255, 0.20);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "df" not in st.session_state:
    st.session_state["df"] = None

if "cleaned_df" not in st.session_state:
    st.session_state["cleaned_df"] = None

if "cleaning_log" not in st.session_state:
    st.session_state["cleaning_log"] = []

if "analyzed" not in st.session_state:
    st.session_state["analyzed"] = False

if "uploaded_filename" not in st.session_state:
    st.session_state["uploaded_filename"] = ""


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🩺 DataDoctor AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered automatic data analysis and cleaning assistant'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🩺 DataDoctor AI")

    st.write(
        "Upload your messy dataset and DataDoctor AI "
        "will automatically analyze and clean it."
    )

    st.divider()

    st.write("### 📂 Supported Files")

    st.write("• CSV")
    st.write("• Excel (.xlsx)")
    st.write("• Excel (.xls)")

    st.divider()

    st.write("### 🔍 Features")

    st.write("✅ Missing value detection")
    st.write("✅ Duplicate detection")
    st.write("✅ Outlier detection")
    st.write("✅ Correlation analysis")
    st.write("✅ Statistical analysis")
    st.write("✅ Automatic charts")
    st.write("✅ Automatic data cleaning")
    st.write("✅ Data quality score")
    st.write("✅ AI recommendations")
    st.write("✅ Before vs After comparison")
    st.write("✅ PDF report")
    st.write("✅ Download cleaned dataset")


# ============================================================
# FILE UPLOAD
# ============================================================

st.markdown("### 📂 Upload Your Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)


# ============================================================
# LOAD DATA
# ============================================================

if uploaded_file is not None:

    if st.session_state["uploaded_filename"] != uploaded_file.name:

        try:

            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state["df"] = df
            st.session_state["cleaned_df"] = None
            st.session_state["cleaning_log"] = []
            st.session_state["analyzed"] = False
            st.session_state["uploaded_filename"] = uploaded_file.name

        except Exception as e:

            st.error(
                f"❌ Could not read the uploaded file: {e}"
            )

            st.stop()


# ============================================================
# MAIN APPLICATION
# ============================================================

if st.session_state["df"] is not None:

    df = st.session_state["df"]

    st.success(
        f"✅ Successfully loaded: "
        f"{st.session_state['uploaded_filename']}"
    )


    # ========================================================
    # DATA QUALITY SCORE
    # ========================================================

    quality_score = calculate_quality_score(df)

    st.header("⭐ Data Quality Score")

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:

        st.metric(
            "Quality Score",
            f"{quality_score} / 100"
        )

    with score_col2:

        if quality_score >= 80:

            st.success("🟢 Excellent Data Quality")

        elif quality_score >= 60:

            st.warning("🟡 Moderate Data Quality")

        else:

            st.error("🔴 Poor Data Quality")

    with score_col3:

        if quality_score >= 80:

            st.write(
                "Your dataset is in good condition."
            )

        elif quality_score >= 60:

            st.write(
                "Some data quality issues need attention."
            )

        else:

            st.write(
                "Your dataset needs significant cleaning."
            )


    st.divider()


    # ========================================================
    # DATASET OVERVIEW
    # ========================================================

    st.header("📐 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Rows",
            f"{df.shape[0]:,}"
        )

    with col2:

        st.metric(
            "Columns",
            f"{df.shape[1]:,}"
        )

    with col3:

        st.metric(
            "Missing Values",
            f"{int(df.isnull().sum().sum()):,}"
        )

    with col4:

        st.metric(
            "Duplicate Rows",
            f"{int(df.duplicated().sum()):,}"
        )


    # ========================================================
    # DATA PREVIEW
    # ========================================================

    with st.expander(
        "👀 View Dataset Preview",
        expanded=True
    ):

        st.dataframe(
            df.head(10),
            use_container_width=True
        )


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    analyze_button = st.button(
        "🧠 Analyze Dataset",
        type="primary",
        use_container_width=True,
        key="analyze_dataset_button"
    )

    if analyze_button:

        st.session_state["analyzed"] = True


    # ========================================================
    # ANALYSIS
    # ========================================================

    if st.session_state["analyzed"]:

        try:

            ai_recommendations = generate_ai_recommendations(df)

        except Exception as e:

            ai_recommendations = [
                f"⚠️ AI recommendation generation failed: {e}"
            ]


        # ====================================================
        # TABS
        # ====================================================

        (
            tab1,
            tab2,
            tab3,
            tab4,
            tab5,
            tab6,
            tab7,
            tab8
        ) = st.tabs(
            [
                "🔍 Insights",
                "🔗 Correlations",
                "📊 Statistics",
                "📈 Visualizations",
                "🧹 Cleaning",
                "🤖 AI Recommendations",
                "✨ Auto Clean",
                "🔄 Before vs After"
            ]
        )


        # ====================================================
        # TAB 1 — INSIGHTS
        # ====================================================

        with tab1:

            st.subheader(
                "🔍 Basic Data Insights"
            )

            insights = generate_insights(df)

            for insight in insights:

                st.write(insight)


        # ====================================================
        # TAB 2 — CORRELATIONS
        # ====================================================

        with tab2:

            st.subheader(
                "🔗 Correlation Analysis"
            )

            correlations = correlation_insights(df)

            for correlation in correlations:

                st.write(correlation)


        # ====================================================
        # TAB 3 — STATISTICS
        # ====================================================

        with tab3:

            st.subheader(
                "📊 Statistical Summary"
            )

            summaries = generate_summary(df)

            for summary in summaries:

                st.write(summary)


        # ====================================================
        # TAB 4 — VISUALIZATIONS
        # ====================================================

        with tab4:

            st.subheader(
                "📈 Automatic Visualizations"
            )

            numerical_cols = (
                df.select_dtypes(
                    include="number"
                ).columns.tolist()
            )

            categorical_cols = (
                df.select_dtypes(
                    include=["object", "category"]
                ).columns.tolist()
            )


            # ------------------------------------------------
            # NUMERICAL DISTRIBUTIONS
            # ------------------------------------------------

            if len(numerical_cols) > 0:

                st.write(
                    "### 📊 Numerical Distributions"
                )

                for column in numerical_cols:

                    fig, ax = plt.subplots()

                    ax.hist(
                        df[column].dropna(),
                        bins=20
                    )

                    ax.set_title(
                        f"Distribution of {column}"
                    )

                    ax.set_xlabel(column)
                    ax.set_ylabel("Frequency")

                    st.pyplot(fig)

                    plt.close(fig)


            # ------------------------------------------------
            # OUTLIER DETECTION
            # ------------------------------------------------

            if len(numerical_cols) > 0:

                st.write(
                    "### 📦 Outlier Detection"
                )

                for column in numerical_cols:

                    fig, ax = plt.subplots()

                    ax.boxplot(
                        df[column].dropna()
                    )

                    ax.set_title(
                        f"Box Plot of {column}"
                    )

                    ax.set_ylabel(column)

                    st.pyplot(fig)

                    plt.close(fig)


            # ------------------------------------------------
            # CORRELATION HEATMAP
            # ------------------------------------------------

            if len(numerical_cols) >= 2:

                st.write(
                    "### 🔗 Correlation Heatmap"
                )

                correlation_matrix = (
                    df[numerical_cols].corr()
                )

                fig, ax = plt.subplots()

                image = ax.imshow(
                    correlation_matrix,
                    interpolation="nearest"
                )

                ax.set_xticks(
                    range(len(numerical_cols))
                )

                ax.set_yticks(
                    range(len(numerical_cols))
                )

                ax.set_xticklabels(
                    numerical_cols,
                    rotation=45,
                    ha="right"
                )

                ax.set_yticklabels(
                    numerical_cols
                )

                fig.colorbar(image)

                ax.set_title(
                    "Correlation Matrix"
                )

                st.pyplot(fig)

                plt.close(fig)


            # ------------------------------------------------
            # NUMERICAL RELATIONSHIP
            # ------------------------------------------------

            if len(numerical_cols) >= 2:

                st.write(
                    "### 🔵 Numerical Relationship"
                )

                x_column = numerical_cols[0]
                y_column = numerical_cols[1]

                fig, ax = plt.subplots()

                ax.scatter(
                    df[x_column],
                    df[y_column]
                )

                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)

                ax.set_title(
                    f"{x_column} vs {y_column}"
                )

                st.pyplot(fig)

                plt.close(fig)


            # ------------------------------------------------
            # CATEGORY DISTRIBUTIONS
            # ------------------------------------------------

            if len(categorical_cols) > 0:

                st.write(
                    "### 📊 Category Distributions"
                )

                for column in categorical_cols:

                    value_counts = (
                        df[column]
                        .value_counts()
                        .head(10)
                    )

                    fig, ax = plt.subplots()

                    ax.bar(
                        value_counts.index.astype(str),
                        value_counts.values
                    )

                    ax.set_title(
                        f"Top Categories in {column}"
                    )

                    ax.set_xlabel(column)
                    ax.set_ylabel("Count")

                    plt.xticks(
                        rotation=45,
                        ha="right"
                    )

                    st.pyplot(fig)

                    plt.close(fig)


            # ------------------------------------------------
            # VISUALIZATION RECOMMENDATIONS
            # ------------------------------------------------

            st.write(
                "### 💡 Visualization Recommendations"
            )

            visualizations = (
                recommend_visualizations(df)
            )

            for visualization in visualizations:

                st.write(visualization)


        # ====================================================
        # TAB 5 — CLEANING
        # ====================================================

        with tab5:

            st.subheader(
                "🧹 Data Cleaning Recommendations"
            )

            cleaning = (
                cleaning_recommendations(df)
            )

            for recommendation in cleaning:

                st.write(recommendation)


        # ====================================================
        # TAB 6 — AI RECOMMENDATIONS
        # ====================================================

        with tab6:

            st.subheader(
                "🤖 DataDoctor AI Recommendations"
            )

            st.write(
                "DataDoctor has analyzed your dataset "
                "and generated recommendations based "
                "on detected data-quality patterns."
            )

            st.divider()

            for recommendation in ai_recommendations:

                st.info(recommendation)

            st.divider()

            st.success(
                "🧠 AI analysis completed successfully!"
            )


        # ====================================================
        # TAB 7 — AUTO CLEAN
        # ====================================================

        with tab7:

            st.subheader(
                "✨ Automatic Data Cleaning"
            )

            st.write(
                "DataDoctor can automatically fix common "
                "data quality problems."
            )


            clean_button = st.button(
                "🧹 Clean My Dataset",
                type="primary",
                key="clean_dataset_button"
            )


            if clean_button:

                with st.spinner(
                    "🩺 DataDoctor is cleaning your dataset..."
                ):

                    try:

                        cleaned_df, cleaning_log = (
                            auto_clean_data(df)
                        )

                        st.session_state["cleaned_df"] = (
                            cleaned_df
                        )

                        st.session_state["cleaning_log"] = (
                            cleaning_log
                        )

                    except Exception as e:

                        st.error(
                            f"❌ Cleaning failed: {e}"
                        )


                if st.session_state["cleaned_df"] is not None:

                    st.success(
                        "✅ Dataset cleaned successfully!"
                    )


            # =================================================
            # SHOW CLEANED DATA
            # =================================================

            if st.session_state["cleaned_df"] is not None:

                cleaned_df = (
                    st.session_state["cleaned_df"]
                )

                cleaning_log = (
                    st.session_state["cleaning_log"]
                )


                st.write(
                    "### 📝 Cleaning Report"
                )


                if len(cleaning_log) > 0:

                    for log in cleaning_log:

                        st.write(log)

                else:

                    st.info(
                        "No cleaning changes were required."
                    )


                # ------------------------------------------------
                # BEFORE / AFTER METRICS
                # ------------------------------------------------

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


                col1, col2, col3, col4 = st.columns(4)


                with col1:

                    st.metric(
                        "Before Missing",
                        before_missing
                    )


                with col2:

                    st.metric(
                        "After Missing",
                        after_missing
                    )


                with col3:

                    st.metric(
                        "Before Duplicates",
                        before_duplicates
                    )


                with col4:

                    st.metric(
                        "After Duplicates",
                        after_duplicates
                    )


                st.divider()


                # ------------------------------------------------
                # CLEANED DATA
                # ------------------------------------------------

                st.write(
                    "### 👀 Cleaned Dataset Preview"
                )

                st.dataframe(
                    cleaned_df,
                    use_container_width=True
                )


                # ------------------------------------------------
                # DOWNLOAD CSV
                # ------------------------------------------------

                csv_data = (
                    cleaned_df
                    .to_csv(index=False)
                    .encode("utf-8")
                )


                st.download_button(
                    label="📥 Download Cleaned Dataset",
                    data=csv_data,
                    file_name="datadoctor_cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_cleaned_csv"
                )


                # ------------------------------------------------
                # PDF REPORT
                # ------------------------------------------------

                try:

                    pdf_report = generate_pdf_report(
                        dataset_name=(
                            st.session_state[
                                "uploaded_filename"
                            ]
                        ),
                        df=df,
                        quality_score=quality_score,
                        cleaned_df=cleaned_df
                    )


                    st.download_button(
                        label="📄 Download DataDoctor Report",
                        data=pdf_report,
                        file_name="DataDoctor_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="download_pdf_report"
                    )

                except Exception as e:

                    st.warning(
                        f"⚠️ PDF report could not be generated: {e}"
                    )


            else:

                st.info(
                    "👆 Click '🧹 Clean My Dataset' "
                    "to automatically clean your data."
                )


        # ====================================================
        # TAB 8 — BEFORE VS AFTER
        # ====================================================

        with tab8:

            st.subheader(
                "🔄 Before vs After Cleaning"
            )


            if st.session_state["cleaned_df"] is None:

                st.info(
                    "👆 First go to the ✨ Auto Clean tab "
                    "and click 'Clean My Dataset'."
                )


            else:

                cleaned_df = (
                    st.session_state["cleaned_df"]
                )


                before_score = (
                    calculate_quality_score(df)
                )

                after_score = (
                    calculate_quality_score(cleaned_df)
                )


                st.write(
                    "### ⭐ Data Quality Score"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Before Cleaning",
                        f"{before_score} / 100"
                    )


                with col2:

                    st.metric(
                        "After Cleaning",
                        f"{after_score} / 100"
                    )


                with col3:

                    improvement = (
                        after_score - before_score
                    )

                    st.metric(
                        "Improvement",
                        f"{improvement:+d} points"
                    )


                st.divider()


                # ------------------------------------------------
                # MISSING VALUES
                # ------------------------------------------------

                st.write(
                    "### 🕳️ Missing Values"
                )


                before_missing = int(
                    df.isnull().sum().sum()
                )

                after_missing = int(
                    cleaned_df.isnull().sum().sum()
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "Before",
                        before_missing
                    )


                with col2:

                    st.metric(
                        "After",
                        after_missing
                    )


                st.divider()


                # ------------------------------------------------
                # DUPLICATES
                # ------------------------------------------------

                st.write(
                    "### 📑 Duplicate Rows"
                )


                before_duplicates = int(
                    df.duplicated().sum()
                )

                after_duplicates = int(
                    cleaned_df.duplicated().sum()
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "Before",
                        before_duplicates
                    )


                with col2:

                    st.metric(
                        "After",
                        after_duplicates
                    )


                st.divider()


                # ------------------------------------------------
                # DATASET SIZE
                # ------------------------------------------------

                st.write(
                    "### 📊 Dataset Size"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "Rows Before",
                        df.shape[0]
                    )


                with col2:

                    st.metric(
                        "Rows After",
                        cleaned_df.shape[0]
                    )


                st.divider()


                st.success(
                    "🎉 DataDoctor successfully compared "
                    "your original and cleaned datasets!"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🩺 DataDoctor AI | Automatic Dataset Analysis & Cleaning"
)