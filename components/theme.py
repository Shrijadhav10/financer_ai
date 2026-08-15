"""Shared visual language for the Financer AI Streamlit pages."""

import streamlit as st


def apply_theme():
    """Apply a compact, accessible dashboard theme on every page."""
    st.markdown(
        """
        <style>
          :root { --ink: #172033; --muted: #64748b; --brand: #635bff; }
          .stApp { background: #f7f8fc; color: var(--ink); }
          [data-testid="stSidebar"] { background: linear-gradient(180deg, #111a33, #202d52); }
          [data-testid="stSidebar"] * { color: #f8fafc; }
          [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div { background: #ffffff; }
          [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * { color: #172033; }
          .hero { padding: 1.6rem 1.8rem; border-radius: 22px; color: #fff; background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 55%, #0f766e 100%); margin: 0 0 1.35rem; box-shadow: 0 14px 35px rgba(79,70,229,.2); }
          .hero h1 { margin: 0; font-size: 2.15rem; line-height: 1.15; }
          .hero p { margin: .5rem 0 0; opacity: .88; font-size: 1rem; }
          .section-label { font-size: .76rem; font-weight: 700; letter-spacing: .09em; color: #6366f1; text-transform: uppercase; margin: 1.45rem 0 .35rem; }
          div[data-testid="stMetric"] { background: #fff; border: 1px solid #e8eaf2; border-radius: 16px; padding: .85rem 1rem; box-shadow: 0 4px 14px rgba(15,23,42,.05); }
          div[data-testid="stMetricLabel"] { color: #64748b; }
          div[data-testid="stMetricValue"] { color: #172033; }
          .stPlotlyChart { background: #fff; border: 1px solid #e8eaf2; border-radius: 16px; padding: .35rem; }
          .stDataFrame { border: 1px solid #e8eaf2; border-radius: 14px; overflow: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_hero(title, subtitle, icon="✦"):
    st.markdown(f'<div class="hero"><h1>{icon} {title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)
