import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import statsmodels.api as sm
from data_loader import load_data

st.title("Regression Exploration")

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

df_orig = pd.read_csv('./Kayla_Daily_Survey.csv')
df = pd.read_csv("./cleaned_kayla_survey_data.csv")
df = df.drop(columns=["Timestamp"])
df_orig = df_orig.drop(columns=["Timestamp"])
df["Sleep_Next_Night"] = df["Sleep_Hours"].shift(-1)
df["Next_Morning_Back_Pain"] = df["Morning_Back_Pain"].shift(-1)
df_orig = df_orig.rename(columns={
    "Survery_Date": "Survey_Date"
})
df_orig = df_orig.sort_values("Survey_Date")


# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("Filters")

comp_filter = st.sidebar.selectbox(
    "Competition Days",
    ["All", "Only Comp Days", "Exclude Comp Days"]
)

travel_filter = st.sidebar.selectbox(
    "Travel Days",
    ["All", "Only Travel Days", "Exclude Travel Days"]
)

cycle_filter = st.sidebar.selectbox(
    "Period Days",
    ["All", "Only Period Days", "Exclude Period Days"]
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = df.copy()

if comp_filter == "Only Comp Days":
    filtered_df = filtered_df[filtered_df["Comp_day"] == 1]

elif comp_filter == "Exclude Comp Days":
    filtered_df = filtered_df[filtered_df["Comp_day"] == 0]

if travel_filter == "Only Travel Days":
    filtered_df = filtered_df[filtered_df["Travel_day"] == 1]

elif travel_filter == "Exclude Travel Days":
    filtered_df = filtered_df[filtered_df["Travel_day"] == 0]

if cycle_filter == "Only Period Days":
    filtered_df = filtered_df[filtered_df["Period_day"] == 1]

elif cycle_filter == "Exclude Period Days":
    filtered_df = filtered_df[filtered_df["Period_day"] == 0]

# -----------------------------
# TARGET VARIABLE
# -----------------------------
st.header("Choose Outcome Variable")

target = st.selectbox(
    "Outcome Variable (Y)",
    [
        "Sleep_Hours",
        "Prac_Energy_Level",
        "Mood_Number",
        "Meals_Quality",
        "Sleep_Next_Night",
        "Next_Morning_Back_Pain"
    ]
)

# -----------------------------
# FEATURE OPTIONS
# -----------------------------
possible_features = [
    "Travel_day",
    "Comp_day",
    "Period_day",
    "Sleep_Quality",
    "Mood_Number",
    "Meals_Quality",
    "Alcoholic_Drinks",
    "Prac_Energy_Level",
    "Morning_Back_Pain",
    "Sleep_Hours",
    "Active Recovery",
    "Jump",
    "Speed",
    "Off",
    "Premeet",
    "Chicken",
    "Beef",
    "Salmon",
    "Pork",
    "Happy",
    "Stressed",
    "Anxious",
    "Tired",
    "focused",
    "sore",
    "strong",
    "sleep_lag1",
    "sleep_3day_avg",
    "Sleep_Next_Night",
    "right_shin",
    "left_shin",
    "knee",
    "lower_back",
    "left_foot",
    "tight_hips",
    "traps"
]

# Remove target from predictors
possible_features = [x for x in possible_features if x != target]

# -----------------------------
# FEATURE SELECTION
# -----------------------------
st.header("Choose Predictor Variables")

features = st.multiselect(
    "Predictors (X)",
    possible_features,
    default=["Travel_day", "Comp_day", "Sleep_Quality"]
)

# -----------------------------
# RUN REGRESSION
# -----------------------------
if len(features) > 0:

    reg_df = filtered_df[[target] + features].dropna()

    X = reg_df[features]
    y = reg_df[target]

    # Add intercept
    X = sm.add_constant(X)

    # Fit model
    model = sm.OLS(y, X).fit()

    # -----------------------------
    # OUTPUTS
    # -----------------------------
    st.header("Regression Results")

    st.write(f"Days of data: {len(reg_df)}")

    st.write("### R-squared")
    st.write(round(model.rsquared, 3))

    st.write("### Coefficients")
    st.dataframe(model.params)

    st.write("### P-values")
    st.dataframe(model.pvalues)

    # st.write("### Full Summary")
    # st.text(model.summary())

    # -----------------------------
    # ACTUAL VS PREDICTED
    # -----------------------------
    reg_df["Predicted"] = model.predict(X)

    fig, ax = plt.subplots()

    sns.scatterplot(
        x=reg_df[target],
        y=reg_df["Predicted"],
        ax=ax
    )

    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.set_title("Actual vs Predicted")

    st.pyplot(fig)

else:
    st.warning("Please select at least one predictor variable.")