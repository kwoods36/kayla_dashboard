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

tab1,tab3 = st.tabs([
    "Overview",
    "Current Cylce Phase"
])

# ----------------------
# TAB 1: OVERVIEW
# ----------------------
with tab1:
    days = len(df)
    st.subheader(f"{days} days of Survey Data")
    df_orig_renamed = df_orig.rename(columns=DISPLAY_NAMES)
    
    st.subheader("Survey Answers last 7 days")
    st.write(df_orig_renamed.tail(7)[::-1])
    st.subheader("Last 7 Days")
    st.metric("Average Hours of Sleep", df["Sleep_Hours"].tail(7).mean().round(2))
    st.metric("Average Energy (/5)", df["Prac_Energy_Level"].tail(7).mean())

    pain_cols = [
    "right_shin", "left_shin", "knee", "lower_back",
    "left_foot", "tight_hips", "traps"
    ]
    
    pain_sums = df[pain_cols].tail(7).sum().sort_values(ascending=False)
    
    st.subheader("Total Pain Frequency")
    
    st.bar_chart(pain_sums)

# ----------------------
# TAB 2
# ----------------------

    
# ----------------------
# TAB 3
# ----------------------   
with tab3:
    # Dates of observed period starts
    period_starts = df.loc[df["period_start"], "Survey_Date"]
    
    # ----------------------------------------------------
    # Estimate average cycle length
    # ----------------------------------------------------
    
    cycle_lengths = period_starts.diff().dt.days.dropna()
    
    # Ignore implausible gaps (likely missing surveys)
    cycle_lengths = cycle_lengths[
        cycle_lengths.between(20, 40)
    ]
    
    if len(cycle_lengths) > 0:
        avg_cycle_length = round(cycle_lengths.mean())
    else:
        avg_cycle_length = 28
    
    st.subheader(f"Estimated cycle length: {avg_cycle_length} days")
    current_phase = df["cycle_phase"].iloc[-1]

    st.subheader(f"Current Cycle Phase - {current_phase}")
    #st.write(current_phase)

    phase_info = {

    "Early Menstrual":
        """
        • Energy may be lower than usual.
        • Prioritize sleep, hydration, and iron-rich foods.
        • Light movement may feel better than high-intensity training.
        """,

    "Late Menstrual":
        """
        • Energy often begins to improve.
        • Many athletes start feeling stronger again.
        • This can be a good time to gradually increase training intensity.
        """,

    "Early Follicular":
        """
        • Energy and motivation are often increasing.
        • Recovery may feel easier.
        • Strength and power training may feel more comfortable.
        """,

    "Late Follicular":
        """
        • Many women report peak energy and confidence.
        • High-intensity workouts may feel especially good.
        • Continue fueling well to support training.
        """,

    "Ovulatory":
        """
        • Power and explosiveness may be near their highest.
        • Some athletes notice increased confidence and coordination.
        • Be mindful of proper warm-ups, as some research suggests injury risk may increase around ovulation.
        """,

    "Early Luteal":
        """
        • Energy often remains fairly stable.
        • Appetite may begin to increase.
        • Continue prioritizing carbohydrates and hydration around training.
        """,

    "Late Luteal":
        """
        • Fatigue, bloating, or soreness may become more noticeable.
        • Prioritize sleep and recovery.
        • Don't be discouraged if workouts feel more difficult than usual.
        """
    }

    st.subheader("What to Expect")

    st.info(phase_info.get(current_phase, "No information available."))
    

    