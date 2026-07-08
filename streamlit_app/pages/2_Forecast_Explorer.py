"""Page 2 — Forecast Explorer: browse saved forecasts by category/region and horizon."""

import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import (
    artifacts_missing,
    load_model_comparison,
    load_overall_forecast,
    load_segment_forecast_metrics,
    load_segment_forecasts,
)
from utils.styling import CATEGORICAL_SEQUENCE, PLOTLY_TEMPLATE, apply_page_config, kpi_card, missing_artifact_banner, render_sidebar_branding

apply_page_config("Forecast Explorer", icon="🔮")
render_sidebar_branding()

st.title("🔮 Forecast Explorer")
missing_artifact_banner(artifacts_missing())

with st.spinner("Loading saved forecasts..."):
    overall_forecast = load_overall_forecast()
    segment_forecasts = load_segment_forecasts()
    segment_metrics = load_segment_forecast_metrics()
    comparison = load_model_comparison()

if overall_forecast.empty and segment_forecasts.empty:
    st.info("No forecast files found. Run the notebook through Section 7 first.")
    st.stop()

# ---------------------------------------------------------------------------
# Selection controls
# ---------------------------------------------------------------------------
available_segments = ["Overall"] + (
    sorted(segment_forecasts.columns.difference(["Order Date"]).tolist())
    if not segment_forecasts.empty else []
)

col1, col2 = st.columns(2)
with col1:
    selection = st.selectbox("Select Category / Region", available_segments)
with col2:
    horizon = st.slider("Forecast Horizon (months)", min_value=1, max_value=3, value=3)

st.divider()

# ---------------------------------------------------------------------------
# Resolve the chosen series
# ---------------------------------------------------------------------------
if selection == "Overall":
    if overall_forecast.empty:
        st.warning("Overall forecast file not found.")
        st.stop()
    model_cols = [c for c in overall_forecast.columns if c not in ["Order Date", "Actual"]]
    best_col = model_cols[0] if len(model_cols) == 1 else st.selectbox("Model", model_cols)
    plot_df = overall_forecast[["Order Date", best_col, "Actual"]].tail(horizon)
    forecast_series = plot_df[best_col]
    actual_series = plot_df["Actual"]
    metrics_row = comparison[comparison["Model"] == best_col] if not comparison.empty else None
else:
    if segment_forecasts.empty or selection not in segment_forecasts.columns:
        st.warning(f"No forecast available for {selection}.")
        st.stop()
    plot_df = segment_forecasts[["Order Date", selection]].dropna().tail(horizon)
    forecast_series = plot_df[selection]
    actual_series = None
    metrics_row = (
        segment_metrics[segment_metrics["Segment"] == selection] if not segment_metrics.empty else None
    )

# ---------------------------------------------------------------------------
# Chart
# ---------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=plot_df["Order Date"], y=forecast_series, mode="lines+markers",
    name="Forecast", line=dict(color=CATEGORICAL_SEQUENCE[0], width=3),
))
if actual_series is not None:
    fig.add_trace(go.Scatter(
        x=plot_df["Order Date"], y=actual_series, mode="lines+markers",
        name="Actual", line=dict(color=CATEGORICAL_SEQUENCE[2], width=2, dash="dot"),
    ))

# Simple visual confidence band (+/- MAE from the saved metrics, if available)
if metrics_row is not None and not metrics_row.empty and "MAE" in metrics_row.columns:
    mae = float(metrics_row["MAE"].iloc[0])
    fig.add_trace(go.Scatter(
        x=list(plot_df["Order Date"]) + list(plot_df["Order Date"])[::-1],
        y=list(forecast_series + mae) + list(forecast_series - mae)[::-1],
        fill="toself", fillcolor="rgba(46,94,170,0.15)", line=dict(color="rgba(255,255,255,0)"),
        name="Approx. Confidence Interval (± MAE)", showlegend=True,
    ))

fig.update_layout(title=f"Forecast — {selection}", template=PLOTLY_TEMPLATE, xaxis_title="Month", yaxis_title="Sales ($)")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Metrics + table + download
# ---------------------------------------------------------------------------
col_a, col_b = st.columns([1, 2])
with col_a:
    st.subheader("Model Accuracy")
    if metrics_row is not None and not metrics_row.empty:
        kpi_card("MAE", f"{float(metrics_row['MAE'].iloc[0]):,.2f}")
        kpi_card("RMSE", f"{float(metrics_row['RMSE'].iloc[0]):,.2f}")
        if "MAPE" in metrics_row.columns:
            kpi_card("MAPE", f"{float(metrics_row['MAPE'].iloc[0]):,.2f}%")
    else:
        st.info("No saved accuracy metrics for this selection.")

with col_b:
    st.subheader("Forecast Table")
    st.dataframe(plot_df, use_container_width=True)
    csv_bytes = plot_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Forecast CSV", data=csv_bytes,
        file_name=f"forecast_{selection.replace(' ', '_').lower()}.csv", mime="text/csv",
    )

with st.expander("Full model comparison (from the notebook)"):
    if not comparison.empty:
        st.dataframe(comparison, use_container_width=True)
    else:
        st.info("Run Section 6 of the notebook to generate `predictions/model_comparison.csv`.")
