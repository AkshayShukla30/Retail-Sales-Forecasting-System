"""
styling.py
----------
Shared visual styling so every page looks like one coherent product
instead of four disconnected scripts.
"""

import streamlit as st

# A clean, restrained palette used consistently across every chart
COLOR_PALETTE = {
    "primary": "#2E5EAA",
    "secondary": "#F2A93B",
    "success": "#2E8B57",
    "danger": "#C0392B",
    "neutral": "#6B7280",
    "background": "#F7F9FC",
}

PLOTLY_TEMPLATE = "plotly_white"
CATEGORICAL_SEQUENCE = ["#2E5EAA", "#F2A93B", "#2E8B57", "#C0392B", "#8E44AD", "#16A085"]


def apply_page_config(title: str, icon: str = "📊") -> None:
    """Call once per page as the first Streamlit command."""
    st.set_page_config(page_title=f"{title} | Retail Sales Intelligence", page_icon=icon, layout="wide")


def render_sidebar_branding() -> None:
    st.sidebar.markdown("## 🛒 Retail Sales Intelligence")
    st.sidebar.caption("Forecasting · Anomaly Detection · Demand Segmentation")
    st.sidebar.divider()


def kpi_card(label: str, value: str, delta: str | None = None) -> None:
    st.metric(label=label, value=value, delta=delta)


def missing_artifact_banner(warnings: list[str]) -> None:
    if warnings:
        st.warning(
            "Some artifacts are missing, so parts of this page may be empty:\n\n"
            + "\n".join(f"- {w}" for w in warnings)
        )
