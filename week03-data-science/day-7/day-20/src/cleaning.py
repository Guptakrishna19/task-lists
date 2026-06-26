import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union

def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None, keep: str = "first") -> pd.DataFrame:
    """
    Safely removes duplicate rows from a DataFrame.
    Handles empty DataFrames gracefully.
    """
    if df.empty:
        return df.copy()
    return df.drop_duplicates(subset=subset, keep=keep)

def standardize_categories(series: pd.Series, mapping: Optional[Dict[str, str]] = None) -> pd.Series:
    """
    Standardizes categorical text values by stripping whitespace and converting to lowercase.
    Applies custom category mapping if provided.
    """
    if series.empty:
        return series.copy()
    
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.lower()
    )
    if mapping:
        # Standardize keys in user mapping for matching
        std_mapping = {k.strip().lower(): v for k, v in mapping.items()}
        cleaned = cleaned.map(std_mapping).fillna(cleaned)
    return cleaned

def coerce_numeric(series: pd.Series) -> pd.Series:
    """
    Converts a column to numeric safely, turning invalid parsing values into NaN.
    """
    return pd.to_numeric(series, errors="coerce")

def coerce_datetime(series: pd.Series) -> pd.Series:
    """
    Converts a column to datetime safely, turning invalid parsing values into NaT.
    """
    return pd.to_datetime(series, errors="coerce")

def iqr_bounds(series: pd.Series) -> tuple[float, float]:
    """
    Calculates IQR lower and upper bounds for outlier detection.
    Returns (lower_bound, upper_bound). Returns (0.0, 0.0) if empty or non-numeric.
    """
    if series.empty or not np.issubdtype(series.dtype, np.number):
        return 0.0, 0.0
    
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound

def detect_outliers_iqr(series: pd.Series) -> pd.Series:
    """
    Returns a boolean mask identifying IQR outliers.
    """
    if series.empty or not np.issubdtype(series.dtype, np.number):
        return pd.Series(False, index=series.index)
        
    lower, upper = iqr_bounds(series)
    return (series < lower) | (series > upper)

def winsorize_outliers(series: pd.Series) -> pd.Series:
    """
    Caps outliers outside of IQR bounds instead of removing them.
    """
    if series.empty or not np.issubdtype(series.dtype, np.number):
        return series.copy()
        
    lower, upper = iqr_bounds(series)
    return series.clip(lower=lower, upper=upper)

def quality_report(df: pd.DataFrame, numeric_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Generates a concise data quality report containing row/column counts,
    missing values, duplicate rows, and outlier counts.
    """
    if df.empty:
        return pd.DataFrame([{"Metric": "Rows", "Value": 0}])
        
    report = {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": df.isna().sum().sum(),
        "Duplicate Rows": df.duplicated().sum()
    }
    
    if numeric_columns:
        total_outliers = 0
        for col in numeric_columns:
            if col in df.columns:
                total_outliers += detect_outliers_iqr(df[col]).sum()
        report["Outlier Count"] = total_outliers
        
    return pd.DataFrame(report.items(), columns=["Metric", "Value"])
