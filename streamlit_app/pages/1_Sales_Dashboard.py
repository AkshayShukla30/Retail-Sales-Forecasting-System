"""Page 1 — Sales Dashboard: KPIs, trends, and category/region filters."""

import plotly.express as px
import streamlit as st

from utils.data_loader import artifacts_missing, load_transactions
from utils.styling import (
    CATEGORICAL_SEQUENCE,
    PLOTLY_TEMPLATE,
    apply_page_config,
    kpi_card,
    missing_artifact_banner,
    render_sidebar_branding,
)

apply_page_config("Sales Dashboard", icon="📊")
render_sidebar_branding()

st.title("📊 Sales Dashboard")
missing_artifact_banner(artifacts_missing())

with st.spinner("Loading transactions..."):
    df = load_transactions()

if df.empty:
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar filters (no hardcoded values — options are derived from the data)
# ---------------------------------------------------------------------------
st.sidebar.subheader("Filters")
categories = sorted(df["Category"].dropna().unique().tolist())
regions = sorted(df["Region"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)

filtered = df[df["Category"].isin(selected_categories) & df["Region"].isin(selected_regions)]

if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("Revenue", f"${filtered['Sales'].sum():,.0f}")
with col2:
    n_orders = filtered["Order ID"].nunique() if "Order ID" in filtered.columns else len(filtered)
    kpi_card("Orders", f"{n_orders:,}")
with col3:
    kpi_card("Average Sale", f"${filtered['Sales'].mean():,.2f}")
with col4:
    kpi_card("Sub-Categories", f"{filtered['Sub-Category'].nunique()}")

st.divider()

# ---------------------------------------------------------------------------
# Monthly trend
# ---------------------------------------------------------------------------
monthly_trend = (
    filtered.set_index("Order Date").resample("MS")["Sales"].sum().reset_index()
)
fig_trend = px.line(
    monthly_trend, x="Order Date", y="Sales", markers=True,
    title="Monthly Sales Trend", template=PLOTLY_TEMPLATE,
)
fig_trend.update_traces(line_color=CATEGORICAL_SEQUENCE[0])
st.plotly_chart(fig_trend, use_container_width=True)

# ---------------------------------------------------------------------------
# Category / Region breakdown
# ---------------------------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    by_category = filtered.groupby("Category")["Sales"].sum().reset_index().sort_values("Sales")
    fig_cat = px.bar(
        by_category, x="Sales", y="Category", orientation="h",
        title="Revenue by Category", template=PLOTLY_TEMPLATE,
        color_discrete_sequence=CATEGORICAL_SEQUENCE,
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_right:
    by_region = filtered.groupby("Region")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    fig_region = px.bar(
        by_region, x="Region", y="Sales",
        title="Revenue by Region", template=PLOTLY_TEMPLATE,
        color_discrete_sequence=CATEGORICAL_SEQUENCE,
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ---------------------------------------------------------------------------
# Sub-category deep dive
# ---------------------------------------------------------------------------
st.subheader("Sub-Category Detail")
by_subcat = (
    filtered.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
)
fig_subcat = px.bar(
    by_subcat, x="Sub-Category", y="Sales",
    title="Revenue by Sub-Category", template=PLOTLY_TEMPLATE,
    color_discrete_sequence=CATEGORICAL_SEQUENCE,
)
fig_subcat.update_layout(xaxis_tickangle=-35)
st.plotly_chart(fig_subcat, use_container_width=True)

with st.expander("View filtered raw data"):
    st.dataframe(filtered, use_container_width=True)
