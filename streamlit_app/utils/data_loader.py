"""
data_loader.py
---------------
Centralized, cached loaders for every artifact produced by
`Retail_Sales_Forecasting.ipynb`.

This module NEVER trains a model. It only reads files from
`processed/`, `predictions/`, and `models/`. If an artifact is
missing, functions return `None` (or an empty DataFrame) and the
calling page is responsible for showing a friendly message.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Paths (relative to the app root, kept in one place -> "no hardcoded values")
# ---------------------------------------------------------------------------
APP_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = APP_ROOT / "processed"
PREDICTIONS_DIR = APP_ROOT / "predictions"
MODELS_DIR = APP_ROOT / "models"
REPORTS_DIR = APP_ROOT / "reports"


def _read_csv_safe(path: Path, parse_dates: Optional[list] = None) -> pd.DataFrame:
    """Read a CSV if it exists, else return an empty DataFrame."""
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, parse_dates=parse_dates)


@st.cache_data(show_spinner=False)
def load_transactions() -> pd.DataFrame:
    """Load the cleaned, feature-engineered transaction-level dataset."""
    df = _read_csv_safe(PROCESSED_DIR / "cleaned_transactions.csv", parse_dates=["Order Date", "Ship Date"])
    return df


@st.cache_data(show_spinner=False)
def load_monthly_sales() -> pd.DataFrame:
    df = _read_csv_safe(PROCESSED_DIR / "monthly_sales.csv", parse_dates=["Order Date"])
    return df


@st.cache_data(show_spinner=False)
def load_weekly_sales() -> pd.DataFrame:
    df = _read_csv_safe(
        PROCESSED_DIR / "weekly_sales_with_anomaly_flags.csv",
        parse_dates=["Order Date"]
    )
    return df


@st.cache_data(show_spinner=False)
def load_model_comparison() -> pd.DataFrame:
    return _read_csv_safe(PREDICTIONS_DIR / "model_comparison.csv")


@st.cache_data(show_spinner=False)
def load_overall_forecast() -> pd.DataFrame:
    return _read_csv_safe(PREDICTIONS_DIR / "overall_forecast.csv", parse_dates=["Order Date"])


@st.cache_data(show_spinner=False)
def load_segment_forecasts() -> pd.DataFrame:
    return _read_csv_safe(PREDICTIONS_DIR / "segment_forecasts.csv", parse_dates=["Order Date"])


@st.cache_data(show_spinner=False)
def load_segment_forecast_metrics() -> pd.DataFrame:
    df = _read_csv_safe(PREDICTIONS_DIR / "segment_forecast_metrics.csv")
    if not df.empty:
        df = df.rename(columns={df.columns[0]: "Segment"})
    return df


@st.cache_data(show_spinner=False)
def load_anomalies() -> pd.DataFrame:
    return _read_csv_safe(PREDICTIONS_DIR / "anomalies.csv", parse_dates=["Order Date"])


@st.cache_data(show_spinner=False)
def load_subcategory_segments() -> pd.DataFrame:
    return _read_csv_safe(PROCESSED_DIR / "subcategory_segments.csv")


@st.cache_resource(show_spinner=False)
def load_joblib_model(filename: str):
    """Load a persisted scikit-learn / xgboost / prophet model saved with joblib."""
    path = MODELS_DIR / filename
    if not path.exists():
        return None
    return joblib.load(path)


@st.cache_data(show_spinner=False)
def load_best_model_info() -> dict:
    path = REPORTS_DIR / "best_model.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_artifact_manifest() -> dict:
    path = REPORTS_DIR / "artifact_manifest.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def artifacts_missing() -> list[str]:
    """Return a list of human-readable warnings for any missing core artifact."""
    warnings = []
    checks = {
        "Processed transactions": PROCESSED_DIR / "cleaned_transactions.csv",
        "Monthly sales": PROCESSED_DIR / "monthly_sales.csv",
        "Model comparison": PREDICTIONS_DIR / "model_comparison.csv",
        "Overall forecast": PREDICTIONS_DIR / "overall_forecast.csv",
        "Anomalies": PREDICTIONS_DIR / "anomalies.csv",
        "Sub-category segments": PROCESSED_DIR / "subcategory_segments.csv",
    }
    for label, path in checks.items():
        if not path.exists():
            warnings.append(f"{label} not found at `{path.relative_to(APP_ROOT)}` — run the notebook first.")
    return warnings
