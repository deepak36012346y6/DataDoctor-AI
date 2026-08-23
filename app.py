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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🩺 DataDoctor AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered automatic data analysis assistant'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🩺 DataDoctor AI")

    st.write(
        "Upload your messy dataset and DataDoctor will "
        "automatically analyze and clean it."
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
# MAIN APPLICATION
# ============================================================

if uploaded_file is not None:

    try:

        # ====================================================
        # READ DATA
        # ====================================================

        if uploaded_file.name.lower().endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(uploaded_file)


        st.success(
            f"✅ Successfully loaded: {uploaded_file.name}"
        )


        # ====================================================
        # DATA QUALITY SCORE
        # ====================================================

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


        # ====================================================
        # DATASET OVERVIEW
        # ====================================================

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


        # ====================================================
        # DATA PREVIEW
        # ====================================================

        with st.expander(
            "👀 View Dataset Preview",
            expanded=True
        ):

            st.dataframe(
                df.head(10),
                use_container_width=True
            )


        # ====================================================
        # ANALYZE BUTTON
        # ====================================================

        analyze_button = st.button(
            "🧠 Analyze Dataset",
            type="primary",
            use_container_width=True
        )


        if analyze_button:

            # =================================================
            # GENERATE AI RECOMMENDATIONS
            # =================================================

            ai_recommendations = (
                generate_ai_recommendations(df)
            )


            # =================================================
            # TABS
            # =================================================

            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
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


            # =================================================
            # TAB 1 — INSIGHTS
            # =================================================

            with tab1:

                st.subheader(
                    "🔍 Basic Data Insights"
                )

                insights = generate_insights(df)

                for insight in insights:

                    st.write(insight)


            # =================================================
            # TAB 2 — CORRELATIONS
            # =================================================

            with tab2:

                st.subheader(
                    "🔗 Correlation Analysis"
                )

                correlations = correlation_insights(df)

                for correlation in correlations:

                    st.write(correlation)


            # =================================================
            # TAB 3 — STATISTICS
            # =================================================

            with tab3:

                st.subheader(
                    "📊 Statistical Summary"
                )

                summaries = generate_summary(df)

                for summary in summaries:

                    st.write(summary)


            # =================================================
            # TAB 4 — VISUALIZATIONS
            # =================================================

            with tab4:

                st.subheader(
                    "📈 Automatic Visualizations"
                )

                numerical_cols = df.select_dtypes(
                    include="number"
                ).columns.tolist()

                categorical_cols = df.select_dtypes(
                    include=["object", "category"]
                ).columns.tolist()


                # ------------------------------------------------
                # HISTOGRAMS
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
                # BOX PLOTS
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

                    correlation_matrix = df[
                        numerical_cols
                    ].corr()

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
                # SCATTER PLOT
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
                # CATEGORICAL CHARTS
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


            # =================================================
            # TAB 5 — CLEANING RECOMMENDATIONS
            # =================================================

            with tab5:

                st.subheader(
                    "🧹 Data Cleaning Recommendations"
                )

                cleaning = (
                    cleaning_recommendations(df)
                )

                for recommendation in cleaning:

                    st.write(recommendation)


            # =================================================
            # TAB 6 — AI RECOMMENDATIONS
            # =================================================

            with tab6:

                st.subheader(
                    "🤖 DataDoctor AI Recommendations"
                )

                st.write(
                    "DataDoctor has analyzed your dataset "
                    "and generated recommendations based "
                    "on the detected data-quality patterns."
                )

                st.divider()

                for recommendation in ai_recommendations:

                    st.info(
                        recommendation
                    )

                st.divider()

                st.success(
                    "🧠 AI analysis completed successfully!"
                )


            # =================================================
            # TAB 7 — AUTO CLEAN
            # =================================================

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
                    type="primary"
                )


                if clean_button:

                    with st.spinner(
                        "🩺 DataDoctor is cleaning your dataset..."
                    ):

                        cleaned_df, cleaning_log = (
                            auto_clean_data(df)
                        )


                    st.session_state[
                        "cleaned_df"
                    ] = cleaned_df

                    st.session_state[
                        "cleaning_log"
                    ] = cleaning_log


                    st.success(
                        "✅ Dataset cleaned successfully!"
                    )


                    st.write(
                        "### 📝 Cleaning Report"
                    )

                    for log in cleaning_log:

                        st.write(log)


                    # ------------------------------------------
                    # BEFORE / AFTER METRICS
                    # ------------------------------------------

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


                    # ------------------------------------------
                    # CLEANED DATASET PREVIEW
                    # ------------------------------------------

                    st.write(
                        "### 👀 Cleaned Dataset Preview"
                    )

                    st.dataframe(
                        cleaned_df.head(10),
                        use_container_width=True
                    )


                    # ------------------------------------------
                    # DOWNLOAD CLEANED CSV
                    # ------------------------------------------

                    csv_data = cleaned_df.to_csv(
                        index=False
                    ).encode("utf-8")


                    st.download_button(
                        label="📥 Download Cleaned Dataset",
                        data=csv_data,
                        file_name="datadoctor_cleaned_data.csv",
                        mime="text/csv",
                        use_container_width=True
                    )


                    # ------------------------------------------
                    # GENERATE PDF REPORT
                    # ------------------------------------------

                    pdf_report = generate_pdf_report(
                        dataset_name=uploaded_file.name,
                        df=df,
                        quality_score=quality_score,
                        cleaned_df=cleaned_df
                    )


                    st.download_button(
                        label="📄 Download DataDoctor Report",
                        data=pdf_report,
                        file_name="DataDoctor_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )


            # =================================================
            # TAB 8 — BEFORE VS AFTER
            # =================================================

            with tab8:

                st.subheader(
                    "🔄 Before vs After Cleaning"
                )


                if "cleaned_df" not in st.session_state:

                    st.info(
                        "👆 First go to the ✨ Auto Clean tab "
                        "and click 'Clean My Dataset'."
                    )

                else:

                    cleaned_df = (
                        st.session_state["cleaned_df"]
                    )


                    # ------------------------------------------
                    # QUALITY SCORE
                    # ------------------------------------------

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


                    # ------------------------------------------
                    # MISSING VALUES
                    # ------------------------------------------

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


                    # ------------------------------------------
                    # DUPLICATES
                    # ------------------------------------------

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


                    # ------------------------------------------
                    # DATASET SIZE
                    # ------------------------------------------

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


                    # ------------------------------------------
                    # FINAL SUCCESS MESSAGE
                    # ------------------------------------------

                    st.success(
                        "🎉 DataDoctor successfully compared "
                        "your original and cleaned datasets!"
                    )


    except Exception as e:

        st.error(
            f"❌ Error while processing the file: {e}"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🩺 DataDoctor AI | Automatic Dataset Analysis "
    "& Cleaning"
)