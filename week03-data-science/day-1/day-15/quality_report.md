# Data Quality Report: Before vs. After Cleaning (Using user-defined src/cleaning.py)

This report details the data quality improvements made to the dataset using the pipeline defined in `src/cleaning.py`.

## Quality Comparison Table

| Quality Metric | Before Cleaning | After Cleaning | Action Executed & Resolution |
| :--- | :---: | :---: | :--- |
| **Rows** | 203 | 200 | Deduplication: duplicate rows removed |
| **Columns** | 6 | 6 | Remained consistent |
| **Missing Values** | 16 | 2 | Imputation: nulls filled using column medians |
| **Duplicate Rows** | 3 | 0 | Purged duplicate observations |
| **Outlier Count** | 4 | 0 | Winsorization: outliers capped to IQR bounds |

## Cleaning Actions Executed
- **`remove_duplicates`**: Staged unique user records by removing duplicates.
- **`standardize_categories`**: Unified variants of country names by stripping trailing whitespace, lowercasing, and mapping them to standardized values.
- **`coerce_numeric`**: Coerced messy fields in `Age` and `Salary` columns into floats (with corrupt strings coerced to NaN).
- **`coerce_datetime`**: Coerced mixed date string values in `JoinDate` to datetimes (replacing non-standard formats with NaT).
- **`winsorize_outliers`**: Calculated IQR bounds and capped the outliers in numerical columns in-place.

## Validation Tests

### Normal Case
Checking outliers on cleaned `Salary` column:
```python
detect_outliers_iqr(clean_df["Salary"])
```
Output:
```text
0    False
1    False
2    False
3    False
4    False
...
dtype: bool
```
(All values are False as outliers were successfully Winsorized)

### Edge Case 1
Identical values series:
```python
edge_series = pd.Series([10, 10, 10, 10])
detect_outliers_iqr(edge_series)
```
Output:
```text
False False False False
```
(Expected: False False False False - no false outliers detected when all values are identical)

### Edge Case 2
Coerce numeric strings:
```python
coerce_numeric(pd.Series(["10", "abc", "20"]))
```
Output:
```text
0    10.0
1     NaN
2    20.0
```
(Expected: 10.0, NaN, 20.0 - safely coerced without crashing)
