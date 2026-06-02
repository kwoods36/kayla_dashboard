import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from data_loader import load_data
from constants import display_names

st.title("Kayla's Dashboard")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f7fb;
    }
    </style>
    """,
    unsafe_allow_html=True
)
df, df_orig = load_data()
DISPLAY_NAMES = display_names()
REVERSE_DISPLAY_NAMES = {
    v: k for k, v in DISPLAY_NAMES.items()
}

tab1,tab2, tab3 = st.tabs([
    "Overview",
    "Coming Soon: Daily Readiness Score",
    "Coming Soon: Current Cylce Phase"
])

# ----------------------
# TAB 1: OVERVIEW
# ----------------------
with tab1:
    days = len(df)
    st.subheader(f"{days} days of Survey Data")
    df_orig_renamed = df_orig.rename(columns=DISPLAY_NAMES)
    
    st.subheader("Survey Answers last 7 days")
    st.write(df_orig_renamed.tail(7))
    st.subheader("Last 7 Days")
    st.metric("Average Hours of Sleep", df["Sleep_Hours"].tail(7).mean().round(2))
    st.metric("Average Energy (/5)", df["Prac_Energy_Level"].tail(7).mean())

    pain_cols = [
    "right_shin", "left_shin", "knee", "lower_back",
    "left_foot", "tight_hips", "traps"
    ]
    
    pain_sums = df[pain_cols].sum().sort_values(ascending=False)
    
    st.subheader("Total Pain Frequency")
    
    st.bar_chart(pain_sums)

with tab2:
    st.subheader("In Progress")
    
    
with tab3:
    st.subheader("In Progress")