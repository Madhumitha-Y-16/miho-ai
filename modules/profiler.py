import pandas as pd
import numpy as np


def detect_column_type(series):
    if series.dropna().empty:
        return "Empty"
    if pd.api.types.is_bool_dtype(series):
        return "Boolean"
    if pd.api.types.is_numeric_dtype(series):
        return "Numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "Date / Time"

    values = series.dropna().astype(str).head(5000)
    numeric_values = pd.to_numeric(values, errors="coerce")
    if len(values) and numeric_values.notna().mean() >= 0.80:
        return "Potential Numeric"

    try:
        date_values = pd.to_datetime(values, errors="coerce", format="mixed")
        if len(values) and date_values.notna().mean() >= 0.80:
            return "Potential Date"
    except (ValueError, TypeError):
        pass

    unique_count = series.nunique(dropna=True)
    unique_ratio = unique_count / max(int(series.notna().sum()), 1)
    if unique_count <= 30 or unique_ratio <= 0.05:
        return "Categorical"
    return "Text"


def count_whitespace_issues(series):
    if not (pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)):
        return 0
    values = series.dropna().astype(str)
    if values.empty:
        return 0
    return int((values != values.str.strip()).sum())


def detect_outliers(series):
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if len(numeric) < 4 or numeric.nunique() < 2:
        return 0
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        return 0
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return int(((numeric < lower) | (numeric > upper)).sum())


def profile_dataset(df):
    """Return (summary, column_report, numeric_report, whitespace_report)."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("profile_dataset expects a pandas DataFrame.")

    total_rows, total_columns = df.shape
    total_cells = int(total_rows * total_columns)
    missing_cells = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum()) if total_rows else 0

    rows = []
    for column in df.columns:
        series = df[column]
        detected = detect_column_type(series)
        rows.append({
            "Column": str(column),
            "Data Type": str(series.dtype),
            "Detected Type": detected,
            "Missing Values": int(series.isna().sum()),
            "Missing %": round(float(series.isna().mean() * 100), 2) if total_rows else 0.0,
            "Unique Values": int(series.nunique(dropna=True)),
            "Duplicate Values": int(series.duplicated().sum()) if total_rows else 0,
            "Whitespace Issues": count_whitespace_issues(series),
            "Potential Outliers": detect_outliers(series) if pd.api.types.is_numeric_dtype(series) else 0,
            "Constant Column": bool(series.nunique(dropna=True) <= 1)
        })

    column_report = pd.DataFrame(rows, columns=[
        "Column", "Data Type", "Detected Type", "Missing Values", "Missing %",
        "Unique Values", "Duplicate Values", "Whitespace Issues",
        "Potential Outliers", "Constant Column"
    ])

    numeric_df = df.select_dtypes(include=[np.number])
    numeric_report = numeric_df.describe().T.reset_index().rename(columns={"index": "Column"})
    if "Column" not in numeric_report.columns and not numeric_report.empty:
        numeric_report = numeric_report.rename(columns={numeric_report.columns[0]: "Column"})

    whitespace_report = column_report.loc[
        column_report["Whitespace Issues"] > 0,
        ["Column", "Whitespace Issues"]
    ].reset_index(drop=True)

    type_counts = column_report["Detected Type"].value_counts().to_dict() if not column_report.empty else {}
    summary = {
        "total_rows": int(total_rows),
        "total_columns": int(total_columns),
        "total_cells": total_cells,
        "missing_cells": missing_cells,
        "missing_percentage": round((missing_cells / total_cells) * 100, 2) if total_cells else 0.0,
        "duplicate_rows": duplicate_rows,
        "numeric_columns": int(type_counts.get("Numeric", 0)),
        "categorical_columns": int(type_counts.get("Categorical", 0)),
        "text_columns": int(type_counts.get("Text", 0)),
        "date_columns": int(type_counts.get("Date / Time", 0)),
        "boolean_columns": int(type_counts.get("Boolean", 0)),
        "potential_numeric_columns": int(type_counts.get("Potential Numeric", 0)),
        "potential_date_columns": int(type_counts.get("Potential Date", 0)),
        "empty_columns": int(type_counts.get("Empty", 0)),
        "constant_columns": int(column_report["Constant Column"].sum()) if not column_report.empty else 0,
        "whitespace_issues": int(column_report["Whitespace Issues"].sum()) if not column_report.empty else 0,
        "potential_outliers": int(column_report["Potential Outliers"].sum()) if not column_report.empty else 0
    }

    return summary, column_report, numeric_report, whitespace_report
