import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

from data_loader import load_data


st.title("Sleep Analysis")

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
tab2, tab3, tab4, tab5 = st.tabs([
    "Sleep Trends",
    "Sleep Relationships",
    "Sleep Predictors",
    "Sleep + Cycle",
])

# ----------------------
# TAB 2: SLEEP TRENDS
# ----------------------
with tab2:
    st.subheader("Sleep Over Time")
    # sleep_min, sleep_max = st.slider(
    # "Sleep range",0, 10, (5, 9))

    # df = df[(df["Sleep_Hours"] >= sleep_min) &
    #              (df["Sleep_Hours"] <= sleep_max)]
    
    fig = px.line(
        df,
        x="Survey_Date",
        y="Sleep_Hours",
        title="Sleep Over Time"
    )
    #st.line_chart(df.set_index("Survey_Date")["Sleep_Hours"])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sleep Trend Explorer")

    travel_filter = st.checkbox("Include Travel Days", value=True)
    comp_filter = st.checkbox("Include Competition Days", value=True)
    
    filtered_df = df.copy()
    
    if not travel_filter:
        filtered_df = filtered_df[filtered_df["Travel_day"] == 0]
    
    if not comp_filter:
        filtered_df = filtered_df[filtered_df["Comp_day"] == 0]
    
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered_df, x="Survey_Date", y="Sleep_Hours", ax=ax)
    
    st.pyplot(fig)

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
    st.subheader("What predicts the next night's sleep?")
    col1, col2 = st.columns(2)
    
    protein_cols = ["Beef", "Chicken", "Salmon", "Pork", "Other"]

    protein_long = df.melt(
        id_vars=["Sleep_Next_Night"],
        value_vars=protein_cols,
        var_name="Protein",
        value_name="Ate"
    )
    protein_long = protein_long[protein_long["Ate"] == 1]
    fig1, ax = plt.subplots()

    sns.boxplot(
        data=protein_long,
        x="Protein",
        y="Sleep_Next_Night",
        ax=ax
    )
    
    with col1:
        st.pyplot(fig1)

    workout_cols = ["Active Recovery", "Comp", "Jump", "Off", "Premeet", "Speed"]

    workout_long = df.melt(
        id_vars=["Sleep_Next_Night"],
        value_vars=workout_cols,
        var_name="Workout",
        value_name="Did"
    )
    
    workout_long = workout_long[workout_long["Did"] == 1]
    fig2, ax = plt.subplots()
    sns.boxplot(
    data=workout_long,
    x="Workout",
    y="Sleep_Next_Night"
    )
    with col2:
        st.pyplot(fig2)


with tab5:
    # --- Cycle view ---
    fig = px.box(
        df,
        x="cycle_phase",
        y="Sleep_Hours",
        title="Sleep by Cycle Phase"
    )
    
    
    st.plotly_chart(fig, use_container_width=True)
    

    