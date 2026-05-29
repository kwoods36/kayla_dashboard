import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

st.title("Kayla's Dashboard")

df = pd.read_csv("cleaned_kayla_survey_data.csv")
df = df.drop(columns=["Timestamp"])

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Sleep Trends",
    "Sleep Relationships",
    "Cycle"
])

# ----------------------
# TAB 1: OVERVIEW
# ----------------------
with tab1:
    st.write(df.tail())
    st.subheader("Last 7 Days")
    st.metric("Avg Sleep", df["Sleep_Hours"].tail(7).mean())
    st.metric("Avg Energy", df["Prac_Energy_Level"].tail(7).mean())




fig = px.line(
    df,
    x="Survey_Date",
    y="Sleep_Hours",
    title="Sleep Over Time"
)
# ----------------------
# TAB 2: SLEEP TRENDS
# ----------------------
with tab2:
    st.subheader("Sleep Over Time")
    #st.line_chart(df.set_index("Survey_Date")["Sleep_Hours"])
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Sleep vs Practice Energy
    
    st.subheader("Sleep vs Practice Energy")
    
    fig1, ax1 = plt.subplots()
    sns.scatterplot(
        data=df,
        x="Sleep_Hours",
        y="Prac_Energy_Level",
        ax=ax1
    )
    ax1.set_title("Sleep vs Practice Energy")
    
    st.pyplot(fig1)
    
    # Sleep on Travel vs Non-Travel
    # ----------------------------
    st.subheader("Sleep on Travel vs Non-Travel Days")
    
    # ----------------------
    # TAB 3: RELATIONSHIPS
    # ----------------------
    
    
    fig2, ax2 = plt.subplots()
    sns.boxplot(
        data=df,
        x="Travel_day",
        y="Sleep_Hours",
        ax=ax2
    )
    ax2.set_title("Sleep on Travel vs Non-Travel Days")
    
    st.pyplot(fig2)


with tab4:
    # --- Cycle view ---
    fig = px.box(
        df,
        x="cycle_phase",
        y="Sleep_Hours",
        title="Sleep by Cycle Phase"
    )
    
    
    st.plotly_chart(fig, use_container_width=True)
