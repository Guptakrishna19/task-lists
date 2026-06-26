import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def bin_numerical_features(series: pd.Series, bins: Union[int, List[float]], labels: Optional[List[str]] = None) -> pd.Series:
    """
    Groups a continuous numerical series into discrete bins using pd.cut (equal-width or custom bounds).
    """
    if series.empty:
        return series.copy()
    return pd.cut(series, bins=bins, labels=labels)

def bin_quantile_features(series: pd.Series, q: int, labels: Optional[List[str]] = None) -> pd.Series:
    """
    Groups a continuous numerical series into equal-frequency quantiles using pd.qcut.
    """
    if series.empty:
        return series.copy()
    return pd.qcut(series, q=q, labels=labels)

def extract_datetime_features(df: pd.DataFrame, datetime_col: str) -> pd.DataFrame:
    """
    Converts a column to datetime and extracts features: hour, day_of_week, day_name, is_weekend.
    """
    df_new = df.copy()
    if datetime_col not in df_new.columns:
        return df_new
        
    dates = pd.to_datetime(df_new[datetime_col], errors="coerce")
    df_new[f"{datetime_col}_hour"] = dates.dt.hour
    df_new[f"{datetime_col}_day_of_week"] = dates.dt.dayofweek
    df_new[f"{datetime_col}_day_name"] = dates.dt.day_name()
    df_new[f"{datetime_col}_is_weekend"] = dates.dt.dayofweek.isin([5, 6]).astype(int)
    return df_new

def calculate_interaction_ratio(df: pd.DataFrame, numerator_col: str, denominator_col: str, new_col: str) -> pd.DataFrame:
    """
    Calculates safety ratios or rate interactions, avoiding zero division.
    """
    df_new = df.copy()
    if numerator_col not in df_new.columns or denominator_col not in df_new.columns:
        return df_new
        
    df_new[new_col] = np.where(
        df_new[denominator_col] != 0,
        df_new[numerator_col] / df_new[denominator_col],
        0.0
    )
    return df_new

def ordinal_encode(series: pd.Series, mapping: Dict[str, Union[int, float]]) -> pd.Series:
    """
    Performs ordinal encoding using a mapping dictionary.
    """
    if series.empty:
        return series.copy()
    return series.map(mapping)

def one_hot_encode(df: pd.DataFrame, columns: List[str], prefix_sep: str = "_") -> pd.DataFrame:
    """
    Applies one-hot encoding to specified nominal categories.
    """
    if df.empty:
        return df.copy()
    # Check if column elements exist
    existing_cols = [c for c in columns if c in df.columns]
    if not existing_cols:
        return df.copy()
    return pd.get_dummies(df, columns=existing_cols, prefix_sep=prefix_sep, drop_first=True, dtype=int)

def standard_scale(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Applies Standard Scaling (Z-score normalization) to specified numeric columns.
    """
    df_new = df.copy()
    existing_cols = [c for c in columns if c in df_new.columns]
    if not existing_cols:
        return df_new
        
    scaler = StandardScaler()
    df_new[existing_cols] = scaler.fit_transform(df_new[existing_cols])
    return df_new

def minmax_scale(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Applies Min-Max Scaling (Normalizes values between 0 and 1) to specified numeric columns.
    """
    df_new = df.copy()
    existing_cols = [c for c in columns if c in df_new.columns]
    if not existing_cols:
        return df_new
        
    scaler = MinMaxScaler()
    df_new[existing_cols] = scaler.fit_transform(df_new[existing_cols])
    return df_new
