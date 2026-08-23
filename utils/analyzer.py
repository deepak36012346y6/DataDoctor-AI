import pandas as pd


# ============================================================
# BASIC DATA INSIGHTS
# ============================================================

def generate_insights(df):

    insights = []

    rows, columns = df.shape

    insights.append(
        f"📊 The dataset contains {rows:,} rows and {columns} columns."
    )

    numerical_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    insights.append(
        f"🔢 There are {len(numerical_cols)} numerical columns "
        f"and {len(categorical_cols)} categorical columns."
    )

    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) > 0:

        for column, count in missing.items():

            percentage = (count / rows) * 100

            insights.append(
                f"⚠️ '{column}' contains {count:,} missing values "
                f"({percentage:.2f}% of the dataset)."
            )

    else:

        insights.append(
            "✅ No missing values were detected."
        )

    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:

        insights.append(
            f"⚠️ The dataset contains {duplicates:,} duplicate rows."
        )

    else:

        insights.append(
            "✅ No duplicate rows were detected."
        )

    # Numerical column analysis
    for column in numerical_cols:

        skewness = df[column].skew()

        if abs(skewness) > 1:

            if skewness > 0:

                insights.append(
                    f"📈 '{column}' is highly right-skewed."
                )

            else:

                insights.append(
                    f"📉 '{column}' is highly left-skewed."
                )

        # IQR outlier detection
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ].shape[0]

        if outliers > 0:

            insights.append(
                f"⚠️ '{column}' may contain "
                f"{outliers:,} potential outliers."
            )

    return insights


# ============================================================
# CORRELATION INSIGHTS
# ============================================================

def correlation_insights(df):

    insights = []

    numerical_cols = df.select_dtypes(
        include="number"
    ).columns

    if len(numerical_cols) < 2:

        return [
            "ℹ️ Not enough numerical columns "
            "to analyze correlations."
        ]

    correlation_matrix = df[numerical_cols].corr()

    for i in range(len(numerical_cols)):

        for j in range(i + 1, len(numerical_cols)):

            col1 = numerical_cols[i]
            col2 = numerical_cols[j]

            correlation = correlation_matrix.loc[
                col1,
                col2
            ]

            if correlation >= 0.7:

                insights.append(
                    f"🔗 '{col1}' and '{col2}' have a strong "
                    f"positive correlation ({correlation:.2f})."
                )

            elif correlation <= -0.7:

                insights.append(
                    f"🔗 '{col1}' and '{col2}' have a strong "
                    f"negative correlation ({correlation:.2f})."
                )

    if len(insights) == 0:

        insights.append(
            "ℹ️ No strong correlations were detected "
            "between numerical columns."
        )

    return insights


# ============================================================
# STATISTICAL SUMMARY
# ============================================================

def generate_summary(df):

    summary = []

    numerical_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(numerical_cols) == 0:

        return [
            "ℹ️ No numerical columns available "
            "for statistical summary."
        ]

    for column in numerical_cols:

        min_value = df[column].min()
        max_value = df[column].max()
        mean_value = df[column].mean()
        median_value = df[column].median()

        summary.append(
            f"📊 {column}: "
            f"Min = {min_value:.2f}, "
            f"Max = {max_value:.2f}, "
            f"Mean = {mean_value:.2f}, "
            f"Median = {median_value:.2f}"
        )

    return summary


# ============================================================
# VISUALIZATION RECOMMENDATIONS
# ============================================================

def recommend_visualizations(df):

    recommendations = []

    numerical_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if len(numerical_cols) >= 1:

        recommendations.append(
            "📊 Histogram: Useful for understanding "
            "the distribution of numerical columns."
        )

        recommendations.append(
            "📦 Box Plot: Useful for detecting "
            "outliers in numerical columns."
        )

    if len(numerical_cols) >= 2:

        recommendations.append(
            "🔗 Correlation Heatmap: Useful for finding "
            "relationships between numerical columns."
        )

        recommendations.append(
            "🔵 Scatter Plot: Useful for studying "
            "relationships between two numerical columns."
        )

    if len(categorical_cols) >= 1:

        recommendations.append(
            "📊 Bar Chart: Useful for comparing categories."
        )

    if (
        len(numerical_cols) >= 1
        and len(categorical_cols) >= 1
    ):

        recommendations.append(
            "📊 Grouped Bar Chart: Useful for comparing "
            "numerical values across categories."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "ℹ️ Not enough suitable columns "
            "to recommend visualizations."
        )

    return recommendations


# ============================================================
# CLEANING RECOMMENDATIONS
# ============================================================

def cleaning_recommendations(df):

    recommendations = []

    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if len(missing) > 0:

        for column, count in missing.items():

            percentage = (count / len(df)) * 100

            if percentage < 5:

                recommendations.append(
                    f"🧹 '{column}': {count:,} missing values "
                    f"({percentage:.2f}%). Consider filling them "
                    f"using the median/mode."
                )

            elif percentage < 30:

                recommendations.append(
                    f"⚠️ '{column}': {count:,} missing values "
                    f"({percentage:.2f}%). Consider using an "
                    f"appropriate imputation method."
                )

            else:

                recommendations.append(
                    f"🚨 '{column}': {count:,} missing values "
                    f"({percentage:.2f}%). Consider dropping "
                    f"the column if the missing data cannot "
                    f"be recovered."
                )

    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:

        recommendations.append(
            f"🧹 Found {duplicates:,} duplicate rows. "
            f"Consider removing duplicate records."
        )

    # Outliers
    numerical_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    for column in numerical_cols:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ].shape[0]

        if outliers > 0:

            recommendations.append(
                f"📦 '{column}': {outliers:,} potential "
                f"outliers detected. Consider investigating, "
                f"capping, or treating extreme values."
            )

    # Constant columns
    for column in df.columns:

        if df[column].nunique(dropna=False) <= 1:

            recommendations.append(
                f"🗑️ '{column}' contains only one unique value. "
                f"Consider removing this column because it "
                f"provides little or no information."
            )

    if len(recommendations) == 0:

        recommendations.append(
            "✅ No major cleaning problems were detected."
        )

    return recommendations


# ============================================================
# AUTOMATIC DATA CLEANING
# ============================================================

def auto_clean_data(df):

    cleaned_df = df.copy()

    cleaning_log = []

    # ========================================================
    # 1. REMOVE DUPLICATES
    # ========================================================

    duplicate_count = cleaned_df.duplicated().sum()

    if duplicate_count > 0:

        cleaned_df = cleaned_df.drop_duplicates()

        cleaning_log.append(
            f"🧹 Removed {duplicate_count:,} duplicate rows."
        )

    else:

        cleaning_log.append(
            "✅ No duplicate rows found."
        )


    # ========================================================
    # 2. HANDLE MISSING VALUES
    # ========================================================

    numerical_cols = cleaned_df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_cols = cleaned_df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    # Numerical missing values → Median

    for column in numerical_cols:

        missing_count = cleaned_df[column].isnull().sum()

        if missing_count > 0:

            median_value = cleaned_df[column].median()

            cleaned_df[column] = cleaned_df[column].fillna(
                median_value
            )

            cleaning_log.append(
                f"🔢 Filled {missing_count:,} missing values "
                f"in '{column}' using the median."
            )


    # Categorical missing values → Mode

    for column in categorical_cols:

        missing_count = cleaned_df[column].isnull().sum()

        if missing_count > 0:

            mode_values = cleaned_df[column].mode()

            if len(mode_values) > 0:

                mode_value = mode_values.iloc[0]

                cleaned_df[column] = cleaned_df[column].fillna(
                    mode_value
                )

                cleaning_log.append(
                    f"🔤 Filled {missing_count:,} missing values "
                    f"in '{column}' using the mode."
                )

            else:

                cleaned_df[column] = cleaned_df[column].fillna(
                    "Unknown"
                )

                cleaning_log.append(
                    f"🔤 Filled {missing_count:,} missing values "
                    f"in '{column}' with 'Unknown'."
                )


    # ========================================================
    # 3. RETURN RESULTS
    # ========================================================

    return cleaned_df, cleaning_log


# ============================================================
# DATA QUALITY SCORE
# ============================================================

def calculate_quality_score(df):

    score = 100

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    # ========================================================
    # MISSING VALUES
    # ========================================================

    missing_cells = int(
        df.isnull().sum().sum()
    )

    missing_percentage = (
        missing_cells / total_cells
    ) * 100

    score -= min(
        missing_percentage * 0.5,
        25
    )


    # ========================================================
    # DUPLICATES
    # ========================================================

    duplicate_rows = int(
        df.duplicated().sum()
    )

    if df.shape[0] > 0:

        duplicate_percentage = (
            duplicate_rows / df.shape[0]
        ) * 100

        score -= min(
            duplicate_percentage * 0.5,
            20
        )


    # ========================================================
    # OUTLIERS
    # ========================================================

    numerical_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    outlier_columns = 0

    for column in numerical_cols:

        series = df[column].dropna()

        if len(series) >= 4:

            q1 = series.quantile(0.25)

            q3 = series.quantile(0.75)

            iqr = q3 - q1

            if iqr > 0:

                lower_bound = (
                    q1 - 1.5 * iqr
                )

                upper_bound = (
                    q3 + 1.5 * iqr
                )

                outliers = series[
                    (series < lower_bound) |
                    (series > upper_bound)
                ]

                if len(outliers) > 0:

                    outlier_columns += 1

    score -= min(
        outlier_columns * 5,
        20
    )


    # ========================================================
    # FINAL SCORE
    # ========================================================

    score = max(
        0,
        min(
            100,
            round(score)
        )
    )

    return score


# ============================================================
# 🤖 AI-STYLE AUTOMATIC RECOMMENDATIONS
# ============================================================

def generate_ai_recommendations(df):

    recommendations = []

    rows, columns = df.shape

    numerical_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


    # ========================================================
    # 1. DATASET SIZE
    # ========================================================

    if rows < 50:

        recommendations.append(
            "🤖 AI Recommendation: This is a relatively "
            "small dataset. Be careful when drawing statistical "
            "conclusions or training machine learning models."
        )

    elif rows >= 1000:

        recommendations.append(
            "🤖 AI Recommendation: The dataset contains a "
            "good number of rows for exploratory data analysis "
            "and may be suitable for machine learning after "
            "proper preprocessing."
        )


    # ========================================================
    # 2. MISSING VALUES
    # ========================================================

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if len(missing) > 0:

        for column, count in missing.items():

            percentage = (
                count / rows
            ) * 100

            if percentage >= 30:

                recommendations.append(
                    f"🤖 AI Recommendation: '{column}' has "
                    f"{percentage:.1f}% missing data. Investigate "
                    f"why the values are missing before deciding "
                    f"whether to impute or remove this column."
                )

            elif percentage > 0:

                recommendations.append(
                    f"🤖 AI Recommendation: '{column}' contains "
                    f"{count:,} missing values. Imputation may "
                    f"be appropriate before further analysis."
                )


    # ========================================================
    # 3. DUPLICATES
    # ========================================================

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        recommendations.append(
            f"🤖 AI Recommendation: {duplicate_count:,} "
            f"duplicate rows were detected. Remove duplicates "
            f"if they represent repeated records rather than "
            f"legitimate observations."
        )


    # ========================================================
    # 4. SKEWNESS
    # ========================================================

    for column in numerical_cols:

        series = df[column].dropna()

        if len(series) >= 3:

            skewness = series.skew()

            if skewness > 1:

                recommendations.append(
                    f"🤖 AI Recommendation: '{column}' is strongly "
                    f"right-skewed. Consider a transformation "
                    f"such as log transformation if this column "
                    f"is used in a machine learning model."
                )

            elif skewness < -1:

                recommendations.append(
                    f"🤖 AI Recommendation: '{column}' is strongly "
                    f"left-skewed. Investigate extreme values and "
                    f"consider an appropriate transformation."
                )


    # ========================================================
    # 5. OUTLIERS
    # ========================================================

    for column in numerical_cols:

        series = df[column].dropna()

        if len(series) >= 4:

            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)

            IQR = Q3 - Q1

            if IQR > 0:

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outlier_count = series[
                    (series < lower_bound) |
                    (series > upper_bound)
                ].shape[0]

                if outlier_count > 0:

                    recommendations.append(
                        f"🤖 AI Recommendation: '{column}' has "
                        f"{outlier_count:,} potential outliers. "
                        f"Check whether these values are genuine "
                        f"observations or data-entry errors."
                    )


    # ========================================================
    # 6. STRONG CORRELATIONS
    # ========================================================

    if len(numerical_cols) >= 2:

        correlation_matrix = df[
            numerical_cols
        ].corr()

        for i in range(
            len(numerical_cols)
        ):

            for j in range(
                i + 1,
                len(numerical_cols)
            ):

                col1 = numerical_cols[i]
                col2 = numerical_cols[j]

                correlation = correlation_matrix.loc[
                    col1,
                    col2
                ]

                if abs(correlation) >= 0.9:

                    recommendations.append(
                        f"🤖 AI Recommendation: '{col1}' and "
                        f"'{col2}' have a very strong correlation "
                        f"({correlation:.2f}). Check for possible "
                        f"redundancy or multicollinearity before "
                        f"using both in a machine learning model."
                    )


    # ========================================================
    # 7. CONSTANT COLUMNS
    # ========================================================

    for column in df.columns:

        if df[column].nunique(
            dropna=False
        ) <= 1:

            recommendations.append(
                f"🤖 AI Recommendation: '{column}' contains "
                f"only one unique value. It is unlikely to "
                f"provide useful information to a model and "
                f"could potentially be removed."
            )


    # ========================================================
    # 8. CATEGORICAL COLUMNS
    # ========================================================

    if len(categorical_cols) > 0:

        recommendations.append(
            "🤖 AI Recommendation: Categorical columns were "
            "detected. If machine learning is your next step, "
            "consider suitable encoding such as one-hot or "
            "ordinal encoding depending on the meaning of "
            "each category."
        )


    # ========================================================
    # 9. NUMERICAL COLUMNS
    # ========================================================

    if len(numerical_cols) > 0:

        recommendations.append(
            "🤖 AI Recommendation: Numerical columns are "
            "available for statistical analysis and "
            "visualization. Check their distributions and "
            "scales before machine learning."
        )


    # ========================================================
    # 10. DATASET READY
    # ========================================================

    if len(recommendations) == 0:

        recommendations.append(
            "🤖 AI Recommendation: No major issues were "
            "detected. Your dataset appears relatively clean "
            "and is ready for further analysis."
        )


    return recommendations



