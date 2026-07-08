"""Page 3 — Anomaly Detection: interactive chart, anomaly table, and business explanations."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import artifacts_missing, load_anomalies, load_weekly_sales
from utils.styling import CATEGORICAL_SEQUENCE, PLOTLY_TEMPLATE, apply_page_config, kpi_card, missing_artifact_banner, render_sidebar_branding

apply_page_config("Anomaly Detection", icon="🚨")
render_sidebar_branding()

st.title("🚨 Anomaly Detection")
missing_artifact_banner(artifacts_missing())

with st.spinner("Loading anomaly data..."):
    weekly_df = load_weekly_sales()
    anomalies_df = load_anomalies()

if weekly_df.empty:
    st.info("No weekly sales data found. Run Section 8 of the notebook first.")
    st.stop()

# ---------------------------------------------------------------------------
# Chart
# ---------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=weekly_df["Order Date"], y=weekly_df["sales"], mode="lines",
    name="Weekly Sales", line=dict(color=CATEGORICAL_SEQUENCE[0]),
))

if "is_anomaly_iso" in weekly_df.columns:
    iso_points = weekly_df[weekly_df["is_anomaly_iso"]]
    fig.add_trace(go.Scatter(
        x=iso_points["Order Date"], y=iso_points["sales"], mode="markers",
        name="Isolation Forest Anomaly", marker=dict(color=CATEGORICAL_SEQUENCE[3], size=10, symbol="circle"),
    ))

if "is_anomaly_zscore" in weekly_df.columns:
    z_points = weekly_df[weekly_df["is_anomaly_zscore"]]
    fig.add_trace(go.Scatter(
        x=z_points["Order Date"], y=z_points["sales"], mode="markers",
        name="Z-Score Anomaly", marker=dict(color=CATEGORICAL_SEQUENCE[1], size=11, symbol="x"),
    ))

fig.update_layout(title="Weekly Sales with Detected Anomalies", template=PLOTLY_TEMPLATE, xaxis_title="Week", yaxis_title="Sales ($)")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# KPIs + High-risk weeks
# ---------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
n_iso = int(weekly_df.get("is_anomaly_iso", pd.Series(dtype=bool)).sum()) if "is_anomaly_iso" in weekly_df.columns else 0
n_z = int(weekly_df.get("is_anomaly_zscore", pd.Series(dtype=bool)).sum()) if "is_anomaly_zscore" in weekly_df.columns else 0
n_both = int((weekly_df.get("is_anomaly_iso", False) & weekly_df.get("is_anomaly_zscore", False)).sum()) if {"is_anomaly_iso", "is_anomaly_zscore"}.issubset(weekly_df.columns) else 0

with col1:
    kpi_card("Isolation Forest Flags", f"{n_iso}")
with col2:
    kpi_card("Z-Score Flags", f"{n_z}")
with col3:
    kpi_card("High-Confidence (Both Methods)", f"{n_both}")

st.subheader("Anomaly Table & Likely Business Reasons")
if not anomalies_df.empty:
    display_cols = [c for c in [
        "Order Date", "sales", "z_score", "is_anomaly_iso", "is_anomaly_zscore", "likely_business_reason"
    ] if c in anomalies_df.columns]
    st.dataframe(anomalies_df[display_cols].sort_values("Order Date"), use_container_width=True)

    csv_bytes = anomalies_df[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Anomaly Report CSV", data=csv_bytes, file_name="anomalies.csv", mime="text/csv")
else:
    st.info("Run Section 8 of the notebook to generate `predictions/anomalies.csv`.")
