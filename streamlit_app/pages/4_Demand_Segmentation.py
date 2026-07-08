"""Page 4 — Demand Segmentation: cluster visualization and stocking recommendations."""

import plotly.express as px
import streamlit as st

from utils.data_loader import artifacts_missing, load_subcategory_segments
from utils.styling import CATEGORICAL_SEQUENCE, PLOTLY_TEMPLATE, apply_page_config, missing_artifact_banner, render_sidebar_branding

apply_page_config("Demand Segmentation", icon="🧩")
render_sidebar_branding()

st.title("🧩 Product Demand Segmentation")
missing_artifact_banner(artifacts_missing())

with st.spinner("Loading segmentation results..."):
    segments_df = load_subcategory_segments()

if segments_df.empty:
    st.info("No segmentation data found. Run Section 9 of the notebook first.")
    st.stop()

# ---------------------------------------------------------------------------
# Cluster scatter (PCA-reduced)
# ---------------------------------------------------------------------------
if {"pca_1", "pca_2"}.issubset(segments_df.columns):
    fig = px.scatter(
        segments_df, x="pca_1", y="pca_2",
        color=segments_df["business_label"] if "business_label" in segments_df.columns else segments_df["cluster"].astype(str),
        text="Sub-Category", size="total_sales" if "total_sales" in segments_df.columns else None,
        title="Sub-Category Clusters (PCA-reduced view)",
        template=PLOTLY_TEMPLATE, color_discrete_sequence=CATEGORICAL_SEQUENCE,
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("PCA coordinates not found in the segmentation file — showing table only.")

st.divider()

# ---------------------------------------------------------------------------
# Cluster table + business meaning
# ---------------------------------------------------------------------------
st.subheader("Cluster Table & Stocking Strategy")

available_labels = (
    sorted(segments_df["business_label"].dropna().unique().tolist())
    if "business_label" in segments_df.columns else []
)
if available_labels:
    selected_labels = st.multiselect("Filter by demand segment", available_labels, default=available_labels)
    view_df = segments_df[segments_df["business_label"].isin(selected_labels)]
else:
    view_df = segments_df

display_cols = [c for c in [
    "Sub-Category", "cluster", "business_label", "total_sales", "growth_rate_pct",
    "sales_volatility", "avg_order_value", "stocking_recommendation",
] if c in view_df.columns]
st.dataframe(view_df[display_cols], use_container_width=True)

if "business_label" in segments_df.columns and "stocking_recommendation" in segments_df.columns:
    st.subheader("Recommended Inventory Strategy by Segment")
    for label in available_labels:
        subset = segments_df[segments_df["business_label"] == label]
        rec = subset["stocking_recommendation"].iloc[0] if not subset.empty else "N/A"
        with st.expander(f"📦 {label}  ({len(subset)} sub-categories)"):
            st.write(f"**Recommendation:** {rec}")
            st.write("**Sub-categories in this segment:**", ", ".join(subset["Sub-Category"].tolist()))

csv_bytes = view_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Segmentation CSV", data=csv_bytes, file_name="demand_segments.csv", mime="text/csv")
