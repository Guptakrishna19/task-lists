import pandas as pd
import numpy as np


def remove_duplicates(df, subset=None, keep="first"):
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates(subset=subset, keep=keep)


def standardize_categories(series, mapping=None):
    """
    Standardize categorical text values.
    """
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.lower()
    )

    if mapping:
        cleaned = cleaned.map(mapping).fillna(cleaned)

    return cleaned


def coerce_numeric(series):
    """
    Convert a column to numeric safely.
    Invalid values become NaN.
    """
    return pd.to_numeric(series, errors="coerce")


def coerce_datetime(series):
    """
    Convert a column to datetime safely.
    Invalid values become NaT.
    """
    return pd.to_datetime(series, errors="coerce")


def iqr_bounds(series):
    """
    Calculate IQR lower and upper bounds.
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return lower_bound, upper_bound


def detect_outliers_iqr(series):
    """
    Return boolean mask of outliers.
    """
    lower, upper = iqr_bounds(series)

    return (series < lower) | (series > upper)


def winsorize_outliers(series):
    """
    Cap outliers instead of removing them.
    """
    lower, upper = iqr_bounds(series)

    return series.clip(lower=lower, upper=upper)


def encode_ordinal(series, mapping):
    """
    Ordinal encoding.
    """
    return series.map(mapping)


def encode_onehot(df, columns):
    """
    One-hot encoding.
    """
    return pd.get_dummies(
        df,
        columns=columns,
        drop_first=True
    )


def count_outliers_iqr(series):
    """
    Count IQR outliers.
    """
    return detect_outliers_iqr(series).sum()


def quality_report(df, numeric_columns=None):
    """
    Generate a data quality report.
    """

    report = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": df.isna().sum().sum(),
        "Duplicate Rows": df.duplicated().sum()
    }
    if numeric_columns:
        total_outliers = 0

        for col in numeric_columns:
            total_outliers += count_outliers_iqr(df[col])

        report["Outlier Count"] = total_outliers

    return pd.DataFrame(
        report.items(),
        columns=["Metric", "Value"]
    )